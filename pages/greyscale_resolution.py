import math
import random

import streamlit as st

from utils.test_config import load_test_config
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Contrast Sensitivity Test",
    layout="wide",
)

render_page_header(
    "Contrast Sensitivity Test (Pelli-Style)",
    "Single-letter Pelli-style progression with fixed log contrast steps.",
    "greyscale",
)

render_instructions(
    "How To Run This Test",
    (
        "This version follows a strict Pelli-style progression (no 3AFC). "
        "One letter is shown at a time while contrast decreases by a fixed log step."
    ),
    [
        "Keep viewing distance and screen brightness fixed.",
        "At each level, report whether you can still identify the letter.",
        "Threshold is estimated from the last contrast level you could identify.",
    ],
)

config = load_test_config()
cfg = config["greyscale"]
letters = cfg["letters"]
row_count = int(cfg["preview"]["rows"])
log_step = float(cfg["preview"]["log_contrast_step"])


def student_build_preview_triplets(
    *,
    letters_pool: str,
    rows: int,
    seed: int,
) -> list[str]:
    """Generate a deterministic preview chart."""
    if rows <= 0 or not letters_pool:
        return []
    rng = random.Random(seed)
    return ["".join(rng.choices(letters_pool, k=3)) for _ in range(rows)]


def student_compute_contrast_levels(*, rows: int, step_log10: float) -> list[float]:
    """Return a log-spaced contrast schedule in percent."""
    if rows <= 0:
        return []
    return [100 * (10 ** (-(row_index * step_log10))) for row_index in range(rows)]


def student_advance_contrast_state(
    *,
    trial_index: int,
    response_yes: bool,
    total_levels: int,
) -> tuple[int, bool]:
    """Advance the trial index or finish the run."""
    if not response_yes:
        return (max(0, min(trial_index, total_levels - 1)), True)
    next_index = trial_index + 1
    if next_index >= total_levels:
        return (total_levels - 1, True)
    return (next_index, False)


