import streamlit as st

from pages._shared_3afc_student import (
    shared_student_apply_reversal_update,
    shared_student_build_three_interval_targets,
    shared_student_compute_recent_accuracy,
    shared_student_estimate_threshold_from_reversals,
    shared_student_plot_staircase,
    shared_student_plot_staircase_with_threshold,
    shared_student_update_staircase_state,
    shared_student_validate_audio_params,
)
from utils.adaptive_3afc import (
    estimate_threshold,
    get_or_create_trial,
    init_adaptive_state,
    reset_adaptive_state,
)
from utils.audio_tools import noise_burst_with_gap_wav
from utils.test_config import load_test_config
from utils.three_afc import (
    render_completion_summary,
    render_feedback,
    render_staircase_plot,
    submit_3afc_response,
)
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Sound Gap Detection Test",
    layout="wide",
)

render_page_header(
    "Sound Gap Detection Test",
    "3AFC adaptive test: select which interval contains a silent gap.",
    "gap",
)

render_instructions(
    "How To Run This Test",
    (
        "You will hear three short noise bursts. Exactly one burst contains a "
        "centered silence gap. Pick the correct interval every trial."
    ),
    [
        "Use all three play buttons to compare candidates before answering.",
        "Select the interval with the gap, then submit your response.",
        "The adaptive staircase will shrink or expand the gap based on performance.",
        "After finishing, recreate the staircase plot from the trial history as a lab exercise.",
    ],
)

config = load_test_config()
cfg = config["gap_detection"]


def student_build_gap_intervals_audio(
    *,
    gap_ms: float,
    amplitude: float,
    target_index: int,
    seed: int,
) -> list[bytes]:
    """TODO: Build one 3AFC trial audio set for gap detection.

    Why this function exists:
        The listener must compare three intervals where only one contains the silent
        gap. Centralizing generation here makes stimuli reproducible and easy to test.

    Inputs:
        gap_ms: Gap duration for the target interval.
        amplitude: Playback amplitude for all intervals.
        target_index: Index (0, 1, 2) containing the gap.
        seed: Seed used so generated noise bursts are deterministic.

    Output:
        A list of exactly three WAV byte payloads.

    Required behavior:
        - Target interval gets `gap_ms`.
        - Other intervals get zero gap.
        - Keep amplitude consistent across all three clips.
        - Use deterministic seeds so repeated runs are reproducible.
    """
    raise NotImplementedError("Not implemented yet; follow the docstring guidance.")


