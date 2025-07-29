#!/usr/bin/env python3
"""
**Internal copy of `server.py`** packaged under `kamiwaza_mlx` so end-users can
simply run:

    python -m kamiwaza_mlx.server -m <model> [--port 1234]

The body of the file is identical to the original standalone script (save for
this prologue) to avoid any behavioural changes during the move.
"""

from __future__ import annotations

import argparse, base64, io, json, logging, math, re, time, uuid, asyncio, os
from pathlib import Path
from typing import Any, Dict, List, Tuple, Union, Optional

import requests, uvicorn, mlx.core as mx
from PIL import Image
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, model_validator

# Import for prompt caching
from mlx_lm.models.cache import make_prompt_cache, save_prompt_cache, load_prompt_cache
from mlx_lm.models.cache import RotatingKVCache, QuantizedKVCache

# ────────────────────────── CLI & logging ──────────────────────────
parser = argparse.ArgumentParser()
parser.add_argument("-m", "--model", default="mlx-community/Qwen2-VL-2B-Instruct-4bit")
parser.add_argument("--host", default="0.0.0.0")
parser.add_argument("--port", type=int, default=18_000)
parser.add_argument("-V", "--vision", action="store_true", help="Force vision pipeline; otherwise auto-detect.")
parser.add_argument("--strip-thinking", action="store_true")
parser.add_argument("--enable-prefix-caching", type=lambda x: (str(x).lower() == 'true'), default=True, help="Enable system message caching (default: True). Caches system messages for reuse across requests with the same system context.")
parser.add_argument("--prompt-cache-dir", type=str, default="./.cache/mlx_prompt_caches/", help="Directory to store/load system message cache files.")
args = parser.parse_args()

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
log = logging.getLogger(__name__)

# ───────────────────────── timers / tiny helpers ─────────────────────────

class _Timer:  # noqa: D101 – internal util
    __slots__ = ("start", "in_tok")

    def __init__(self, in_tok: int):
        self.start = time.perf_counter()
        self.in_tok = in_tok
        logging.info("Starting generation with %d input tokens", in_tok)

    def done(self, out_tok: int):
        dt = time.perf_counter() - self.start
        tps = 0.0 if dt == 0 else out_tok / dt
        logging.info(
            "Generation completed: %d output tokens in %.2fs (%.2f output tokens/sec)", out_tok, dt, tps
        )


# ───────────────────────── constants / regex ───────────────────────
MAX_TOKENS = -1
PATCH_LIMIT = 1536
PATCH_SIZE = 32
THINK_RE = re.compile(r"<think>(.*?)</think>", re.S | re.I)  # capture group!

# ──────────────────────────── helpers ──────────────────────────────

def _encode(txt: str):
    if hasattr(PROCESSOR, "encode"):
        return mx.array(PROCESSOR.encode(txt))
    if hasattr(PROCESSOR, "tokenizer"):
        return mx.array(PROCESSOR.tokenizer.encode(txt))
    return mx.array(txt.split())  # fallback

def _tok_len(text: str) -> int:
    # Add safety check for None/empty text
    if text is None:
        log.warning("_tok_len received None text")
        return 0
    if not isinstance(text, str):
        log.warning("_tok_len received non-string: %s = %r", type(text), text)
        text = str(text) if text is not None else ""
    
    if hasattr(PROCESSOR, "encode"):
        return len(PROCESSOR.encode(text))
    if hasattr(PROCESSOR, "tokenizer"):
        return len(PROCESSOR.tokenizer.encode(text))
    return len(text.split())  # hopeless fallback


def _model_cfg(model) -> Dict[str, Any]:
    cfg = getattr(model, "config", {})
    return cfg if isinstance(cfg, dict) else cfg.__dict__


def strip_thoughts(text: str, flag: bool) -> str:
    return THINK_RE.sub("", text) if flag else text


def _cap_image(img: Image.Image) -> Image.Image:
    w, h = img.size
    patches = math.ceil(w / PATCH_SIZE) * math.ceil(h / PATCH_SIZE)
    if patches <= PATCH_LIMIT:
        return img
    scale = math.sqrt(PATCH_LIMIT / patches)
    return img.resize((int(w * scale), int(h * scale)), Image.BICUBIC)


