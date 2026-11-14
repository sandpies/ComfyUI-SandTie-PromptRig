# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""Self-contained pure-Python compatibility helpers & standalone routes for SandTie PromptRig."""
from __future__ import annotations

import hashlib as _hashlib
import json
import os as _os
import re
from types import SimpleNamespace


# -- mv_solver subset --------------------------------------------------------
DURATION_FRAMES = {
    "5 s": 124, "6 s": 141, "7 s": 175, "8 s": 192, "9 s": 209,
    "10 s": 243, "11 s": 260, "12 s": 294, "13 s": 311, "14 s": 328,
    "15 s": 362, "16 s": 379, "17 s": 413, "18 s": 430, "19 s": 464,
    "20 s": 481,
}
mv_solver = SimpleNamespace(DURATION_FRAMES=DURATION_FRAMES)


# -- planner subset ----------------------------------------------------------
_FENCE = re.compile(r"```(?:json)?\s*\n([\s\S]*?)\n```", re.I)


def _parse_obj(text):
    raw = str(text or "").strip()
    if not raw:
        return None
    try:
        obj = json.loads(raw)
        if isinstance(obj, dict):
            return obj
    except ValueError:
        pass
    for b in _FENCE.findall(raw):
        try:
            obj = json.loads(b.strip())
            if isinstance(obj, dict):
                return obj
        except ValueError:
            continue
    a, b = raw.find("{"), raw.rfind("}")
    if 0 <= a < b:
        try:
            obj = json.loads(raw[a:b + 1])
            if isinstance(obj, dict):
                return obj
        except ValueError:
            pass
    return None


def fence(text, tag):
    body = re.sub(r"</?\s*%s\s*>" % re.escape(tag), "", str(text or ""), flags=re.I)
    return f"<{tag}>\n{body}\n</{tag}>"


planner = SimpleNamespace(_parse_obj=_parse_obj, fence=fence)


# -- standard subset ---------------------------------------------------------
T2VA_FIELDS = ("integrated_multimodal_description:", "overall_soundscape:", "non_diegetic_music:")
REF2VA_FIELDS = (
    "subject_definitions:", "summary:", "retention_analysis:",
    "detailed_description:", "overall_soundscape:", "non_diegetic_music:",
)
_SHOT = re.compile(r"\[Shot (\d+)\]\s*(At (\d+):(\d+(?:\.\d+)?))?", re.I)
_RANGE = re.compile(r"\bAt (\d+):(\d+(?:\.\d+)?)\s*-\s*(\d+):(\d+(?:\.\d+)?)", re.I)
_NEG = re.compile(r"\b(no|not|never|without|avoid|don't|doesn't|isn't|can't|won't)\b", re.I)
_DLG = re.compile(r"<d>.*?</d>", re.S | re.I)
_LABEL = re.compile(r"<(Picture|Subject|Video|Audio) (\d+)>")


def _field(text, name):
    t = str(text or "")
    names = REF2VA_FIELDS + T2VA_FIELDS
    i = t.find(name)
    if i < 0:
        return ""
    j = len(t)
    for f in set(names):
        k = t.find(f, i + len(name))
        if k > -1:
            j = min(j, k)
    return t[i + len(name):j]


def _secs(m, a, b):
    return int(m.group(a)) * 60 + float(m.group(b))


def mode_for(lab):
    return "Ref2VA" if ((lab or {}).get("pictures") or (lab or {}).get("audios")) else "T2VA"


