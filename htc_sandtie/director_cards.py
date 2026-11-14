# Generated from ComfyUI-Hand-Tie-Clips (https://github.com/sandpies/ComfyUI-Hand-Tie-Clips) by tools/build_sandtie_pack.py.
# Edit it there, not here: the next build overwrites this file.
"""Director acting cards, scene classifiers, domain-locking, playbook & knowledge matching."""
from __future__ import annotations

import re

from . import catalogs as _cat

LIFE_RULES = {
    "small": (
        "LIFE (small): The frame stays continuously alive. Subjects blink, breathe visibly, and shift their weight naturally "
        "while one or two small details in the background move each beat."
    ),
    "medium": (
        "LIFE (medium): The world moves behind the subjects and every person is physically alive inside it. In every beat, "
        "give each subject active micro-business with their hands, props, eyes, and breath while the background runs "
        "subtle environmental motion."
    ),
    "large": (
        "LIFE (large — MAX INTERACTIVITY): Every layer of the frame hums with continuous kinetic life and tactile business! "
        "Subjects actively manipulate props, eyewear, drinks, hair, or clothing with their fingers, shift weight dynamically, "
        "and engage the camera lens while background lights, air, and surfaces react around them."
    ),
}

LIFE_RULES_POSE_LOCKED = {
    "small": (
        "LIFE (small): The frame stays continuously alive with visible breathing in the ribcage and shoulders and subtle ambient motion in the background."
    ),
    "medium": (
        "LIFE (medium): Every person is physically alive inside their pose — visible breath rising and falling in the chest and shoulders, skin highlights shifting in the light, and subtle environmental motion in the background."
    ),
    "large": (
        "LIFE (large): Every layer of the frame hums with continuous physical life — deep rhythmic breathing across the ribcage and shoulders, natural skin sheen and soft-tissue momentum reacting to every movement, and active ambient light and surface detail in the room."
    ),
}

ENERGY_RULES_GEN = {
    "small": "ENERGY (small): Unhurried, grounded, and deliberate pacing. Movements flow smoothly with relaxed posture, lingering eye contact, and soft, intimate vocal delivery.",
    "medium": "ENERGY (medium): Punchy, dynamic, and physically committed! Subjects move with crisp momentum, decisive hand gestures, sharp posture shifts between beats, and spirited expressive delivery.",
    "large": "ENERGY (large — HIGH VELOCITY): Maximum kinetic momentum and dramatic contrast! Pack every beat with decisive physical actions — sharp posture snaps, torso leans across space, brisk hand choreography, and expressive vocal intensity.",
}

ENERGY_RULES_SEX = {
    "small": "ENERGY (small — SLOW & DEEP RHYTHM): Keep the physical pace slow, unhurried, and lingering along the active pose axis, with smooth full-length strokes, steady supporting hand placement, and natural breathing.",
    "medium": "ENERGY (medium — RHYTHMIC & PROGRESSIVE ESCALATION): Start already in active rhythmic motion along the locked pose axis, then progressively increase the speed and depth of penetration to cover the full length of the erect shaft while maintaining each hand's assigned job.",
    "large": "ENERGY (large — RIGOROUS FULL-DEPTH DRIVE): Drive rigorous, high-speed, full-depth strokes along the locked pose axis covering the entire length of the erect shaft, with firm supporting hand grips and intense physical momentum.",
}

EXPRESSION_RULES_GEN = {
    "small": "EXPRESSION (small): Understated, naturalistic micro-acting in the eyes, brows, and lips that shifts cleanly when the beat turns.",
    "medium": "EXPRESSION (medium): Clear, vivid facial acting! Every beat shows a distinct readable emotional shift in the eyes, eyebrows, and mouth (a slow knowing smirk, a sharp double-take, a teasing lip-bite, or an arched brow).",
    "large": "EXPRESSION (large — THEATRICAL MAX): Vivid, charismatic facial acting straight to camera or scene partner! Contrast distinct facial states cleanly across beats — poised deadpan shifting into wide-eyed surprise or amused confidence.",
}

EXPRESSION_RULES_SEX = {
    "small": "EXPRESSION (small): Genuine, intimate sensual pleasure — half-lidded bedroom eyes, soft natural breathing, and unbroken warm focus consistent with the active pose.",
    "medium": "EXPRESSION (medium): Heated, responsive arousal matching the active pose — arched brows, focused or half-lidded eyes, and breathless vocal pleasure.",
    "large": "EXPRESSION (large — INTENSE EROTIC PLEASURE): Expressive physical and facial intensity matching the active pose — arched brows, glistening eyes, flushed skin, and breathless gasps or moans as speed and depth build.",
}

EXPRESSION_RULES_SEX_ORAL = {
    "small": "EXPRESSION (oral — small): Half-lidded upward gaze and hollowed cheeks with her lips continuously sealed around the shaft.",
    "medium": "EXPRESSION (oral — medium): Arched brows, glistening eyes, hollowed cheeks, and visible throat bulge while her lips stay sealed around the shaft as she gags and moans.",
    "large": "EXPRESSION (oral — large): Watery glistening eyes, deeply hollowed cheeks, and visible throat bulge as she gags and moans around the full length of the shaft, switching to breathless panting only after an explicit pullout.",
}

EXPRESSION_RULES_SEX_PROGRESSIVE = {
    "small": "EXPRESSION (progressive setup — small): In Beat 1, keep a calm, focused expression on her opening activity; in Beat 2 and Beat 3, shift into half-lidded sensual pleasure.",
    "medium": "EXPRESSION (progressive setup — medium): In Beat 1 (Opening Setup), maintain calm, steady focus on her task; in Beat 2 (Entry & Escalation), her composure cracks as she bites her lower lip and gasps; in Beat 3 (Payoff), open into breathless pleasure.",
    "large": "EXPRESSION (progressive setup — large): In [Shot 1] and Beat 1, keep her expression calm and focused on her opening task; in Beat 2, her composure cracks with widened eyes, arched brows, and bitten lower lip; in Beat 3, reach full overstimulated climax.",
}