def load_image(ref: str) -> Image.Image:
    if ref.startswith("data:image/"):
        img = Image.open(io.BytesIO(base64.b64decode(ref.split(",", 1)[1])))
    elif ref.startswith("http"):
        img = Image.open(io.BytesIO(requests.get(ref, timeout=15).content))
    else:
        img = Image.open(ref)
    return _cap_image(img.convert("RGB"))


def _hash_tokens(toks: mx.array) -> str:
    """Return SHA256 hash of token id array (1-D view)."""
    import hashlib, numpy as _np
    # Ensure toks is an mx.array, convert to numpy, flatten, and hash
    # The .astype('uint32') is important for consistent hashing across platforms/setups
    # if the token IDs are, for instance, int64 by default from the tokenizer.
    flat_numpy_array = _np.array(toks, copy=False).astype('uint32').ravel()
    return hashlib.sha256(flat_numpy_array.tobytes()).hexdigest()


def _prepare_cache_for_system_only(
    req: ChatReq,
    global_prompt_cache: Optional[List[Any]],
    cached_prefix_len: int,
    cache_prefix_hash: str,
    is_vision_model: bool,
    enable_prefix_caching_arg: bool,
    func_name_for_log: str
) -> Tuple[Optional[List[Any]], int, mx.array]:
    """Prepare cache and suffix for system-only caching approach."""
    
    if is_vision_model or not enable_prefix_caching_arg:
        # No caching for vision models
        prompt_str = build_prompt(req, 0)
        prompt_ids = _encode(prompt_str)
        return None, 0, prompt_ids
    
    # Check if we have system messages
    system_prompt_str = build_system_prompt(req)
    if not system_prompt_str:
        # No system messages, can't use cache
        prompt_str = build_prompt(req, 0)
        prompt_ids = _encode(prompt_str)
        return None, 0, prompt_ids
    
    # Check if cache is valid for current system prompt
    system_ids = _encode(system_prompt_str)
    system_hash = _hash_tokens(system_ids)
    
    cache_to_use = None
    actual_cached_len = 0
    
    if (global_prompt_cache is not None and 
        cached_prefix_len > 0 and 
        cache_prefix_hash == system_hash):
        # Cache is valid for this system prompt
        cache_to_use = LATE_def_copy_mlx_lm_kv_cache(global_prompt_cache)
        actual_cached_len = cached_prefix_len
        log.info(f"✅ Using cached system prompt ({actual_cached_len} tokens) in {func_name_for_log}")
        
        # Get the user/assistant portion only
        user_assistant_prompt = build_user_and_assistant_prompt(req, 0)
        suffix_ids = _encode(user_assistant_prompt)
    else:
        # Cache doesn't match or doesn't exist
        if global_prompt_cache is not None:
            log.info(f"❌ System prompt hash mismatch in {func_name_for_log}, not using cache")
        
        # Use full prompt
        prompt_str = build_prompt(req, 0)
        suffix_ids = _encode(prompt_str)
    
    # Ensure suffix is not empty
    if suffix_ids.ndim == 1 and len(suffix_ids) == 0:
        # This shouldn't happen with properly formed prompts, but just in case
        log.warning(f"Empty suffix in {func_name_for_log}, using full prompt")
        prompt_str = build_prompt(req, 0)
        suffix_ids = _encode(prompt_str)
        cache_to_use = None
        actual_cached_len = 0
    
    return cache_to_use, actual_cached_len, suffix_ids


def _usage_dict(in_tok: int, out_tok: int, dur: float, reasoning_tok: int) -> Dict[str, Any]:
    """Return an OpenAI-style `usage` dict including optional reasoning tokens."""

    return {
        "input_tokens": in_tok,
        "input_tokens_details": {"cached_tokens": 0},
        "output_tokens": out_tok,
        "output_tokens_details": {"reasoning_tokens": reasoning_tok},
        "total_tokens": in_tok + out_tok,
        "tokens_per_second": (in_tok + out_tok) / max(dur, 1e-6),  # never ÷0
    }


def load_model(repo: str) -> Tuple[Any, Any, bool]:
    want_vl = args.vision or "vl" in Path(repo).name.lower()
    if want_vl:
        try:
            from mlx_vlm import load as vlm_load

            cfg_path = Path(repo) / "config.json"
            cfg = json.load(open(cfg_path)) if cfg_path.exists() else {}
            model, proc = vlm_load(repo, **cfg)
            log.info("🖼️  vision model loaded via mlx-vlm")
            return model, proc, True
        except Exception as e:  # noqa: BLE001 – blanket log here is fine
            log.warning("vision load failed (%s) – falling back to LM", e)

    from mlx_lm import load as lm_load

    model, tok = lm_load(repo)
    log.info("💬  language model loaded via mlx-lm")
    return model, tok, False


