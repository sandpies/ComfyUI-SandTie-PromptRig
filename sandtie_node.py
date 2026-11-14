# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""SandTiePromptRig — Dual-Mode MiniMax H3 Prompt & Conditioning Rig for ComfyUI."""
from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re

from comfy_api.latest import io

from . import media as _media
from .htc_compat import standard as _std
from .htc_sandtie import finisher as _st_fin
from .htc_sandtie import refs as _st_refs
from .htc_sandtie import writer as _st_writer

TAG = "SandTiePromptRig"

WIRE_MODES = [
    "Prompt Only -> Stock H3 Node",
    "Direct H3 Conditioning (+ CLIP/VAE)",
]

H3_FORMATS = [
    "MiniMax H3 Auto (Ref2VA / T2VA)",
    "MiniMax H3 I2VA (First Frame)",
    "MiniMax H3 FL2VA (First + Last Frame)",
    "MiniMax H3 L2VA (Last Frame)",
    "Start Frame Prep (Still Image Prompt)",
    "Storyboard Beats Only",
]

_FMT_TO_CODE = {
    "MiniMax H3 Auto (Ref2VA / T2VA)": "h3_auto",
    "MiniMax H3 I2VA (First Frame)": "h3_i2va",
    "MiniMax H3 FL2VA (First + Last Frame)": "h3_fl2va",
    "MiniMax H3 L2VA (Last Frame)": "h3_l2va",
    "Start Frame Prep (Still Image Prompt)": "h3_keyframe",
    "Storyboard Beats Only": "h3_beats",
}

WRITE_MODES = [
    "LLM + Double-Knot (2-Pass)",
    "LLM 1-Pass Quick Tie",
    "Instant CPU Tie (0 VRAM)",
]

ASPECTS = ["16:9", "9:16"]
DURATIONS = ["5 s", "6 s", "8 s", "10 s", "12 s", "13 s", "14 s", "15 s"]
FPS = 24
CANVAS_MULTIPLE = 32


def _parse_dur_seconds(label: str) -> float:
    m = re.search(r"(\d+(?:\.\d+)?)", str(label or ""))
    if m:
        return max(2.0, min(20.0, float(m.group(1))))
    return 10.0


def _snap_dim(px: int) -> int:
    return max(CANVAS_MULTIPLE, round(int(px) / CANVAS_MULTIPLE) * CANVAS_MULTIPLE)


def _resolve_canvas_size(aspect: str, width: int, height: int) -> tuple[int, int]:
    if int(width or 0) > 0 and int(height or 0) > 0:
        return _snap_dim(int(width)), _snap_dim(int(height))
    return (768, 1344) if str(aspect or "16:9") == "9:16" else (1344, 768)


def _align_frames(dur_s: float) -> int:
    n = max(5, int(round(float(dur_s) * FPS)))
    while n % 17 != 5:
        n += 1
    return n


def _split_h3_sections(block: str) -> tuple[str, str, str]:
    """Extract (storyboard_or_desc, soundscape, music) cleanly from an H3 prompt block."""
    t = str(block or "").strip()
    if not t:
        return "", "", ""
    desc = _std._field(t, "detailed_description:") or _std._field(t, "integrated_multimodal_description:") or t
    snd = _std._field(t, "overall_soundscape:") or ""
    mus = _std._field(t, "non_diegetic_music:") or ""
    return desc.strip(), snd.strip(), mus.strip()


def _parse_rig_state(raw: str) -> dict:
    try:
        doc = json.loads(str(raw or "{}") or "{}")
        return doc if isinstance(doc, dict) else {}
    except Exception:
        return {}


def _save_tensor_ref_if_needed(img_tensor, prefix: str) -> str:
    """Persist a wired IMAGE tensor to `<input>/h3_refs/` by content hash so Eye Scan can reference it."""
    if img_tensor is None:
        return ""
    try:
        import numpy as np
        from PIL import Image
        arr = img_tensor
        if hasattr(arr, "detach"):
            arr = arr[0].detach().cpu().numpy()
        arr = (np.clip(arr, 0.0, 1.0) * 255.0).astype(np.uint8)
        h = hashlib.sha1(arr.tobytes()).hexdigest()[:12]
        fname = f"sandtie_{prefix}_{h}.png"
        dest_dir = _media.refs_dir(create=True)
        dest_path = os.path.join(dest_dir, fname)
        if not os.path.isfile(dest_path):
            Image.fromarray(arr).save(dest_path, format="PNG")
        return fname
    except Exception:
        return ""


