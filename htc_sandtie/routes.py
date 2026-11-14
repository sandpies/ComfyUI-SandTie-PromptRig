# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""SandTie HTTP routes (/sandtie_rig/sandtie/*), 128px thumb cache, Auto-Wake writer, and Reference Bible CRUD."""
from __future__ import annotations

import asyncio
import hashlib
import os

SANDTIE_OPTIONS_ROUTE = "/sandtie_rig/sandtie/options"
SANDTIE_WRITE_ROUTE = "/sandtie_rig/sandtie/write"
SANDTIE_EXTRACT_ROUTE = "/sandtie_rig/sandtie/extract_video"
SANDTIE_PRESET_ROUTE = "/sandtie_rig/sandtie/preset"
SANDTIE_REFBANK_ROUTE = "/sandtie_rig/sandtie/ref_bank"
SANDTIE_THUMB_ROUTE = "/sandtie_rig/sandtie/thumb"

TAG = "SandTiePromptRig"


def _build_ref_thumb(src_path: str, width: int = 128) -> str | None:
    from . import refs as _refs
    try:
        from PIL import Image, ImageOps
    except Exception:
        return None
    if not src_path or not os.path.isfile(src_path):
        return None
    w = max(48, min(320, int(width or 128)))
    try:
        st = os.stat(src_path)
        key = f"{os.path.basename(src_path)}|{int(st.st_mtime)}|{st.st_size}|{w}"
    except Exception:
        key = f"{src_path}|{w}"
    tdir = _refs.thumb_cache_dir()
    digest = hashlib.sha1(key.encode("utf-8", "ignore")).hexdigest()[:24]
    out_path = os.path.join(tdir, f"{digest}_{w}.jpg")
    if os.path.isfile(out_path) and os.path.getsize(out_path) > 0:
        return out_path
    try:
        with Image.open(src_path) as im:
            im = ImageOps.exif_transpose(im)
            if im.mode in ("RGBA", "LA", "P"):
                rgba = im.convert("RGBA")
                bg = Image.new("RGB", rgba.size, (22, 24, 28))
                bg.paste(rgba, mask=rgba.split()[-1])
                im = bg
            elif im.mode != "RGB":
                im = im.convert("RGB")
            im.thumbnail((w, w), Image.Resampling.LANCZOS)
            tmp = out_path + ".tmp"
            im.save(tmp, format="JPEG", quality=84, optimize=True)
            os.replace(tmp, out_path)
        return out_path
    except Exception:
        return None


async def ensure_writer_ready(_llm, auto_wake: bool = True) -> tuple[bool, str]:
    conn = _llm.load_conn()
    backend = _llm.backend_name(conn.get("backend"))
    if await _llm.server_running_async(backend):
        return True, "running"
    if backend != "ninfer" or not auto_wake:
        return False, f"{_llm.active_label()} is not running."
    ok, msg = await _llm.start_process_async(name="ninfer")
    if not ok:
        return False, msg
    for _ in range(50):
        await asyncio.sleep(1.5)
        if await _llm.server_running_async("ninfer"):
            return True, "auto-started nInfer"
        err = _llm.startup_error("ninfer")
        if err:
            return False, f"nInfer stopped during startup: {err}"
    return False, "nInfer did not answer within 75s after auto-start."


