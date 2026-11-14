# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""Dialogue extraction, talk-mode suppression, anti-cliché cues, and TTS sanitation for SandTie."""
from __future__ import annotations

import hashlib
import re

from . import catalogs as _cat
from . import director_cards as _dir

_GLUCK_RX = re.compile(r"\bgluck(?:\s*[,.\-!…]*\s*gluck)*\b", re.I)

_SILENT_RX = re.compile(
    r"\b(?:silent(?:ly)?|in\s+(?:total\s+|complete\s+|utter\s+)?silence|"
    r"(?:no|without|zero)\s+(?:spoken\s+)?(?:dialogue|talking|speech|words|voice(?:\s*lines?)?|vocals?)|"
    r"non[- ]?verbal|mute|speechless|wordless)\b",
    re.I,
)


def sanitize_gluck(q: str) -> str:
    return _GLUCK_RX.sub("Mmmph... hmm!!!", str(q or ""))


def extract_quotes(brief: str) -> list[str]:
    if not brief:
        return []
    out: list[str] = []
    for pat in (r'"([^"\n]{2,220})"', r"“([^”\n]{2,220})”", r"'([^'\n]{3,220})'"):
        for m in re.finditer(pat, brief):
            q = sanitize_gluck(m.group(1).strip())
            if q and q not in out:
                out.append(q)
    return out


def is_silent_request(brief: str, talk_mode: str = "auto", plan: str = "", plan_hint: str = "") -> bool:
    tm = str(talk_mode or "auto").strip().lower()
    if tm == "silent":
        return True
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    if _SILENT_RX.search(combined):
        return True
    return False


def should_suppress_dialogue(
    brief: str,
    flavors: dict | None = None,
    plan: str = "",
    quotes: list[str] | None = None,
) -> bool:
    flavors = flavors or {}
    tm = str(flavors.get("talk_mode") or "auto").strip().lower()
    plan_hint = str(flavors.get("plan_hint") or "")
    if is_silent_request(brief, talk_mode=tm, plan=plan, plan_hint=plan_hint):
        return True
    qs = quotes if quotes is not None else extract_quotes(brief)
    if tm == "quotes_only" and not qs:
        return True
    if tm == "auto" and not qs:
        raw_exp = str(flavors.get("explicit") or "").strip()
        eids = [x.lower() for x in _cat.parse_multi_ids(raw_exp)]
        cid = str(flavors.get("camera") or "").strip().lower()
        combined = f"{brief or ''}\n{plan or ''}\n{plan_hint}"
        has_speech_ask = bool(
            re.search(
                r"\b(?:say\w*|speak\w*|talk\w*|whisper\w*|tell\w*|ask\w*|taunt\w*|mock\w*|count\w*|joi|cei|sph|findom|dialogue|monologue)\b",
                combined,
                re.I,
            )
        )
        if _dir.is_anal(brief, explicit_id=raw_exp, plan=plan, plan_hint=plan_hint) and len(eids) <= 1:
            return True
        if eids and all(eid in _dir.NON_VOCAL_DEFAULT_EXPLICIT_IDS for eid in eids) and not has_speech_ask:
            return True
        if _dir.is_rear_facing(brief, explicit_id=raw_exp, plan=plan, plan_hint=plan_hint, camera_id=cid) and not any(eid in _dir.MIRROR_EXPLICIT_IDS for eid in eids) and not has_speech_ask:
            return True
        if _dir.is_mouth_occupied(brief, explicit_id=raw_exp, plan=plan, plan_hint=plan_hint) and not any(eid in ("rough_deepthroat_mascara", "gloryhole_wall_oral", "bdsm_ballgag_tease") for eid in eids) and not has_speech_ask:
            return True
    return False


_ARC_FALLBACKS = {
    0: [
        "Hold completely still right there—let's see how long that calm look lasts~",
        "Keep your eyes locked straight on mine, don't blink first~",
        "Come closer—we don't have anyone watching for the next two minutes.",
        "Careful, one wrong move and you're letting me take charge tonight~",
    ],
    1: [
        "Right like that—feel your pulse jumping straight under my palms~",
        "Listen to yourself trying to stay composed while your breath shakes...",
        "Look how quickly all that tough talk turned into a whisper~",
        "Wait—hold that exact rhythm, don't speed up until I say so~",
    ],
    2: [
        "There it is—stay right there and let every last wall drop~",
        "Look at you completely undone... I knew you wouldn't last a minute~",
        "Still catching your breath? Good—stay tangled right here with me.",
        "Not a single ounce of calm left, and we only just got started~",
    ],
}


_SFW_ARC_FALLBACKS = {
    0: [
        "Take a breath—everything is lined up cleanly right here.",
        "Look this way for a second before we start moving.",
        "Wait right there—let the light catch the frame first.",
    ],
    1: [
        "Stay right with me on this beat, keep it steady.",
        "Keep moving forward—right through the middle of the room.",
        "Hold that expression right there for one more moment.",
    ],
    2: [
        "That landed right on cue—hold the frame steady.",
        "Good, settle right there and let the scene breathe.",
        "That is exactly what we needed—stay right there.",
    ],
}


def pick_beat_dialogue_cues(
    *,
    brief: str = "",
    talk_opt: dict | None = None,
    acc_opt: dict | None = None,
    playbook_entries: list[dict] | None = None,
    n_beats: int = 3,
    is_sexual_scene: bool = False,
) -> list[str]:
    """Deterministic, varied Beat 1/2/3 dialogue suggestions so no stale template line ever repeats."""
    seed_src = f"{brief}|{(talk_opt or {}).get('id', '')}|{(acc_opt or {}).get('id', '')}|{'/'.join(p.get('title','') for p in (playbook_entries or []))}"
    h_idx = int(hashlib.sha1(seed_src.encode("utf-8", "ignore")).hexdigest()[:8], 16)

    small_words: list[str] = []
    if talk_opt and talk_opt.get("small"):
        small_words = [x.strip() for x in str(talk_opt["small"]).split(",") if x.strip()]
    pb_phrases: list[str] = []
    for pb in playbook_entries or []:
        for p in pb.get("phrases") or []:
            if str(p or "").strip():
                pb_phrases.append(str(p).strip())

    out: list[str] = []
    for b in range(max(1, n_beats)):
        arc_b = 0 if b == 0 else (2 if b == n_beats - 1 else 1)
        if b < len(pb_phrases):
            out.append(pb_phrases[b])
        elif is_sexual_scene:
            pool = _ARC_FALLBACKS[arc_b]
            line = pool[(h_idx + b) % len(pool)]
            if small_words and b == 0:
                tok = small_words[h_idx % len(small_words)]
                if len(tok) <= 32 and tok.lower() not in line.lower():
                    line = f"{tok.rstrip('.!~')} — {line[0].lower() + line[1:]}"
            out.append(line)
        else:
            pool = _SFW_ARC_FALLBACKS[arc_b]
            out.append(pool[(h_idx + b) % len(pool)])
    return out
