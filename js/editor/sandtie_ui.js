/* SANDTIE UI (js/editor/sandtie_ui.js)
 *
 * Unified clean-room R2-styled SandTie Scribe / PromptRig interface powering:
 *   1. HandTieClips' reworked `Standard` tab (`mountSandTieInStandard`)
 *   2. Standalone `SandTiePromptRig` node pop-out (`mountSandTieStandalone`)
 *   3. SWAP's optional Speech/Accent/Style extras (`mountSwapExtras`)
 */
import { el, button, widgetByName } from "./widget_utils.js";

const LLM_URL = "/sandtie_rig/llm";
const SANDTIE_OPTIONS_URL = "/sandtie_rig/sandtie/options";
const SANDTIE_WRITE_URL = "/sandtie_rig/sandtie/write";
const SANDTIE_EXTRACT_URL = "/sandtie_rig/sandtie/extract_video";
const SANDTIE_PRESET_URL = "/sandtie_rig/sandtie/preset";
const SANDTIE_REFBANK_URL = "/sandtie_rig/sandtie/ref_bank";
const SANDTIE_THUMB_URL = "/sandtie_rig/sandtie/thumb";
const UPLOAD_URL = "/sandtie_rig/upload";
const FLAVOR_PROP = "h3_standard_flavors";

const MSEL_STYLE_ID = "stpr-sandtie-msel-style";
const MSEL_CSS = `
/* -- SandTie PromptRig: multi-select popovers & R2 cards ---------------- */
.h3st-shell { display: flex; flex-direction: column; gap: 8px; }
.h3st-head { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; justify-content: space-between; }
.h3st-row { display: flex; align-items: center; gap: 6px; flex-wrap: wrap; }
.h3st-sw-bar {
    display: flex; align-items: center; gap: 8px; flex-wrap: wrap;
    padding: 5px 8px; background: var(--h3-sunken);
    border: 1px solid var(--h3-border-soft); border-radius: var(--h3-radius-sm);
}
.h3st-sw {
    display: inline-flex; align-items: center; gap: 4px; cursor: pointer; user-select: none;
    font-size: var(--h3-fs-sm); color: var(--h3-text); padding: 2px 5px; border-radius: 3px;
}
.h3st-sw:hover { background: rgba(255,255,255,0.04); }
.h3st-sw input { width: auto; margin: 0; accent-color: var(--h3-accent); cursor: pointer; }
.h3st-grid-primary {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(185px, 1fr)); gap: 5px;
}
.h3st-drawer {
    padding: 8px; background: var(--h3-sunken);
    border: 1px solid var(--h3-border-soft); border-radius: var(--h3-radius);
    display: flex; flex-direction: column; gap: 6px;
}
.h3st-drawer[hidden] { display: none !important; }
.h3st-bible {
    padding: 8px; background: var(--h3-sunken);
    border: 1px solid var(--h3-border); border-radius: var(--h3-radius);
    display: flex; flex-direction: column; gap: 6px;
}
.h3st-bible-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(235px, 1fr));
    gap: 6px; max-height: 250px; overflow-y: auto; scrollbar-width: thin;
}
.h3st-bcard {
    background: var(--h3-panel); border: 1px solid var(--h3-border);
    border-radius: var(--h3-radius-sm); padding: 6px; display: flex; flex-direction: column; gap: 4px;
}
.h3st-bcard.h3st-bwired {
    border-color: color-mix(in srgb, var(--h3-accent) 75%, var(--h3-border));
    background: color-mix(in srgb, var(--h3-accent) 6%, var(--h3-panel));
}
.h3st-btop { display: flex; gap: 7px; align-items: center; }
.h3st-bthumb {
    width: 40px; height: 40px; flex: 0 0 40px; border-radius: 3px;
    object-fit: cover; background: #181a20; border: 1px solid var(--h3-border);
    display: flex; align-items: center; justify-content: center;
    font-size: 10px; font-weight: 700; color: var(--h3-accent);
}
.h3st-bdesc {
    font-size: 10.5px; color: var(--h3-muted);
    display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; overflow: hidden;
}
.h3st-pill {
    display: inline-flex; align-items: center; gap: 4px; padding: 2px 6px;
    border-radius: 3px; font-size: 10.5px; font-weight: 600;
    border: 1px solid var(--h3-border); background: var(--h3-sunken); color: var(--h3-muted);
}
.h3st-pill-accent { border-color: rgba(232,255,71,0.55); background: rgba(232,255,71,0.12); color: var(--h3-accent); }
.h3st-pill-ok { border-color: rgba(95,191,122,0.5); background: rgba(95,191,122,0.13); color: #8ee5a8; }
.h3st-pill-warn { border-color: rgba(255,176,32,0.65); background: rgba(255,176,32,0.16); color: #ffd176; cursor: pointer; }
.h3st-chips { display: inline-flex; align-items: center; gap: 3px; background: var(--h3-sunken); border: 1px solid var(--h3-border-soft); border-radius: 3px; padding: 2px 4px; }
.h3st-chips-lbl { font-size: 10px; font-weight: 700; letter-spacing: 0.05em; color: var(--h3-muted); padding: 0 3px; }
.h3st-chip-on { border-color: var(--h3-accent) !important; color: var(--h3-accent) !important; background: rgba(232,255,71,0.12) !important; }

.h3e-msel { position: relative; flex: 1 1 170px; min-width: 140px; display: inline-flex; }
.h3e-root .h3e-msel-btn {
    width: 100%; display: flex; align-items: center; justify-content: space-between;
    gap: 5px; padding: 5px 7px; background: var(--h3-sunken);
    border: 1px solid var(--h3-border); border-radius: var(--h3-radius-sm);
    color: var(--h3-text); font-size: var(--h3-fs-sm); text-align: left; overflow: hidden;
}
.h3e-root .h3e-msel-btn:hover,
.h3e-msel.h3e-msel-open > .h3e-msel-btn { border-color: color-mix(in srgb, var(--h3-accent) 65%, var(--h3-border)); }
.h3e-msel.h3e-msel-active > .h3e-msel-btn {
    border-color: color-mix(in srgb, var(--h3-accent) 85%, var(--h3-border));
    background: color-mix(in srgb, var(--h3-accent) 9%, var(--h3-sunken));
}
.h3e-msel-txt { flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.h3e-msel-badge {
    flex: 0 0 auto; background: var(--h3-accent); color: var(--h3-on-accent);
    font-size: var(--h3-fs-xs); font-weight: 700; padding: 0 5px; border-radius: 2px; line-height: 1.4;
}
.h3e-msel-caret { flex: 0 0 auto; color: var(--h3-faint); font-size: var(--h3-fs-xs); line-height: 1; }
.h3e-msel-pop {
    position: absolute; top: calc(100% + 3px); left: 0; z-index: 60;
    min-width: 310px; max-width: min(460px, 92vw); width: max-content;
    background: var(--h3-panel);
    border: 1px solid color-mix(in srgb, var(--h3-accent) 55%, var(--h3-border));
    border-radius: var(--h3-radius); box-shadow: 0 10px 28px rgba(0,0,0,0.72);
    display: flex; flex-direction: column; overflow: hidden;
}
.h3e-msel [hidden],
.h3e-msel-pop[hidden],
.h3e-msel-item[hidden],
.h3e-msel-grp[hidden] { display: none !important; }
.h3e-msel-pop.h3e-msel-right { left: auto; right: 0; }
.h3e-msel-head {
    display: flex; align-items: center; gap: 4px; padding: 5px 6px;
    background: var(--h3-bg); border-bottom: 1px solid var(--h3-border-soft);
}
.h3e-root .h3e-msel-search { flex: 1 1 auto; min-width: 90px; font-size: var(--h3-fs-sm); padding: 3px 6px; }
.h3e-root .h3e-msel-mode,
.h3e-root .h3e-msel-clear {
    flex: 0 0 auto; display: inline-flex; align-items: center; justify-content: center;
    line-height: 1.1; font-size: var(--h3-fs-xs); padding: 3px 6px;
}
.h3e-root .h3e-msel-mode.h3e-on {
    border-color: var(--h3-accent); color: var(--h3-accent);
    background: color-mix(in srgb, var(--h3-accent) 14%, var(--h3-panel));
}
.h3e-msel-sub {
    padding: 3px 8px; font-size: var(--h3-fs-xs); color: var(--h3-muted);
    background: var(--h3-sunken); border-bottom: 1px solid var(--h3-border-soft);
    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.h3e-msel-list { max-height: 290px; overflow-y: auto; overflow-x: hidden; scrollbar-width: thin; padding: 3px 0; }
.h3e-msel-grp {
    padding: 5px 8px 2px; font-size: var(--h3-fs-xs); font-weight: 700;
    letter-spacing: 0.06em; text-transform: uppercase; color: var(--h3-accent);
    background: color-mix(in srgb, var(--h3-bg) 60%, transparent);
    border-top: 1px solid var(--h3-border-soft);
}
.h3e-msel-grp:first-child { border-top: 0; }
.h3e-msel-item {
    display: flex; align-items: center; gap: 6px; padding: 4px 8px;
    font-size: var(--h3-fs-sm); color: var(--h3-text); cursor: pointer; user-select: none;
    content-visibility: auto; contain-intrinsic-size: auto 26px;
}
.h3e-msel-item:hover { background: color-mix(in srgb, var(--h3-accent) 12%, var(--h3-panel)); }
.h3e-msel-item.h3e-msel-checked { background: color-mix(in srgb, var(--h3-accent) 18%, var(--h3-panel)); }
.h3e-root .h3e-msel-item input[type="checkbox"] { width: auto; margin: 0; flex: 0 0 auto; accent-color: var(--h3-accent); cursor: pointer; }
.h3e-msel-ord {
    flex: 0 0 auto; min-width: 18px; height: 16px; padding: 0 4px; border-radius: 2px;
    background: var(--h3-accent); color: var(--h3-on-accent); font-size: var(--h3-fs-xs); font-weight: 700;
    display: inline-flex; align-items: center; justify-content: center; line-height: 1;
}
.h3e-msel-ord:empty { display: none; }
.h3e-msel-lbl { flex: 1 1 auto; min-width: 0; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
.h3e-msel-tag {
    flex: 0 0 auto; font-size: 9.5px; font-weight: 700; padding: 1px 4px; border-radius: 2px;
    border: 1px solid var(--h3-border); color: var(--h3-muted); background: var(--h3-bg);
}
.h3e-msel-tag.asp-916 { color: #7dd3fc; border-color: rgba(125,211,252,0.45); background: rgba(14,116,144,0.22); }
.h3e-msel-tag.asp-169 { color: #fcd34d; border-color: rgba(252,211,77,0.45); background: rgba(180,83,9,0.22); }
.h3e-msel-tag.dur-tag { color: #a7f3d0; border-color: rgba(95,191,122,0.4); background: rgba(16,85,55,0.22); }
`;

function ensureMselStyle() {
    let st = document.getElementById(MSEL_STYLE_ID);
    if (!st) {
        st = document.createElement("style");
        st.id = MSEL_STYLE_ID;
        document.head.appendChild(st);
    }
    if (st.textContent !== MSEL_CSS) st.textContent = MSEL_CSS;
}