EXPRESSION_RULES_REAR = {
    "small": "EXPRESSION (rear / facing-away body acting): Expressive physical poise through a relaxed arched spine, steady breathing in the shoulders, and fingers resting naturally on the surface ahead while keeping torso and head facing forward.",
    "medium": "EXPRESSION (rear / facing-away body acting): Vivid physical arousal expressed through a deepening lumbar arch, fingers gripping the sheets or thighs ahead, and responsive hip and glute rhythm while keeping shoulders, torso, and head facing forward away from the lens.",
    "large": "EXPRESSION (rear / facing-away body acting): High-intensity physical ecstasy expressed through a steep spine bow, shoulders drawing back as fingers clench the pillow or surface ahead, toes curling, and trembling thighs while keeping torso and head facing forward away from the lens.",
}

_PROGRESSIVE_SETUP_RX = re.compile(
    r"\b(?:gam(?:er|ing|e)|controller|play(?:ing)?\s+(?:a\s+)?(?:video\s*)?game|free\s*use|casual(?:ly)?|unbothered|"
    r"distract\w*|multitask\w*|while\s+(?:she\s+|he\s+)?(?:plays?|reads?|works?|cooks?|texts?|scrolls?|studies|watches)|"
    r"on\s+(?:her|the)\s+phone|reading\s+a\s+book|before\s+(?:anything|he\s+enters|sliding\s+in)|"
    r"starts?\s+(?:out\s+)?(?:calm|normal|focused|casual)|slow\s+build)\b",
    re.I,
)

_SEX_RX = re.compile(
    r"\b(?:sex\w*|nude|naked|topless|bottomless|undress\w*|strip\w*|flash\w*|peek\w*|cowgirl|missionary|doggy|prone\s*bone|"
    r"spooning|lotus|blowjob|bj|deepthroat\w*|throatfuck\w*|facefuck\w*|handjob|footjob|titfuck|paizuri|tittyfuck|titjob|"
    r"cunnilingus|facesit\w*|queening|69|sixty[- ]?nine|pussy|labia|clit\w*|cock|dick|penis|shaft|glans|balls|scrotum|"
    r"breasts?|tits|boobs|nipples?|cleavage|underboob|sideboob|ass|butt|glutes?|cheeks|asshole|anus|anal|starfish|pucker|"
    r"dildo|vibrator|magic\s*wand|strap[- ]?on|pegging|plug|butt\s*plug|beads|orgasm\w*|cum\w*|climax\w*|creampie|"
    r"facial|bukkake|swallow\w*|squir\w*|straddl\w*|grind\w*|thrust\w*|penetrat\w*|ride|riding|twerk\w*|booty|"
    r"erotic|fetish|bdsm|femdom|domme|submissive|bondage|handcuffs?|ballgag|gag\w*|collar|leash|whip|crop|spank\w*|"
    r"slap\w*|hair[- ]?pull\w*|chok\w*|joi|cei|sph|findom|cuck\w*|edging|ruined|armpit|"
    r"foot\s*worship|sole\w*|toes?|pantyhose|stockings?|panties|thong|bikini|lingerie|latex|oiled|saliva|spit\w*|drool\w*|"
    r"moan\w*|groan\w*|dirty\s*talk|arous\w*|seduc\w*)\b",
    re.I,
)

_ANAL_RX = re.compile(
    r"\b(?:anal\w*|assfuck\w*|butt\s*fuck\w*|(?:in|into|inside|up)\s+(?:her|his|their|the)\s+ass(?:hole)?|"
    r"asshole|anus|rectum|sphincter|starfish|rosebud|pegging|butt\s*plug\w*|anal\s*beads|backdoor|sodomy)\b",
    re.I,
)

_REAR_FACING_RX = re.compile(
    r"\b(?:from\s+behind|doggy\w*|prone\s*bone|reverse\s*cowgirl|on\s+(?:her\s+)?stomach|face[- ]?down|"
    r"chest[- ]?down|all\s+fours|facing\s+(?:forward\s+)?away|"
    r"(?:bare\s+)?back\s+(?:and\s+(?:rounded\s+)?(?:glutes|ass(?:\s+cheeks)?)\s+)?(?:to|visible\s+to|facing)\s+the\s+(?:camera|lens|viewer)|"
    r"three[- ]quarter\s+rear|rear\s+(?:three[- ]quarter|medium|close[- ]?up)|"
    r"bent\s+over|rear[- ]?entry|behind\s+her\s+hips|spitroast|69\s+position|sixty[- ]?nine|seated\s+lotus)\b",
    re.I,
)

_OVER_SHOULDER_RX = re.compile(
    r"\b(?:look(?:s|ing)?\s+back\s+over\s+(?:her|his|their)\s+shoulder|glanc(?:es|ing)\s+back\s+over\s+(?:her|his|their)\s+shoulder|over[- ]the[- ]shoulder\s+(?:ass|selfie|look))\b",
    re.I,
)

_FRONT_OR_MULTI_POS_RX = re.compile(
    r"\b(?:missionary|on\s+her\s+back|legs?\s+lifted\s+high|knees?\s+pulled\s+to\s+her\s+chest|front[- ]view|"
    r"multi[- ]?(?:positions?|angles?)|multiple\s+(?:positions?|angles?)|across\s+(?:multi(?:ple)?\s+)?positions?|"
    r"blowjob|deep\s*throat\w*|fellatio|face[- ]?to[- ]?face)\b",
    re.I,
)

_ORAL_OCCUPIED_RX = re.compile(
    r"\b(?:blowjob|bj|deepthroat\w*|throatfuck\w*|facefuck\w*|suck(?:s|ing)\s+(?:his|her|the|a)?\s*(?:cock|dick|shaft|dildo|strap[- ]?on)|"
    r"o[- ]?ring\s+(?:lip\s+|vacuum\s+)?seal|ballgag\w*|gagged|spitroast|69\s+position|sixty[- ]?nine)\b",
    re.I,
)

_COMBAT_RX = re.compile(
    r"\b(?:fight\w*|combat|punch\w*|uppercut|jab|roundhouse|kick\w*|martial\s*arts?|kung\s*fu|muay\s*thai|karate|judo|"
    r"brawl\w*|tackle\w*|suplex|chokehold|headlock|wrestl\w*|grappl\w*|gun[- ]?fu|shootout|gunfight|pistol|"
    r"shotgun|rifle|sniper|revolver|muzzle\s*flash|katana|sword\w*|lightsaber|dagger|blade|slash\w*|parry|disarm\w*|"
    r"kamehameha|ki\s*blast|plasma\s*beam|shockwave|superhero\s*landing|fireball|explosion|detonat\w*|bullet[- ]?time)\b",
    re.I,
)