MODEL, PROCESSOR, IS_VISION = load_model(args.model)
MODEL_NAME = Path(args.model).name
MODEL_CREATED = int(time.time())

# Global variables for system message caching
GLOBAL_PROMPT_CACHE = None
GLOBAL_CACHE_FILE_PATH: str | None = None
CACHE_PRIMED_THIS_SESSION = False
CACHED_PREFIX_LEN = 0
CACHE_PREFIX_HASH = ""

if args.enable_prefix_caching and not IS_VISION:
    try:
        # Sanitize model name for use as a filename
        sanitized_model_name = re.sub(r'[^a-zA-Z0-9_.-]', '_', MODEL_NAME)
        cache_dir = Path(args.prompt_cache_dir)
        cache_dir.mkdir(parents=True, exist_ok=True)
        GLOBAL_CACHE_FILE_PATH = str(cache_dir / f"{sanitized_model_name}.safetensors")
        log.info(f"System message cache path set to: {GLOBAL_CACHE_FILE_PATH}")

        if os.path.exists(GLOBAL_CACHE_FILE_PATH):
            log.info(f"Attempting to load system message cache from {GLOBAL_CACHE_FILE_PATH}...")
            GLOBAL_PROMPT_CACHE = load_prompt_cache(GLOBAL_CACHE_FILE_PATH) 
            log.info("System message cache loaded successfully.")
            CACHE_PRIMED_THIS_SESSION = True # If loaded, it's already primed
            # load len
            len_path = GLOBAL_CACHE_FILE_PATH + ".len"
            if os.path.exists(len_path):
                try:
                    CACHED_PREFIX_LEN = int(Path(len_path).read_text())
                except Exception:
                    CACHED_PREFIX_LEN = 0
            # load hash
            hash_path = GLOBAL_CACHE_FILE_PATH + ".hash"
            if os.path.exists(hash_path):
                try:
                    CACHE_PREFIX_HASH = Path(hash_path).read_text().strip()
                except Exception:
                    CACHE_PREFIX_HASH = ""
        else:
            log.info(f"System message cache file not found at {GLOBAL_CACHE_FILE_PATH}. Will be created on first request with a system message.")
    except Exception as e:
        log.error(f"Error during system message cache setup: {e}. Caching might not work.")

# ─────────────────── Pydantic request / schema ────────────────────

class MsgPart(BaseModel):
    type: str
    text: str | None = None
    image_url: Dict[str, str] | None = None


class ChatMsg(BaseModel):
    role: str
    content: Union[str, List[MsgPart]]


class ChatReq(BaseModel):
    model: str = MODEL_NAME
    messages: List[ChatMsg]
    images: List[str] | None = None
    max_tokens: int = MAX_TOKENS
    temperature: float = 1.0
    top_p: float = 1.0
    stream: bool = False
    strip_thinking: bool | None = None

    @model_validator(mode="after")
    def _flatten(cls, v):  # noqa: D401
        imgs, flat = list(v.images or []), []
        for m in v.messages:
            if isinstance(m.content, list):
                buf = []
                for p in m.content:
                    if p.type == "text" and p.text:
                        buf.append(p.text)
                    elif p.type == "image_url" and p.image_url:
                        imgs.append(p.image_url["url"])
                m.content = "\n".join(buf)
            flat.append({"role": m.role, "content": m.content})
        v.__dict__["flat"] = flat
        v.__dict__["all_images"] = imgs
        return v


class _ThinkFilter:  # noqa: D401 – simple state machine
    def __init__(self):
        self.state, self.buf = "NORMAL", ""

    def feed(self, s: str) -> str | None:  # noqa: C901 – tiny FSM, keep inline
        self.buf += s
        out = ""
        while True:
            if self.state == "NORMAL":
                i = self.buf.find("<think>")
                if i == -1:
                    out, self.buf = self.buf, ""
                    return out
                out += self.buf[:i]
                self.buf = self.buf[i + 7 :]
                self.state = "IN"
            elif self.state == "IN":
                j = self.buf.find("</think>")
                if j == -1:
                    return None
                self.buf = self.buf[j + 8 :]
                self.state = "STRIP_NL"
            elif self.state == "STRIP_NL":
                self.buf = self.buf.lstrip("\n")
                self.state = "NORMAL"