export const BUILTIN_DIAL_COMBOS = [
    { id: "__builtin_916_pov_intimate", label: "9:16 First-Person POV + Warm Intimate", values: { camera: "portrait_vertical_stack", light: "vip_amber_booth", energy: "medium", expression: "large", life: "large", pov: "male", talk_mode: "auto" } },
    { id: "__builtin_anime_to_real", label: "2D Anime -> Photoreal Transition (1->2)", values: { style: "h3_sakuga_2d,h3_astro_cinema", dial_modes: { style: "sequence" }, energy: "large", expression: "large" } },
    { id: "__builtin_neon_cyber_action", label: "Neon Cyberpunk + Action Combo", values: { light: "cyber_dual_gel", colour: "teal_orange", energy: "large", life: "large" } },
    { id: "__builtin_slow_sensual_purr", label: "Slow Sensual Tease (Small Energy + Soft Purr)", values: { energy: "small", expression: "small", life: "medium", talk_mode: "auto" } },
    { id: "__builtin_mirror_vertical_doggy", label: "9:16 Vanity Mirror Doggy + Warm Candlelight", values: { explicit: "standing_mirror_vanity_doggy", camera: "mirror_three_way_reflection", light: "candlelight_flicker_boudoir", ambience: "intimate_skin_foley", energy: "medium", expression: "large" } },
    { id: "__builtin_kpop_dance_3angle", label: "K-Pop Idol 3-Angle Dance Cut + UV Stage Haze", values: { style: "korean_drama_glow", camera: "multi_angle_action_close", pose: "dance_kpop_chest_pop_body_wave,dance_gravure_s_curve_hip_roll", light: "strip_club_uv_blacklight_laser_haze", music: "kpop_girl_crush_bass_drop_124", energy: "large", expression: "large", talk_mode: "silent" } },
    { id: "__builtin_penthouse_rain_silent", label: "Penthouse Midnight Rain + Candlelight Whisper (Silent)", values: { place: "plate_luxury_rooftop_infinity_pool", light: "candlelight_and_moonlight_split", ambience: "tokyo_love_hotel_rain_hum", music: "bedroom_lofi_rain_64", energy: "small", expression: "small", talk_mode: "silent" } },
    { id: "__builtin_editorial_flash_glamour", label: "Editorial 35mm Flash Fashion Slow-Mo Glamour", values: { style: "editorial_vogue_flash_cinema", light: "editorial_softbox_beauty_key", camera: "dolly_push_to_ecu_eyes", music: "city_pop_80s_112", energy: "medium", expression: "medium", talk_mode: "silent" } },
    { id: "__builtin_anime2real_water_dragon", label: "Anime2Real Water Dragon + Neon Rain Street vs Goons", values: { style: "anime2real_live_action_vfx", combat: "combat_anime2real_water_breathing_dragon", fx: "vfx_anime2real_water_dragon_slash", fx_timing: "from_start", place: "plate_shibuya_rain_crosswalk_crater", wardrobe: "anime2real_demon_slayer_haori_corps", energy: "large", life: "large" } },
    { id: "__builtin_anime2real_mixed_2d_ink", label: "Mixed-Reality 2D Cel-Slash + Photoreal Brawler", values: { style: "anime2real_live_action_vfx", combat: "combat_anime2real_2d_ink_manga_mixed_reality", fx: "vfx_anime2real_2d_cel_slash_ribbons", fx_timing: "from_start", energy: "large", life: "large" } },
    { id: "__builtin_one_take_cowgirl_transition", label: "One Continuous Take: Thong Aside -> Cowgirl Sink & Bounce", values: { explicit: "cont_panties_aside_rub_to_cowgirl_sink_to_grind", wardrobe: "partial_panties_pulled_aside", light: "candlelight_flicker_boudoir", energy: "medium", expression: "large", life: "large" } },
    { id: "__builtin_one_take_deepthroat_facial", label: "One Continuous Take: Handjob & Lick -> Deepthroat -> Facial", values: { explicit: "cont_handjob_lick_to_deepthroat_to_swallow", camera: "portrait_vertical_stack", energy: "large", expression: "large" } },
    { id: "__builtin_gravure_idol_s_curve_dance", label: "4K Gravure Idol S-Curve Dance + Body-Contour Pedestal", values: { style: "japanese_4k_gravure_idol_cinema", camera: "body_contour_s_curve_pedestal_glide", pose: "dance_gravure_s_curve_hip_roll,dance_kpop_chest_pop_body_wave", light: "tokyo_love_hotel_magenta_violet_velvet", colour: "peach_milk_gravure", energy: "medium", expression: "large", life: "large" } },
    { id: "__builtin_ensemble_s1_s9_cypher_squad", label: "Multi-Character Ensemble (S1-S9): V-Formation + 360 Cypher Orbit", values: { camera: "ensemble_360_cypher_orbit_s1_s9", pose: "ensemble_v_formation_idol_squad_s1_s9", lens: "comp_ensemble_s1_s9_depth_stagger", energy: "large", life: "large" } },
    { id: "__builtin_anime2real_senbonzakura_storm", label: "Anime2Real Bankai Senbonzakura Blade-Petal Storm", values: { style: "anime2real_live_action_vfx", combat: "combat_anime2real_senbonzakura_cherry_blossom_blade_storm", fx: "vfx_anime2real_senbonzakura_petal_vortex", fx_timing: "from_start", place: "plate_anime2real_soul_society_cherry_blossom_courtyard", wardrobe: "anime2real_bleach_shihakusho_open_chest_zanpakuto", colour: "ufotable_neon_hdr_contrast", energy: "large" } },
    { id: "__builtin_anime2real_sandevistan_blitz", label: "Anime2Real Cyberpunk Sandevistan Afterimage Blitz", values: { style: "anime2real_live_action_vfx", combat: "combat_anime2real_sandevistan_afterimage_time_freeze_blitz", fx: "vfx_anime2real_sandevistan_afterimage_ribbon", fx_timing: "from_start", camera: "sandevistan_freeze_orbit_180", colour: "emerald_matrix_gunmetal", energy: "large" } },
    { id: "__builtin_fetish_femdom_leash_worship", label: "Playbook: Collar & Leash Petplay -> Boot Worship -> Facesit", values: { explicit: "cont_femdom_leash_crawl_to_boot_lick_to_facesit_smother", fetish: "collar_leash_petplay_walk,foot_domination", wardrobe: "fetish_latex_catsuit_unzipped", talkstyle: "velvet_hypnotic_domme_count", energy: "large", expression: "large" } },
    { id: "__builtin_under_desk_secret_to_cowgirl", label: "Secret Under-Desk Stroke & Deepthroat -> Executive Lap Cowgirl", values: { explicit: "cont_under_desk_two_hand_stroke_to_deepthroat_to_lap_cowgirl", fetish: "office_under_desk_secret", place: "plate_executive_boardroom_under_mahogany_table", wardrobe: "fetish_office_siren_skirt", talkstyle: "secretive_office_whisper", energy: "medium", expression: "large" } },
    { id: "__builtin_s1_vs_s2_katana_rain_duel", label: "S1 vs S2: Rainy Lantern Alley Katana Sparks Duel", values: { style: "john_wick_neon_gunfu", combat: "combat_s1_s2_mirror_blade_duel", fx: "vfx_sword_spark_shower", fx_timing: "from_start", place: "plate_rainy_chinatown_lantern_alley", light: "rain_neon_puddle_bounce", colour: "crimson_john_wick_gold", ambience: "neon_alley_puddle_footsteps", music: "taiko_war_drums_138", energy: "large", life: "large" } },
    { id: "__builtin_s1_s2_tag_team_corridor_clear", label: "S1 + S2 Tag-Team: Corridor Sweep -> Vault Flying Knee Brawl", values: { style: "john_wick_neon_gunfu", combat: "combat_s1_s2_tag_team_combo_finisher", camera: "track_side", light: "cyber_dual_gel", fx: "vfx_kinetic_shockwave_dust_ring", fx_timing: "from_start", music: "john_wick_club_techno_132", energy: "large" } },
    { id: "__builtin_parkour_table_slide_gunfu", label: "Parkour Gun-Fu: Boardroom Table Slide & Brass Rain", values: { style: "john_wick_neon_gunfu", combat: "combat_env_table_slide_gun_sweep", fx: "vfx_muzzle_brass_storm", fx_timing: "from_start", place: "plate_executive_boardroom_glass_table", camera: "whip_pan_reaction_match", music: "john_wick_club_techno_132", energy: "large" } },
    { id: "__builtin_anime2real_domain_void_shrine", label: "Anime2Real: Domain Shrine Fracture & Crimson Slashes", values: { style: "anime2real_live_action_vfx", combat: "combat_anime2real_domain_void_shrine_cut", fx: "vfx_crimson_lightning_black_sparks", fx_timing: "from_start", place: "plate_shibuya_rain_crosswalk_crater", colour: "emerald_anime_midnight", music: "anime_orchestral_choir_148", energy: "large" } },
    { id: "__builtin_wuxia_moonlit_bamboo_swordplay", label: "90s Wuxia Cinema: Moonlit Snowy Bamboo Jian Duel", values: { style: "wuxia_wirefu_cinema", combat: "combat_s1_s2_sword_vs_barehand_catch", place: "plate_snowy_bamboo_forest_moonlight", wardrobe: "action_traditional_samurai_kimono_slit", colour: "emerald_anime_midnight", ambience: "dojo_wood_creak_wind", music: "taiko_war_drums_138", energy: "large" } },
    { id: "__builtin_bdsm_shibari_candlelit_wall", label: "BDSM Shibari: Crimson Rope Chest Harness + Fireplace Chalet", values: { explicit: "bdsm_shibari_chest_harness_wall_tie", fetish: "shibari_rope_chest_diamonds", wardrobe: "fetish_shibari_crimson_rope_harness", place: "plate_satin_four_poster_fireplace_cabin", light: "fireplace_ember_warm_low", ambience: "fireplace_ember_pop_silk", energy: "medium", expression: "large" } },
    { id: "__builtin_lesbian_steamy_shower_duo", label: "Steamy Shower: Wet Glass Press & Two-Subject Embrace", values: { explicit: "lesbian_standing_shower_breast_press_thigh_ride", wardrobe: "nude_both_partners", place: "plate_glass_walled_rain_shower_penthouse", fx: "fx_steam_mirror_condensation_clear", fx_timing: "from_start", ambience: "bathhouse_steam_water_drip", energy: "medium", expression: "large" } },
    { id: "__builtin_pegging_dominant_harness_bed", label: "Domme Pegging: Leather Harness Strap-On Doggy", values: { explicit: "cont_strapon_harness_buckle_to_pegging_doggy", fetish: "pegging,strap_on", wardrobe: "fetish_strapon_harness_nude", light: "red_velvet_boudoir", ambience: "intimate_skin_foley", energy: "medium", expression: "large" } },
    { id: "__builtin_90s_erotic_thriller_noir", label: "90s Erotic Thriller: Venetian Blinds Noir Office Dialogue", values: { style: "erotic_thriller_90s_35mm", place: "executive_corner_office_midnight", light: "sunset_blinds_gold", wardrobe: "fetish_office_siren_skirt", talkstyle: "husky_velvet", music: "sultry_jazz_noir_sax_72", colour: "champagne_honey_glow", energy: "small", expression: "medium" } },
    { id: "__builtin_yacht_sunset_continuous_take", label: "Luxury Superyacht Sunset: Swimsuit Climb-Out -> Wet Missionary", values: { explicit: "cont_pool_edge_climb_out_to_wet_missionary", fetish: "yacht_sunpad_ocean_wind", place: "plate_superyacht_aft_sunpad_mediterranean", wardrobe: "partial_bikini_strings_untied_hanging", light: "sunset_silhouette_halo_rim", colour: "champagne_honey_glow", energy: "medium", expression: "large" } },
    { id: "__builtin_candlelit_aftercare_whisper", label: "Post-Climax Aftercare: Alpine Fireplace Cuddle & Husky Murmur", values: { fetish: "aftercare_cuddle_pillow_talk", place: "plate_satin_four_poster_fireplace_cabin", wardrobe: "partial_silk_robe_open_front", light: "fireplace_ember_warm_low", talkstyle: "husky_aftercare_murmur", ambience: "fireplace_ember_pop_silk", music: "ethereal_shoegaze_dream_95", energy: "small", expression: "medium" } },
    { id: "__builtin_switch_banter_displaced_lace", label: "Switch Banter & Displaced Lace (9:16 Continuous)", values: { explicit: "cont_panties_aside_rub_to_cowgirl_sink_to_grind", wardrobe: "partial_panties_pulled_aside", place: "plate_penthouse_master_bed_mirror", light: "candlelight_flicker_boudoir", talkstyle: "switch_power_reversal_tease", ambience: "intimate_skin_foley", energy: "medium", expression: "large" } },
    { id: "__builtin_shower_glass_press_lift_916", label: "Steamy Shower Glass Press -> Standing Lift (9:16 One Take)", values: { explicit: "cont_shower_glass_press_to_standing_carry", fetish: "glass_press_shower_window", wardrobe: "nude_wet_shower", place: "plate_glass_walled_rain_shower_penthouse", fx: "fx_steam_mirror_condensation_clear", fx_timing: "from_start", talkstyle: "pillow_giggle_banter", ambience: "bathhouse_steam_water_drip", energy: "medium", expression: "large" } },
    { id: "__builtin_car_backseat_fogged_916", label: "Rainy Car Backseat Fogged Window Straddle (9:16 Hushed)", values: { explicit: "cont_car_backseat_fogged_glass_straddle_to_climax", place: "plate_rain_car_backseat_city_lights", wardrobe: "partial_dress_hiked_waist", light: "rain_neon_puddle_bounce", talkstyle: "risk_adrenaline_hush", ambience: "rain_thunder_window_glass", energy: "medium", expression: "large" } },
    { id: "__builtin_desk_spin_ledger_169", label: "Executive Desk Chair Spin -> Bent-Over Ledger (16:9)", values: { explicit: "cont_desk_chair_spin_to_bent_over_ledger", fetish: "office_under_desk_secret", place: "executive_corner_office_midnight", wardrobe: "fetish_office_siren_skirt", light: "sunset_blinds_gold", talkstyle: "cocky_dominant_commentary", ambience: "penthouse_night_hum", energy: "medium", expression: "large" } },
];

const ALL_DIAL_KEYS = [
    "camera", "light", "style", "place", "wardrobe", "combat", "explicit", "talkstyle",
    "lens", "colour", "fx", "pose", "fetish", "character", "tv_show", "era", "accent", "ambience", "music",
];

const PRIMARY_DIALS = [
    ["camera", "Cam · Auto"],
    ["light", "Light · Auto"],
    ["style", "Style · Auto"],
    ["place", "Place · Auto"],
    ["wardrobe", "Wear · Auto"],
    ["combat", "Action · Off"],
    ["explicit", "Stage · Off"],
    ["talkstyle", "Speech · Auto"],
];

const SECONDARY_DIALS = [
    ["lens", "Optics · Auto"],
    ["colour", "Grade · Auto"],
    ["fx", "FX · None"],
    ["pose", "Pose · Auto"],
    ["fetish", "Playbook · Off"],
    ["character", "Cast Type · Rail"],
    ["tv_show", "Genre · Auto"],
    ["era", "Era · Present"],
    ["accent", "Accent · Default"],
    ["ambience", "Ambience · Auto"],
    ["music", "Music · Auto"],
];

export function readRigState(node) {
    let st = {};
    try {
        const rw = widgetByName(node, "rig_state");
        if (rw?.value) st = JSON.parse(String(rw.value) || "{}") || {};
    } catch {}
    if (!st || typeof st !== "object") st = {};
    let fl = (st.flavors && typeof st.flavors === "object") ? st.flavors : null;
    if (!fl) {
        try {
            fl = JSON.parse(String(widgetByName(node, "flavors_json")?.value || "{}") || "{}");
        } catch {
            fl = {};
        }
    }
    return {
        prompt_out: String(st.prompt_out ?? widgetByName(node, "prompt_out")?.value ?? ""),
        storyboard_out: String(st.storyboard_out ?? widgetByName(node, "storyboard_out")?.value ?? ""),
        ref_plan_json: String(st.ref_plan_json ?? widgetByName(node, "ref_plan_json")?.value ?? ""),
        flavors: (fl && typeof fl === "object") ? fl : {},
    };
}

export function patchRigState(node, patch) {
    const cur = readRigState(node);
    const next = Object.assign({}, cur, patch || {});
    const rw = widgetByName(node, "rig_state");
    if (rw) {
        rw.value = JSON.stringify(next);
        try { rw.callback?.(rw.value, node.graph?.canvas, node); } catch (_) {}
    }
    const legacy = [
        ["prompt_out", next.prompt_out],
        ["storyboard_out", next.storyboard_out],
        ["ref_plan_json", next.ref_plan_json],
        ["flavors_json", JSON.stringify(next.flavors || {})],
    ];
    for (const [wn, val] of legacy) {
        const w = widgetByName(node, wn);
        if (w) {
            w.value = val;
            try { w.callback?.(val, node.graph?.canvas, node); } catch (_) {}
        }
    }
    return next;
}

export function h3FormatCodeFromLabel(fmtVal) {
    const s = String(fmtVal || "");
    if (s.includes("I2VA")) return "h3_i2va";
    if (s.includes("FL2VA")) return "h3_fl2va";
    if (s.includes("L2VA")) return "h3_l2va";
    if (s.includes("Start Frame")) return "h3_keyframe";
    if (s.includes("Beats")) return "h3_beats";
    return "h3_auto";
}

let _sharedCatalog = null;
let _sharedStatus = { running: false, backend: "ninfer", backend_label: "nInfer", model: "" };