def contract_errors(block, *, mode, lab, duration_s):
    t = str(block or "")
    errs = []
    if not t.strip():
        return ["the block is empty"]
    if "```" in t:
        errs.append("remove the markdown fences: the block is pasted as is")
    fields = REF2VA_FIELDS if mode == "Ref2VA" else T2VA_FIELDS
    pos = [t.find(f) for f in fields]
    missing = [f for f, p in zip(fields, pos) if p < 0]
    if missing:
        errs.append(f"{mode} needs these fields, spelled exactly: {', '.join(missing)}")
    elif pos != sorted(pos):
        errs.append(f"the fields are out of order; {mode} order is: " + " / ".join(fields))
    if not missing and t.lstrip().find(fields[0]) != 0:
        errs.append(f"the block must start with `{fields[0]}`: nothing before it (no instruction line, no title)")
    if mode == "T2VA":
        if "subject_definitions:" in t or _LABEL.search(t):
            errs.append("T2VA has no reference labels: remove every <Picture N>, <Subject N>, <Video N>, <Audio N> and subject_definitions")
    else:
        pics = {p["n"] for p in lab.get("pictures") or []}
        subs = set((lab.get("subjects") or {}).keys())
        auds = {a["n"] for a in lab.get("audios") or []}
        used = {(k, int(n)) for k, n in _LABEL.findall(t)}
        for k, n in sorted(used):
            if k == "Picture" and n not in pics:
                errs.append(f"<Picture {n}> is not on the rail; the pictures are " + (", ".join(f"<Picture {x}>" for x in sorted(pics)) or "none"))
            if k == "Subject" and n not in subs:
                errs.append(f"<Subject {n}> is not defined by the rail")
            if k == "Audio" and n not in auds:
                errs.append((f"<Audio {n}> is not on the rail; the audios are " + ", ".join(f"<Audio {x}>" for x in sorted(auds))) if auds else f"remove <Audio {n}>: no audio reference is on the rail")
            if k == "Video":
                errs.append(f"remove <Video {n}>: the Standard writer cites no clips")
        for n in sorted(pics):
            if ("Picture", n) not in used:
                errs.append(f"<Picture {n}> is on the rail but never cited")
        for n in sorted(subs):
            if ("Subject", n) not in used:
                errs.append(f"<Subject {n}> is defined by the rail but never cited")
        for n in sorted(auds):
            if ("Audio", n) not in used:
                errs.append(f"<Audio {n}> is on the rail but never cited")
        summ = _field(t, "summary:")
        if summ and not re.match(r"\s*\[[^\]]+\]", summ):
            errs.append("summary must open with its [task type], e.g. [reference generation]")
        ret = _field(t, "retention_analysis:")
        for n in sorted(subs):
            if not re.search(rf"^\s*<Subject {n}>", ret, re.M):
                errs.append(f"retention_analysis needs its own line for <Subject {n}>")
        for p in lab.get("pictures") or []:
            if p.get("subject") is None and not re.search(rf"^\s*<Picture {p['n']}>", ret, re.M):
                errs.append(f"retention_analysis needs its own line for <Picture {p['n']}>")
        for a in lab.get("audios") or []:
            if not re.search(rf"^\s*<Audio {a['n']}>", ret, re.M):
                errs.append(f"retention_analysis needs its own line for <Audio {a['n']}>")
    if re.search(r"(?<![\w<])@\w", t):
        errs.append("no @tags in the block: use the labels the node listed")
    body = _field(t, "detailed_description:" if mode == "Ref2VA" else "integrated_multimodal_description:")
    shots = list(_SHOT.finditer(body))
    if not shots:
        errs.append("the description needs [Shot 1]")
    else:
        if shots[0].group(1) != "1" or shots[0].group(2):
            errs.append("[Shot 1] comes first and has no timestamp")
        last = 0.0
        for m in shots[1:]:
            if not m.group(2):
                errs.append(f"[Shot {m.group(1)}] needs `At MM:SS.mmm,`")
                continue
            s = _secs(m, 3, 4)
            if s <= last or s >= float(duration_s):
                errs.append(f"[Shot {m.group(1)}] at {s:.3f}s must be after the last cut and inside the {float(duration_s):.2f}s clip")
            last = max(last, s)
    for m in _RANGE.finditer(body):
        if _secs(m, 3, 4) > float(duration_s) + 0.05:
            errs.append(f"the range ending at {_secs(m, 3, 4):.3f}s runs past the {float(duration_s):.2f}s clip")
    outside = _DLG.sub(" ", t)
    neg = sorted({w.lower() for w in _NEG.findall(outside)})
    if neg:
        errs.append("the paste is additive: rewrite every negation as what IS there (" + ", ".join(neg) + ")")
    for d in _DLG.findall(t):
        if re.search(r"[\u2018\u2019\u201c\u201d\u00a0]", d):
            errs.append("straight quotes and plain spaces inside <d> lines")
            break
    return errs


standard = SimpleNamespace(
    T2VA_FIELDS=T2VA_FIELDS,
    REF2VA_FIELDS=REF2VA_FIELDS,
    _field=_field,
    mode_for=mode_for,
    contract_errors=contract_errors,
)


# -- refs subset -------------------------------------------------------------
_RETENTION = {"fully_preserved", "partially_copy", "reference", "prop", "style_only", "motion_only"}