def build_prompt(req: ChatReq, n_imgs: int) -> str:
    if IS_VISION:
        from mlx_vlm import apply_chat_template

        return apply_chat_template(PROCESSOR, config=_model_cfg(MODEL), prompt=req.flat, num_images=n_imgs)
    if getattr(PROCESSOR, "chat_template", None):
        return PROCESSOR.apply_chat_template(req.flat, tokenize=False, add_generation_prompt=True)
    chunks = [f"<|{m['role']}|>\n{m['content']}</s>" for m in req.flat]
    chunks.append("<|assistant|>\n")
    return "\n".join(chunks)


def build_system_prompt(req: ChatReq) -> str:
    """Build prompt containing only system message(s) for caching."""
    # Extract only system messages
    system_messages = [m for m in req.flat if m['role'] == 'system']
    
    if not system_messages:
        return ""
    
    if IS_VISION:
        # For vision models, we can't easily separate system from user in the template
        # So we'll return empty string and not cache for vision models
        return ""
    
    if getattr(PROCESSOR, "chat_template", None):
        # Apply chat template to system messages only
        # Don't add generation prompt since we're not generating yet
        return PROCESSOR.apply_chat_template(system_messages, tokenize=False, add_generation_prompt=False)
    
    # Manual template formatting for system messages only
    chunks = [f"<|{m['role']}|>\n{m['content']}</s>" for m in system_messages]
    return "\n".join(chunks)


def build_user_and_assistant_prompt(req: ChatReq, n_imgs: int) -> str:
    """Build prompt containing everything after system messages."""
    # Extract non-system messages
    non_system_messages = [m for m in req.flat if m['role'] != 'system']
    
    if not non_system_messages:
        # If only system messages, return just the assistant prompt
        if getattr(PROCESSOR, "chat_template", None):
            return PROCESSOR.apply_chat_template([], tokenize=False, add_generation_prompt=True)
        return "<|assistant|>\n"
    
    if IS_VISION:
        from mlx_vlm import apply_chat_template
        # For vision, we need to include all messages
        return apply_chat_template(PROCESSOR, config=_model_cfg(MODEL), prompt=req.flat, num_images=n_imgs)
    
    if getattr(PROCESSOR, "chat_template", None):
        # Apply chat template to non-system messages and add generation prompt
        return PROCESSOR.apply_chat_template(non_system_messages, tokenize=False, add_generation_prompt=True)
    
    # Manual template formatting
    chunks = [f"<|{m['role']}|>\n{m['content']}</s>" for m in non_system_messages]
    chunks.append("<|assistant|>\n")
    return "\n".join(chunks)


# ─────────────────── generation (vision / language) ───────────────