function parseMultiValue(raw) {
    if (!raw) return [];
    const arr = Array.isArray(raw) ? raw : String(raw).split(",");
    const out = [];
    const seen = new Set();
    for (const part of arr) {
        const s = String(part || "").trim();
        if (!s || s === "none" || seen.has(s)) continue;
        seen.add(s);
        out.push(s);
    }
    return out;
}

function serializeMultiValue(arr) {
    return (arr || []).filter(Boolean).join(",");
}

function parseAspectSpec(raw) {
    const s = String(raw || "").trim();
    const m = s.match(/(\d+)\s*:\s*(\d+)/);
    if (m) {
        const w = Number(m[1]);
        const h = Number(m[2]);
        const label = `${w}:${h}`;
        if (w > 0 && h > 0) {
            if (h > w) return { label, bucket: "9:16" };
            if (w > h) return { label, bucket: "16:9" };
            return { label, bucket: "either" };
        }
    }
    if (/portrait|vertical/i.test(s)) return { label: "9:16", bucket: "9:16" };
    return { label: "16:9", bucket: "16:9" };
}

function createSandTieCore(node, {
    mountBody,
    briefEl,
    planBox,
    blockBox,
    say,
    saveDraft,
    getDurationLabel,
    getAspect,
    getRefPlan,
    setRefPlan,
    getStartImage,
    getVoiceFiles,
    previousHopContext,
    setBusyState,
    isBusy,
    standalone = false,
    onApplyStandalone = null,
    legacyButtons = null,
}) {
    ensureMselStyle();

    const defaultFlavors = {
        time_tied: true, kinetic_grip: true, eye_scan: true, double_knot: true, wake_writer: true,
        fx_timing: "delayed_mid", talk_mode: "auto", life: "medium", energy: "medium", expression: "medium", pov: "off",
        camera: "", light: "", lens: "", fx: "", style: "", colour: "", place: "", wardrobe: "",
        combat: "", explicit: "", fetish: "", pose: "", character: "", tv_show: "", era: "",
        talkstyle: "", accent: "", ambience: "", music: "", dial_modes: {},
    };

    function loadFlavors() {
        try {
            const raw = standalone
                ? (readRigState(node).flavors || {})
                : (node.properties?.[FLAVOR_PROP] || {});
            const merged = Object.assign({}, defaultFlavors, raw && typeof raw === "object" ? raw : {});
            // Map legacy switch names if present
            if ("fast_engine" in raw && !("time_tied" in raw)) merged.time_tied = Boolean(raw.fast_engine);
            if ("vision_scan" in raw && !("eye_scan" in raw)) merged.eye_scan = Boolean(raw.vision_scan);
            if ("pass2_refine" in raw && !("double_knot" in raw)) merged.double_knot = Boolean(raw.pass2_refine);
            if ("auto_wake" in raw && !("wake_writer" in raw)) merged.wake_writer = Boolean(raw.auto_wake);
            merged.dial_modes = Object.assign({}, raw?.dial_modes || {});
            return merged;
        } catch {
            return Object.assign({}, defaultFlavors, { dial_modes: {} });
        }
    }

    const flavors = loadFlavors();

    function persistFlavors() {
        if (standalone) {
            patchRigState(node, { flavors: Object.assign({}, flavors, { dial_modes: Object.assign({}, flavors.dial_modes || {}) }) });
        } else {
            node.properties ??= {};
            node.properties[FLAVOR_PROP] = Object.assign({}, flavors, { dial_modes: Object.assign({}, flavors.dial_modes || {}) });
        }
    }

    const undoStack = [];
    function pushUndoSnapshot() {
        const snap = { brief: briefEl.value, plan: planBox.value, block: blockBox.value, flavors: JSON.stringify(flavors) };
        const top = undoStack[undoStack.length - 1];
        if (top && top.brief === snap.brief && top.plan === snap.plan && top.block === snap.block && top.flavors === snap.flavors) return;
        undoStack.push(snap);
        if (undoStack.length > 15) undoStack.shift();
        syncUndoBtn();
    }

    const shell = el("div", "h3st-shell");

    // 1. Header bar (Brand + Combos + Smart Actions)
    const headRow = el("div", "h3st-head");
    const brandLeft = el("div", "h3st-row");
    const brandTitle = el("strong", null, "⌖ SandTie Scribe");
    brandTitle.style.color = "var(--h3-text)";
    const activeCountPill = el("span", "h3st-pill", "0 active");
    brandLeft.append(brandTitle, activeCountPill);

    const comboSel = el("select", "h3e-select");
    comboSel.style.maxWidth = "190px";
    comboSel.title = "Load a built-in or saved SandTie preset combo";
    const saveComboBtn = button("+ Save", "Save active dials as a custom combo", saveUserCombo);
    const delComboBtn = button("×", "Delete selected saved combo", deleteUserCombo);
    const surpriseBtn = button("Surprise Roll", "Domain-locked & aspect-safe creative roll (excludes multi-hop-only join rigs)", runSurpriseRoll);
    const matchBtn = button("Match Dials", "Analyze brief text & wired refs to pick fitting dials automatically", runMatchDials);
    const briefBtn = button("Compose Brief", "Draft a clean descriptive brief from wired Reference Bible & active dials", runComposeBrief);
    const resetBtn = button("Reset", "Reset all 19 dials (keeps switches & brief)", resetAllDials);

    const headRight = el("div", "h3st-row");
    headRight.append(comboSel, saveComboBtn, delComboBtn, surpriseBtn, matchBtn, briefBtn, resetBtn);
    headRow.append(brandLeft, headRight);

    // 2. Switches + Writer Status bar
    const swRow = el("div", "h3st-sw-bar");
    function makeSw(key, icon, text, tip) {
        const lbl = el("label", "h3st-sw");
        lbl.title = tip;
        const chk = document.createElement("input");
        chk.type = "checkbox";
        chk.checked = Boolean(flavors[key]);
        chk.addEventListener("change", () => {
            flavors[key] = chk.checked;
            persistFlavors();
        });
        lbl.append(chk, el("span", null, `${icon} ${text}`));
        return { lbl, chk };
    }
    const swTime = makeSw("time_tied", "⏱", "Time-Tied", "Lock exact [Shot N] cuts and MM:SS.mmm beat windows");
    const swKinetic = makeSw("kinetic_grip", "⚡", "Kinetic Grip", "Chained physical verbs, hand roles & clear facial shifts");
    const swEye = makeSw("eye_scan", "👁", "Eye Scan", "2.5 MP cached reference scan for ethnicity, features & attire");
    const swDouble = makeSw("double_knot", "✧", "Double-Knot", "Pass-2 continuity audit locking tags, domains & zero negations");
    const swWake = makeSw("wake_writer", "☕", "Wake Writer", "Auto-start nInfer if VRAM was evicted by a render");

    const writerModeSel = el("select", "h3e-select");
    writerModeSel.style.marginLeft = "auto";
    writerModeSel.style.maxWidth = "116px";
    writerModeSel.title = "Writer Connection Mode (LM Studio / nInfer)";
    for (const [bid, blbl] of [["lmstudio", "LM Studio"], ["ninfer", "nInfer"]]) {
        const o = el("option", null, blbl);
        o.value = bid;
        writerModeSel.appendChild(o);
    }
    writerModeSel.addEventListener("change", async () => {
        const nextBack = writerModeSel.value;
        const lbl = nextBack === "ninfer" ? "nInfer" : "LM Studio";
        cfgBackSel.value = nextBack;
        cfgPathRow.hidden = nextBack !== "ninfer";
        statusPill.textContent = `Checking ${lbl}…`;
        statusPill.className = "h3st-pill";
        try {
            await fetch(LLM_URL, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ backend: nextBack }),
            });
            await Promise.all([
                refreshStatus(false),
                writerCfgDrawer.hidden ? Promise.resolve() : loadWriterSettings(),
            ]);
        } catch (_) {}
    });

    const statusPill = el("span", "h3st-pill", "Checking writer…");
    const startBtn = button("Start", "Launch local nInfer writer server", () => toggleServer("start"));
    const stopBtn = button("Stop", "Stop local writer to free VRAM", () => toggleServer("stop"));
    const cfgBtn = button("⚙", "Configure Writer URL, Model & Server Exe", () => {
        const open = writerCfgDrawer.hidden;
        writerCfgDrawer.hidden = !open;
        cfgBtn.classList.toggle("h3st-chip-on", open);
        if (open) loadWriterSettings();
    });
    swRow.append(swTime.lbl, swKinetic.lbl, swEye.lbl, swDouble.lbl, swWake.lbl, writerModeSel, statusPill, startBtn, stopBtn, cfgBtn);

    const writerCfgDrawer = el("div", "h3st-drawer");
    writerCfgDrawer.hidden = true;
    const cfgBackSel = el("select", "h3e-select");
    cfgBackSel.style.maxWidth = "125px";
    cfgBackSel.addEventListener("change", async () => {
        const nextBack = cfgBackSel.value;
        const lbl = nextBack === "ninfer" ? "nInfer" : "LM Studio";
        writerModeSel.value = nextBack;
        cfgPathRow.hidden = nextBack !== "ninfer";
        statusPill.textContent = `Checking ${lbl}…`;
        statusPill.className = "h3st-pill";
        try {
            await fetch(LLM_URL, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ backend: nextBack }),
            });
            await Promise.all([loadWriterSettings(), refreshStatus(false)]);
        } catch (_) {}
    });
    const cfgUrlInp = el("input", "h3e-writer-brief");
    cfgUrlInp.type = "text";
    cfgUrlInp.placeholder = "http://127.0.0.1:1234";
    cfgUrlInp.style.flex = "1 1 170px";
    const cfgModelInp = el("input", "h3e-writer-brief");
    cfgModelInp.type = "text";
    cfgModelInp.placeholder = "model id (optional / auto after Start)";
    cfgModelInp.title = "API model ID reported over /v1/models (not a file path; leave blank to auto-pick once running).";
    cfgModelInp.style.flex = "1 1 170px";
    const cfgModelPick = el("select", "h3e-select");
    cfgModelPick.style.maxWidth = "175px";
    cfgModelPick.addEventListener("change", () => {
        if (cfgModelPick.value) cfgModelInp.value = cfgModelPick.value;
    });
    const cfgUnloadLbl = el("label", "h3st-sw");
    const cfgUnloadChk = document.createElement("input");
    cfgUnloadChk.type = "checkbox";
    cfgUnloadChk.checked = true;
    cfgUnloadLbl.append(cfgUnloadChk, el("span", null, "Unload on Run"));
    const cfgSaveBtn = button("Save & Test", "Save writer connection and refresh model list", () => saveWriterSettings(), "h3e-btn h3e-btn-accent");
    const cfgRow = el("div", "h3st-row");
    cfgRow.append(el("strong", null, "Writer:"), cfgBackSel, cfgUrlInp, cfgModelInp, cfgModelPick, cfgUnloadLbl, cfgSaveBtn);

    const cfgPathRow = el("div", "h3st-row");
    const cfgExeInp = el("input", "h3e-writer-brief");
    cfgExeInp.type = "text";
    cfgExeInp.placeholder = "nInfer exe path (e.g. C:\\ninfer\\ninfer-serve.exe)";
    cfgExeInp.title = "Full path to ninfer-serve.exe (or its folder). Leave blank to auto-detect in C:\\ninfer, D:\\ninfer, or C:\\AI\\NInfer.";
    cfgExeInp.style.flex = "1 1 220px";
    const cfgModelFileInp = el("input", "h3e-writer-brief");
    cfgModelFileInp.type = "text";
    cfgModelFileInp.placeholder = "nInfer .ninfer file (or models folder / blank = auto)";
    cfgModelFileInp.title = "Full path to your .ninfer model file (e.g. Ternary-Bonsai-2-27B-ninfer-v3.ninfer), a models folder containing one, or blank to auto-pick from models\\.";
    cfgModelFileInp.style.flex = "1 1 240px";
    cfgPathRow.append(el("span", "h3st-chips-lbl", "PATHS"), cfgExeInp, cfgModelFileInp);
    cfgPathRow.hidden = true;

    writerCfgDrawer.append(cfgRow, cfgPathRow);

    // 3. Active Summary & Advisory Strip (Aspect Mix, Domain Clash, Best Length, × chips)
    const activeStrip = el("div", "h3st-row");

    // 4. Multi-Select Dials (Primary 8 + Toggleable Secondary 11 Tray)
    const dialControllers = {};
    const allMsels = [];
    const primaryGrid = el("div", "h3st-grid-primary");
    const secondaryGrid = el("div", "h3st-grid-primary");
    const secondaryDrawer = el("div", "h3st-drawer");
    secondaryDrawer.hidden = true;
    secondaryDrawer.appendChild(secondaryGrid);

    const fxTimingSel = el("select", "h3e-select");
    fxTimingSel.style.maxWidth = "145px";
    for (const [val, txt] of [["delayed_mid", "FX: Delayed Mid"], ["from_start", "FX: From Start"]]) {
        const o = el("option", null, txt);
        o.value = val;
        fxTimingSel.appendChild(o);
    }
    fxTimingSel.value = flavors.fx_timing || "delayed_mid";
    fxTimingSel.addEventListener("change", () => { flavors.fx_timing = fxTimingSel.value; persistFlavors(); });

    function closeAllPopovers(except = null) {
        for (const ms of allMsels) {
            if (ms !== except) ms.closePopover();
        }
    }

    function createMultiSelect(key, placeholder, defaultMode = "sequence", opts = {}) {
        const wrap = el("div", "h3e-msel");
        const btn = el("button", "h3e-msel-btn");
        btn.type = "button";
        const btnTxt = el("span", "h3e-msel-txt", placeholder);
        const btnBadge = el("span", "h3e-msel-badge");
        btnBadge.hidden = true;
        const btnCaret = el("span", "h3e-msel-caret", "▾");
        btn.append(btnTxt, btnBadge, btnCaret);

        const pop = el("div", "h3e-msel-pop");
        pop.hidden = true;

        const head = el("div", "h3e-msel-head");
        const search = el("input", "h3e-writer-brief h3e-msel-search");
        search.type = "text";
        search.placeholder = "Filter…";
        const randBtn = button("🎲", `Randomize ${key} cleanly`, () => {
            const cands = itemsData.filter((it) => !it.multi_hop_only && (aspectFilter === "all" || it.aspect_best === "either" || it.aspect_best === aspectFilter));
            if (!cands.length) return;
            const pick = cands[Math.floor(Math.random() * cands.length)];
            setValue(pick.id);
            renderActiveStrip();
        }, "h3e-btn h3e-msel-clear");

        let aspectFilter = "all";
        const aspBtn = button("All", "Filter options by aspect (All / 9:16 / 16:9)", () => {
            aspectFilter = aspectFilter === "all" ? "9:16" : (aspectFilter === "9:16" ? "16:9" : "all");
            aspBtn.textContent = aspectFilter === "all" ? "All" : aspectFilter;
            aspBtn.classList.toggle("h3e-on", aspectFilter !== "all");
            filterRows(search.value);
        }, "h3e-btn h3e-msel-mode");

        let mode = flavors.dial_modes?.[key] || defaultMode;
        const modeLabels = opts.allowSplit
            ? { sequence: "1→2", blend: "Blend", split: "S1/S2" }
            : { sequence: "1→2", blend: "Blend" };
        const modeCycle = opts.allowSplit ? ["sequence", "blend", "split"] : ["sequence", "blend"];
        const modeBtn = button(modeLabels[mode] || "1→2", "Cycle how multiple picks combine", () => {
            mode = modeCycle[(modeCycle.indexOf(mode) + 1) % modeCycle.length];
            flavors.dial_modes ??= {};
            flavors.dial_modes[key] = mode;
            modeBtn.textContent = modeLabels[mode] || mode;
            modeBtn.classList.toggle("h3e-on", mode !== "sequence");
            persistFlavors();
        }, "h3e-btn h3e-msel-mode");

        const clearBtn = button("Clear", "Clear selections on this dial", () => {
            setValue("");
            renderActiveStrip();
        }, "h3e-btn h3e-msel-clear");

        head.append(search, randBtn, aspBtn, modeBtn, clearBtn);
        const sub = el("div", "h3e-msel-sub", placeholder);
        const list = el("div", "h3e-msel-list");
        pop.append(head, sub, list);
        wrap.append(btn, pop);

        let itemsData = [];
        let itemMap = new Map();
        let rowEntries = [];
        let selectedIds = parseMultiValue(flavors[key]);

        function syncRows() {
            const selSet = new Set(selectedIds);
            for (const r of rowEntries) {
                const idx = selectedIds.indexOf(r.id);
                const checked = selSet.has(r.id);
                r.chk.checked = checked;
                r.row.classList.toggle("h3e-msel-checked", checked);
                r.ord.textContent = checked && selectedIds.length > 1 ? String(idx + 1) : "";
            }
            const first = selectedIds.length ? itemMap.get(selectedIds[0]) : null;
            if (!selectedIds.length) {
                btnTxt.textContent = placeholder;
                btnBadge.hidden = true;
                wrap.classList.remove("h3e-msel-active");
                sub.textContent = placeholder;
            } else {
                btnTxt.textContent = selectedIds.length === 1 ? (first?.label || selectedIds[0]) : `${selectedIds.length} selected (${first?.label || selectedIds[0]})`;
                btnBadge.textContent = String(selectedIds.length);
                btnBadge.hidden = selectedIds.length <= 1;
                wrap.classList.add("h3e-msel-active");
                sub.textContent = selectedIds.map((id) => itemMap.get(id)?.label || id).join(" · ");
            }
        }

        function filterRows(q) {
            const tok = String(q || "").trim().toLowerCase();
            for (const r of rowEntries) {
                const textOk = !tok || r.searchBlob.includes(tok);
                const aspOk = aspectFilter === "all" || r.item.aspect_best === "either" || r.item.aspect_best === aspectFilter;
                r.row.hidden = !(textOk && aspOk);
            }
            for (const g of list.querySelectorAll(".h3e-msel-grp")) {
                const grpName = g.dataset.grp || "";
                const anyVis = rowEntries.some((r) => r.group === grpName && !r.row.hidden);
                g.hidden = !anyVis;
            }
        }

        function setValue(val) {
            selectedIds = parseMultiValue(val);
            flavors[key] = serializeMultiValue(selectedIds);
            persistFlavors();
            syncRows();
        }

        function populate(items) {
            itemsData = Array.isArray(items) ? items : [];
            itemMap = new Map(itemsData.map((it) => [it.id, it]));
            rowEntries = [];
            list.textContent = "";

            const grouped = new Map();
            for (const it of itemsData) {
                const g = it.group || "General";
                if (!grouped.has(g)) grouped.set(g, []);
                grouped.get(g).push(it);
            }
            const frag = document.createDocumentFragment();
            for (const [grp, gItems] of grouped.entries()) {
                const gEl = el("div", "h3e-msel-grp", grp);
                gEl.dataset.grp = grp;
                frag.appendChild(gEl);
                for (const it of gItems) {
                    const row = el("label", "h3e-msel-item");
                    const chk = document.createElement("input");
                    chk.type = "checkbox";
                    const ord = el("span", "h3e-msel-ord");
                    const lbl = el("span", "h3e-msel-lbl", it.label || it.id);
                    row.title = [it.label, it.aspect_tip, it.duration_tip, it.multi_hop_only ? "Multi-hop Co-Pilot join camera" : ""].filter(Boolean).join("\n");
                    row.append(chk, ord, lbl);
                    if (it.aspect_best === "9:16" || it.aspect_best === "16:9") {
                        row.appendChild(el("span", `h3e-msel-tag asp-${it.aspect_best === "9:16" ? "916" : "169"}`, it.aspect_best));
                    }
                    if (it.duration_best && (key === "explicit" || key === "combat" || key === "camera")) {
                        row.appendChild(el("span", "h3e-msel-tag dur-tag", it.duration_best));
                    }
                    chk.addEventListener("change", () => {
                        pushUndoSnapshot();
                        if (chk.checked) {
                            if (!selectedIds.includes(it.id)) selectedIds = [...selectedIds, it.id];
                        } else {
                            selectedIds = selectedIds.filter((x) => x !== it.id);
                        }
                        flavors[key] = serializeMultiValue(selectedIds);
                        persistFlavors();
                        syncRows();
                        renderActiveStrip();
                    });
                    rowEntries.push({
                        id: it.id,
                        item: it,
                        group: grp,
                        row,
                        chk,
                        ord,
                        searchBlob: `${it.label || ""} ${it.id} ${grp} ${it.domain || ""}`.toLowerCase(),
                    });
                    frag.appendChild(row);
                }
            }
            list.appendChild(frag);
            selectedIds = selectedIds.filter((id) => itemMap.has(id));
            syncRows();
        }

        function closePopover() {
            pop.hidden = true;
            wrap.classList.remove("h3e-msel-open");
        }

        btn.addEventListener("click", (e) => {
            e.stopPropagation();
            const willOpen = pop.hidden;
            closeAllPopovers(willOpen ? api : null);
            pop.hidden = !willOpen;
            wrap.classList.toggle("h3e-msel-open", willOpen);
            if (willOpen) {
                const rect = wrap.getBoundingClientRect();
                pop.classList.toggle("h3e-msel-right", rect.left > window.innerWidth * 0.52);
                search.focus();
            }
        });
        pop.addEventListener("click", (e) => e.stopPropagation());
        search.addEventListener("input", () => filterRows(search.value));

        const api = {
            wrap,
            populate,
            setValue,
            getSelected: () => selectedIds.slice(),
            getItem: (id) => itemMap.get(id),
            getItems: () => itemsData,
            closePopover,
        };
        allMsels.push(api);
        dialControllers[key] = api;
        return api;
    }

    for (const [k, ph] of PRIMARY_DIALS) {
        const ms = createMultiSelect(k, ph, "sequence", { allowSplit: k === "wardrobe" });
        primaryGrid.appendChild(ms.wrap);
    }
    for (const [k, ph] of SECONDARY_DIALS) {
        const ms = createMultiSelect(k, ph, k === "character" ? "split" : "sequence", { allowSplit: k === "character" });
        secondaryGrid.appendChild(ms.wrap);
    }
    secondaryGrid.appendChild(fxTimingSel);

    // 5. Toggle Bar for Optics Tray, Scripts Drawer, Clip->Beats Drawer & Quick Chips
    const toolRow = el("div", "h3st-row");
    const trayToggleBtn = button("▸ + Optics, Grade & Audio", "Toggle secondary optics, color, FX, pose, playbook & audio dials", () => {
        secondaryDrawer.hidden = !secondaryDrawer.hidden;
        updateTrayButton();
    });
    const scriptsToggleBtn = button("▤ Scripts", "Load clean-room SandTie showcase scripts", () => {
        const open = scriptsDrawer.hidden;
        scriptsDrawer.hidden = !open;
        clipDrawer.hidden = true;
        scriptsToggleBtn.classList.toggle("h3st-chip-on", open);
        clipToggleBtn.classList.remove("h3st-chip-on");
    });
    const clipToggleBtn = button("▶ Clip → Beats", "Extract timed beats from a video via 30-FPS OpenCV", () => {
        const open = clipDrawer.hidden;
        clipDrawer.hidden = !open;
        scriptsDrawer.hidden = true;
        clipToggleBtn.classList.toggle("h3st-chip-on", open);
        scriptsToggleBtn.classList.remove("h3st-chip-on");
    });

    function updateTrayButton() {
        const secOn = SECONDARY_DIALS.filter(([k]) => parseMultiValue(flavors[k]).length > 0).length;
        const prefix = secondaryDrawer.hidden ? "▸ +" : "▾ Hide";
        trayToggleBtn.textContent = `${prefix} Optics, Grade & Audio${secOn ? ` (${secOn} on)` : ""}`;
        trayToggleBtn.classList.toggle("h3st-chip-on", !secondaryDrawer.hidden || secOn > 0);
    }

    const chipWidgets = {};
    function buildChipGroup(key, title, choices) {
        const grp = el("div", "h3st-chips");
        grp.appendChild(el("span", "h3st-chips-lbl", title));
        const btns = [];
        for (const [val, lbl] of choices) {
            const b = button(lbl, `${title}: ${lbl}`, () => {
                flavors[key] = val;
                persistFlavors();
                syncChips();
            }, "h3e-btn");
            b.style.padding = "2px 6px";
            b.style.fontSize = "10.5px";
            b.dataset.val = val;
            btns.push(b);
            grp.appendChild(b);
        }
        chipWidgets[key] = btns;
        return grp;
    }

    function syncChips() {
        for (const [k, btns] of Object.entries(chipWidgets)) {
            const cur = String(flavors[k] || "");
            for (const b of btns) b.classList.toggle("h3st-chip-on", b.dataset.val === cur);
        }
    }

    const talkGrp = buildChipGroup("talk_mode", "TALK", [["auto", "Auto"], ["talk_all", "All"], ["quotes_only", "Quotes"], ["silent", "Silent"]]);
    const energyGrp = buildChipGroup("energy", "ENERGY", [["small", "S"], ["medium", "M"], ["large", "L"]]);
    const exprGrp = buildChipGroup("expression", "EXPR", [["small", "S"], ["medium", "M"], ["large", "L"]]);
    const povGrp = buildChipGroup("pov", "POV", [["off", "Off"], ["male", "M"], ["female", "F"]]);
    syncChips();

    const spacerTool = el("span");
    spacerTool.style.flex = "1 1 auto";
    toolRow.append(trayToggleBtn, scriptsToggleBtn, clipToggleBtn, spacerTool, talkGrp, energyGrp, exprGrp, povGrp);

    // 6. Scripts Drawer & Clip->Beats Drawer
    const scriptsDrawer = el("div", "h3st-drawer");
    scriptsDrawer.hidden = true;
    const scriptSel = el("select", "h3e-select");
    scriptSel.style.flex = "1 1 280px";
    const loadRawScriptBtn = button("Load Raw", "Paste selected script verbatim into Prompt block", () => loadOrAdaptScript(false));
    const adaptScriptBtn = button("Adapt to Refs & Dials", "Rebind <Subject N> and active Place/Style/Light/Colour onto this script", () => loadOrAdaptScript(true), "h3e-btn h3e-btn-accent");
    const scRow = el("div", "h3st-row");
    scRow.append(el("strong", null, "Curated Clean-Room Scripts:"), scriptSel, loadRawScriptBtn, adaptScriptBtn);
    scriptsDrawer.appendChild(scRow);

    const clipDrawer = el("div", "h3st-drawer");
    clipDrawer.hidden = true;
    const vidInput = el("input", "h3e-writer-brief");
    vidInput.type = "text";
    vidInput.placeholder = "video filename in input/ or h3_refs/…";
    const inSecInp = el("input", "h3e-writer-brief");
    inSecInp.type = "number";
    inSecInp.style.maxWidth = "68px";
    inSecInp.placeholder = "IN s";
    const outSecInp = el("input", "h3e-writer-brief");
    outSecInp.type = "number";
    outSecInp.style.maxWidth = "68px";
    outSecInp.placeholder = "OUT s";
    const extractBtn = button("Extract Beats", "Run 30-FPS OpenCV optical flow + jump-cut storyboard extractor", runVideoExtractor, "h3e-btn h3e-btn-accent");
    const extractedBadge = el("span", "h3st-pill", "No clip extracted");
    const clRow = el("div", "h3st-row");
    clRow.append(el("strong", null, "▶ Video → Beats:"), vidInput, inSecInp, outSecInp, extractBtn, extractedBadge);
    clipDrawer.appendChild(clRow);

    let extractedVideoData = null;

    // 7. Prominent Reference Bible (open by default!)
    let bibleOpen = true;
    let bibleFilter = "all";
    let bibleQuery = "";
    let refBankItems = [];

    const bibleBox = el("div", "h3st-bible");
    const bibleHead = el("div", "h3st-head");
    const bibleLeft = el("div", "h3st-row");
    const bibleToggleBtn = button("▾ 📖 Reference Bible", "Show or fold Reference Bible cards", () => {
        bibleOpen = !bibleOpen;
        renderReferenceBible();
    });
    const bibleWiredPills = el("div", "h3st-row");
    bibleLeft.append(bibleToggleBtn, bibleWiredPills);

    const bibleRight = el("div", "h3st-row");
    const castAllBtn = button("Cast Filtered → S1..S9", "Assign filtered Reference Bible cast onto Subject 1..N", castFilteredToRail);
    const saveRailBtn = button("Save Rail → Bible", "Import current rail subjects/plates into your persistent Reference Bible", importRailToBible);
    const uploadInp = document.createElement("input");
    uploadInp.type = "file";
    uploadInp.accept = "image/*";
    uploadInp.hidden = true;
    uploadInp.addEventListener("change", async () => {
        const f = uploadInp.files?.[0];
        uploadInp.value = "";
        if (!f) return;
        await uploadAndScanFile(f);
    });
    const uploadBtn = button("+ Upload & Eye Scan", "Upload an image to h3_refs, run 2.5 MP Eye Scan, and save to Reference Bible", () => uploadInp.click());
    bibleRight.append(castAllBtn, saveRailBtn, uploadBtn, uploadInp);
    bibleHead.append(bibleLeft, bibleRight);

    const bibleBody = el("div", "h3st-shell");
    const bibleFilterRow = el("div", "h3st-row");
    const bibleSearchInp = el("input", "h3e-writer-brief");
    bibleSearchInp.type = "text";
    bibleSearchInp.style.flex = "1 1 160px";
    bibleSearchInp.placeholder = "Search Reference Bible (name, @tag, ethnicity, outfit)…";
    bibleSearchInp.addEventListener("input", () => {
        bibleQuery = bibleSearchInp.value;
        renderBibleCardsOnly();
    });
    const clearRailBtn = button("Clear Rail", "Clear wired refs in ref_plan", () => {
        setRefPlan(JSON.stringify({ refs: [], subjects: {} }));
        renderReferenceBible();
    });

    const bfBtns = {};
    for (const [fk, fl] of [["all", "All"], ["subject", "Cast"], ["place", "Plates"], ["prop", "Props"]]) {
        const b = button(fl, `Show ${fl}`, () => {
            bibleFilter = fk;
            renderReferenceBible();
        });
        b.style.padding = "2px 7px";
        b.style.fontSize = "11px";
        bfBtns[fk] = b;
        bibleFilterRow.appendChild(b);
    }
    bibleFilterRow.append(bibleSearchInp, clearRailBtn);
    const bibleGrid = el("div", "h3st-bible-grid");
    bibleBody.append(bibleFilterRow, bibleGrid);
    bibleBox.append(bibleHead, bibleBody);

    function readRefPlanObj() {
        try {
            const d = JSON.parse(String(getRefPlan() || "") || "{}");
            return { refs: Array.isArray(d?.refs) ? d.refs : [], subjects: (d?.subjects && typeof d.subjects === "object") ? d.subjects : {} };
        } catch {
            return { refs: [], subjects: {} };
        }
    }

    function writeRefPlanObj(doc) {
        setRefPlan(JSON.stringify({ refs: doc.refs || [], subjects: doc.subjects || {} }));
    }

    function assignBibleItemToSlot(item, roleTarget) {
        const doc = readRefPlanObj();
        const wasSame = doc.refs.some((r) => String(r.file || "") === String(item.file || "") && (r.subject ? `S${r.subject}` : (r.retention === "prop" ? "Prop" : "Plate")) === roleTarget);
        const refs = doc.refs.filter((r) => String(r.file || "") !== String(item.file || ""));
        const subjects = Object.assign({}, doc.subjects);

        // Clean up unused subject metadata for subjects no longer present on kept refs
        const cleanUnusedSubjects = (list) => {
            const liveSubs = new Set(list.map((r) => r.subject).filter((x) => x !== null && x !== undefined));
            for (const k of Object.keys(subjects)) {
                if (!liveSubs.has(Number(k))) delete subjects[k];
            }
        };

        if (roleTarget === "__remove__" || wasSame) {
            cleanUnusedSubjects(refs);
            doc.refs = refs;
            doc.subjects = subjects;
            writeRefPlanObj(doc);
            renderReferenceBible();
            return;
        }

        const usedSlots = new Set(refs.map((r) => Number(r.slot || 0)).filter((n) => n >= 1));
        const pickFreeSlot = (prefer = 0) => {
            if (prefer >= 1 && prefer <= 9 && !usedSlots.has(prefer)) return prefer;
            for (let n = 1; n <= 9; n++) if (!usedSlots.has(n)) return n;
            return refs.length + 1;
        };

        if (roleTarget === "Plate" || roleTarget === "Prop") {
            const slot = pickFreeSlot(0);
            refs.push({
                slot, tag: item.tag || "plate", file: item.file,
                subject: null, retention: roleTarget === "Prop" ? "prop" : "reference", desc: item.desc || "",
            });
        } else {
            const sn = Math.max(1, Math.min(9, Number(String(roleTarget).replace(/\D+/g, "")) || nextOpenSubjectSlot(refs)));
            const filtered = refs.filter((r) => Number(r.subject) !== sn);
            const usedAfter = new Set(filtered.map((r) => Number(r.slot || 0)).filter((n) => n >= 1));
            let slot = sn;
            if (usedAfter.has(slot)) {
                slot = 1;
                while (usedAfter.has(slot) && slot < 9) slot++;
            }
            filtered.push({
                slot, tag: item.tag || `subject${sn}`, file: item.file,
                subject: sn, retention: "fully_preserved", desc: item.desc || "",
                voice: item.voice || "",
            });
            subjects[sn] = {
                name: item.char_name || item.name || "",
                locked: item.locked || "",
                context: item.context || "",
            };
            filtered.sort((a, b) => Number(a.slot || 0) - Number(b.slot || 0));
            cleanUnusedSubjects(filtered);
            doc.refs = filtered;
            doc.subjects = subjects;
            writeRefPlanObj(doc);
            renderReferenceBible();
            return;
        }
        refs.sort((a, b) => Number(a.slot || 0) - Number(b.slot || 0));
        cleanUnusedSubjects(refs);
        doc.refs = refs;
        doc.subjects = subjects;
        writeRefPlanObj(doc);
        renderReferenceBible();
    }

    function nextOpenSubjectSlot(refsList) {
        const used = new Set((refsList || []).map((r) => Number(r.subject)).filter((n) => Number.isFinite(n) && n >= 1));
        for (let n = 1; n <= 9; n++) if (!used.has(n)) return n;
        return 9;
    }

    function castFilteredToRail() {
        const cast = refBankItems.filter((it) => it.role === "subject" && (!bibleQuery || `${it.name} ${it.tag} ${it.desc}`.toLowerCase().includes(bibleQuery.toLowerCase())));
        if (!cast.length) return;
        const doc = { refs: [], subjects: {} };
        cast.slice(0, 9).forEach((it, idx) => {
            const sn = idx + 1;
            doc.refs.push({ slot: sn, tag: it.tag || `subject${sn}`, file: it.file, subject: sn, retention: "fully_preserved", desc: it.desc || "", voice: it.voice || "" });
            doc.subjects[sn] = { name: it.char_name || it.name || "", locked: it.locked || "", context: it.context || "" };
        });
        writeRefPlanObj(doc);
        renderReferenceBible();
        say(`Cast ${Math.min(9, cast.length)} Reference Bible subject(s) onto S1..S${Math.min(9, cast.length)}.`, "hint");
    }

    let editingCardId = "";

    function renderBibleCardsOnly() {
        const doc = readRefPlanObj();
        const nextSub = nextOpenSubjectSlot(doc.refs);
        const byFileSlot = new Map();
        for (const r of doc.refs) {
            if (!r.file) continue;
            byFileSlot.set(String(r.file), r.subject ? `S${r.subject}` : (r.retention === "prop" ? "Prop" : "Plate"));
        }
        const q = bibleQuery.trim().toLowerCase();
        const visible = refBankItems.filter((it) => {
            if (bibleFilter !== "all" && it.role !== bibleFilter) return false;
            if (!q) return true;
            return `${it.name} ${it.tag} ${it.desc} ${it.voice}`.toLowerCase().includes(q);
        });

        bibleGrid.textContent = "";
        if (!visible.length) {
            const emptyMsg = el("div", "h3e-note", refBankItems.length ? "No Reference Bible items match this filter." : "No saved Reference Bible entries yet — click + Upload & Eye Scan or Save Rail → Bible.");
            bibleGrid.appendChild(emptyMsg);
            return;
        }
        const frag = document.createDocumentFragment();
        for (const it of visible.slice(0, 60)) {
            const activeSlot = byFileSlot.get(it.file) || "";
            const card = el("div", "h3st-bcard" + (activeSlot ? " h3st-bwired" : ""));
            const top = el("div", "h3st-btop");
            const img = document.createElement("img");
            img.className = "h3st-bthumb";
            img.loading = "lazy";
            img.alt = it.name || it.tag;
            img.src = `${SANDTIE_THUMB_URL}?file=${encodeURIComponent(it.file)}&w=128&v=${it.mtime || 1}`;
            const meta = el("div");
            meta.style.minWidth = "0";
            meta.style.flex = "1 1 auto";
            const nm = el("div", null, `${it.name || it.tag} `);
            nm.style.fontWeight = "700";
            nm.style.fontSize = "11.5px";
            nm.style.whiteSpace = "nowrap";
            nm.style.overflow = "hidden";
            nm.style.textOverflow = "ellipsis";
            const tagSp = el("span", null, `@${it.tag}`);
            tagSp.style.color = "var(--h3-muted)";
            tagSp.style.fontWeight = "400";
            nm.appendChild(tagSp);
            const subMeta = el("div", null, `${it.role}${it.voice ? " · ♪ " + it.voice : ""}`);
            subMeta.style.fontSize = "10px";
            subMeta.style.color = "var(--h3-muted)";
            meta.append(nm, subMeta);
            top.append(img, meta);
            if (activeSlot) top.appendChild(el("span", "h3st-pill h3st-pill-accent", activeSlot));

            const desc = el("div", "h3st-bdesc", it.desc || "Pending Eye Scan…");
            const acts = el("div", "h3st-row");
            if (it.role === "subject") {
                if (activeSlot && activeSlot.startsWith("S")) {
                    const rmBtn = button(`✓ ${activeSlot} ×`, `Wired as ${activeSlot} — click to remove from rail`, () => assignBibleItemToSlot(it, "__remove__"), "h3e-btn h3st-chip-on");
                    rmBtn.style.padding = "2px 6px";
                    rmBtn.style.fontSize = "10.5px";
                    acts.appendChild(rmBtn);
                } else {
                    const nextBtn = button(`+ S${nextSub}`, `Wire into next open slot (S${nextSub}) — supports S1 through S9`, () => assignBibleItemToSlot(it, `S${nextSub}`));
                    nextBtn.style.padding = "2px 6px";
                    nextBtn.style.fontSize = "10.5px";
                    acts.appendChild(nextBtn);
                }
                const slotSel = el("select", "h3e-select");
                slotSel.style.maxWidth = "56px";
                slotSel.style.padding = "2px 4px";
                slotSel.style.fontSize = "10.5px";
                slotSel.title = "Pick exact cast slot S1..S9";
                const phOpt = el("option", null, activeSlot || "S#");
                phOpt.value = "";
                slotSel.appendChild(phOpt);
                for (let n = 1; n <= 9; n++) {
                    const o = el("option", null, `S${n}`);
                    o.value = `S${n}`;
                    slotSel.appendChild(o);
                }
                slotSel.addEventListener("change", () => {
                    if (slotSel.value) assignBibleItemToSlot(it, slotSel.value);
                });
                acts.appendChild(slotSel);
            } else {
                const slotRole = it.role === "prop" ? "Prop" : "Plate";
                const cb = button(activeSlot === slotRole ? `✓ ${slotRole} ×` : `+ ${slotRole}`, activeSlot === slotRole ? `Remove ${slotRole} from rail` : `Wire as ${slotRole}`, () => assignBibleItemToSlot(it, activeSlot === slotRole ? "__remove__" : slotRole));
                cb.style.padding = "2px 6px";
                cb.style.fontSize = "10.5px";
                if (activeSlot === slotRole) cb.classList.add("h3st-chip-on");
                acts.appendChild(cb);
            }
            const scanBtn = button("👁", "Run 2.5 MP Eye Scan on this reference", () => scanBibleItem(it));
            scanBtn.style.padding = "2px 6px";
            scanBtn.style.fontSize = "10.5px";
            const editBtn = button("✎", "Edit Reference Bible name, @tag, role, voice & description", () => {
                editingCardId = editingCardId === it.id ? "" : it.id;
                renderBibleCardsOnly();
            });
            editBtn.style.padding = "2px 6px";
            editBtn.style.fontSize = "10.5px";
            if (editingCardId === it.id) editBtn.classList.add("h3st-chip-on");
            const delBtn = button("×", "Remove from Reference Bible", () => deleteBibleItem(it));
            delBtn.style.padding = "2px 6px";
            delBtn.style.fontSize = "10.5px";
            acts.append(scanBtn, editBtn, delBtn);

            card.append(top, desc, acts);

            if (editingCardId === it.id) {
                const ed = el("div", "h3st-shell");
                ed.style.paddingTop = "4px";
                ed.style.borderTop = "1px solid var(--h3-border-soft)";
                const nmInp = el("input", "h3e-writer-brief");
                nmInp.type = "text";
                nmInp.value = it.name || "";
                nmInp.placeholder = "Display name";
                const tagInp = el("input", "h3e-writer-brief");
                tagInp.type = "text";
                tagInp.value = it.tag || "";
                tagInp.placeholder = "@tag";
                const roleSel = el("select", "h3e-select");
                for (const rk of ["subject", "place", "prop"]) {
                    const o = el("option", null, rk);
                    o.value = rk;
                    roleSel.appendChild(o);
                }
                roleSel.value = it.role || "subject";
                const voiceInp = el("input", "h3e-writer-brief");
                voiceInp.type = "text";
                voiceInp.value = it.voice || "";
                voiceInp.placeholder = "voice file (e.g. mara.wav)";
                const descInp = el("textarea", "h3e-json");
                descInp.rows = 2;
                descInp.value = it.desc || "";
                const saveCardBtn = button("Save", "Save changes to Reference Bible", async () => {
                    const r = await fetch(SANDTIE_REFBANK_URL, {
                        method: "POST", headers: { "Content-Type": "application/json" },
                        body: JSON.stringify({
                            action: "save",
                            item: {
                                id: it.id, file: it.file, name: nmInp.value.trim(),
                                char_name: nmInp.value.trim().split(" ")[0],
                                tag: tagInp.value.trim().replace(/^@/, ""),
                                role: roleSel.value, voice: voiceInp.value.trim(), desc: descInp.value.trim(),
                            },
                        }),
                    });
                    const j = await r.json();
                    if (j.ok) {
                        refBankItems = j.items || [];
                        editingCardId = "";
                        renderReferenceBible();
                        say(`Updated ${nmInp.value.trim() || it.file}.`, "hint");
                    }
                }, "h3e-btn h3e-btn-accent");
                const r1 = el("div", "h3st-row");
                r1.append(nmInp, tagInp, roleSel);
                const r2 = el("div", "h3st-row");
                r2.append(voiceInp, saveCardBtn);
                ed.append(r1, descInp, r2);
                card.appendChild(ed);
            }

            frag.appendChild(card);
        }
        bibleGrid.appendChild(frag);
    }

    function renderReferenceBible() {
        const doc = readRefPlanObj();
        bibleToggleBtn.textContent = `${bibleOpen ? "▾" : "▸"} 📖 Reference Bible (${refBankItems.length} Saved)`;
        bibleToggleBtn.classList.toggle("h3st-chip-on", bibleOpen);
        bibleBody.hidden = !bibleOpen;
        bibleWiredPills.textContent = "";
        for (const r of doc.refs) {
            if (!r.file) continue;
            const badgeLbl = r.subject ? `S${r.subject}: @${r.tag} ×` : `${r.retention === "prop" ? "Prop" : "Plate"}: @${r.tag} ×`;
            const pBtn = button(badgeLbl, `Click to unassign @${r.tag}`, () => assignBibleItemToSlot({ file: r.file }, "__remove__"), "h3st-pill h3st-pill-accent");
            pBtn.style.cursor = "pointer";
            bibleWiredPills.appendChild(pBtn);
        }
        const counts = { all: refBankItems.length, subject: 0, place: 0, prop: 0 };
        for (const it of refBankItems) counts[it.role] = (counts[it.role] || 0) + 1;
        for (const [fk, b] of Object.entries(bfBtns)) {
            const lbl = fk === "all" ? "All" : (fk === "subject" ? "Cast" : (fk === "place" ? "Plates" : "Props"));
            b.textContent = `${lbl} (${counts[fk] || 0})`;
            b.classList.toggle("h3st-chip-on", bibleFilter === fk);
        }
        if (bibleOpen) renderBibleCardsOnly();
    }

    async function importRailToBible() {
        const r = await fetch(SANDTIE_REFBANK_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "import_rail", ref_plan: getRefPlan(), voice_files: getVoiceFiles() }),
        });
        const j = await r.json();
        if (j.ok) {
            refBankItems = j.items || [];
            renderReferenceBible();
            say(`Saved rail references into Reference Bible (${refBankItems.length} total).`, "hint");
        }
    }

    async function scanBibleItem(item) {
        say(`Eye-Scanning ${item.file} at 2.5 MP…`, "hint");
        const r = await fetch(SANDTIE_REFBANK_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "scan", id: item.id, file: item.file, role: item.role, auto_wake: Boolean(flavors.wake_writer) }),
        });
        const j = await r.json();
        if (!j.ok) return say(j.error || "Eye Scan failed", "error");
        refBankItems = j.items || [];
        renderReferenceBible();
        say(`Eye Scan updated ${item.name || item.file}.`, "hint");
    }

    async function deleteBibleItem(item) {
        const r = await fetch(SANDTIE_REFBANK_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "delete", id: item.id, file: item.file }),
        });
        const j = await r.json();
        if (j.ok) {
            refBankItems = j.items || [];
            renderReferenceBible();
        }
    }

    async function uploadAndScanFile(file) {
        const fd = new FormData();
        fd.append("file", file, file.name);
        const upRes = await fetch(UPLOAD_URL, { method: "POST", body: fd });
        const upJson = await upRes.json();
        const savedName = upJson?.files?.[0]?.name;
        if (!savedName) return say(upJson?.error || "Upload failed", "error");
        say(`Uploaded ${savedName} — running 2.5 MP Eye Scan…`, "hint");
        const r = await fetch(SANDTIE_REFBANK_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ action: "scan", file: savedName, role: "auto", auto_wake: Boolean(flavors.wake_writer) }),
        });
        const j = await r.json();
        if (j.ok) {
            refBankItems = j.items || [];
            bibleOpen = true;
            renderReferenceBible();
            say(`Added ${savedName} to Reference Bible.`, "hint");
        } else {
            say(j.error || "Upload succeeded, scan failed.", "error");
        }
    }

    // 8. Primary Action Bar + Block Tools + Telemetry
    let activeAbortCtrl = null;
    const fastBtn = button("⚡ Quick Tie (1-Pass)", "1-pass instant write using all active SandTie dials & Eye Scan", () => runSandTie("fast"), "h3e-btn h3e-btn-accent");
    const skelBtn = button("◩ Skeleton (0 VRAM)", "Build timed beat skeleton on CPU with zero LLM/VRAM usage", () => runSandTie("skeleton"));
    const cpuBtn = button("◩ CPU Tie", "Assemble instant complete H3 prompt on CPU with zero VRAM usage", () => runSandTie("cpu"));
    const freshDlgBtn = button("❝ Fresh Dialogue", "Rewrite spoken <d> lines while keeping physical pose/hands locked", () => runSandTie("dialogue"));
    const copyBtn = button("Copy", "Copy Prompt block to clipboard", async () => {
        if (!blockBox.value.trim()) return;
        try { await navigator.clipboard.writeText(blockBox.value); say("Copied prompt block to clipboard.", "hint"); } catch (_) {}
    });
    const undoBtn = button("Undo", "Restore previous brief / storyboard / prompt / dials snapshot", () => {
        const prev = undoStack.pop();
        if (!prev) return;
        briefEl.value = prev.brief;
        planBox.value = prev.plan;
        blockBox.value = prev.block;
        try { Object.assign(flavors, JSON.parse(prev.flavors)); } catch (_) {}
        syncAllWidgets();
        saveDraft();
        syncUndoBtn();
    });
    function syncUndoBtn() {
        undoBtn.disabled = undoStack.length === 0;
        undoBtn.textContent = undoStack.length ? `Undo (${undoStack.length})` : "Undo";
    }
    syncUndoBtn();

    const abortBtn = button("■ Abort", "Cancel active writer request", () => {
        if (activeAbortCtrl) { activeAbortCtrl.abort(); activeAbortCtrl = null; say("Writer request aborted.", "hint"); }
    });
    abortBtn.hidden = true;

    const telemetryPill = el("span", "h3st-pill", "0s · 0b · 0w · 0/7000c");

    function updateTelemetry() {
        const txt = String(blockBox.value || "").trim();
        const shots = (txt.match(/\[\s*Shot\s+\d+\s*\]/gi) || []).length;
        const beats = (txt.match(/\bAt\s+\d+:\d+/gi) || []).length;
        const dlgs = (txt.match(/<d>/gi) || []).length;
        const words = txt ? txt.split(/\s+/).length : 0;
        const chars = txt.length;
        telemetryPill.textContent = `${shots}s · ${beats}b · <d>${dlgs} · ${words}w · ${chars}/7000c`;
        telemetryPill.className = "h3st-pill" + (chars > 7000 ? " h3st-pill-warn" : "");
    }
    blockBox.addEventListener("input", updateTelemetry);
    updateTelemetry();

    // 9. Combos & Smart Roll Helpers
    function refreshComboSelect() {
        comboSel.textContent = "";
        const ph = el("option", null, `Combos (${BUILTIN_DIAL_COMBOS.length} Built-In)…`);
        ph.value = "";
        comboSel.appendChild(ph);
        let userList = [];
        try { userList = JSON.parse(localStorage.getItem("h3_sandtie_user_combos") || "[]"); } catch {}
        if (userList.length) {
            const ug = document.createElement("optgroup");
            ug.label = "Saved User Combos";
            for (const c of userList) {
                const o = el("option", null, c.label);
                o.value = c.id;
                ug.appendChild(o);
            }
            comboSel.appendChild(ug);
        }
        const bg = document.createElement("optgroup");
        bg.label = "SandTie Built-In Combos";
        for (const c of BUILTIN_DIAL_COMBOS) {
            const o = el("option", null, c.label);
            o.value = c.id;
            bg.appendChild(o);
        }
        comboSel.appendChild(bg);
    }

    function applyComboValues(vals) {
        pushUndoSnapshot();
        for (const k of ALL_DIAL_KEYS) flavors[k] = "";
        Object.assign(flavors, vals || {});
        flavors.dial_modes = Object.assign({}, vals?.dial_modes || {});
        persistFlavors();
        syncAllWidgets();
    }

    comboSel.addEventListener("change", () => {
        const cid = comboSel.value;
        if (!cid) return;
        let userList = [];
        try { userList = JSON.parse(localStorage.getItem("h3_sandtie_user_combos") || "[]"); } catch {}
        const found = [...userList, ...BUILTIN_DIAL_COMBOS].find((c) => c.id === cid);
        if (found) applyComboValues(found.values);
    });

    function saveUserCombo() {
        const name = window.prompt("Name this SandTie dial combo:", "My Custom Rig");
        if (!name || !name.trim()) return;
        let userList = [];
        try { userList = JSON.parse(localStorage.getItem("h3_sandtie_user_combos") || "[]"); } catch {}
        const vals = {};
        for (const k of ALL_DIAL_KEYS) if (flavors[k]) vals[k] = flavors[k];
        vals.talk_mode = flavors.talk_mode;
        vals.energy = flavors.energy;
        vals.expression = flavors.expression;
        vals.pov = flavors.pov;
        vals.dial_modes = Object.assign({}, flavors.dial_modes || {});
        userList.unshift({ id: `user_${Date.now()}`, label: name.trim(), values: vals });
        localStorage.setItem("h3_sandtie_user_combos", JSON.stringify(userList.slice(0, 40)));
        refreshComboSelect();
    }

    function deleteUserCombo() {
        const cid = comboSel.value;
        if (!cid || !cid.startsWith("user_")) return;
        let userList = [];
        try { userList = JSON.parse(localStorage.getItem("h3_sandtie_user_combos") || "[]"); } catch {}
        userList = userList.filter((c) => c.id !== cid);
        localStorage.setItem("h3_sandtie_user_combos", JSON.stringify(userList));
        refreshComboSelect();
    }

    function domainsMatch(a, b) {
        const da = a || "general";
        const db = b || "general";
        if (da === db || da === "general" || db === "general") return true;
        if ((da === "bedroom" || da === "sofa_lounge" || da === "mirror_vanity" || da === "bdsm_dom") && (db === "bedroom" || db === "sofa_lounge" || db === "mirror_vanity" || db === "bdsm_dom")) {
            return !(da === "sofa_lounge" && db === "bdsm_dom") && !(db === "sofa_lounge" && da === "bdsm_dom");
        }
        return false;
    }

    function runSurpriseRoll() {
        pushUndoSnapshot();
        const aspSpec = parseAspectSpec(getAspect());
        const targetAsp = aspSpec.bucket;
        const fitAsp = (it) => targetAsp === "either" || it.aspect_best === "either" || it.aspect_best === targetAsp;
        const pickOne = (k, pred = null) => {
            const arr = (dialControllers[k]?.getItems() || []).filter((it) => !it.multi_hop_only && fitAsp(it) && (!pred || pred(it)));
            return arr.length ? arr[Math.floor(Math.random() * arr.length)] : null;
        };

        const themes = ["cinema_drama", "action_combat", "intimate_romance", "dance_performance"];
        const theme = themes[Math.floor(Math.random() * themes.length)];
        for (const k of ALL_DIAL_KEYS) flavors[k] = "";

        if (theme === "action_combat") {
            const cb = pickOne("combat");
            const pl = pickOne("place", (x) => x.domain === "combat_action" || x.domain === "general");
            const wr = pickOne("wardrobe", (x) => x.domain === "combat_action" || x.domain === "general");
            flavors.combat = cb?.id || "";
            flavors.place = pl?.id || "";
            flavors.wardrobe = wr?.id || "";
            flavors.fx = pickOne("fx")?.id || "";
            flavors.style = pickOne("style")?.id || "";
            flavors.energy = "large";
        } else if (theme === "intimate_romance") {
            const pl = pickOne("place", (x) => ["bedroom", "sofa_lounge", "mirror_vanity", "wet_shower", "wet_tub", "wet_pool", "office_desk", "car_cabin"].includes(x.domain));
            const domP = pl?.domain || "bedroom";
            const wr = pickOne("wardrobe", (x) => domainsMatch(domP, x.domain) && x.domain !== "combat_action");
            const domW = wr?.domain || "general";
            const ex = pickOne("explicit", (x) => domainsMatch(domP, x.domain) && domainsMatch(domW, x.domain));
            const domE = ex?.domain || "general";
            const pb = pickOne("fetish", (x) => domainsMatch(domP, x.domain) && domainsMatch(domW, x.domain) && domainsMatch(domE, x.domain));
            flavors.place = pl?.id || "";
            flavors.explicit = ex?.id || "";
            flavors.wardrobe = wr?.id || "";
            flavors.fetish = pb?.id || "";
            flavors.energy = "medium";
            flavors.expression = "large";
        } else if (theme === "dance_performance") {
            flavors.pose = pickOne("pose")?.id || "";
            flavors.place = pickOne("place", (x) => x.domain === "general" || x.domain === "sofa_lounge")?.id || "";
            flavors.music = pickOne("music")?.id || "";
            flavors.style = pickOne("style")?.id || "";
            flavors.energy = "large";
        } else {
            flavors.place = pickOne("place", (x) => x.domain === "general" || x.domain === "office_desk" || x.domain === "sofa_lounge")?.id || "";
            flavors.style = pickOne("style")?.id || "";
            flavors.talkstyle = pickOne("talkstyle")?.id || "";
            flavors.energy = "medium";
        }
        flavors.camera = pickOne("camera")?.id || "";
        flavors.light = pickOne("light")?.id || "";
        flavors.colour = pickOne("colour")?.id || "";
        flavors.ambience = pickOne("ambience")?.id || "";
        persistFlavors();
        syncAllWidgets();
        say(`Surprise Roll (${theme}, ${aspSpec.label}, domain-locked ✓).`, "hint");
    }

    function runMatchDials() {
        const txt = String(briefEl.value || "").toLowerCase();
        if (!txt.trim()) return say("Type a brief first so Match Dials can score matching dials.", "hint");
        pushUndoSnapshot();
        const tokens = txt.split(/[^a-z0-9]+/).filter((t) => t.length >= 4);
        const asp = parseAspectSpec(getAspect()).bucket;
        let matched = 0;
        for (const k of ALL_DIAL_KEYS) {
            const items = dialControllers[k]?.getItems() || [];
            let best = null;
            let bestScore = 0;
            for (const it of items) {
                if (it.multi_hop_only) continue;
                if (asp !== "either" && it.aspect_best !== "either" && it.aspect_best !== asp) continue;
                const hay = `${it.label} ${it.id} ${it.group}`.toLowerCase();
                let sc = 0;
                for (const tk of tokens) if (hay.includes(tk)) sc += 1;
                if (sc > bestScore) { bestScore = sc; best = it; }
            }
            if (best && bestScore >= 1) {
                flavors[k] = best.id;
                matched += 1;
            }
        }
        persistFlavors();
        syncAllWidgets();
        say(`Matched ${matched} dial(s) from your brief.`, "hint");
    }

    function runComposeBrief() {
        const doc = readRefPlanObj();
        const castNames = doc.refs.filter((r) => r.subject).map((r) => doc.subjects?.[r.subject]?.name || `@${r.tag}`);
        const who = castNames.length ? castNames.join(" and ") : "The lead character";
        const pName = dialControllers.place?.getItem(parseMultiValue(flavors.place)[0])?.label?.split("·")[0]?.trim() || "";
        const wName = dialControllers.wardrobe?.getItem(parseMultiValue(flavors.wardrobe)[0])?.label || "";
        const act = dialControllers.combat?.getItem(parseMultiValue(flavors.combat)[0])?.label
            || dialControllers.explicit?.getItem(parseMultiValue(flavors.explicit)[0])?.label
            || dialControllers.pose?.getItem(parseMultiValue(flavors.pose)[0])?.label
            || "moves expressively with natural eye contact";
        const bits = [who];
        if (wName) bits.push(`wearing ${wName.toLowerCase()}`);
        if (pName) bits.push(`inside ${pName.toLowerCase()}`);
        bits.push(`— ${act}.`);
        pushUndoSnapshot();
        briefEl.value = bits.join(" ");
        saveDraft();
    }

    function resetAllDials() {
        pushUndoSnapshot();
        for (const k of ALL_DIAL_KEYS) flavors[k] = "";
        flavors.dial_modes = {};
        persistFlavors();
        syncAllWidgets();
    }

    function renderActiveStrip() {
        activeStrip.textContent = "";
        const aspSpec = parseAspectSpec(getAspect());
        const targetLabel = aspSpec.label;
        const targetBucket = aspSpec.bucket;
        let has916 = false;
        let has169 = false;
        const activeEntries = [];
        for (const k of ALL_DIAL_KEYS) {
            for (const id of parseMultiValue(flavors[k])) {
                const it = dialControllers[k]?.getItem(id);
                if (!it) continue;
                activeEntries.push([k, id, it]);
                if (it.aspect_best === "9:16") has916 = true;
                if (it.aspect_best === "16:9") has169 = true;
            }
        }
        activeCountPill.textContent = `${activeEntries.length} active`;

        // Aspect mix pill
        const hasMix = (has916 && has169) || (targetBucket === "9:16" && has169) || (targetBucket === "16:9" && has916);
        const aspBtn = button(
            hasMix ? `⚠️ Aspect Mix (${targetLabel}) — Fix` : `${targetLabel} Match ✓`,
            hasMix ? `Clear dials locked against ${targetLabel}` : `All active dials match ${targetLabel} canvas aspect`,
            () => {
                if (!hasMix) return;
                pushUndoSnapshot();
                for (const k of ALL_DIAL_KEYS) {
                    const kept = parseMultiValue(flavors[k]).filter((id) => {
                        const it = dialControllers[k]?.getItem(id);
                        return !it || it.aspect_best === "either" || targetBucket === "either" || it.aspect_best === targetBucket;
                    });
                    flavors[k] = serializeMultiValue(kept);
                }
                persistFlavors();
                syncAllWidgets();
            },
            hasMix ? "h3st-pill h3st-pill-warn" : "h3st-pill h3st-pill-ok",
        );
        activeStrip.appendChild(aspBtn);

        // Domain conflict check
        const domItems = [];
        for (const k of ["place", "wardrobe", "explicit", "fetish"]) {
            for (const id of parseMultiValue(flavors[k])) {
                const it = dialControllers[k]?.getItem(id);
                if (it && it.domain && it.domain !== "general") domItems.push({ k, it });
            }
        }
        let domClash = null;
        for (let i = 0; i < domItems.length; i++) {
            for (let j = i + 1; j < domItems.length; j++) {
                if (!domainsMatch(domItems[i].it.domain, domItems[j].it.domain)) {
                    domClash = `${domItems[i].it.domain} vs ${domItems[j].it.domain}`;
                    break;
                }
            }
            if (domClash) break;
        }
        if (domClash) {
            const dBtn = button(`⚠️ Domain Clash (${domClash}) — Clear Mismatch`, "Keep Place domain & clear clashing wardrobe/staging dials", () => {
                pushUndoSnapshot();
                const anchorDom = domItems[0].it.domain;
                for (const k of ["wardrobe", "explicit", "fetish"]) {
                    const kept = parseMultiValue(flavors[k]).filter((id) => {
                        const it = dialControllers[k]?.getItem(id);
                        return !it || domainsMatch(anchorDom, it.domain);
                    });
                    flavors[k] = serializeMultiValue(kept);
                }
                persistFlavors();
                syncAllWidgets();
            }, "h3st-pill h3st-pill-warn");
            activeStrip.appendChild(dBtn);
        }

        // Best Duration advisory pill
        const durSec = parseFloat(String(getDurationLabel() || "10").replace(/[^\d.]/g, "")) || 10;
        const needLong = activeEntries.find(([_k, _id, it]) => it.duration_best && parseFloat(it.duration_best) > durSec + 0.4);
        if (needLong) {
            const bestPill = el("span", "h3st-pill h3st-pill-warn", `⏱ Best Length: ${needLong[2].duration_best} (current ${durSec}s)`);
            bestPill.title = needLong[2].duration_tip || "Recommended duration for unhurried pacing";
            activeStrip.appendChild(bestPill);
        }

        for (const [k, id, it] of activeEntries) {
            const chip = button(`${it.label} ×`, `Remove ${it.label}`, () => {
                pushUndoSnapshot();
                const next = parseMultiValue(flavors[k]).filter((x) => x !== id);
                dialControllers[k]?.setValue(serializeMultiValue(next));
                renderActiveStrip();
            }, "h3e-btn h3st-chip-on");
            chip.style.padding = "2px 6px";
            chip.style.fontSize = "10.5px";
            activeStrip.appendChild(chip);
        }
        updateTrayButton();
    }

    function syncAllWidgets() {
        swTime.chk.checked = Boolean(flavors.time_tied);
        swKinetic.chk.checked = Boolean(flavors.kinetic_grip);
        swEye.chk.checked = Boolean(flavors.eye_scan);
        swDouble.chk.checked = Boolean(flavors.double_knot);
        swWake.chk.checked = Boolean(flavors.wake_writer);
        fxTimingSel.value = flavors.fx_timing || "delayed_mid";
        syncChips();
        for (const k of ALL_DIAL_KEYS) dialControllers[k]?.setValue(flavors[k] || "");
        renderActiveStrip();
        renderReferenceBible();
    }

    // 10. Server Status & API Calls
    function paintServerButtons() {
        if (_sharedStatus.backend) writerModeSel.value = _sharedStatus.backend;
        if (_sharedStatus.running) {
            statusPill.textContent = `${_sharedStatus.backend_label || "Writer"} Ready`;
            statusPill.className = "h3st-pill h3st-pill-ok";
        } else {
            statusPill.textContent = `${_sharedStatus.backend_label || "Writer"} Offline`;
            statusPill.className = "h3st-pill";
        }
    }

    let statusRefreshSeq = 0;
    async function refreshStatus(forceCatalog = false) {
        const mySeq = ++statusRefreshSeq;
        try {
            const needCat = forceCatalog || !_sharedCatalog;
            const url = needCat ? SANDTIE_OPTIONS_URL : `${SANDTIE_OPTIONS_URL}?lite=1`;
            const r = await fetch(url);
            const j = await r.json();
            if (mySeq !== statusRefreshSeq) return;
            if (j.ok) {
                _sharedStatus = {
                    running: Boolean(j.running),
                    backend: j.backend,
                    backend_label: j.backend_label,
                    model: j.model,
                    startup_error: j.startup_error || "",
                };
                paintServerButtons();
                if (j.catalog) {
                    _sharedCatalog = j.catalog;
                    populateFromCatalog(_sharedCatalog);
                }
            }
        } catch (_) {}
    }

    function populateFromCatalog(cat) {
        if (!cat) return;
        for (const k of ALL_DIAL_KEYS) {
            const items = cat[k] || [];
            dialControllers[k]?.populate(items);
        }
        scriptSel.textContent = "";
        const ph = el("option", null, `— Pick from ${(cat.scripts || []).length} clean SandTie scripts —`);
        ph.value = "";
        scriptSel.appendChild(ph);
        const grpMap = new Map();
        for (const sc of cat.scripts || []) {
            const g = sc.group || "Showcase";
            if (!grpMap.has(g)) grpMap.set(g, []);
            grpMap.get(g).push(sc);
        }
        for (const [g, list] of grpMap.entries()) {
            const og = document.createElement("optgroup");
            og.label = g;
            for (const sc of list) {
                const o = el("option", null, sc.label);
                o.value = sc.id;
                og.appendChild(o);
            }
            scriptSel.appendChild(og);
        }
        refBankItems = cat.ref_bank || [];
        syncAllWidgets();
    }

    let writerLoadSeq = 0;
    let writerCfgLoaded = false;
    async function loadWriterSettings() {
        const mySeq = ++writerLoadSeq;
        try {
            const r = await fetch(LLM_URL);
            const j = await r.json();
            if (!j.ok || mySeq !== writerLoadSeq) return;
            writerCfgLoaded = true;
            cfgBackSel.textContent = "";
            const backs = Array.isArray(j.backends) && j.backends.length
                ? j.backends
                : [{ id: "lmstudio", label: "LM Studio" }, { id: "ninfer", label: "nInfer" }];
            for (const b of backs) {
                const o = el("option", null, b.label || b.id);
                o.value = b.id;
                cfgBackSel.appendChild(o);
            }
            cfgBackSel.value = j.backend || "lmstudio";
            writerModeSel.value = j.backend || "lmstudio";
            cfgUrlInp.value = j.server_url || "";
            cfgModelInp.value = j.model || "";
            cfgModelInp.placeholder = cfgBackSel.value === "ninfer"
                ? "model id (auto after Start; blank = auto)"
                : "model id (optional on LM Studio)";
            cfgUnloadChk.checked = j.unload_on_run !== false;
            const curPaths = (j.server_paths && j.server_paths[cfgBackSel.value]) || {};
            const hasProg = (backs.find((b) => b.id === cfgBackSel.value)?.program) || (cfgBackSel.value === "ninfer");
            cfgPathRow.hidden = !hasProg;
            cfgExeInp.value = curPaths.exe || "";
            cfgExeInp.placeholder = curPaths.found_exe
                ? `Auto-detected: ${curPaths.found_exe}`
                : "nInfer exe path (e.g. C:\\ninfer\\ninfer-serve.exe)";
            cfgModelFileInp.value = curPaths.model_file || "";
            cfgModelPick.textContent = "";
            const ph = el("option", null, (j.models || []).length ? "— Pick loaded model —" : "— No models listed —");
            ph.value = "";
            cfgModelPick.appendChild(ph);
            for (const m of j.models || []) {
                const mid = typeof m === "string" ? m : (m?.id || "");
                if (!mid) continue;
                const o = el("option", null, (m?.loaded ? "● " : "") + mid);
                o.value = mid;
                cfgModelPick.appendChild(o);
            }
        } catch (_) {}
    }

    async function saveWriterSettings({ quiet = false } = {}) {
        try {
            const activeBack = cfgBackSel.value || writerModeSel.value || "lmstudio";
            const patch = {
                backend: activeBack,
                server_url: cfgUrlInp.value.trim(),
                model: cfgModelInp.value.trim(),
                unload_on_run: cfgUnloadChk.checked,
            };
            if (activeBack === "ninfer" || !cfgPathRow.hidden) {
                patch.servers = {
                    [activeBack]: {
                        exe: cfgExeInp.value.trim(),
                        model_file: cfgModelFileInp.value.trim(),
                    },
                };
            }
            const r = await fetch(LLM_URL, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify(patch),
            });
            const j = await r.json();
            if (!j.ok) {
                say(j.error || "Failed to save writer settings.", "error");
                return false;
            }
            await Promise.all([loadWriterSettings(), refreshStatus(false)]);
            if (!quiet) {
                say(`Saved writer (${j.backend || activeBack} @ ${j.server_url || cfgUrlInp.value}).`, "hint");
            }
            return true;
        } catch (err) {
            say(String(err), "error");
            return false;
        }
    }

    async function toggleServer(action) {
        const btn = action === "start" ? startBtn : stopBtn;
        btn.disabled = true;
        try {
            if (action === "start" && writerCfgLoaded) {
                const savedOk = await saveWriterSettings({ quiet: true });
                if (!savedOk) return;
            }
            say(action === "start" ? "Starting local writer…" : "Stopping local writer…", "hint");
            const reqBody = { action };
            if (action === "start" && writerCfgLoaded && cfgModelFileInp.value.trim()) {
                reqBody.model_file = cfgModelFileInp.value.trim();
            }
            const r = await fetch(LLM_URL, {
                method: "POST", headers: { "Content-Type": "application/json" },
                body: JSON.stringify(reqBody),
            });
            const j = await r.json();
            if (!j.ok) {
                await refreshStatus(false);
                say(j.error || j.note || `Failed to ${action} local writer.`, "error");
                return;
            }
            if (action === "stop") {
                await refreshStatus(false);
                say(j.note || "Stopped local writer.", "hint");
                return;
            }
            if (j.running) {
                await refreshStatus(false);
                if (writerCfgLoaded) await loadWriterSettings();
                say(`${_sharedStatus.backend_label || "Writer"} Ready!`, "hint");
                return;
            }
            say(j.note || "Starting local writer… waiting for server.", "hint");
            for (let i = 0; i < 40; i++) {
                await new Promise((res) => setTimeout(res, 1500));
                await refreshStatus(false);
                if (_sharedStatus.running) {
                    if (writerCfgLoaded) await loadWriterSettings();
                    say(`${_sharedStatus.backend_label || "Writer"} Ready!`, "hint");
                    return;
                }
                if (_sharedStatus.startup_error) {
                    say(`Writer stopped during startup: ${_sharedStatus.startup_error}`, "error");
                    return;
                }
            }
            say("Timed out waiting for local writer — check server.err in your nInfer folder.", "error");
        } catch (err) {
            say(String(err), "error");
        } finally {
            btn.disabled = false;
        }
    }

    async function loadOrAdaptScript(adapt) {
        const pid = scriptSel.value;
        if (!pid) return say("Select a script first.", "hint");
        const r = await fetch(SANDTIE_PRESET_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                id: pid, adapt: Boolean(adapt), duration: getDurationLabel(),
                ref_plan: getRefPlan(), voice_files: getVoiceFiles(),
                flavors, brief: briefEl.value,
            }),
        });
        const j = await r.json();
        if (!j.ok) return say(j.error || "Failed to load script", "error");
        pushUndoSnapshot();
        if (j.script) blockBox.value = j.script;
        if (j.plan) planBox.value = j.plan;
        if (j.brief && !briefEl.value.trim()) briefEl.value = j.brief;
        if (j.updated_ref_plan) setRefPlan(j.updated_ref_plan);
        saveDraft();
        updateTelemetry();
        say(adapt ? `Adapted script to wired refs & dials (${j.mode}).` : "Loaded raw script.", "hint");
    }

    async function runVideoExtractor() {
        const vf = vidInput.value.trim();
        if (!vf) return say("Enter a reference video filename inside input/ or h3_refs/.", "error");
        say(`Extracting 30-FPS optical flow beats from ${vf}…`, "hint");
        const r = await fetch(SANDTIE_EXTRACT_URL, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                video_file: vf,
                in_sec: parseFloat(inSecInp.value || "0") || 0,
                out_sec: parseFloat(outSecInp.value || "0") || 0,
                auto_wake: Boolean(flavors.wake_writer),
            }),
        });
        const j = await r.json();
        if (!j.ok) return say(j.error || "Video extractor failed", "error");
        extractedVideoData = j;
        extractedBadge.textContent = `${j.duration_s}s · ${(j.beats || []).length} beats`;
        extractedBadge.className = "h3st-pill h3st-pill-ok";
        if (j.shot1 || (j.beats || []).length) {
            pushUndoSnapshot();
            planBox.value = [`[Shot 1] ${j.shot1 || ""}`, ...(j.beats || [])].filter(Boolean).join("\n");
            saveDraft();
        }
        say(`Extracted ${(j.beats || []).length} timed beats from ${vf}.`, "hint");
    }

    async function runSandTie(stage) {
        if (isBusy()) return;
        const aspSpec = parseAspectSpec(getAspect());
        flavors.aspect = aspSpec.bucket === "either" ? aspSpec.label : aspSpec.bucket;
        if (standalone) {
            flavors.output_format = h3FormatCodeFromLabel(widgetByName(node, "h3_format")?.value || "");
        }
        flavors.current_block = blockBox.value;
        setBusyState(true);
        abortBtn.hidden = false;
        activeAbortCtrl = new AbortController();
        say(stage === "skeleton" ? "Building 0-VRAM beat skeleton…" : (stage === "cpu" ? "Assembling instant CPU H3 prompt…" : `Running SandTie (${stage})…`), "hint");
        try {
            const r = await fetch(SANDTIE_WRITE_URL, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                signal: activeAbortCtrl.signal,
                body: JSON.stringify({
                    stage,
                    brief: briefEl.value,
                    plan: planBox.value,
                    duration: getDurationLabel(),
                    ref_plan: getRefPlan(),
                    start_image_file: getStartImage(),
                    voice_files: getVoiceFiles(),
                    prev_hop_context: previousHopContext ? previousHopContext() : "",
                    flavors,
                    extracted_video: extractedVideoData,
                }),
            });
            const j = await r.json();
            if (!j.ok && stage !== "fast" && stage !== "write") {
                return say(j.error || (j.errors || []).join("; ") || "SandTie failed", "error");
            }
            pushUndoSnapshot();
            if (j.skeleton && (stage === "skeleton" || !planBox.value.trim())) planBox.value = j.skeleton;
            if (j.plan && (stage === "plan" || stage === "fast" || stage === "write" || stage === "cpu")) planBox.value = j.plan;
            if (j.block) blockBox.value = j.block;
            if (j.updated_ref_plan) setRefPlan(j.updated_ref_plan);
            saveDraft();
            updateTelemetry();
            const warns = (j.warnings || []).map((w) => `• ${w}`).join("\n");
            if (!j.ok) {
                say(((j.errors || []).join("; ") || j.error || "Contract issue") + (warns ? "\n" + warns : ""), "error");
            } else {
                say(`${stage.toUpperCase()} ready (${j.mode || "H3"}).` + (warns ? `\n${warns}` : ""), "hint");
            }
        } catch (err) {
            if (err?.name !== "AbortError") say(String(err), "error");
        } finally {
            activeAbortCtrl = null;
            abortBtn.hidden = true;
            setBusyState(false);
        }
    }

    document.addEventListener("click", () => closeAllPopovers(null));

    // Assemble layout inside mountBody cleanly
    const actionBar = el("div", "h3st-row");
    actionBar.append(fastBtn, skelBtn);
    if (standalone) {
        actionBar.appendChild(cpuBtn);
        if (legacyButtons?.planBtn) actionBar.appendChild(legacyButtons.planBtn);
        if (legacyButtons?.writeBtn) actionBar.appendChild(legacyButtons.writeBtn);
        const applyBtn = button("✓ Apply to Node Outputs", "Sync prompt, storyboard, soundscape, music & ref_plan onto node sockets", () => onApplyStandalone?.(), "h3e-btn h3e-btn-accent");
        actionBar.appendChild(applyBtn);
    } else {
        if (legacyButtons?.planBtn) actionBar.appendChild(legacyButtons.planBtn);
        if (legacyButtons?.writeBtn) actionBar.appendChild(legacyButtons.writeBtn);
        if (legacyButtons?.acceptBtn) actionBar.appendChild(legacyButtons.acceptBtn);
        if (legacyButtons?.hopTargetSel) actionBar.appendChild(legacyButtons.hopTargetSel);
        if (legacyButtons?.sendHopBtn) actionBar.appendChild(legacyButtons.sendHopBtn);
    }
    const barSpacer = el("span");
    barSpacer.style.flex = "1 1 auto";
    actionBar.append(barSpacer, abortBtn);

    const blockTools = el("div", "h3st-row");
    blockTools.append(telemetryPill, freshDlgBtn, copyBtn, undoBtn);

    shell.append(headRow, swRow, writerCfgDrawer, activeStrip, primaryGrid, toolRow, secondaryDrawer, scriptsDrawer, clipDrawer, bibleBox);

    if (legacyButtons?.beforeEl && legacyButtons.beforeEl.parentElement === mountBody) {
        mountBody.insertBefore(shell, legacyButtons.beforeEl);
    } else {
        mountBody.appendChild(shell);
    }
    if (legacyButtons?.row && legacyButtons.row.parentElement === mountBody) {
        legacyButtons.row.textContent = "";
        legacyButtons.row.appendChild(actionBar);
    } else {
        mountBody.appendChild(actionBar);
    }
    if (legacyButtons?.blockCol) {
        legacyButtons.blockCol.insertBefore(blockTools, blockBox);
    } else {
        mountBody.appendChild(blockTools);
    }

    refreshComboSelect();
    if (_sharedCatalog) populateFromCatalog(_sharedCatalog);
    refreshStatus(!_sharedCatalog);

    return {
        fastBtn,
        refreshStatus,
        runSandTie,
        syncAllWidgets,
        renderReferenceBible,
        refresh: () => {
            renderActiveStrip();
            updateTelemetry();
        },
        openBible: () => { bibleOpen = true; renderReferenceBible(); },
        usePersonalEngine: () => true,
        runPersonal: (st) => runSandTie(st),
        syncBlockToolbar: updateTelemetry,
    };
}