ANAL_EXPLICIT_IDS = {
    "anal_on_back_knees_up", "anal_between_thighs_closeup",
    "anal_standing_bent_over_desk", "rough_anal_doggy_cheek_spread_spank",
    "cont_precision_anal_slow_buried_to_fast_recoil_to_pullout_ring",
    "cont_anal_beads_lubed_insertion_to_slow_pop_out_climax",
    "multi_pos_anal_doggy_to_thighs_to_pullout", "pegging_doggy_strapon",
    "pegging_missionary_legs_up", "cont_strapon_harness_buckle_to_pegging_doggy",
    "butt_plug_insertion_wink", "anal_beads_slow_pullout",
}

DP_EXPLICIT_IDS = {
    "multi_mmf_standing_sandwich_dp",
    "multi_mmf_double_vaginal_and_anal_standing_lift_carry", "multi_mmf_airtight_triple",
    "cont_mmf_dp_cowgirl_mount_to_rear_anal_entry_to_sandwich_ride",
}

REAR_EXPLICIT_IDS = {
    "reverse_cowgirl", "reverse_cowgirl_looking_into_mirror",
    "reverse_cowgirl_palms_on_his_knees_twerk",
    "cont_reverse_cowgirl_slide_in_to_squat_twerk_to_back_cum",
    "doggy_arched", "doggy_face_buried_pillow_high_arch",
    "doggy_standing_balcony_railing_night", "doggy_one_leg_propped_on_couch",
    "cont_doggy_skirt_flip_rub_to_slide_in_to_spank_climax",
    "cont_pov_doggy_waist_pull_to_hair_arch_to_ass_cum",
    "cont_anal_beads_lubed_insertion_to_slow_pop_out_climax",
    "cont_mirror_standing_kiss_neck_to_skirt_hike_rear_entry",
    "cont_rough_hairpull_doggy_to_spank_arch_to_back_cum",
    "anal_standing_bent_over_desk",
    "rough_anal_doggy_cheek_spread_spank",
    "cont_precision_anal_slow_buried_to_fast_recoil_to_pullout_ring",
    "climax_back_and_glutes_arch_cumshot", "prone_bone",
    "rough_prone_bone_wrist_pin_cheek_ripple",
    "multi_ffm_side_by_side_doggy_alternating_thrusts",
    "pegging_doggy_strapon", "rough_doggy_spank", "rough_over_desk_spank_and_hair_yank",
    "rough_reverse_cowgirl_hip_slam_ankle_grip",
    "rough_sofa_armrest_folded_over_spank_and_pound", "pov_male_doggy",
    "desk_counter_bend_over",
    "standing_mirror_vanity_doggy", "butt_plug_insertion_wink",
    "anal_beads_slow_pullout", "dildo_mirror_suction_standing_doggy_watch",
    "cont_mirror_standing_dress_hike_to_rear_entry_to_neck_grab_watch",
    "mirror_selfie_rear_arch_tease", "bdsm_leather_paddle_spank_red_glutes",
    "cont_balcony_wine_sip_to_railing_doggy_arch",
    "cont_gym_stretch_leggings_peel_to_bench_doggy",
    "cont_bed_massage_oil_to_prone_bone_climax",
    "cont_strapon_harness_buckle_to_pegging_doggy",
    "cont_couch_undress_bra_toss_to_reverse_cowgirl", "solo_prone_pillow_grinding_hump",
}

FRONT_FACING_REAR_ENTRY_EXPLICIT_IDS = {
    "anal_between_thighs_closeup", "multi_pos_anal_doggy_to_thighs_to_pullout",
    "anal_on_back_knees_up", "pegging_missionary_legs_up",
    "shower_glass_pressed_breasts", "cont_shower_wet_soap_lather_breasts_to_glass_pressed_doggy",
    "cont_shower_glass_breast_press_to_standing_rear_entry_to_arch_climax",
    "worship_wet_shower_glass_pressed_breasts_and_glutes",
    "rough_balcony_glass_pressed_breasts_pound", "side_spooning",
    "cont_spooning_thigh_lift_to_slide_in_to_neck_kiss_creampie",
    "cont_couch_spoon_to_leg_lift_to_deep_creampie", "rough_sideways_spoon_leg_lift_throttle",
    "cont_free_use_gaming_skirt_flip_to_couch_doggy_to_controller_drop_climax",
    "sixty_nine_side",
    "cont_sixty_nine_lick_to_mounted_grind_to_mouth_finish",
    "cont_spitroast_all_fours_deepthroat_and_doggy_to_dual_climax",
    "multi_mmf_couch_lap_spitroast", "multi_fff_strapon_spitroast",
    "multi_ffm_stacked_doggy_lick", "rough_doggy_hairpull",
    "rough_two_finger_mouth_hook_doggy", "rough_strapon_femdom_hairpull_pegging",
    "dildo_mirror_suction_ride",
    "bdsm_wrist_cuff_standing_mirror_control", "handjob_reverse_over_shoulder_stroke",
    "lesbian_mirror_behind_breast_cup_finger", "lesbian_sixty_nine_side_mutual_lick",
    "cont_kiss_strip_jacket_to_desk_bend_doggy",
}

OVER_SHOULDER_EXPLICIT_IDS = {
    "ass_worship_cheek_spread_pov", "worship_oiled_glute_and_sole_arch_footjob",
}

MIRROR_EXPLICIT_IDS = {
    "standing_mirror_vanity_doggy", "dildo_mirror_suction_ride",
    "dildo_mirror_suction_standing_doggy_watch", "reverse_cowgirl_looking_into_mirror",
    "cont_mirror_standing_kiss_neck_to_skirt_hike_rear_entry",
    "cont_mirror_standing_dress_hike_to_rear_entry_to_neck_grab_watch",
    "mirror_selfie_rear_arch_tease", "bdsm_wrist_cuff_standing_mirror_control",
    "lesbian_mirror_behind_breast_cup_finger", "solo_mirror_standing_spread_touch",
    "cont_gym_stretch_leggings_peel_to_bench_doggy",
}

MIRROR_CAMERA_IDS = {
    "mirror_dual_ots", "mirror_over_shoulder_eye_lock",
    "mirror_three_way_reflection", "mirror_pan_off",
    "mirror_dual_subject_eye_reflection",
}

