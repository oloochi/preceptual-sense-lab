import math
import random

import streamlit as st

from utils.test_config import load_test_config
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Visual Resolution (Tumbling E Staircase)",
    layout="wide",
)

render_page_header(
    "Visual Resolution Test (Tumbling E Staircase)",
    "Single-optotype adaptive staircase with error logging and MAR tracking.",
    "size",
)

render_instructions(
    "How To Run This Test",
    (
        "You will see one Tumbling E at a time. Choose its orientation. "
        "Correct responses make the next E smaller; incorrect responses make it larger. "
        "The smallest rendered optotype is 4 px, so if that remains easy, increase "
        "viewing distance."
    ),
    [
        "Keep viewing distance fixed during the run.",
        "Answer every trial with one of: Up, Down, Left, Right.",
        "If the smallest E is still obvious, move farther from the display and restart.",
    ],
)

config = load_test_config()
cfg = config["tumbling_e"]
SIZE_LEVELS_PX = [int(v) for v in cfg["size_levels_px"]]
ORIENTATIONS = ["Up", "Down", "Left", "Right"]


def student_next_size_index(*, current_index: int, is_correct: bool, max_index: int) -> int:
    """Compute the next adaptive size index for the staircase."""
    if is_correct:
        next_index = current_index + 1
    else:
        next_index = current_index - 1
        
    return max(0, min(next_index, max_index))


def student_build_trial_log_row(
    *,
    trial_no: int,
    size_px: int,
    mar_arcmin: float,
    correct_orientation: str,
    response: str,
) -> dict[str, str | int | float]:
    """Build a complete, standardized row for the trial log table."""
    return {
        "Trial": trial_no,
        "Size (px)": size_px,
        "MAR (arcmin)": round(mar_arcmin, 2),
        "Target": correct_orientation,
        "Response": response,
        "Correct": "Yes" if response == correct_orientation else "No",
    }


def student_validate_screen_geometry(
    *, distance_cm: float, screen_width_mm: float, screen_width_px: int
) -> bool:
    """Validate whether screen-geometry inputs are usable."""
    return distance_cm > 0.0 and screen_width_mm > 0.0 and screen_width_px > 0


def student_compute_mar_arcmin(size_px: int, mm_per_px: float, distance_cm: float) -> float:
    """Compute MAR (minimum angle of resolution) in arcminutes."""
    if distance_cm <= 0:
        return 0.0
        
    # The Tumbling E grid is 5x5, so the resolution gap detail (MAR) is 1/5th the total size
    total_size_mm = size_px * mm_per_px
    detail_mm = total_size_mm / 5.0
    distance_mm = distance_cm * 10.0
    
    # Small-angle geometry: angle in radians is approx (detail / distance)
    angle_radians = detail_mm / distance_mm
    
    # Convert radians to degrees, then to arcminutes
    return (angle_radians * 180.0 / math.pi) * 60.0