def student_apply_reversal_update(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_apply_reversal_update(
        current_level=current_level,
        step=step,
        is_correct=is_correct,
        correct_streak=correct_streak,
        down_n=down_n,
        min_level=min_level,
        max_level=max_level,
    )


def student_plot_staircase(history: list[dict], threshold: float, y_label: str, title: str) -> None:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    shared_student_plot_staircase(
        history=history,
        threshold=threshold,
        y_label=y_label,
        title=title,
    )


def student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_build_three_interval_targets(target_index=target_index)


def student_update_staircase_state(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_update_staircase_state(
        current_level=current_level,
        step=step,
        is_correct=is_correct,
        correct_streak=correct_streak,
        down_n=down_n,
        min_level=min_level,
        max_level=max_level,
    )


def student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_estimate_threshold_from_reversals(
        reversals=reversals,
        fallback_level=fallback_level,
        tail_count=tail_count,
    )


def student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_compute_recent_accuracy(history=history, window=window)


def student_validate_audio_params(*, amplitude: float, gap_ms: float) -> bool:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_validate_audio_params(amplitude=amplitude, stimulus_value=gap_ms)


def student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    shared_student_plot_staircase_with_threshold(
        history=history,
        threshold=threshold,
        y_label=y_label,
        title=title,
    )


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_build_gap_intervals_audio`.\n"
        "- Implement shared 3AFC helpers in `pages/_shared_3afc_student.py`:\n"
        "  - `shared_student_apply_reversal_update`\n"
        "  - `shared_student_plot_staircase`\n"
        "  - `shared_student_build_three_interval_targets`\n"
        "  - `shared_student_update_staircase_state`\n"
        "  - `shared_student_estimate_threshold_from_reversals`\n"
        "  - `shared_student_compute_recent_accuracy`\n"
        "  - `shared_student_validate_audio_params`\n"
        "  - `shared_student_plot_staircase_with_threshold`"
    )

st.caption(
    "How these functions connect: generate three noise intervals (one with gap) -> "
    "update adaptive staircase from responses -> estimate threshold from reversals -> plot."
)

try:
    _ = student_build_three_interval_targets(target_index=1)
    _ = student_build_gap_intervals_audio(
        gap_ms=float(cfg["adaptive"]["start_level"]),
        amplitude=float(cfg["playback"]["amplitude"]["default"]),
        target_index=1,
        seed=123,
    )
    _ = student_apply_reversal_update(
        current_level=float(cfg["adaptive"]["start_level"]),
        step=float(cfg["adaptive"]["initial_step"]),
        is_correct=True,
        correct_streak=1,
        down_n=int(cfg["adaptive"]["down"]),
        min_level=float(cfg["adaptive"]["min_level"]),
        max_level=float(cfg["adaptive"]["max_level"]),
    )
    _ = student_update_staircase_state(
        current_level=float(cfg["adaptive"]["start_level"]),
        step=float(cfg["adaptive"]["initial_step"]),
        is_correct=False,
        correct_streak=0,
        down_n=int(cfg["adaptive"]["down"]),
        min_level=float(cfg["adaptive"]["min_level"]),
        max_level=float(cfg["adaptive"]["max_level"]),
    )
    _ = student_estimate_threshold_from_reversals(
        reversals=[float(cfg["adaptive"]["start_level"])],
        fallback_level=float(cfg["adaptive"]["start_level"]),
        tail_count=1,
    )
    _ = student_compute_recent_accuracy(
        history=[{"Correct": "Yes"}, {"Correct": "No"}],
        window=2,
    )
    _ = student_validate_audio_params(
        amplitude=float(cfg["playback"]["amplitude"]["default"]),
        gap_ms=float(cfg["adaptive"]["start_level"]),
    )
    student_plot_staircase(
        history=[{"Trial": 1, "Level": float(cfg["adaptive"]["start_level"]), "Correct": "Yes"}],
        threshold=float(cfg["adaptive"]["start_level"]),
        y_label="Gap (ms)",
        title="Preview Staircase",
    )
    student_plot_staircase_with_threshold(
        history=[{"Trial": 1, "Level": float(cfg["adaptive"]["start_level"]), "Correct": "Yes"}],
        threshold=float(cfg["adaptive"]["start_level"]),
        y_label="Gap (ms)",
        title="Preview Staircase",
    )
except NotImplementedError as error:
    st.error(str(error))
    st.warning(
        "Assignment mode is active for this page. Complete `student_build_gap_intervals_audio` "
        "in this file and the shared 3AFC TODOs in `pages/_shared_3afc_student.py`, then reload."
    )
    st.stop()

adaptive = init_adaptive_state(
    "gap",
    start_level=float(cfg["adaptive"]["start_level"]),
    min_level=float(cfg["adaptive"]["min_level"]),
    max_level=float(cfg["adaptive"]["max_level"]),
    initial_step=float(cfg["adaptive"]["initial_step"]),
    min_step=float(cfg["adaptive"]["min_step"]),
    max_reversals=int(cfg["adaptive"]["max_reversals"]),
    down=int(cfg["adaptive"]["down"]),
)
trial = get_or_create_trial("gap")
current_gap_ms = float(adaptive["current_level"])
feedback_key = "gap_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback"]["amplitude"]["min"]),
        max_value=float(cfg["playback"]["amplitude"]["max"]),
        value=float(cfg["playback"]["amplitude"]["default"]),
        step=float(cfg["playback"]["amplitude"]["step"]),
        key="gap_amplitude",
    )
    st.caption(
        f"Current adaptive gap level: {current_gap_ms:.2f} ms | "
        f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}"
    )
    play_cols = st.columns(3)
    for idx in range(3):
        gap_ms = current_gap_ms if idx == trial["target_index"] else 0.0
        wav_bytes = noise_burst_with_gap_wav(
            duration_s=float(cfg["playback"]["burst_duration_s"]),
            gap_ms=gap_ms,
            amplitude=amplitude,
            seed=trial["seed"] + idx,
        )
        play_cols[idx].audio(wav_bytes, format="audio/wav")
        play_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    render_feedback(feedback_key)
    choice = st.radio("Which interval had the gap?", [1, 2, 3], horizontal=True)
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        submit_3afc_response(
            state_key="gap",
            adaptive=adaptive,
            trial=trial,
            level_used=current_gap_ms,
            selected_interval=int(choice),
            feedback_key=feedback_key,
        )

    estimated_gap = estimate_threshold(adaptive)
    st.metric("Estimated Gap Threshold (ms)", f"{estimated_gap:.2f}")

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        render_completion_summary(adaptive, estimated_value=estimated_gap, value_label="ms")
        render_staircase_plot(
            history=history,
            estimated_value=estimated_gap,
            threshold_label="Estimated Threshold",
            y_label="Gap (ms)",
            title="Gap Detection Adaptive Staircase",
        )

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("gap")
        st.session_state.pop(feedback_key, None)
        st.rerun()