def _wait_for_ninfer_exit(timeout_ms: int = 2500) -> int:
    stopped = 0
    try:
        import ctypes
        from ctypes import wintypes

        TH32CS_SNAPPROCESS = 0x00000002
        SYNCHRONIZE = 0x00100000
        PROCESS_TERMINATE = 0x0001
        INVALID_HANDLE_VALUE = ctypes.c_void_p(-1).value

        class PROCESSENTRY32(ctypes.Structure):
            _fields_ = [
                ("dwSize", wintypes.DWORD), ("cntUsage", wintypes.DWORD),
                ("th32ProcessID", wintypes.DWORD), ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)),
                ("th32ModuleID", wintypes.DWORD), ("cntThreads", wintypes.DWORD),
                ("th32ParentProcessID", wintypes.DWORD), ("pcPriClassBase", ctypes.c_long),
                ("dwFlags", wintypes.DWORD), ("szExeFile", ctypes.c_char * 260),
            ]

        k32 = ctypes.WinDLL("kernel32", use_last_error=True)
        snap = k32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
        if snap == INVALID_HANDLE_VALUE:
            return 0
        pe = PROCESSENTRY32()
        pe.dwSize = ctypes.sizeof(PROCESSENTRY32)
        try:
            ok = k32.Process32First(snap, ctypes.byref(pe))
            while ok:
                name = (pe.szExeFile or b"").decode("latin-1", "ignore").lower()
                if name == "ninfer-serve.exe":
                    h = k32.OpenProcess(PROCESS_TERMINATE | SYNCHRONIZE, False, pe.th32ProcessID)
                    if h:
                        if k32.TerminateProcess(h, 0):
                            print(f"[{TAG}] stopped {name} (pid {pe.th32ProcessID})", flush=True)
                            stopped += 1
                        k32.WaitForSingleObject(h, int(timeout_ms))
                        k32.CloseHandle(h)
                ok = k32.Process32Next(snap, ctypes.byref(pe))
        finally:
            k32.CloseHandle(snap)
    except Exception:
        pass
    return stopped