export function mountPersonalStudio(node, ctx) {
    return mountSandTieInStandard(node, ctx);
}

export function mountSandTieInStandard(node, ctx) {
    const planBtn = ctx.row?.querySelectorAll("button")?.[0] || null;
    const writeBtn = ctx.row?.querySelectorAll("button")?.[1] || null;
    const acceptBtn = ctx.row?.querySelectorAll("button")?.[2] || null;
    const hopTargetSel = ctx.row?.querySelector("select") || null;
    const sendHopBtn = ctx.row?.querySelectorAll("button")?.[3] || null;

    return createSandTieCore(node, {
        mountBody: ctx.body,
        briefEl: ctx.brief,
        planBox: ctx.planBox,
        blockBox: ctx.blockBox,
        say: ctx.say,
        saveDraft: ctx.saveDraft,
        getDurationLabel: () => String(widgetByName(node, "duration")?.value || "10 s"),
        getAspect: () => String(widgetByName(node, "aspect")?.value || widgetByName(node, "aspect_ratio")?.value || "16:9"),
        getRefPlan: () => String(widgetByName(node, "ref_plan")?.value || ""),
        setRefPlan: (v) => {
            const w = widgetByName(node, "ref_plan");
            if (w) {
                w.value = v;
                try { w.callback?.(v, node.graph?.canvas, node); } catch (_) {}
            }
            try { node._h3Editor?.refRail?.render?.(); } catch (_) {}
            try { ctx.onRefsChanged?.(); } catch (_) {}
        },
        getStartImage: ctx.startImage,
        getVoiceFiles: ctx.voiceFiles,
        previousHopContext: ctx.previousHopContext,
        setBusyState: ctx.setBusyState,
        isBusy: ctx.isBusy,
        standalone: false,
        legacyButtons: {
            beforeEl: ctx.brief,
            row: ctx.row,
            planBtn,
            writeBtn,
            acceptBtn,
            hopTargetSel,
            sendHopBtn,
            blockCol: ctx.blockBox?.parentElement || null,
        },
    });
}