if IS_VISION:  # ──────────── VISION PATH ────────────
    from mlx_vlm.utils import generate as vlm_gen, stream_generate as vlm_stream

    def sync_gen(prompt: str, imgs, req: ChatReq) -> str:  # noqa: D401
        timer = _Timer(len(prompt))
        result = vlm_gen(
            MODEL,
            PROCESSOR,
            prompt,
            image=imgs,
            max_tokens=req.max_tokens,
            temp=req.temperature,
            top_p=req.top_p,
            verbose=False,
        )
        # MLX VLM returns (text, stats) tuple, extract just the text
        txt = result[0] if isinstance(result, tuple) else result
        timer.done(_tok_len(txt))
        return txt

    def stream_chunks(prompt: str, imgs, req: ChatReq):  # noqa: C901 – ported as-is
        rid, created, first = f"chatcmpl-{uuid.uuid4()}", int(time.time()), False
        should_strip = args.strip_thinking if req.strip_thinking is None else req.strip_thinking
        timer = _Timer(len(prompt))
        out_tok = 0

        def _emit(chunk: str):
            nonlocal first, out_tok
            if not chunk:
                return
            out_tok += _tok_len(chunk)
            delta = {"content": chunk}
            if not first:
                delta["role"] = "assistant"  # ← add the value!
                first = True
            return _sse_chunk(rid, created, delta)

        if not should_strip:
            for r in vlm_stream(
                MODEL,
                PROCESSOR,
                prompt,
                image=imgs,
                max_tokens=req.max_tokens,
                temp=req.temperature,
                top_p=req.top_p,
            ):
                if r.text:
                    yield _emit(r.text)
            yield "data: [DONE]\n\n"
            final = {
                "id": rid,
                "object": "chat.completion.chunk",
                "created": created,
                "model": MODEL_NAME,
                "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
            }
            yield f"data: {json.dumps(final)}\n\n"
            timer.done(out_tok)
            yield "data: [DONE]\n\n"

        state, buf = "NORMAL", ""
        for r in vlm_stream(
            MODEL,
            PROCESSOR,
            prompt,
            image=imgs,
            max_tokens=req.max_tokens,
            temp=req.temperature,
            top_p=req.top_p,
        ):
            if not r.text:
                continue
            buf += r.text
            while True:
                if state == "NORMAL":
                    k = buf.find("<think>")
                    if k == -1:
                        chunk, buf = buf, ""
                    else:
                        chunk, buf, state = buf[:k], buf[k + 7 :], "IN_THINK"
                    if chunk:
                        yield _emit(chunk)
                    if k == -1:
                        break
                elif state == "IN_THINK":
                    k = buf.find("</think>")
                    if k == -1:
                        buf = ""
                        break
                    buf, state = buf[k + 8 :], "STRIP"
                elif state == "STRIP":
                    buf = buf.lstrip("\n")
                    state = "NORMAL"
        if buf:
            yield _emit(buf)
        final = {
            "id": rid,
            "object": "chat.completion.chunk",
            "created": created,
            "model": MODEL_NAME,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(final)}\n\n"
        timer.done(out_tok)
        yield "data: [DONE]\n\n"