def student_format_trial_log_row(
    *,
    trial_no: int,
    size_px: int,
    mar_arcmin: float,
    correct_orientation: str,
    response: str,
) -> dict[str, str | int | float]:
    """Wrapper/formatter for a standardized trial-log row."""
    return student_build_trial_log_row(
        trial_no=trial_no,
        size_px=size_px,
        mar_arcmin=mar_arcmin,
        correct_orientation=correct_orientation,
        response=response,
    )


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_next_size_index`.\n"
        "- Implement `student_build_trial_log_row`.\n"
        "- Implement `student_validate_screen_geometry`.\n"
        "- Implement `student_compute_mar_arcmin`.\n"
        "- Implement `student_format_trial_log_row`.\n"
        "- Keep existing table column names."
    )

st.caption(
    "How these functions connect: validate screen geometry -> convert size to MAR -> "
    "log each trial consistently -> update index for next adaptive trial."
)

try:
    _ = student_next_size_index(current_index=0, is_correct=True, max_index=len(SIZE_LEVELS_PX) - 1)
    _ = student_build_trial_log_row(
        trial_no=1,
        size_px=SIZE_LEVELS_PX[0],
        mar_arcmin=1.0,
        correct_orientation="Up",
        response="Up",
    )
except NotImplementedError as error:
    st.error(str(error))
    st.info("This page is locked until the student TODO functions are implemented.")
    st.stop()

if not student_validate_screen_geometry(
    distance_cm=float(cfg["setup"]["distance_cm"]["default"]),
    screen_width_mm=float(cfg["setup"]["screen_width_mm"]["default"]),
    screen_width_px=int(cfg["setup"]["screen_width_px"]["default"]),
):
    st.error("Geometry validation function returned invalid result.")
    st.stop()


def init_tumbling_state() -> dict:
    key = "tumbling_e_state"
    if key not in st.session_state:
        st.session_state[key] = {
            "size_index": 0,
            "trial_orientation": random.choice(ORIENTATIONS),
            "history": [],
        }
    return st.session_state[key]


def next_orientation(previous: str) -> str:
    candidate = random.choice(ORIENTATIONS)
    while candidate == previous:
        candidate = random.choice(ORIENTATIONS)
    return candidate


def e_symbol(size_px: int, orientation: str) -> str:
    rotation = {"Right": 0, "Down": 90, "Left": 180, "Up": 270}[orientation]
    return (
        "<div style='display:flex; justify-content:center; align-items:center; "
        "background:#ffffff; border:1px solid #d0d0d0; border-radius:8px; padding:0.3rem;'>"
        # LAB NOTE: SVG geometry enforces t=d (stroke thickness equals spacing) on a 5x5 grid.
        f"<svg width='{size_px}' height='{size_px}' viewBox='0 0 5 5' "
        "xmlns='http://www.w3.org/2000/svg' style='display:block; shape-rendering:crispEdges;'>"
        f"<g transform='rotate({rotation} 2.5 2.5)' fill='#101010'>"
        "<rect x='0' y='0' width='1' height='5'/>"
        "<rect x='0' y='0' width='5' height='1'/>"
        "<rect x='0' y='2' width='5' height='1'/>"
        "<rect x='0' y='4' width='5' height='1'/>"
        "</g></svg></div>"
    )


with st.container(border=True):
    st.subheader("Test Setup")
    col_1, col_2, col_3 = st.columns(3)
    distance_cm = col_1.number_input(
        "Viewing distance (cm)",
        min_value=float(cfg["setup"]["distance_cm"]["min"]),
        max_value=float(cfg["setup"]["distance_cm"]["max"]),
        value=float(cfg["setup"]["distance_cm"]["default"]),
        step=float(cfg["setup"]["distance_cm"]["step"]),
    )
    screen_width_mm = col_2.number_input(
        "Screen width (mm)",
        min_value=float(cfg["setup"]["screen_width_mm"]["min"]),
        max_value=float(cfg["setup"]["screen_width_mm"]["max"]),
        value=float(cfg["setup"]["screen_width_mm"]["default"]),
        step=float(cfg["setup"]["screen_width_mm"]["step"]),
    )
    screen_width_px = col_3.number_input(
        "Screen width (pixels)",
        min_value=int(cfg["setup"]["screen_width_px"]["min"]),
        max_value=int(cfg["setup"]["screen_width_px"]["max"]),
        value=int(cfg["setup"]["screen_width_px"]["default"]),
        step=int(cfg["setup"]["screen_width_px"]["step"]),
    )
    mm_per_px = float(screen_width_mm) / float(screen_width_px)
    st.caption(f"Pixel pitch: {mm_per_px:.4f} mm/px")
    st.caption(
        "Smallest E size in this app is 4 px. Increase viewing distance to push "
        "difficulty when needed."
    )


def mar_arcmin_for_size(size_px: int, mm_per_px: float, distance_cm: float) -> float:
    return student_compute_mar_arcmin(size_px=size_px, mm_per_px=mm_per_px, distance_cm=distance_cm)


state = init_tumbling_state()
feedback_key = "tumbling_e_last_feedback"
current_index = int(state["size_index"])
current_size_px = SIZE_LEVELS_PX[current_index]
current_orientation = state["trial_orientation"]
current_mar = mar_arcmin_for_size(current_size_px, mm_per_px, distance_cm)

with st.container(border=True):
    st.subheader("Adaptive Tumbling E Trial")
    st.caption(
        f"Current size: {current_size_px}px | Current MAR: {current_mar:.2f} arcmin"
    )
    st.markdown(e_symbol(current_size_px, current_orientation), unsafe_allow_html=True)

with st.container(border=True):
    st.subheader("Respond")
    last_feedback = st.session_state.get(feedback_key)
    if last_feedback == "correct":
        st.success("Previous response: Correct.")
    elif last_feedback == "incorrect":
        st.error("Previous response: Incorrect.")

    response = st.radio("Orientation", ORIENTATIONS, horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
    )
    if submitted:
        is_correct = response == current_orientation
        next_index = student_next_size_index(
            current_index=current_index,
            is_correct=is_correct,
            max_index=len(SIZE_LEVELS_PX) - 1,
        )
        state["history"].append(
            student_build_trial_log_row(
                trial_no=len(state["history"]) + 1,
                size_px=current_size_px,
                mar_arcmin=current_mar,
                correct_orientation=current_orientation,
                response=response,
            )
        )

        state["size_index"] = next_index
        state["trial_orientation"] = next_orientation(current_orientation)
        st.session_state[feedback_key] = "correct" if is_correct else "incorrect"
        st.rerun()

with st.container(border=True):
    st.subheader("Trial Log")
    history = state["history"]
    if history:
        st.dataframe(history, width="stretch", hide_index=True)
        wrong_only = [row for row in history if row["Correct"] == "No"]
        st.markdown("**Incorrect Responses**")
        if wrong_only:
            st.dataframe(wrong_only, width="stretch", hide_index=True)
        else:
            st.caption("No incorrect responses yet.")
    else:
        st.caption("No responses yet.")

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Staircase", width="stretch"):
        st.session_state.pop("tumbling_e_state", None)
        st.session_state.pop(feedback_key, None)
        st.rerun()