def parse_ref_plan(text):
    t = (text or "").strip()
    if not t:
        return {"refs": [], "subjects": {}}
    try:
        data = json.loads(t)
    except json.JSONDecodeError as exc:
        raise ValueError(f"ref_plan is not valid JSON: {exc}") from exc
    raw_subjects = {}
    if isinstance(data, list):
        raw_refs = data
    elif isinstance(data, dict):
        raw_refs = data.get("refs")
        if raw_refs is None:
            raw_refs = []
        raw_subjects = data.get("subjects") or {}
    else:
        raise ValueError(f"ref_plan must be an object or array, got {type(data).__name__}")
    refs = []
    for i, raw in enumerate(raw_refs or []):
        if not isinstance(raw, dict):
            continue
        tag = str(raw.get("tag") or f"ref_{i + 1}").strip().lstrip("@")
        subj = raw.get("subject")
        if subj is not None:
            try:
                subj = int(subj)
            except (TypeError, ValueError):
                subj = None
        ret = str(raw.get("retention") or "").strip()
        if ret not in _RETENTION:
            ret = "fully_preserved" if subj else "reference"
        refs.append({
            "tag": tag,
            "file": _os.path.basename(str(raw.get("file") or "").strip()),
            "slot": i + 1,
            "subject": subj,
            "retention": ret,
            "desc": str(raw.get("desc") or "").strip(),
            "shots": raw.get("shots"),
            "voice": _os.path.basename(str(raw.get("voice") or "").strip()),
            "voice_start": float(raw.get("voice_start") or 0.0),
            "voice_end": float(raw.get("voice_end") or 0.0),
            "mp": float(raw.get("mp") or 0.0),
            "qwen_mp": float(raw.get("qwen_mp") or 0.0),
            "source": str(raw.get("source") or "image"),
            "strength": float(raw.get("strength") if raw.get("strength") not in (None, "") else 1.0),
        })
    subjects = {}
    if isinstance(raw_subjects, dict):
        for k, v in raw_subjects.items():
            try:
                num = int(k)
            except (TypeError, ValueError):
                continue
            if isinstance(v, dict):
                subjects[num] = {
                    "name": str(v.get("name") or "").strip(),
                    "locked": str(v.get("locked") or "").strip(),
                    "context": str(v.get("context") or "").strip(),
                }
    return {"refs": refs, "subjects": subjects}


def active_refs(refs_list, hop_index, wired_slots):
    shot_no = hop_index + 1
    out = []
    for r in refs_list:
        if r["slot"] not in wired_slots:
            continue
        if r["shots"] is not None and shot_no not in r["shots"]:
            continue
        out.append(r)
    return sorted(out, key=lambda r: r["slot"])


def ordinals(active):
    return {r["tag"]: i + 1 for i, r in enumerate(active)}


refs = SimpleNamespace(parse_ref_plan=parse_ref_plan, active_refs=active_refs, ordinals=ordinals)


# -- standalone HTTP routes (/sandtie_rig/llm, /upload, /vocab) --------------
MAX_UPLOAD_FILES = 32
MAX_UPLOAD_BYTES = 256 * 1024 * 1024
TAG = "SandTiePromptRig"