REAR_POSE_IDS = {"dance_bed_prone_ankle_cross_sway"}
OVER_SHOULDER_POSE_IDS = {"dance_rear_arch_glute_shimmy_lookback"}

POV_MALE_EXPLICIT_IDS = {
    "pov_male_cowgirl_grind", "pov_male_doggy", "pov_male_missionary",
    "cont_pov_cowgirl_slow_hip_circles_to_fast_bounce_to_hand_milk",
    "cont_pov_doggy_waist_pull_to_hair_arch_to_ass_cum",
    "cont_femdom_boot_step_chest_to_heel_grind_to_joi_countdown",
    "ass_worship_cheek_spread_pov", "good_boy_mommy_praise_pet",
    "boot_heel_trample_pov", "thigh_scissor_crush_pov", "giantess_macro_towering_pov",
    "bdsm_under_desk_heels_worship_collar", "bdsm_face_worship_heel_chest_press",
}

POV_FEMALE_EXPLICIT_IDS = set()

ORAL_OCCUPIED_EXPLICIT_IDS = {
    "blowjob_drool_pullback", "deepthroat_to_smile_facial",
    "oral_kneeling_two_hand_base_stroke_upward_gaze",
    "oral_side_profile_throat_bulge_drool", "oral_two_girls_alternating_lick_suck",
    "pov_3quarter_topdown_deepthroat", "sixty_nine_side",
    "multi_mmf_missionary_plus_side_bj",
    "multi_mmf_cowgirl_plus_standing_facefuck", "multi_mmf_airtight_triple",
    "multi_mmf_couch_lap_spitroast", "multi_ffm_balls_lick_plus_deepthroat",
    "multi_gangbang_kneeling_circle_oral",
    "multi_gangbang_5man_standing_ring_bukkake_worship",
    "rough_throatfuck_bed_edge_upside_down",
    "rough_face_slap_spit_glaze_deepthroat",
    "rough_kneeling_collar_leash_yank_throatfuck_drool", "gloryhole_wall_oral",
    "worship_milking_table_underneath_oiled_two_hand_and_oral",
    "cont_handjob_lick_to_deepthroat_to_swallow",
    "cont_rough_sloppy_throatfuck_to_chin_grip_to_mascara_facial",
    "cont_milking_table_oil_two_hand_stroke_to_deepthroat_to_cum_milk",
    "cont_spitroast_all_fours_deepthroat_and_doggy_to_dual_climax",
    "cont_threesome_side_by_side_kiss_to_alternating_bj_to_shared_facial",
    "cont_gangbang_kneeling_double_handjob_to_alternating_throat_to_bukkake",
    "cont_under_desk_two_hand_stroke_to_deepthroat_to_lap_cowgirl",
    "cont_harem_3girl_oil_rub_to_triple_tongue_shaft_worship_to_shared_glaze",
}

CUNNILINGUS_ONLY_EXPLICIT_IDS = {
    "cunnilingus_calm",
    "cont_cunnilingus_thigh_grip_to_two_finger_gspot_to_squirt",
    "multi_fff_daisy_chain_triad_cunnilingus", "multi_ffm_missionary_cunnilingus_daisy",
}

NON_SOLO_BJ_ORAL_IDS = {
    "gloryhole_wall_oral", "sixty_nine_side",
    "cont_sixty_nine_lick_to_mounted_grind_to_mouth_finish",
    "cont_spitroast_all_fours_deepthroat_and_doggy_to_dual_climax",
    "multi_mmf_couch_lap_spitroast", "multi_fff_strapon_spitroast",
    "multi_mmf_missionary_plus_side_bj", "multi_mmf_cowgirl_plus_standing_facefuck",
    "multi_mmf_airtight_triple", "multi_ffm_balls_lick_plus_deepthroat",
    "multi_gangbang_kneeling_circle_oral",
    "multi_gangbang_5man_standing_ring_bukkake_worship",
    "cont_gangbang_kneeling_double_handjob_to_alternating_throat_to_bukkake",
    "cont_threesome_side_by_side_kiss_to_alternating_bj_to_shared_facial",
    "cont_harem_3girl_oil_rub_to_triple_tongue_shaft_worship_to_shared_glaze",
    "oral_two_girls_alternating_lick_suck",
    "worship_milking_table_underneath_oiled_two_hand_and_oral",
    "cont_milking_table_oil_two_hand_stroke_to_deepthroat_to_cum_milk",
    "cont_under_desk_two_hand_stroke_to_deepthroat_to_lap_cowgirl",
    "oral_kneeling_two_hand_base_stroke_upward_gaze",
    "oral_side_profile_throat_bulge_drool",
    "cont_handjob_lick_to_deepthroat_to_swallow",
    "rough_kneeling_collar_leash_yank_throatfuck_drool",
}

NON_VAGINAL_PARTNER_EXPLICIT_IDS = {
    "cunnilingus_calm",
    "cont_cunnilingus_thigh_grip_to_two_finger_gspot_to_squirt",
    "facesitting_slow_grind",
    "cont_facesitting_hover_tease_to_full_smother_grind",
    "handjob_double_oiled", "footjob_unison_soles",
    "cont_footjob_soles_to_tiptoe_lick_to_toes_cum", "titfuck_slow_massage",
    "titfuck_oiled_squeeze_upward_lick", "cont_oil_pour_breasts_to_massage_to_titfuck",
    "cont_kiss_unhook_to_titfuck_to_facial",
    "rough_strapon_femdom_hairpull_pegging", "bdsm_collar_leash",
    "cont_femdom_leash_crawl_to_boot_lick_to_facesit_smother",
    "cont_femdom_boot_step_chest_to_heel_grind_to_joi_countdown",
    "climax_glasses_and_tongue_facial",
    "rough_kneeling_hair_grip_facial_glaze",
    "worship_oiled_glute_and_sole_arch_footjob",
    "bdsm_under_desk_heels_worship_collar", "bdsm_face_worship_heel_chest_press",
    "bdsm_wax_play_drip_candle_arch", "bdsm_dominant_mistress_riding_chair_leash",
    "handjob_twist_and_glans_circle", "handjob_reverse_over_shoulder_stroke",
    "fingering_gspot_come_hither_squirt", "fingering_standing_wall_skirt_under",
    "footjob_heels_on_shaft_nylon_sandwich", "titjob_plus_handjob_double_pump",
    "thighjob_lubed_inner_thigh_glide", "climax_cum_in_mouth_open_show",
    "climax_breasts_and_collarbone_pearl", "climax_inner_thigh_and_pussy_glaze",
    "climax_ruined_multiple_twitch_drip", "climax_double_partner_simultaneous_glaze",
    "climax_creampie_gravity_drip_spread", "cont_strapon_harness_buckle_to_pegging_doggy",
}