else:  # ──────────── TEXT-ONLY PATH ────────────
    from mlx_lm.generate import stream_generate as lm_stream
    from mlx_lm.sample_utils import make_sampler

    def _sampler(req: ChatReq):
        return make_sampler(temp=req.temperature, top_p=req.top_p, min_p=0.0, min_tokens_to_keep=1)

    def sync_gen(prompt: str, _imgs, req: ChatReq) -> str:  # noqa: C901, D401
        global GLOBAL_PROMPT_CACHE, CACHED_PREFIX_LEN, CACHE_PREFIX_HASH
        sampler = _sampler(req)
        
        cache_to_use, actual_cached_len, suffix_ids_val = _prepare_cache_for_system_only(
            req,
            GLOBAL_PROMPT_CACHE,
            CACHED_PREFIX_LEN,
            CACHE_PREFIX_HASH,
            IS_VISION,
            args.enable_prefix_caching,
            "sync_gen"
        )
        
        # Calculate total prompt length for reporting
        full_prompt_len = len(_encode(prompt))
        suffix_len = len(suffix_ids_val) if suffix_ids_val.ndim == 1 else suffix_ids_val.shape[-1]
        
        log.info("🪟 Using cache? %s | full prompt %d tokens | processing %d tokens (cached system: %d)", 
                 cache_to_use is not None, full_prompt_len, suffix_len, actual_cached_len)

        timer = _Timer(suffix_len)
        out, comp_tok, think_tok_count_if_stripped = [], 0, 0
        t0 = time.perf_counter()

        first_iter = True
        for r in lm_stream(
            model=MODEL,
            tokenizer=PROCESSOR,
            prompt=suffix_ids_val,
            max_tokens=req.max_tokens,
            sampler=sampler,
            prompt_cache=cache_to_use
        ):
            if first_iter:
                start_pos = getattr(r, "pos", getattr(r, "position", -1))
                log.debug("🔍 First step model start_pos = %s", start_pos)
                first_iter = False
            if r.token == PROCESSOR.eos_token_id:
                break
            out.append(r.text)
            comp_tok += 1
            # This counts tokens inside <think> tags if they were to be stripped.
            # The actual reasoning_tok for usage depends on whether stripping happens.
            if "<think>" in r.text:
                 think_tok_count_if_stripped += len(PROCESSOR.encode("".join(THINK_RE.findall(r.text))))
        dt = time.perf_counter() - t0

        full = "".join(out)
        # Calculate actual reasoning tokens based on the final full string and stripping choice
        final_reasoning_tok = 0
        if not (req.strip_thinking or args.strip_thinking):
            inner_thoughts = THINK_RE.findall(full)
            final_reasoning_tok = sum(len(PROCESSOR.encode(seg)) for seg in inner_thoughts)
        
        req.__dict__["_usage"] = _usage_dict(suffix_len, comp_tok, dt, final_reasoning_tok)

        timer.done(comp_tok)

        return full if not (req.strip_thinking or args.strip_thinking) else strip_thoughts(full, True)

    def stream_chunks(prompt: str, _imgs, req: ChatReq):  # noqa: C901
        global GLOBAL_PROMPT_CACHE, CACHED_PREFIX_LEN, CACHE_PREFIX_HASH
        rid, created, sent_role = f"chatcmpl-{uuid.uuid4()}", int(time.time()), False
        sampler = _sampler(req)

        cache_to_use, actual_cached_len, suffix_ids_val = _prepare_cache_for_system_only(
            req,
            GLOBAL_PROMPT_CACHE,
            CACHED_PREFIX_LEN,
            CACHE_PREFIX_HASH,
            IS_VISION,
            args.enable_prefix_caching,
            "stream_chunks"
        )
        
        # Calculate total prompt length for reporting
        full_prompt_len = len(_encode(prompt))
        suffix_len = len(suffix_ids_val) if suffix_ids_val.ndim == 1 else suffix_ids_val.shape[-1]
        
        log.info("🪟 Using cache? %s | full prompt %d tokens | processing %d tokens (cached system: %d) (stream)", 
                 cache_to_use is not None, full_prompt_len, suffix_len, actual_cached_len)

        timer = _Timer(suffix_len)
        # reasoning_tok for streaming is harder to calculate accurately upfront if stripping thoughts.
        # The _ThinkFilter handles stripping, and final usage might not be easily available here.
        # For simplicity, we'll set it to 0 here or acknowledge it's an approximation for streaming.

        think = _ThinkFilter()
        strip_it = args.strip_thinking if req.strip_thinking is None else req.strip_thinking
        SYNC_EVERY, tok_ctr, out_tok = 16, 0, 0

        first_iter = True
        for r in lm_stream(
            model=MODEL,
            tokenizer=PROCESSOR,
            prompt=suffix_ids_val,
            max_tokens=req.max_tokens,
            sampler=sampler,
            prompt_cache=cache_to_use
        ):
            if first_iter:
                start_pos = getattr(r, "pos", getattr(r, "position", -1))
                log.debug("🔍 First step model start_pos = %s (stream)", start_pos)
                first_iter = False
            if r.token == PROCESSOR.eos_token_id:
                break
            piece = r.text
            if strip_it:
                stripped_piece = think.feed(piece)
                if stripped_piece is None:
                    tok_ctr += 1
                    if tok_ctr % SYNC_EVERY == 0:
                        mx.synchronize()
                    continue
                piece = stripped_piece
            
            if piece == "" and r.text:
                 piece = "\n"
            elif piece == "" and not r.text:
                 continue

            delta = {"content": piece}
            if not sent_role:
                delta["role"] = "assistant"
                sent_role = True
            out_tok += 1
            yield _sse_chunk(rid, created, delta)
            tok_ctr += 1
            if tok_ctr % SYNC_EVERY == 0:
                mx.synchronize()

        timer.done(out_tok)
        final = {
            "id": rid,
            "object": "chat.completion.chunk",
            "created": created,
            "model": MODEL_NAME,
            "choices": [{"index": 0, "delta": {}, "finish_reason": "stop"}],
        }
        yield f"data: {json.dumps(final)}\n\n"
        yield "data: [DONE]\n\n"


# ───────────────────────── SSE helper ─────────────────────────────

def _sse_chunk(rid: str, created: int, delta: Dict[str, str]) -> str:
    payload = {
        "id": rid,
        "object": "chat.completion.chunk",
        "created": created,
        "model": MODEL_NAME,
        "choices": [{"index": 0, "delta": delta, "finish_reason": None}],
    }
    return f"data: {json.dumps(payload)}\n\n"


# ─────────────────────────── FastAPI app ─────────────────────────
app = FastAPI()