export function mountSandTieStandalone(node, mountEl, { onSyncOutputs } = {}) {
    mountEl.textContent = "";
    const initState = readRigState(node);
    const status = el("div", "h3e-note h3e-writer-status");
    status.style.display = "none";
    const briefEl = el("textarea", "h3e-json");
    briefEl.rows = 2;
    briefEl.placeholder = "Describe the scene brief: who, where, what they do, camera, dialogue…";
    briefEl.value = String(widgetByName(node, "brief")?.value || "");

    const planBox = el("textarea", "h3e-json");
    planBox.rows = 8;
    planBox.value = initState.storyboard_out || "";
    const blockBox = el("textarea", "h3e-json");
    blockBox.rows = 12;
    blockBox.value = initState.prompt_out || "";

    const split = el("div", "h3e-standard-grid");
    const c1 = el("div", "h3e-standard-col");
    c1.append(el("div", "h3e-draft-meta", "Storyboard (Beats):"), planBox);
    const c2 = el("div", "h3e-standard-col");
    c2.append(el("div", "h3e-draft-meta", "H3 Prompt Output:"), blockBox);
    split.append(c1, c2);

    let busy = false;
    const planBtn = button("Plan", "Draft storyboard beats", () => core.runSandTie("plan"));
    const writeBtn = button("Write", "Write full H3 prompt from storyboard", () => core.runSandTie("write"));

    function commitW(name, val) {
        const w = widgetByName(node, name);
        if (!w) return;
        w.value = val;
        try { w.callback?.(val, node.graph?.canvas, node); } catch (_) {}
    }

    function applyOutputs() {
        const txt = blockBox.value.trim();
        commitW("brief", briefEl.value);
        patchRigState(node, {
            storyboard_out: planBox.value,
            prompt_out: txt,
        });
        onSyncOutputs?.(txt);
    }

    const core = createSandTieCore(node, {
        mountBody: mountEl,
        briefEl,
        planBox,
        blockBox,
        say: (txt, kind) => {
            status.style.display = txt ? "" : "none";
            status.className = "h3e-note h3e-writer-status" + (kind === "error" ? " h3e-note-error" : " h3e-note-hint");
            status.textContent = txt || "";
        },
        saveDraft: () => {
            commitW("brief", briefEl.value);
            patchRigState(node, {
                storyboard_out: planBox.value,
                prompt_out: blockBox.value,
            });
        },
        getDurationLabel: () => String(widgetByName(node, "duration")?.value || "10 s"),
        getAspect: () => {
            const wVal = Number(widgetByName(node, "width")?.value || 0);
            const hVal = Number(widgetByName(node, "height")?.value || 0);
            if (wVal > 0 && hVal > 0) return hVal > wVal ? "9:16" : (wVal > hVal ? "16:9" : "1:1");
            return String(widgetByName(node, "aspect")?.value || "16:9");
        },
        getRefPlan: () => readRigState(node).ref_plan_json || "",
        setRefPlan: (v) => patchRigState(node, { ref_plan_json: String(v || "") }),
        getStartImage: () => "",
        getVoiceFiles: () => [],
        previousHopContext: null,
        setBusyState: (v) => { busy = Boolean(v); planBtn.disabled = busy; writeBtn.disabled = busy; },
        isBusy: () => busy,
        standalone: true,
        onApplyStandalone: applyOutputs,
        legacyButtons: { planBtn, writeBtn, blockCol: c2 },
    });

    mountEl.append(briefEl, status, split);
    return core;
}