NON_VOCAL_DEFAULT_EXPLICIT_IDS = (
    ANAL_EXPLICIT_IDS
    | {
        "reverse_cowgirl", "reverse_cowgirl_looking_into_mirror",
        "reverse_cowgirl_palms_on_his_knees_twerk",
        "doggy_arched", "doggy_face_buried_pillow_high_arch",
        "doggy_standing_balcony_railing_night", "doggy_one_leg_propped_on_couch",
        "prone_bone",
        "sixty_nine_side",
        "multi_pos_kiss_undress_to_missionary",
        "multi_pos_cowgirl_to_reverse_to_creampie",
        "multi_pos_lesbian_kiss_to_cunnilingus_to_trib", "rough_doggy_spank",
        "rough_doggy_hairpull", "pov_male_cowgirl_grind", "pov_male_doggy",
        "pov_male_missionary",
        "blowjob_drool_pullback", "deepthroat_to_smile_facial",
        "oral_kneeling_two_hand_base_stroke_upward_gaze",
        "oral_side_profile_throat_bulge_drool", "oral_two_girls_alternating_lick_suck",
        "titfuck_slow_massage", "titfuck_oiled_squeeze_upward_lick",
        "climax_pullout_creampie",
        "climax_internal_creampie_drip_closeup", "climax_back_and_glutes_arch_cumshot",
        "climax_belly_and_navel_missionary_finish", "climax_glasses_and_tongue_facial",
        "footjob_unison_soles", "cunnilingus_calm",
        "facesitting_slow_grind",
        "cont_kiss_unhook_to_titfuck_to_facial",
        "cont_handjob_lick_to_deepthroat_to_swallow",
        "cont_panties_aside_rub_to_cowgirl_sink_to_grind",
        "cont_cowgirl_upright_bounce_to_lean_in_kiss_to_creampie",
        "cont_doggy_skirt_flip_rub_to_slide_in_to_spank_climax",
        "cont_reverse_cowgirl_slide_in_to_squat_twerk_to_back_cum",
        "cont_missionary_panties_peel_to_legs_up_to_belly_cum",
        "cont_spooning_thigh_lift_to_slide_in_to_neck_kiss_creampie",
        "cont_standing_wall_leg_hitch_to_thrusts_to_creampie_drip",
        "cont_sixty_nine_lick_to_mounted_grind_to_mouth_finish",
        "cont_solo_dress_unzip_to_fingers_to_squirt_arch",
        "cont_oil_pour_breasts_to_massage_to_titfuck",
        "cont_footjob_soles_to_tiptoe_lick_to_toes_cum",
        "cont_cunnilingus_thigh_grip_to_two_finger_gspot_to_squirt",
        "cont_facesitting_hover_tease_to_full_smother_grind",
        "cont_mirror_standing_kiss_neck_to_skirt_hike_rear_entry",
        "cont_desk_lean_back_panties_hook_to_standing_missionary",
        "cont_shower_wet_soap_lather_breasts_to_glass_pressed_doggy",
        "cont_pov_cowgirl_slow_hip_circles_to_fast_bounce_to_hand_milk",
        "cont_pov_doggy_waist_pull_to_hair_arch_to_ass_cum",
        "cont_lesbian_kiss_bra_peel_to_breast_suckle_to_thigh_rub",
        "cont_lesbian_double_dildo_insert_to_synchronized_ride",
        "cont_dildo_suction_mount_mirror_to_deep_squat_ride_climax",
        "cont_anal_beads_lubed_insertion_to_slow_pop_out_climax",
        "cont_pantyhose_rip_crotch_seam_to_missionary_slide_in",
        "cont_mating_press_legs_fold_to_ankles_locked_to_creampie",
        "cont_threesome_side_by_side_kiss_to_alternating_bj_to_shared_facial",
        "cont_spitroast_all_fours_deepthroat_and_doggy_to_dual_climax",
        "cont_rough_panties_rip_to_mating_press_to_pinned_creampie",
        "cont_rough_hairpull_doggy_to_spank_arch_to_back_cum",
        "cont_rough_sloppy_throatfuck_to_chin_grip_to_mascara_facial",
        "cont_mmf_dp_cowgirl_mount_to_rear_anal_entry_to_sandwich_ride",
        "cont_ffm_cowgirl_ride_to_partner_kiss_breast_suckle_to_shared_finish",
        "cont_gangbang_kneeling_double_handjob_to_alternating_throat_to_bukkake",
        "multi_mmf_standing_sandwich_dp", "multi_mmf_missionary_plus_side_bj",
        "multi_mmf_cowgirl_plus_standing_facefuck",
        "multi_mmf_double_handjob_double_facial", "multi_mmf_airtight_triple",
        "multi_mmf_couch_lap_spitroast", "multi_ffm_stacked_doggy_lick",
        "multi_ffm_face_sit_plus_cowgirl", "multi_ffm_balls_lick_plus_deepthroat",
        "multi_ffm_cowgirl_assisted_hips", "multi_ffm_kissing_over_cum_swap",
        "multi_ffm_missionary_cunnilingus_daisy", "multi_ffm_double_footjob_worship",
        "multi_fff_lesbian_trio_worship", "multi_fff_strapon_spitroast",
        "multi_gangbang_kneeling_circle_oral", "multi_gangbang_pinned_limbs_train",
        "multi_reverse_gangbang_3girls_1guy", "multi_orgy_foursome_side_by_side_swap",
        "rough_mating_press_ankles_pinned_mattress",
        "rough_prone_bone_wrist_pin_cheek_ripple",
        "rough_throatfuck_bed_edge_upside_down",
        "rough_standing_wall_pin_leg_hook_pound",
        "rough_choke_collarbone_cowgirl_lean_back",
        "rough_jackhammer_missionary_under_thigh_hook",
        "rough_over_desk_spank_and_hair_yank", "rough_face_slap_spit_glaze_deepthroat",
        "rough_nelson_full_nelson_standing_pound",
        "rough_piledriver_folded_vertical_slam",
        "rough_reverse_cowgirl_hip_slam_ankle_grip",
        "rough_sideways_spoon_leg_lift_throttle",
        "rough_kneeling_hair_grip_facial_glaze", "rough_two_finger_mouth_hook_doggy",
        "rough_panties_ripped_off_pinned_entry",
        "rough_counter_edge_legs_spread_wide_hammer",
        "rough_squirt_gush_overstimulation_pin",
        "rough_strapon_femdom_hairpull_pegging",
        "rough_balcony_glass_pressed_breasts_pound",
        "cont_under_desk_two_hand_stroke_to_deepthroat_to_lap_cowgirl",
        "cont_shower_glass_breast_press_to_standing_rear_entry_to_arch_climax",
        "cont_mirror_standing_dress_hike_to_rear_entry_to_neck_grab_watch",
        "cont_femdom_leash_crawl_to_boot_lick_to_facesit_smother",
        "cont_milking_table_oil_two_hand_stroke_to_deepthroat_to_cum_milk",
        "cont_harem_3girl_oil_rub_to_triple_tongue_shaft_worship_to_shared_glaze",
        "cont_free_use_gaming_skirt_flip_to_couch_doggy_to_controller_drop_climax",
        "cont_blindfold_ice_nipple_trace_to_legs_up_missionary_to_creampie",
        "multi_harem_4to9_girls_king_bed_swarm_worship",
        "multi_gangbang_5man_standing_ring_bukkake_worship",
        "multi_ffm_stacked_cowgirl_plus_standing_behind_tit_grab",
        "multi_mmf_double_vaginal_and_anal_standing_lift_carry",
        "multi_fff_daisy_chain_triad_cunnilingus",
        "multi_ffm_side_by_side_doggy_alternating_thrusts",
        "rough_standing_single_leg_hoist_wall_slam",
        "rough_bed_corner_ankle_shackle_spreader_bar_pound",
        "rough_kneeling_collar_leash_yank_throatfuck_drool",
        "rough_sofa_armrest_folded_over_spank_and_pound",
        "worship_milking_table_underneath_oiled_two_hand_and_oral",
        "worship_wet_shower_glass_pressed_breasts_and_glutes",
        "worship_oiled_glute_and_sole_arch_footjob",
        "worship_whipped_cream_honey_breast_drip_lick",
        "lesbian_standing_shower_breast_press_thigh_ride",
        "lesbian_facesit_reverse_69_spank",
        "dildo_mirror_suction_standing_doggy_watch",
        "dildo_sybian_saddle_straddle_hands_behind_head",
        "cont_couch_spoon_to_leg_lift_to_deep_creampie",
        "cont_bathtub_soap_slide_to_straddle_ride",
        "mirror_selfie_rear_arch_tease", "bdsm_shibari_chest_harness_wall_tie",
        "bdsm_leather_paddle_spank_red_glutes",
        "bdsm_spreader_bar_ankle_cuff_missionary",
        "bdsm_silk_blindfold_sensory_feather_tease",
        "bdsm_wrist_cuff_standing_mirror_control",
        "bdsm_wax_play_drip_candle_arch", "handjob_twist_and_glans_circle",
        "handjob_reverse_over_shoulder_stroke", "fingering_gspot_come_hither_squirt",
        "fingering_standing_wall_skirt_under", "footjob_heels_on_shaft_nylon_sandwich",
        "titjob_plus_handjob_double_pump", "thighjob_lubed_inner_thigh_glide",
        "lesbian_sixty_nine_side_mutual_lick",
        "lesbian_wall_pinned_kiss_to_fingering",
        "lesbian_cunnilingus_thighs_over_shoulders",
        "lesbian_breast_worship_oiled_grind",
        "lesbian_mirror_behind_breast_cup_finger", "lesbian_strapon_cowgirl_eye_lock",
        "lesbian_foot_and_pussy_worship_duo", "lesbian_magic_wand_assisted_cunnilingus",
        "solo_mirror_standing_spread_touch", "solo_shower_handheld_spray_climax",
        "solo_prone_pillow_grinding_hump", "solo_stocking_rip_thigh_spread_touch",
        "solo_ahegao_overstimulation_tremor", "solo_glass_dildo_clear_view_ride",
        "solo_nipple_ice_cube_to_clit_rub", "climax_cum_in_mouth_open_show",
        "climax_breasts_and_collarbone_pearl", "climax_inner_thigh_and_pussy_glaze",
        "climax_double_partner_simultaneous_glaze",
        "climax_creampie_gravity_drip_spread", "cont_kiss_strip_jacket_to_desk_bend_doggy",
        "cont_bed_massage_oil_to_prone_bone_climax",
        "cont_car_backseat_makeout_to_panties_aside_ride",
        "cont_balcony_wine_sip_to_railing_doggy_arch",
        "cont_pool_edge_climb_out_to_wet_missionary",
        "cont_kitchen_apron_cooking_to_counter_lift",
        "cont_gym_stretch_leggings_peel_to_bench_doggy",
        "cont_strapon_harness_buckle_to_pegging_doggy",
        "cont_lesbian_bathtub_foam_kiss_to_scissoring",
        "cont_couch_undress_bra_toss_to_reverse_cowgirl",
        "multi_pos_gym_stretch_to_shower_to_bed",
        "multi_pos_yacht_deck_to_cabin_oral_to_sunset_cowgirl",
        "multi_pos_office_under_desk_to_chair_spin_to_glass_wall",
        "multi_pos_lesbian_sofa_makeout_to_69_to_double_dildo",
    }
)