# ─────────────────── KVCache Copy Helper ───────────────────
def LATE_def_copy_mlx_lm_kv_cache(original_cache_list: List[Any]) -> List[Any]:
    """Creates a deep copy of a list of mlx-lm cache objects (e.g., KVCache, RotatingKVCache, QuantizedKVCache)."""
    if original_cache_list is None:
        return None
    
    copied_cache_list = []
    for item_cache in original_cache_list:
        new_item_cache = type(item_cache)() # Create new instance of the same type

        # Copy common attributes like offset and step
        if hasattr(item_cache, 'offset'):
            new_item_cache.offset = item_cache.offset
        if hasattr(item_cache, 'step'):
             new_item_cache.step = item_cache.step

        # Handle .keys and .values (which can be single mx.array or a tuple/list of them)
        for attr_name in ["keys", "values"]:
            original_attr_val = getattr(item_cache, attr_name, None)
            if original_attr_val is None:
                setattr(new_item_cache, attr_name, None)
            elif isinstance(original_attr_val, mx.array):
                # Use mx.array(original_array) to create a copy
                setattr(new_item_cache, attr_name, mx.array(original_attr_val))
            elif isinstance(original_attr_val, (list, tuple)):
                # Assuming it's a list/tuple of mx.arrays (like in QuantizedKVCache)
                copied_list_of_arrays = [
                    mx.array(arr) if isinstance(arr, mx.array) else arr 
                    for arr in original_attr_val
                ]
                setattr(new_item_cache, attr_name, type(original_attr_val)(copied_list_of_arrays))
            else:
                # Fallback for other types - this path should ideally not be hit for standard caches
                log.warning(f"Attribute '{attr_name}' of type {type(original_attr_val)} for cache item {type(item_cache)} is not an mx.array or list/tuple of mx.arrays. Attempting shallow copy.")
                setattr(new_item_cache, attr_name, original_attr_val)

        # Specific attributes for RotatingKVCache
        if isinstance(item_cache, RotatingKVCache):
            if hasattr(item_cache, 'max_size'): new_item_cache.max_size = item_cache.max_size
            if hasattr(item_cache, 'keep'): new_item_cache.keep = item_cache.keep
            if hasattr(item_cache, '_idx'): new_item_cache._idx = item_cache._idx
        
        # Specific attributes for QuantizedKVCache
        if isinstance(item_cache, QuantizedKVCache):
            if hasattr(item_cache, 'group_size'): new_item_cache.group_size = item_cache.group_size
            if hasattr(item_cache, 'bits'): new_item_cache.bits = item_cache.bits

        copied_cache_list.append(new_item_cache)
        
    return copied_cache_list

@app.get("/v1/models")
async def list_models() -> dict:
    """Return the single loaded model in OpenAI's `/v1/models` schema."""

    model_info = {
        "id": MODEL_NAME,
        "object": "model",
        "created": MODEL_CREATED,
        "owned_by": "kamiwaza",
    }
    return {"object": "list", "data": [model_info]}