export function mountSwapExtras(node, { body, wardInput, beforeEl }) {
    const row = el("div", "h3st-row");
    row.style.margin = "2px 0";
    const talkSel = el("select", "h3e-select");
    talkSel.title = "Optional SandTie Speech style for swapped dialogue";
    const styleSel = el("select", "h3e-select");
    styleSel.title = "Optional SandTie Visual Style overlay";
    const wardSel = el("select", "h3e-select");
    wardSel.title = "Quick wardrobe override from SandTie catalog";

    function fill(sel, placeholder, items) {
        sel.textContent = "";
        const ph = el("option", null, placeholder);
        ph.value = "";
        sel.appendChild(ph);
        for (const it of items || []) {
            const o = el("option", null, it.label);
            o.value = it.id;
            sel.appendChild(o);
        }
    }

    wardSel.addEventListener("change", () => {
        if (!wardSel.value) return;
        const opt = (_sharedCatalog?.wardrobe || []).find((x) => x.id === wardSel.value);
        if (opt && wardInput) wardInput.value = opt.label;
    });

    row.append(talkSel, styleSel, wardSel);
    if (beforeEl && beforeEl.parentElement === body) body.insertBefore(row, beforeEl);
    else body.appendChild(row);

    const hydrate = (cat) => {
        if (!cat) return;
        fill(talkSel, "Speech: Auto", cat.talkstyle);
        fill(styleSel, "Style: Clip Default", cat.style);
        fill(wardSel, "Wardrobe Quick Pick…", cat.wardrobe);
    };

    if (_sharedCatalog) hydrate(_sharedCatalog);
    else fetch(SANDTIE_OPTIONS_URL).then((r) => r.json()).then((j) => {
        if (j?.catalog) { _sharedCatalog = j.catalog; hydrate(_sharedCatalog); }
    }).catch(() => {});

    return {
        extraPayload: () => ({
            sandtie_talkstyle: talkSel.value || "",
            sandtie_style: styleSel.value || "",
        }),
    };
}