def strip_d_examples(rule_text: str) -> str:
    out = re.sub(r"\s*\(`?[^()]*?<d>.*?</d>`?\)", "", rule_text or "", flags=re.S)
    out = re.sub(r"\s*\(DIALOGUE\)\s*[^<]*<d>.*?</d>\s*\.?", "", out, flags=re.S | re.I)
    out = re.sub(r"\s*`?<d>.*?</d>`?", "", out, flags=re.S)
    out = re.sub(r"\s*Sample Dialogue Lines \(adapt to the scene\):.*$", "", out, flags=re.S)
    return re.sub(r"\s{2,}", " ", out).strip()


def is_sexual(brief: str, explicit_id: str = "", wardrobe_id: str = "", fetish_id: str = "") -> bool:
    eids = _cat.parse_multi_ids(explicit_id)
    wids = _cat.parse_multi_ids(wardrobe_id)
    fids = _cat.parse_multi_ids(fetish_id)
    if eids or fids or any(w.startswith(("nude_", "fetish_", "partial_")) for w in wids):
        return True
    return bool(_SEX_RX.search(brief or ""))


def is_pegging_scene(brief: str, explicit_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if any(eid in ("pegging_doggy_strapon", "pegging_missionary_legs_up", "rough_strapon_femdom_hairpull_pegging", "cont_strapon_harness_buckle_to_pegging_doggy") for eid in eids):
        return True
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    return bool(re.search(r"\b(?:pegging|pegs?\s+him|strap[- ]?on\s+(?:in(?:to)?|inside)\s+(?:his|the\s+man's)\s+anus)\b", combined, re.I))


def is_non_vaginal_partner_scene(explicit_id: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    return bool(eids) and all(eid in NON_VAGINAL_PARTNER_EXPLICIT_IDS for eid in eids)


def is_anal(brief: str, explicit_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if any(eid in DP_EXPLICIT_IDS for eid in eids):
        return False
    if any(eid in ANAL_EXPLICIT_IDS or eid.startswith(("anal_", "pegging_", "butt_plug_", "cont_precision_anal_")) for eid in eids):
        return True
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    if re.search(r"\b(?:double[- ]penetration|triple[- ]penetration|airtight|standing\s+sandwich|\bdp\s+sandwich)\b", combined, re.I):
        return False
    return bool(_ANAL_RX.search(combined))


def is_rear_facing(brief: str, explicit_id: str = "", plan: str = "", plan_hint: str = "", camera_id: str = "", pose_id: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    cids = [x.lower() for x in _cat.parse_multi_ids(camera_id)]
    pids = [x.lower() for x in _cat.parse_multi_ids(pose_id)]
    if any(e in FRONT_FACING_REAR_ENTRY_EXPLICIT_IDS for e in eids):
        return False
    if eids:
        non_climax_eids = [e for e in eids if not e.startswith("climax_")]
        has_rear_pick = any(e in REAR_EXPLICIT_IDS for e in eids)
        has_front_climax = any(e in ("climax_facial_f04", "climax_titjob_to_face", "climax_footjob_toes") for e in eids)
        if has_rear_pick and len(non_climax_eids) == len([e for e in non_climax_eids if e in REAR_EXPLICIT_IDS]) and not has_front_climax:
            return True
        if len(eids) > 1 and not all(e in REAR_EXPLICIT_IDS or e == "climax_pullout_creampie" for e in eids):
            return False
    if pids and all(p in REAR_POSE_IDS for p in pids) and not any(e not in REAR_EXPLICIT_IDS for e in eids):
        return True
    if cids and all(c in ("track_back", "follow_shot", "mirror_dual_ots", "mirror_over_shoulder_eye_lock", "mirror_three_way_reflection") for c in cids):
        return True
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    if _FRONT_OR_MULTI_POS_RX.search(combined):
        return False
    if _REAR_FACING_RX.search(combined) and not _OVER_SHOULDER_RX.search(combined):
        return True
    if is_anal(brief, explicit_id=explicit_id, plan=plan, plan_hint=plan_hint) and not re.search(
        r"\b(?:on\s+(?:her|his)\s+back|missionary|legs?\s+lifted\s+high|knees?\s+pulled\s+to\s+her\s+chest|between\s+(?:her|<Subject\s+1>[^']*)\s+(?:spread\s+)?thighs|front[- ]view)\b",
        combined,
        re.I,
    ):
        return True
    return False


def is_multi_position_scene(brief: str, plan: str = "", plan_hint: str = "", explicit_id: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if len(eids) >= 2:
        return True
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    return bool(_REAR_FACING_RX.search(combined) and _FRONT_OR_MULTI_POS_RX.search(combined))


def is_over_shoulder(brief: str, explicit_id: str = "", camera_id: str = "", plan: str = "", plan_hint: str = "", pose_id: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    cids = [x.lower() for x in _cat.parse_multi_ids(camera_id)]
    pids = [x.lower() for x in _cat.parse_multi_ids(pose_id)]
    if any(eid in OVER_SHOULDER_EXPLICIT_IDS for eid in eids) or any(cid in ("selfie_shoulder", "rear_thigh_to_back") for cid in cids) or any(pid in OVER_SHOULDER_POSE_IDS for pid in pids):
        return True
    return bool(_OVER_SHOULDER_RX.search(f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"))


def is_mouth_occupied(brief: str, explicit_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if eids and all(eid in CUNNILINGUS_ONLY_EXPLICIT_IDS for eid in eids):
        return False
    if any(eid.startswith("multi_pos_") for eid in eids) or "bdsm_ballgag_tease" in eids:
        return False
    if eids and all(eid in ORAL_OCCUPIED_EXPLICIT_IDS for eid in eids):
        return True
    if len(eids) == 1:
        if eids[0] in ORAL_OCCUPIED_EXPLICIT_IDS:
            return True
        if eids[0] in CUNNILINGUS_ONLY_EXPLICIT_IDS:
            return False
        opt = _cat.dial_option("explicit", eids[0])
        if opt and _ORAL_OCCUPIED_RX.search(f"{opt.get('label', '')} {opt.get('rule', '')}"):
            return True
    return bool(_ORAL_OCCUPIED_RX.search(f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"))


def uses_solo_blowjob_template(brief: str, explicit_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    if not is_mouth_occupied(brief, explicit_id=explicit_id, plan=plan, plan_hint=plan_hint):
        return False
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if any(
        eid in NON_SOLO_BJ_ORAL_IDS
        or eid.startswith(("multi_mmf_", "multi_ffm_", "multi_fff_", "multi_gangbang_", "multi_pos_", "cont_spitroast_", "cont_threesome_", "cont_gangbang_", "cont_harem_", "cont_mmf_", "cont_ffm_"))
        for eid in eids
    ):
        return False
    combined = f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"
    if re.search(r"\b(?:gloryhole|milking\s+table|69|sixty[- ]?nine|spitroast|dildo|threesome|gangbang)\b", combined, re.I):
        return False
    return True


def is_mirror_scene_active(explicit_id: str = "", camera_id: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    cids = [x.lower() for x in _cat.parse_multi_ids(camera_id)]
    return any(x in MIRROR_EXPLICIT_IDS for x in eids) or any(x in MIRROR_CAMERA_IDS for x in cids)


def resolve_pov_mode(brief: str, flavors: dict | None = None, plan: str = "") -> str:
    flavors = flavors or {}
    pov_val = str(flavors.get("pov") or "off").strip().lower()
    if pov_val in ("male", "female", "on"):
        return pov_val
    eids = [x.lower() for x in _cat.parse_multi_ids(flavors.get("explicit"))]
    if eids and all(eid in POV_FEMALE_EXPLICIT_IDS for eid in eids):
        return "female"
    if eids and all(eid in POV_MALE_EXPLICIT_IDS for eid in eids):
        return "male"
    if len(eids) == 1:
        if eids[0] in POV_FEMALE_EXPLICIT_IDS:
            return "female"
        if eids[0] in POV_MALE_EXPLICIT_IDS:
            return "male"
    combined = f"{brief or ''}\n{plan or ''}\n{flavors.get('plan_hint') or ''}"
    if re.search(r"\b(?:multi[- ]?angle\w*|multiple\s+angles|orbit\w*|arcing|finish\s+with\s+a\s+pov|end\s+with\s+a\s+pov|pov\s+or\s+3/4)\b", combined, re.I):
        return "off"
    if re.search(r"\bfemale\s+pov\b", combined, re.I):
        return "female"
    if re.search(r"\bmale\s+pov\b", combined, re.I):
        return "male"
    if re.search(r"\b(?:pov|first[- ]person\s+(?:view|camera|perspective|eyes))\b", combined, re.I):
        return "on"
    return "off"


def is_combat(brief: str, combat_id: str = "", wardrobe_id: str = "", fx_id: str = "") -> bool:
    cids = _cat.parse_multi_ids(combat_id)
    wids = _cat.parse_multi_ids(wardrobe_id)
    fids = _cat.parse_multi_ids(fx_id)
    if cids or any(w.startswith("action_") for w in wids) or any(f.startswith("vfx_") for f in fids):
        return True
    return bool(_COMBAT_RX.search(brief or ""))


def is_progressive_or_casual_setup(brief: str = "", explicit_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    if any(eid.startswith(("playful_", "undress_", "dance_", "joi_")) for eid in eids):
        return True
    return bool(_PROGRESSIVE_SETUP_RX.search(f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}"))


def is_continuous_transition_scene(brief: str = "", explicit_id: str = "", wardrobe_id: str = "", plan: str = "", plan_hint: str = "") -> bool:
    eids = [x.lower() for x in _cat.parse_multi_ids(explicit_id)]
    wids = [x.lower() for x in _cat.parse_multi_ids(wardrobe_id)]
    if any(eid.startswith("cont_") for eid in eids) or any(w.startswith("partial_") for w in wids) or len(wids) >= 2:
        return True
    return bool(re.search(r"\b(?:pulled?\s+aside|peel\w*\s+off|hiked\s+up|undress\w*|transition\w*\s+into|escalat\w*\s+into)\b", f"{brief or ''}\n{plan or ''}\n{plan_hint or ''}", re.I))


def playbook_matches(brief: str, explicit_id: str = "") -> list[dict]:
    if not brief and not explicit_id:
        return []
    text = f"{brief or ''} {explicit_id or ''}".lower()
    pb = _cat._load_json("playbook.json")
    hits = []
    for k, entry in pb.items():
        if re.search(rf"\b{re.escape(k.replace('_', '[ _-]?'))}\b", text, re.I):
            hits.append(entry)
    return hits[:2]


def format_playbook_directive(entry: dict, *, has_camera_or_explicit: bool = False, has_subject_or_wardrobe: bool = False) -> str:
    title = entry.get("title") or "Specialty"
    bits = []
    if entry.get("shooting") and not has_camera_or_explicit:
        bits.append(f"Framing: {entry['shooting']}")
    if entry.get("styling") and not has_subject_or_wardrobe:
        bits.append(f"Styling: {entry['styling']}")
    if entry.get("vocab"):
        bits.append(f"Textures/Verbs: {entry['vocab']}")
    if entry.get("phrases"):
        bits.append(f"Line vibe: {entry['phrases'][0]}")
    return f"PLAYBOOK MODULE ({title}): " + " ".join(bits)


def dance_vocab_directive(brief: str) -> str:
    if not brief or not re.search(r"\b(?:dance|dancing|choreo\w*|groove|twerk|hip\s*sway|body\s*wave|gravure|idol)\b", brief, re.I):
        return ""
    dv = _cat.dance_vocab_doc()
    pr = dv.get("pacing_rules") or {}
    return (
        "SANDTIE DANCE VOCABULARY: "
        f"{pr.get('motion_language', '')} {pr.get('anatomy_order', '')} {pr.get('orientation_lock', '')}"
    ).strip()


def knowledge_primer(has_camera_pick: bool = False, is_pov: bool = False) -> str:
    kd = _cat.knowledge_doc().get("know") or {}
    parts = [kd.get("head", "")]
    if not has_camera_pick and not is_pov:
        parts.extend(kd.get("camera") or [])
    parts.extend(kd.get("picture") or [])
    if kd.get("write"):
        parts.append(kd["write"])
    return "\n".join(p for p in parts if p)


def knowledge_terms_in_brief(brief: str, picked_refs: set[str] | None = None, is_multi_shot: bool = False) -> list[tuple[str, str, dict]]:
    if not brief:
        return []
    picked_refs = picked_refs or set()
    terms = _cat.knowledge_doc().get("terms") or []
    out = []
    seen = set()
    for pat, ref in terms:
        if ref in seen or ref in picked_refs:
            continue
        if is_multi_shot and ref.startswith("camera:"):
            continue
        try:
            m = re.search(rf"(?:{pat})", brief, re.I)
        except re.error:
            continue
        if not m:
            continue
        cid, _, oid = ref.partition(":")
        opt = _cat.dial_option(cid, oid)
        if opt and opt.get("rule"):
            seen.add(ref)
            out.append((m.group(0), ref, opt))
    return out