def _ordered_autogrow_items(group_dict: dict | None, prefix: str, limit: int) -> list[tuple[int, object]]:
    """Extract ordered `(slot_1based, value)` pairs from an Autogrow dict (`ref_image_1..9`, etc.)."""
    out: list[tuple[int, object]] = []
    if not isinstance(group_dict, dict):
        return out
    rows: list[tuple[int, object]] = []
    for k, v in group_dict.items():
        if v is None:
            continue
        m = re.search(r"(\d+)$", str(k))
        idx = int(m.group(1)) if m else len(rows) + 1
        rows.append((idx, v))
    rows.sort(key=lambda x: x[0])
    for idx, v in rows[:limit]:
        out.append((idx, v))
    return out


def _build_wired_ref_plan(ref_plan_json: str, wired_imgs: list[tuple[int, object]]) -> str:
    """Merge any canvas-wired `ref_image_1..9` sockets into `ref_plan_json` cleanly if not already listed."""
    raw = str(ref_plan_json or "").strip()
    try:
        doc = json.loads(raw) if raw else {}
    except Exception:
        doc = {}
    if not isinstance(doc, dict):
        doc = {}
    refs = list(doc.get("refs") or [])
    by_slot = {int(r.get("slot") or 0): r for r in refs if isinstance(r, dict)}
    changed = False
    for slot_idx, tensor in wired_imgs:
        if tensor is None:
            continue
        existing = by_slot.get(slot_idx)
        if existing and str(existing.get("file") or "").strip():
            continue
        fname = _save_tensor_ref_if_needed(tensor, f"ref{slot_idx}")
        if fname:
            refs = [r for r in refs if int(r.get("slot") or 0) != slot_idx]
            refs.append({
                "slot": slot_idx,
                "tag": f"subject{slot_idx}",
                "file": fname,
                "subject": slot_idx,
                "retention": "fully_preserved",
                "desc": "",
            })
            changed = True
    if not changed:
        return raw
    doc["refs"] = sorted(refs, key=lambda r: int(r.get("slot") or 0))
    doc.setdefault("subjects", {})
    return json.dumps(doc, separators=(",", ":"))


def _collect_conditioning_media(
    ref_plan_json: str,
    wired_imgs: list[tuple[int, object]],
    wired_vids: list[tuple[int, object]],
    wired_auds: list[tuple[int, object]],
) -> tuple[dict | None, dict | None, dict | None]:
    """Build ordered `ref_images`, `ref_videos`, `ref_audios` dicts merging Reference Bible files + canvas wires."""
    img_by_slot: dict[int, object] = {idx: t for idx, t in wired_imgs if t is not None}
    ordered_imgs: list[object] = []
    used_slots: set[int] = set()
    voice_files: list[str] = []

    try:
        doc = json.loads(str(ref_plan_json or "") or "{}")
    except Exception:
        doc = {}
    refs = sorted(
        [r for r in (doc.get("refs") or []) if isinstance(r, dict)],
        key=lambda r: int(r.get("slot") or 99),
    )

    for r in refs:
        if len(ordered_imgs) >= 9:
            break
        sl = int(r.get("slot") or 0)
        tensor = img_by_slot.get(sl) if sl >= 1 else None
        if tensor is None and str(r.get("file") or "").strip():
            fname = str(r["file"]).strip()
            tensor = _media.load_image(fname, cap_mp=float(r.get("mp") or 0.0))
            if tensor is None:
                raise FileNotFoundError(
                    f"{TAG}: Reference Bible image '{fname}' was not found in input/h3_refs/. "
                    "Re-upload it in SandTie Studio or remove it from the rail."
                )
        if tensor is not None:
            ordered_imgs.append(tensor)
            if sl >= 1:
                used_slots.add(sl)
        vf = str(r.get("voice") or "").strip()
        if vf and vf not in voice_files:
            voice_files.append(vf)

    for sl in sorted(img_by_slot):
        if sl in used_slots or len(ordered_imgs) >= 9:
            continue
        ordered_imgs.append(img_by_slot[sl])

    ref_images = {f"ref_image_{i + 1}": t for i, t in enumerate(ordered_imgs[:9])} or None

    ref_videos = {f"ref_video_{i + 1}": t for i, (_s, t) in enumerate(wired_vids[:3]) if t is not None} or None

    aud_items: list[dict] = []
    for _s, a in wired_auds[:3]:
        if a is not None:
            aud_items.append(a)
    for vf in voice_files:
        if len(aud_items) >= 3:
            break
        loaded = _media.load_audio(vf)
        if loaded is None:
            raise FileNotFoundError(
                f"{TAG}: Reference Bible voice audio '{vf}' was not found in input/h3_refs/. "
                "Update or clear the voice field in SandTie Studio."
            )
        aud_items.append(loaded)
    ref_audios = {f"ref_audio_{i + 1}": a for i, a in enumerate(aud_items[:3])} or None
    return ref_images, ref_videos, ref_audios