def student_compute_log_contrast_sensitivity(threshold_percent: float) -> float:
    """Convert percent threshold to log contrast sensitivity."""
    if threshold_percent <= 0:
        return 0.0
    return math.log10(1 / (threshold_percent / 100.0))


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_build_preview_triplets`.\n"
        "- Implement `student_compute_contrast_levels`.\n"
        "- Implement `student_advance_contrast_state`.\n"
        "- Implement `student_compute_log_contrast_sensitivity`.\n"
        "- Keep function signatures unchanged."
    )

st.caption(
    "How these functions connect: generate deterministic preview rows -> compute contrast schedule "
    "-> advance trial state based on responses -> compute final log contrast sensitivity."
)

try:
    contrast_levels_pct = student_compute_contrast_levels(rows=row_count, step_log10=log_step)
    preview_triplets = student_build_preview_triplets(
        letters_pool=letters,
        rows=row_count,
        seed=int(cfg["preview"]["seed"]),
    )
    _ = student_advance_contrast_state(trial_index=0, response_yes=True, total_levels=row_count)
except NotImplementedError as error:
    st.error(str(error))
    st.info("This page is locked until the student TODO functions are implemented.")
    st.stop()

if len(contrast_levels_pct) != row_count or len(preview_triplets) != row_count:
    st.error("Student function outputs are invalid. Check list lengths and return values.")
    st.stop()


def draw_letter_card(letter: str, contrast_pct: float) -> str:
    bg = int(cfg["background_rgb"])
    contrast = max(0.0, min(1.0, contrast_pct / 100.0))
    fg = int(max(0, min(255, bg * (1.0 - contrast))))
    return (
        "<div style='background:rgb(255,255,255); border:1px solid #d3d3d3; border-radius:10px; "
        "padding:1rem 0.5rem; text-align:center;'>"
        f"<div style='font-size:3rem; font-weight:700; color:rgb({fg},{fg},{fg}); "
        "font-family:serif;'>"
        f"{letter}</div></div>"
    )


if "greyscale_pelli_index" not in st.session_state:
    st.session_state["greyscale_pelli_index"] = 0
if "greyscale_pelli_letter" not in st.session_state:
    st.session_state["greyscale_pelli_letter"] = random.choice(letters)
if "greyscale_pelli_history" not in st.session_state:
    st.session_state["greyscale_pelli_history"] = []
if "greyscale_pelli_finished" not in st.session_state:
    st.session_state["greyscale_pelli_finished"] = False
if "greyscale_pelli_threshold_pct" not in st.session_state:
    st.session_state["greyscale_pelli_threshold_pct"] = contrast_levels_pct[0]

with st.container(border=True):
    st.subheader("Pelli-Style Contrast Chart Preview")
    st.caption("Letter groups are shown from high contrast (top) to low contrast (bottom).")
    bg = int(cfg["background_rgb"])
    html_rows = []
    for row_idx in range(row_count):
        contrast = 10 ** (-(row_idx * log_step))
        fg = int(max(0, min(255, bg * (1.0 - contrast))))
        triplet = preview_triplets[row_idx]
        html_rows.append(
            f"<div style='letter-spacing:0.45rem; font-size:1.9rem; font-weight:700; "
            f"color:rgb({fg},{fg},{fg}); margin:0.2rem 0;'>{triplet}</div>"
        )
    st.markdown(
        (
            "<div style='background:rgb(255,255,255); border:1px solid #d3d3d3; "
            "border-radius:10px; padding:1rem; text-align:center; font-family:serif;'>"
            + "".join(html_rows)
            + "</div>"
        ),
        unsafe_allow_html=True,
    )

trial_index = int(st.session_state["greyscale_pelli_index"])
finished = bool(st.session_state["greyscale_pelli_finished"])
current_contrast_pct = contrast_levels_pct[min(trial_index, len(contrast_levels_pct) - 1)]
current_letter = st.session_state["greyscale_pelli_letter"]

with st.container(border=True):
    st.subheader("Single-Letter Trial")
    st.caption(f"Current level: {trial_index + 1}/{len(contrast_levels_pct)}")
    st.caption(f"Current contrast: {current_contrast_pct:.2f}%")
    st.markdown(draw_letter_card(current_letter, current_contrast_pct), unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Respond")
    response = st.radio(
        "Can you identify this letter?",
        ["Yes", "No"],
        horizontal=True,
        key="greyscale_pelli_response",
    )
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=finished,
    )
    if submitted and not finished:
        # LAB NOTE: This block drives the Pelli-style staircase progression.
        # Optional extensions can add stricter scoring rules (for example typed-letter checks).
        can_identify = response == "Yes"
        st.session_state["greyscale_pelli_history"].append(
            {
                "Level": trial_index + 1,
                "Letter": current_letter,
                "Contrast (%)": round(current_contrast_pct, 2),
                "Identified": "Yes" if can_identify else "No",
            }
        )

        next_index, next_finished = student_advance_contrast_state(
            trial_index=trial_index,
            response_yes=can_identify,
            total_levels=len(contrast_levels_pct),
        )

        if can_identify:
            st.session_state["greyscale_pelli_threshold_pct"] = current_contrast_pct
        else:
            if trial_index > 0:
                st.session_state["greyscale_pelli_threshold_pct"] = contrast_levels_pct[
                    trial_index - 1
                ]
        st.session_state["greyscale_pelli_index"] = min(next_index, len(contrast_levels_pct) - 1)
        st.session_state["greyscale_pelli_finished"] = bool(next_finished)
        if not next_finished:
            st.session_state["greyscale_pelli_letter"] = random.choice(letters)
        st.rerun()

threshold_pct = float(st.session_state["greyscale_pelli_threshold_pct"])
log_cs = student_compute_log_contrast_sensitivity(threshold_pct)
bit_depth_est = max(1, math.ceil(math.log2(100.0 / max(threshold_pct, 1e-6))))

with st.container(border=True):
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Contrast Threshold (%)", f"{threshold_pct:.2f}")
    col_2.metric("Estimated log Contrast Sensitivity", f"{log_cs:.2f}")
    st.metric("Estimated Bit Depth (per channel)", bit_depth_est)
    if finished:
        st.success("Pelli-style run complete.")

with st.container(border=True):
    st.subheader("Trial Log")
    history = st.session_state["greyscale_pelli_history"]
    if history:
        st.dataframe(history, width="stretch", hide_index=True)
    else:
        st.caption("No responses yet.")

with st.container(border=True):
    st.subheader("Test Controls")

    if st.button("Restart Test", width="stretch"):
        for key in [
            "greyscale_pelli_index",
            "greyscale_pelli_letter",
            "greyscale_pelli_history",
            "greyscale_pelli_finished",
            "greyscale_pelli_threshold_pct",
            "greyscale_pelli_response",
        ]:
            st.session_state.pop(key, None)
        st.rerun()