def register_extra_routes(instance, web) -> None:
    from . import llm as _llm
    from . import media as _media

    @instance.routes.get("/sandtie_rig/vocab")
    async def _st_vocab(_request):
        return web.json_response({"ok": True, "axes": [], "vocab": {}, "max_ref_images": 9, "fps": 24})

    @instance.routes.post("/sandtie_rig/upload")
    async def _st_upload(request):
        if not (request.content_type or "").startswith("multipart/"):
            return web.json_response({"ok": False, "error": "expected multipart/form-data"}, status=400)
        try:
            reader = await request.multipart()
        except Exception as exc:
            return web.json_response({"ok": False, "error": f"bad multipart: {exc}"}, status=400)
        dest = _media.refs_dir(create=True)
        saved, skipped, total = [], [], 0
        try:
            while True:
                part = await reader.next()
                if part is None:
                    break
                if not getattr(part, "filename", None):
                    continue
                if len(saved) >= MAX_UPLOAD_FILES:
                    skipped.append(f"{part.filename}: batch limit reached")
                    break
                name = _os.path.basename(part.filename or "")
                kind = _media.kind_of(name)
                if kind is None:
                    skipped.append(f"{name}: not an image, video or audio file")
                    continue
                size = 0
                digest = _hashlib.sha256()
                temp = _os.path.join(dest, f".upload_{_os.getpid()}_{len(saved)}.part")
                try:
                    with open(temp, "wb") as fh:
                        while True:
                            chunk = await part.read_chunk()
                            if not chunk:
                                break
                            size += len(chunk)
                            total += len(chunk)
                            if total > MAX_UPLOAD_BYTES:
                                raise ValueError("upload too large")
                            digest.update(chunk)
                            fh.write(chunk)
                except Exception:
                    try:
                        _os.remove(temp)
                    except OSError:
                        pass
                    raise
                hexed = digest.hexdigest()
                same = _media.find_by_hash(dest, hexed)
                if same:
                    try:
                        _os.remove(temp)
                    except OSError:
                        pass
                    saved.append({"name": same, "size": size, "kind": kind, "deduped": True})
                    continue
                path = _media.claim_for_hash(dest, name, hexed)
                try:
                    _os.replace(temp, path)
                except Exception:
                    try:
                        _os.remove(temp)
                    except OSError:
                        pass
                    raise
                saved.append({"name": _os.path.basename(path), "size": size, "kind": kind, "deduped": False})
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc), "files": saved, "skipped": skipped}, status=400)
        return web.json_response({"ok": True, "files": saved, "skipped": skipped})

    @instance.routes.get("/sandtie_rig/llm")
    async def _st_llm_get(_request):
        try:
            import asyncio
            conn = _llm.load_conn()
            found, running = await asyncio.gather(
                _llm.models(conn["server_url"]),
                _llm.server_running_async(conn.get("backend")),
            )
            return web.json_response({
                "ok": True,
                "server_url": conn["server_url"],
                "model": conn["model"],
                "temperature": conn["temperature"],
                "keep_warm": conn["keep_warm"],
                "unload_on_run": conn["unload_on_run"],
                "vram_settle_s": conn["vram_settle_s"],
                "backend": conn.get("backend") or "lmstudio",
                "backend_label": _llm.backend_spec(conn.get("backend"))["label"],
                "model_optional": bool(_llm.backend_spec(conn.get("backend"))["model_optional"]),
                "backends": [{"id": k, "label": v["label"], "program": k in dict(_llm.SERVER_EXES)} for k, v in _llm.BACKENDS.items()],
                "server_paths": {
                    name: {
                        "exe": str((conn.get("servers") or {}).get(name, {}).get("exe") or ""),
                        "model_file": str((conn.get("servers") or {}).get(name, {}).get("model_file") or ""),
                        "found_exe": _llm._server_exe(name) or "",
                    }
                    for name in _llm.BACKENDS
                },
                "models": found if isinstance(found, list) else [],
                "running": bool(running),
                "startup_error": "" if running else _llm.startup_error(conn.get("backend")),
            })
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=500)

    @instance.routes.post("/sandtie_rig/llm")
    async def _st_llm_set(request):
        try:
            body = await request.json()
        except Exception:
            return web.json_response({"ok": False, "error": "expected JSON body"}, status=400)
        try:
            if isinstance(body, dict) and body.get("action") == "start":
                _ok, _msg = await _llm.start_process_async(model_file=str(body.get("model_file") or "").strip() or None)
                _conn = _llm.load_conn()
                _run = await _llm.server_running_async(_conn.get("backend"))
                return web.json_response({
                    "ok": _ok,
                    "error": "" if _ok else _msg,
                    "note": _msg,
                    "running": _run,
                    "startup_error": "" if _run else _llm.startup_error(_conn.get("backend")),
                    **_conn,
                })
            if isinstance(body, dict) and body.get("action") == "stop":
                _n = _llm.stop_process()
                _conn = _llm.load_conn()
                _run = await _llm.server_running_async(_conn.get("backend"))
                return web.json_response({
                    "ok": True,
                    "note": f"stopped {_n} process(es)",
                    "running": _run,
                    "startup_error": "",
                    **_conn,
                })
            if isinstance(body, dict) and body.get("action") == "status":
                _conn = _llm.load_conn()
                _run = await _llm.server_running_async(_conn.get("backend"))
                return web.json_response({
                    "ok": True,
                    "running": _run,
                    "startup_error": "" if _run else _llm.startup_error(_conn.get("backend")),
                    **_conn,
                })
            conn = _llm.save_conn(body if isinstance(body, dict) else {})
            return web.json_response({"ok": True, **conn})
        except Exception as exc:
            return web.json_response({"ok": False, "error": str(exc)}, status=500)