def _downstream_cond_or_latent_wired(dynprompt, unique_id) -> bool:
    """Detect whether output slot 1 (`positive`) or 2 (`latent`) is linked in the active ComfyUI prompt."""
    if dynprompt is None or not unique_id:
        return False
    try:
        orig = dynprompt.get_original_prompt() if hasattr(dynprompt, "get_original_prompt") else {}
        uid = str(unique_id)
        for node_info in (orig or {}).values():
            inputs = (node_info or {}).get("inputs") or {}
            for val in inputs.values():
                if isinstance(val, (list, tuple)) and len(val) >= 2 and str(val[0]) == uid and int(val[1]) in (1, 2):
                    return True
    except Exception:
        pass
    return False


class SandTiePromptRig(io.ComfyNode):
    """Dual-mode MiniMax H3 Prompt & Conditioning Rig (`Prompt Only` ⇄ `Direct H3 Conditioning`)."""

    @classmethod
    def define_schema(cls):
        ref_imgs_tpl = io.Autogrow.TemplateNames(
            input=io.Image.Input(
                "ref_image",
                tooltip="Canvas reference image (auto-grows up to 9; merges with Reference Bible).",
            ),
            names=[f"ref_image_{i}" for i in range(1, 10)],
            min=0,
        )
        ref_vids_tpl = io.Autogrow.TemplateNames(
            input=io.Image.Input(
                "ref_video",
                tooltip="Reference video frames at 24 fps (auto-grows up to 3).",
            ),
            names=[f"ref_video_{i}" for i in range(1, 4)],
            min=0,
        )
        ref_auds_tpl = io.Autogrow.TemplateNames(
            input=io.Audio.Input(
                "ref_audio",
                tooltip="Standalone voice or audio reference (auto-grows up to 3).",
            ),
            names=[f"ref_audio_{i}" for i in range(1, 4)],
            min=0,
        )
        return io.Schema(
            node_id="StandaloneSandTiePromptRig",
            display_name="SandTie PromptRig (H3)",
            category="MiniMax H3",
            description=(
                "Dual-mode MiniMax H3 Prompt & Conditioning Rig. "
                "In Prompt Only mode (0 VRAM), connect `prompt` straight into MiniMaxH3ReferenceToVideo / ImageToVideo. "
                "Switch wire_mode to Direct H3 Conditioning to encode Reference Bible + canvas refs into `positive` + `latent`."
            ),
            inputs=[
                io.DynamicCombo.Input("wire_mode", options=[
                    io.DynamicCombo.Option(WIRE_MODES[0], []),
                    io.DynamicCombo.Option(WIRE_MODES[1], [
                        io.Clip.Input("clip", tooltip="MiniMax H3 text encoder (Qwen3-VL)."),
                        io.Vae.Input("vae", optional=True, tooltip="MiniMax H3 Video VAE."),
                        io.Vae.Input("audio_vae", optional=True, tooltip="MiniMax H3 Audio VAE."),
                        io.Combo.Input("ref_image_size", options=["match", "max"], default="match", socketless=True),
                        io.Int.Input("width", default=0, min=0, max=4096, step=32,
                                     tooltip="0 = auto from aspect at H3 native 768p (1344x768 or 768x1344)."),
                        io.Int.Input("height", default=0, min=0, max=4096, step=32,
                                     tooltip="0 = auto from aspect at H3 native 768p."),
                    ]),
                ]),
                io.Combo.Input("h3_format", options=H3_FORMATS, default=H3_FORMATS[0], socketless=True),
                io.Autogrow.Input("ref_images", optional=True, template=ref_imgs_tpl),
                io.Autogrow.Input("ref_videos", optional=True, template=ref_vids_tpl),
                io.Autogrow.Input("ref_audios", optional=True, template=ref_auds_tpl),
                io.Image.Input("first_frame", optional=True, tooltip="Optional first-frame keyframe anchor (I2VA / FL2VA)."),
                io.Image.Input("last_frame", optional=True, tooltip="Optional last-frame keyframe anchor (FL2VA / L2VA)."),
                io.Combo.Input("write_mode", options=WRITE_MODES, default=WRITE_MODES[0], socketless=True),
                io.Combo.Input("aspect", options=ASPECTS, default="16:9", socketless=True),
                io.Combo.Input("duration", options=DURATIONS, default="10 s", socketless=True),
                io.String.Input("brief", multiline=True, default="", socketless=True),
                io.String.Input("brief_in", optional=True, force_input=True,
                                tooltip="Optional incoming brief string override (re-ties automatically when connected)."),
                io.String.Input("rig_state", default="{}", socketless=True,
                                tooltip="Internal SandTie Studio state JSON (prompt, storyboard, ref_plan, dials)."),
            ],
            outputs=[
                io.String.Output(display_name="prompt",
                                 tooltip="Compiled MiniMax H3 prompt (connect to MiniMaxH3ReferenceToVideo / ImageToVideo prompt)."),
                io.Conditioning.Output(display_name="positive",
                                       tooltip="Native MiniMax H3 conditioning (active when wire_mode = Direct H3 Conditioning)."),
                io.Latent.Output(display_name="latent",
                                 tooltip="Empty MiniMax H3 AV latent sized to aspect & duration (active in Direct H3 Conditioning mode)."),
            ],
            hidden=[io.Hidden.dynprompt, io.Hidden.unique_id],
        )

    @classmethod
    def fingerprint_inputs(cls, wire_mode=None, rig_state="{}", **kwargs):
        wm = wire_mode if isinstance(wire_mode, dict) else {"wire_mode": str(wire_mode or "")}
        if str(wm.get("wire_mode") or "") != WIRE_MODES[1]:
            return ""
        st = _parse_rig_state(rig_state)
        try:
            doc = json.loads(str(st.get("ref_plan_json") or "") or "{}")
        except Exception:
            return ""
        sig = []
        for r in doc.get("refs") or []:
            if not isinstance(r, dict):
                continue
            for fn in (r.get("file"), r.get("voice")):
                f = str(fn or "").strip()
                if not f:
                    continue
                p = _media.resolve(f)
                if p and os.path.isfile(p):
                    st_f = os.stat(p)
                    sig.append(f"{f}:{st_f.st_mtime_ns}:{st_f.st_size}")
                else:
                    sig.append(f"{f}:missing")
        return "|".join(sig)

    @classmethod
    def execute(
        cls,
        wire_mode: dict,
        h3_format: str = H3_FORMATS[0],
        ref_images: dict | None = None,
        ref_videos: dict | None = None,
        ref_audios: dict | None = None,
        first_frame=None,
        last_frame=None,
        write_mode: str = WRITE_MODES[0],
        aspect: str = "16:9",
        duration: str = "10 s",
        brief: str = "",
        brief_in: str = "",
        rig_state: str = "{}",
    ) -> io.NodeOutput:
        wm_dict = wire_mode if isinstance(wire_mode, dict) else {"wire_mode": str(wire_mode or WIRE_MODES[0])}
        fmt_label = str(h3_format.get("h3_format") if isinstance(h3_format, dict) else (h3_format or H3_FORMATS[0]))
        fmt_code = _FMT_TO_CODE.get(fmt_label, "h3_auto")
        dur_s = _parse_dur_seconds(duration)

        state = _parse_rig_state(rig_state)
        flavors = state.get("flavors") if isinstance(state.get("flavors"), dict) else {}
        flavors = dict(flavors)
        w_in = int(wm_dict.get("width") or 0)
        h_in = int(wm_dict.get("height") or 0)
        eff_aspect = ("9:16" if h_in > w_in else ("16:9" if w_in > h_in else "1:1")) if (w_in > 0 and h_in > 0) else aspect
        flavors["aspect"] = eff_aspect
        flavors["output_format"] = fmt_code
        flavors["double_knot"] = write_mode == WRITE_MODES[0]

        wired_imgs = _ordered_autogrow_items(ref_images, "ref_image_", 9)
        wired_vids = _ordered_autogrow_items(ref_videos, "ref_video_", 3)
        wired_auds = _ordered_autogrow_items(ref_audios, "ref_audio_", 3)

        ref_plan_raw = str(state.get("ref_plan_json") or "")
        merged_ref_plan = _build_wired_ref_plan(ref_plan_raw, wired_imgs)
        start_fname = _save_tensor_ref_if_needed(first_frame, "start") if first_frame is not None else ""

        cached_prompt = str(state.get("prompt_out") or "").strip()
        active_brief = str(brief_in or "").strip() or str(brief or "").strip()

        if cached_prompt and not str(brief_in or "").strip():
            out_prompt = _st_fin.format_h3_output(cached_prompt, output_format=fmt_code, duration_s=dur_s)
        else:
            stage = "keyframe" if fmt_code == "h3_keyframe" else "cpu"
            try:
                loop = asyncio.new_event_loop()
                try:
                    res = loop.run_until_complete(
                        _st_writer.run_sandtie_write(
                            stage,
                            active_brief or "Perform the staged scene cleanly.",
                            complete_fn=None,
                            ref_plan=merged_ref_plan,
                            duration_s=dur_s,
                            start_image="1" if start_fname else None,
                            flavors=flavors,
                        )
                    )
                finally:
                    loop.close()
            except Exception:
                lab = _st_refs.sandtie_labels(merged_ref_plan)
                res = _st_writer.build_cpu_tie_block(
                    active_brief or "Perform the staged scene cleanly.",
                    lab=lab,
                    duration_s=dur_s,
                    flavors=flavors,
                )
            out_prompt = str(res.get("block") or cached_prompt or "").strip()

        is_direct = str(wm_dict.get("wire_mode") or "") == WIRE_MODES[1]
        if not is_direct:
            dynp = getattr(getattr(cls, "hidden", None), "dynprompt", None)
            uid = getattr(getattr(cls, "hidden", None), "unique_id", None)
            if _downstream_cond_or_latent_wired(dynp, uid):
                raise ValueError(
                    f"{TAG}: `positive` or `latent` is wired while wire_mode is '{WIRE_MODES[0]}'. "
                    f"Switch wire_mode to '{WIRE_MODES[1]}' and connect `clip` (or connect only `prompt`)."
                )
            return io.NodeOutput(out_prompt, None, None)

        clip = wm_dict.get("clip")
        if clip is None:
            raise ValueError(f"{TAG}: Direct H3 Conditioning mode requires the `clip` input.")
        vae = wm_dict.get("vae")
        audio_vae = wm_dict.get("audio_vae")
        ref_image_size = str(wm_dict.get("ref_image_size") or "match")
        w, h = _resolve_canvas_size(aspect, int(wm_dict.get("width") or 0), int(wm_dict.get("height") or 0))
        length = _align_frames(dur_s)

        from comfy_extras.nodes_minimax_h3 import (
            MiniMaxH3ImageToVideo,
            MiniMaxH3ReferenceToVideo,
            PH3ImageConditioning,
        )

        ref_images, ref_videos, ref_audios = _collect_conditioning_media(
            merged_ref_plan, wired_imgs, wired_vids, wired_auds
        )

        if fmt_code == "h3_keyframe":
            ph3_imgs = None
            if ref_images:
                ph3_imgs = {f"image_{i + 1}": t for i, t in enumerate(ref_images.values())}
            cond_out = PH3ImageConditioning.execute(
                clip=clip,
                prompt=out_prompt,
                width=w,
                height=h,
                vae=vae,
                images=ph3_imgs,
            )
            return io.NodeOutput(out_prompt, cond_out.args[0], cond_out.args[1])

        if fmt_code in ("h3_i2va", "h3_fl2va", "h3_l2va"):
            if vae is None:
                raise ValueError(
                    f"{TAG}: Direct {fmt_code.upper()} conditioning requires the Video `vae` input."
                )
            if fmt_code in ("h3_i2va", "h3_fl2va") and first_frame is None:
                raise ValueError(f"{TAG}: Direct {fmt_code.upper()} conditioning requires `first_frame`.")
            if fmt_code in ("h3_l2va", "h3_fl2va") and last_frame is None:
                raise ValueError(f"{TAG}: Direct {fmt_code.upper()} conditioning requires `last_frame`.")
            cond_out = MiniMaxH3ImageToVideo.execute(
                clip=clip,
                vae=vae,
                prompt=out_prompt,
                width=w,
                height=h,
                length=length,
                first_frame=first_frame,
                last_frame=last_frame,
            )
            return io.NodeOutput(out_prompt, cond_out.args[0], cond_out.args[1])

        cond_out = MiniMaxH3ReferenceToVideo.execute(
            clip=clip,
            prompt=out_prompt,
            width=w,
            height=h,
            length=length,
            ref_image_size=ref_image_size,
            vae=vae,
            audio_vae=audio_vae,
            ref_images=ref_images,
            ref_videos=ref_videos,
            ref_audios=ref_audios,
        )
        return io.NodeOutput(out_prompt, cond_out.args[0], cond_out.args[1])


NODE_CLASS_MAPPINGS = {
    "StandaloneSandTiePromptRig": SandTiePromptRig,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "StandaloneSandTiePromptRig": "SandTie PromptRig (H3)",
}
