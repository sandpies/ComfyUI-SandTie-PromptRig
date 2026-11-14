# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""SandTie PromptRig (H3) — Standalone MiniMax H3 Prompt & Conditioning Rig for ComfyUI."""
from .sandtie_node import NODE_CLASS_MAPPINGS, NODE_DISPLAY_NAME_MAPPINGS

try:
    from aiohttp import web as _web
    from server import PromptServer as _PromptServer
    from .htc_compat import register_extra_routes as _register_extra
    from .htc_sandtie import routes as _st_routes

    _inst = getattr(_PromptServer, "instance", None)
    if _inst is not None:
        _st_routes.register_sandtie_routes(_inst, _web)
        _register_extra(_inst, _web)
except Exception as _exc:  # noqa: BLE001
    print(f"[SandTiePromptRig] routes skipped: {_exc!r}", flush=True)

WEB_DIRECTORY = "./js"

__all__ = ["NODE_CLASS_MAPPINGS", "NODE_DISPLAY_NAME_MAPPINGS", "WEB_DIRECTORY"]