@app.post("/v1/chat/completions")
async def completions(req: ChatReq):  # noqa: C901 – same as original
    if req.model != MODEL_NAME:
        log.warning("Requested model '%s' ≠ loaded '%s'", req.model, MODEL_NAME)

    imgs = [load_image(u) for u in req.all_images] if IS_VISION else []
    prompt_str = build_prompt(req, len(imgs))
    
    # Extract system prompt for caching
    system_prompt_str = build_system_prompt(req) if not IS_VISION else ""

    global GLOBAL_PROMPT_CACHE, CACHE_PRIMED_THIS_SESSION, CACHED_PREFIX_LEN, CACHE_PREFIX_HASH  # Ensure globals are modifiable

    # ----- determine if existing cache should be discarded -----
    should_discard_cache = False
    if args.enable_prefix_caching and not IS_VISION and GLOBAL_PROMPT_CACHE is not None and system_prompt_str:
        # A cache exists and we have a system prompt. Check if the system prompt has changed.
        current_system_ids = _encode(system_prompt_str)
        current_system_hash = _hash_tokens(current_system_ids)
        
        if current_system_hash != CACHE_PREFIX_HASH:
            # System prompt has changed. Cache is not usable and should be replaced.
            log.info(
                "🔄 System prompt has changed. Discarding old cache."
            )
            should_discard_cache = True
        # else: system prompt matches -> keep cache

    if should_discard_cache:
        log.info("Executing cache discard operation.")
        GLOBAL_PROMPT_CACHE = None
        CACHED_PREFIX_LEN = 0
        CACHE_PREFIX_HASH = ""
        CACHE_PRIMED_THIS_SESSION = False
        try:
            if GLOBAL_CACHE_FILE_PATH:
                len_path = GLOBAL_CACHE_FILE_PATH + ".len"
                hash_path = GLOBAL_CACHE_FILE_PATH + ".hash"
                if os.path.exists(GLOBAL_CACHE_FILE_PATH):
                    os.remove(GLOBAL_CACHE_FILE_PATH)
                    log.info(f"Deleted cache file: {GLOBAL_CACHE_FILE_PATH}")
                if os.path.exists(len_path):
                    os.remove(len_path)
                    log.info(f"Deleted cache length file: {len_path}")
                if os.path.exists(hash_path):
                    os.remove(hash_path)
                    log.info(f"Deleted cache hash file: {hash_path}")
        except Exception as e:
            log.warning(f"Could not delete old cache files: {e}")
    # -----------------------------------------------------------------------

    # Create cache if needed and we have a system prompt
    if (args.enable_prefix_caching and not IS_VISION and GLOBAL_PROMPT_CACHE is None and 
        not CACHE_PRIMED_THIS_SESSION and GLOBAL_CACHE_FILE_PATH is not None and system_prompt_str):
        log.info(f"Creating system message cache from current request, saving to {GLOBAL_CACHE_FILE_PATH}...")
        cache_creation_start_time = time.perf_counter()
        try:
            system_ids = _encode(system_prompt_str)
            if system_ids.ndim == 1:
                system_ids = system_ids[None, :]
            
            temp_cache = make_prompt_cache(MODEL)
            MODEL(system_ids, cache=temp_cache)  # Prime the cache with system prompt only

            CACHED_PREFIX_LEN = int(system_ids.shape[-1])
            CACHE_PREFIX_HASH = _hash_tokens(system_ids)
            try:
                Path(GLOBAL_CACHE_FILE_PATH + ".len").write_text(str(CACHED_PREFIX_LEN))
                Path(GLOBAL_CACHE_FILE_PATH + ".hash").write_text(CACHE_PREFIX_HASH)
            except Exception:
                pass

            GLOBAL_PROMPT_CACHE = temp_cache
            save_prompt_cache(GLOBAL_CACHE_FILE_PATH, GLOBAL_PROMPT_CACHE)
            CACHE_PRIMED_THIS_SESSION = True
            cache_creation_duration = time.perf_counter() - cache_creation_start_time
            log.info(f"System message cache created and saved ({CACHED_PREFIX_LEN} tokens) in {cache_creation_duration:.2f} seconds.")
        except Exception as e:
            log.error(f"Error creating/priming system message cache: {e}")

    # The generation functions (sync_gen, stream_chunks) will use GLOBAL_PROMPT_CACHE if set

    if not req.stream:
        txt = strip_thoughts(sync_gen(prompt_str, imgs, req), req.strip_thinking or args.strip_thinking)

        if IS_VISION:
            usage = _usage_dict(len(prompt_str), _tok_len(txt), 0.0, 0)
        else:
            usage = req.__dict__.get("_usage")
            if not isinstance(usage, dict):
                p_tok, c_tok, dur = (len(prompt_str), len(txt), 0.0)
                usage = _usage_dict(p_tok, c_tok, dur, 0)
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": txt},
                    "finish_reason": "stop",
                }
            ],
            "usage": usage,
        }

    async def event_stream():
        for chunk in stream_chunks(prompt_str, imgs, req):
            yield chunk
            await asyncio.sleep(0)

    if req.stream:
        return StreamingResponse(event_stream(), media_type="text/event-stream")
    else:
        if IS_VISION:
            usage = _usage_dict(len(prompt_str), _tok_len(txt), 0.0, 0)
        else:
            usage = req.__dict__.get("_usage")
            if not isinstance(usage, dict):
                p_tok, c_tok, dur = (len(prompt_str), len(txt), 0.0)
                usage = _usage_dict(p_tok, c_tok, dur, 0)
        return {
            "id": f"chatcmpl-{uuid.uuid4()}",
            "object": "chat.completion",
            "created": int(time.time()),
            "model": MODEL_NAME,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": txt},
                    "finish_reason": "stop",
                }
            ],
            "usage": usage,
        }

def main_entry() -> None:
    uvicorn.run(app, host=args.host, port=args.port)

# ─────────────────────────── main ────────────────────────────────
if __name__ == "__main__":
    log.info(
        "Serving %s on %s:%d  (vision=%s)", MODEL_NAME, args.host, args.port, IS_VISION
    )
    uvicorn.run(app, host=args.host, port=args.port) 