def register_sandtie_routes(instance, web) -> None:
    from .. import llm as _llm
    from .. import media as _media
    from ..htc_compat import mv_solver as _mvs
    from . import catalogs as _cat
    from . import finisher as _fin
    from . import refs as _refs
    from . import vision_cv as _vcv
    from . import writer as _wr

    def _free_writer_on_prompt(json_data):
        try:
            conn = _llm.load_conn()
            if conn.get("unload_on_run", True):
                spec = _llm.backend_spec(conn.get("backend"))
                if not spec.get("evictable", True):
                    n_stopped = _llm.stop_process()
                    n_waited = _wait_for_ninfer_exit(2500)
                    if n_stopped or n_waited:
                        print(f"[{TAG}] auto-stopped {spec['label']} before render", flush=True)
                else:
                    _llm.free_for_render()
        except Exception as exc:
            print(f"[{TAG}] on_prompt writer stop skipped: {exc!r}", flush=True)
        return json_data

    if hasattr(instance, "add_on_prompt_handler"):
        instance.add_on_prompt_handler(_free_writer_on_prompt)

    @instance.routes.get(SANDTIE_OPTIONS_ROUTE)
    async def _sandtie_options(request):
        try:
            conn = _llm.load_conn()
            running = await _llm.server_running_async(conn.get("backend"))
            lite = str(request.query.get("lite") or "").strip().lower() in ("1", "true", "yes")
            payload = {
                "ok": True,
                "running": running,
                "backend": conn.get("backend") or "lmstudio",
                "backend_label": _llm.backend_spec(conn.get("backend"))["label"],
                "model": conn.get("model") or "",
                "startup_error": "" if running else _llm.startup_error(conn.get("backend")),
            }
            if not lite:
                payload["catalog"] = _cat.ui_catalog()
            return web.json_response(payload)
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=500)

    @instance.routes.post(SANDTIE_PRESET_ROUTE)
    async def _sandtie_preset(request):
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "expected JSON"}, status=400)
        body = body if isinstance(body, dict) else {}
        pid = str(body.get("id") or "").strip()
        raw_script = str(body.get("script") or "").strip()
        text = raw_script or _cat.load_preset_script(pid)
        if not text:
            return web.json_response({"ok": False, "error": f"Preset not found: {pid}"})
        if body.get("adapt"):
            dur_label = str(body.get("duration") or "").strip()
            frames = _mvs.DURATION_FRAMES.get(dur_label)
            try:
                duration_s = (frames / 24.0) if frames else float(dur_label.split()[0])
            except Exception:
                duration_s = 10.0
            raw_vf = body.get("voice_files")
            voice_files = [str(v or "").strip() for v in (raw_vf if isinstance(raw_vf, list) else ()) if str(v or "").strip()]
            flavors = body.get("flavors") if isinstance(body.get("flavors"), dict) else {}
            adapted = _fin.adapt_preset_script(
                text, ref_plan=str(body.get("ref_plan") or ""),
                duration_s=duration_s, voice_files=voice_files,
                flavors=flavors, brief=str(body.get("brief") or ""),
            )
            adapted["id"] = pid
            return web.json_response(adapted)
        return web.json_response({"ok": True, "id": pid, "script": text})

    @instance.routes.get(SANDTIE_THUMB_ROUTE)
    async def _sandtie_thumb(request):
        fname = os.path.basename(str(request.query.get("file") or "").strip())
        if not fname:
            return web.Response(status=400, text="missing file")
        fpath = _media.resolve(fname, kinds={"image"})
        if not fpath or not os.path.isfile(fpath):
            return web.Response(status=404, text="not found")
        try:
            width = int(request.query.get("w") or 128)
        except Exception:
            width = 128
        thumb_path = await asyncio.get_running_loop().run_in_executor(None, _build_ref_thumb, fpath, width)
        target = thumb_path if (thumb_path and os.path.isfile(thumb_path)) else fpath
        headers = {"Cache-Control": "public, max-age=31536000, immutable" if request.query.get("v") else "public, max-age=300"}
        return web.FileResponse(target, headers=headers)

    @instance.routes.get(SANDTIE_REFBANK_ROUTE)
    async def _sandtie_refbank_get(_request):
        try:
            return web.json_response({"ok": True, "items": _refs.load_ref_bank()})
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=500)

    @instance.routes.post(SANDTIE_REFBANK_ROUTE)
    async def _sandtie_refbank_post(request):
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "expected JSON"}, status=400)
        body = body if isinstance(body, dict) else {}
        action = str(body.get("action") or "list").strip().lower()
        try:
            if action == "list":
                return web.json_response({"ok": True, "items": _refs.load_ref_bank()})
            if action == "save":
                saved = _refs.upsert_ref_bank_item(body.get("item") if isinstance(body.get("item"), dict) else body, user_edited=True)
                return web.json_response({"ok": True, "item": saved, "items": _refs.load_ref_bank()})
            if action == "delete":
                removed = _refs.delete_ref_bank_item(str(body.get("id") or ""), file_name=str(body.get("file") or ""))
                return web.json_response({"ok": True, "removed": removed, "items": _refs.load_ref_bank()})
            if action == "import_rail":
                items = _refs.import_rail_to_ref_bank(str(body.get("ref_plan") or ""), voice_files=body.get("voice_files") or ())
                return web.json_response({"ok": True, "items": items})
            if action == "scan":
                fname = os.path.basename(str(body.get("file") or "").strip())
                role = str(body.get("role") or "subject").strip().lower()
                auto_wake = bool(body.get("auto_wake", True))
                fpath = _media.resolve(fname)
                if not fpath or not os.path.isfile(fpath):
                    return web.json_response({"ok": False, "error": f"Could not resolve image in h3_refs: {fname}"})
                ready, wake_msg = await ensure_writer_ready(_llm, auto_wake=auto_wake)
                if not ready:
                    return web.json_response({"ok": False, "error": wake_msg})
                conn = _llm.load_conn()
                if not conn.get("model"):
                    found = await _llm.models(conn["server_url"])
                    if found:
                        conn["model"] = found[0]["id"]

                async def complete_fn(messages, schema=None, temperature=0.1, max_tokens=320):
                    return await _llm.complete(conn["server_url"], conn["model"], messages, schema=schema, temperature=temperature, max_tokens=max_tokens)

                scanned = await _vcv.scan_reference_file(fpath, role if role in ("subject", "place", "prop") else "auto", complete_fn)
                if not scanned:
                    return web.json_response({"ok": False, "error": "Eye Scan returned empty description."})
                import re
                cleaned = _refs.clean_subject_scan_desc(scanned) if role == "subject" else re.sub(r"^(?:Set|Prop):\s*", "", scanned, flags=re.I).strip()
                existing = _refs.find_ref_bank_entry(file_name=fname) or {}
                saved = _refs.upsert_ref_bank_item({
                    "id": body.get("id") or existing.get("id") or "",
                    "name": body.get("name") or existing.get("name") or "",
                    "tag": body.get("tag") or existing.get("tag") or "",
                    "role": role,
                    "file": fname,
                    "voice": body.get("voice") or existing.get("voice") or "",
                    "desc": cleaned or scanned,
                    "locked": body.get("locked") or existing.get("locked") or "",
                    "context": body.get("context") or existing.get("context") or "",
                }, user_edited=True)
                return web.json_response({"ok": True, "item": saved, "items": _refs.load_ref_bank()})
            return web.json_response({"ok": False, "error": f"Unknown ref_bank action: {action}"}, status=400)
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)})

    @instance.routes.post(SANDTIE_EXTRACT_ROUTE)
    async def _sandtie_extract(request):
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "expected JSON"}, status=400)
        video_file = str((body or {}).get("video_file") or "").strip()
        in_sec = float((body or {}).get("in_sec") or 0.0)
        out_sec = float((body or {}).get("out_sec") or 0.0)
        auto_wake = bool((body or {}).get("auto_wake", True))
        if not video_file:
            return web.json_response({"ok": False, "error": "Pick a video file first."})
        vpath = _media.resolve(video_file)
        if not vpath or not os.path.isfile(vpath):
            return web.json_response({"ok": False, "error": f"Could not resolve video file: {video_file}"})
        ready, wake_msg = await ensure_writer_ready(_llm, auto_wake=auto_wake)
        if not ready:
            return web.json_response({"ok": False, "error": wake_msg})
        conn = _llm.load_conn()
        if not conn.get("model"):
            found = await _llm.models(conn["server_url"])
            if found:
                conn["model"] = found[0]["id"]

        async def complete_fn(messages, schema=None, temperature=0.25, max_tokens=2200):
            return await _llm.complete(conn["server_url"], conn["model"], messages, schema=schema, temperature=temperature, max_tokens=max_tokens)

        try:
            res = await _vcv.extract_video_to_plan(vpath, complete_fn, in_sec=in_sec, out_sec=out_sec)
            res["woke_writer"] = wake_msg == "auto-started nInfer"
            return web.json_response(res)
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)})

    @instance.routes.post(SANDTIE_WRITE_ROUTE)
    async def _sandtie_write(request):
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "expected JSON"}, status=400)
        if not isinstance(body, dict):
            return web.json_response({"ok": False, "error": "expected JSON object"}, status=400)

        stage = str(body.get("stage") or "write").strip().lower()
        brief = str(body.get("brief") or "").strip()
        plan = str(body.get("plan") or "").strip()
        dur_label = str(body.get("duration") or "").strip()
        ref_plan = str(body.get("ref_plan") or "")
        start_file = str(body.get("start_image_file") or "").strip()
        raw_vf = body.get("voice_files")
        voice_files = [str(v or "").strip() for v in (raw_vf if isinstance(raw_vf, list) else ()) if str(v or "").strip()]
        flavors = body.get("flavors") if isinstance(body.get("flavors"), dict) else {}
        extracted_video = body.get("extracted_video") if isinstance(body.get("extracted_video"), dict) else None
        prev_hop_context = str(body.get("prev_hop_context") or "").strip()
        auto_wake = bool(flavors.get("wake_writer", flavors.get("auto_wake", True)))

        frames = _mvs.DURATION_FRAMES.get(dur_label)
        try:
            duration_s = (frames / 24.0) if frames else float(dur_label.split()[0])
        except Exception:
            duration_s = 10.0

        if stage in ("skeleton", "cpu"):
            try:
                out = await _wr.run_sandtie_write(
                    stage, brief or "Perform the configured scene.", complete_fn=None,
                    ref_plan=ref_plan, duration_s=duration_s,
                    start_image="1" if start_file else None, plan=plan,
                    voice_files=voice_files, flavors=flavors, extracted_video=extracted_video,
                    prev_hop_context=prev_hop_context,
                )
                out["duration_s"] = round(duration_s, 3)
                return web.json_response(out)
            except Exception as exc:
                return web.json_response({"ok": False, "error": str(exc)})

        if not brief and not extracted_video and not (stage == "dialogue" and str(flavors.get("current_block") or plan or "").strip()):
            return web.json_response({"ok": False, "error": "Type a scene brief (or extract a video) first."})

        ready, wake_msg = await ensure_writer_ready(_llm, auto_wake=auto_wake)
        if not ready:
            return web.json_response({"ok": False, "error": wake_msg})

        conn = _llm.load_conn()
        if not conn.get("model"):
            found = await _llm.models(conn["server_url"])
            if found:
                conn["model"] = found[0]["id"]
            else:
                return web.json_response({"ok": False, "error": "no model selected -- click ⚙ beside Writer status (or WRITE -> Settings) and pick one."})

        def encode():
            try:
                lab = _refs.sandtie_labels(ref_plan, voice_files=voice_files)
            except Exception:
                lab = {"pictures": [], "audios": []}
            ims = []
            for p in lab.get("pictures") or []:
                url = _media.vision_data_url(p["file"]) if p.get("file") else None
                if url:
                    ims.append({"tag": p["tag"], "data_url": url})
            start_url = _media.vision_data_url(start_file) if start_file else None
            start_path = _media.resolve(start_file) if start_file else ""
            return ims, start_url, start_path

        try:
            images, start_url, start_path = await asyncio.get_running_loop().run_in_executor(None, encode)
        except Exception:
            images, start_url, start_path = [], None, ""

        notes = []
        if wake_msg == "auto-started nInfer":
            notes.append("nInfer was stopped after your last render — auto-started it in VRAM.")
        write_temp = max(0.9, float(conn.get("temperature") or 0.95)) if conn.get("backend") == "ninfer" else float(conn.get("temperature") or 0.8)

        async def complete_fn(messages, schema=None, temperature=None, max_tokens=None):
            t_use = write_temp if temperature is None else float(temperature)
            kw = {"schema": schema, "temperature": t_use}
            if max_tokens is not None:
                kw["max_tokens"] = int(max_tokens)
            try:
                return await _llm.complete(conn["server_url"], conn["model"], messages, **kw)
            except _llm.LLMError as exc:
                if _llm.has_images(messages) and "HTTP 4" in str(exc):
                    notes.append("model processed labels as text-only")
                    return await _llm.complete(conn["server_url"], conn["model"], _llm.text_only(messages), **kw)
                raise

        try:
            out = await _wr.run_sandtie_write(
                stage, brief, complete_fn=complete_fn, ref_plan=ref_plan,
                duration_s=duration_s, images=images, start_image=start_url,
                start_image_path=start_path or "", plan=plan, voice_files=voice_files,
                flavors=flavors, extracted_video=extracted_video,
                prev_hop_context=prev_hop_context, resolve_file_fn=_media.resolve,
            )
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)})

        if notes:
            out["warnings"] = list(out.get("warnings") or []) + notes
        out["duration_s"] = round(duration_s, 3)
        out["running"] = await _llm.server_running_async(conn.get("backend"))
        if not conn.get("keep_warm") and _llm.backend_spec(conn.get("backend")).get("evictable", True):
            try:
                await _llm.unload(conn["server_url"], conn["model"])
            except Exception:
                pass
        return web.json_response(out)
