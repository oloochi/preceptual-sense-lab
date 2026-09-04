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
from utils.audio_tools import single_tone_wav
from utils.test_config import load_test_config
from utils.three_afc import (
    render_completion_summary,
    render_feedback,
    render_recent_accuracy_metric,
    render_staircase_plot,
    submit_3afc_response,
)
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Amplitude Threshold Test",
    layout="wide",
    initial_sidebar_state="collapsed",
)

render_page_header(
    "Amplitude Threshold Test",
    "3AFC adaptive test: identify the interval with higher amplitude.",
    "amplitude",
)

render_instructions(
    "How To Run This Test",
    (
        "You will hear three tones. One tone is slightly louder than the other two. "
        "Select the louder interval in each trial."
    ),
    [
        "Keep system volume fixed and only use in-app playback controls.",
        "Answer every trial even when unsure (forced choice).",
        "Adaptive step sizes shrink after reversals to stabilize the threshold.",
        "After finishing, recreate the staircase plot from trial history as a lab task.",
    ],
)

config = load_test_config()
cfg = config["amplitude_discrimination"]


def student_build_amplitude_intervals_audio(
    *,
    baseline_amplitude: float,
    delta_db: float,
    reference_hz: int,
    target_index: int,
) -> list[bytes]:
    """Build one 3AFC trial audio set for amplitude discrimination."""
    # Convert delta_db to an amplitude multiplier (ratio)
    ratio = 10.0 ** (delta_db / 20.0)
    
    # Calculate target amplitude and clamp to prevent audio clipping
    target_amplitude = max(0.01, min(0.95, baseline_amplitude * ratio))
    duration_s = float(cfg["tone_duration_s"])
    
    wav_outputs = []
    for i in range(3):
        # The target interval gets the louder amplitude; others get the baseline
        amp = target_amplitude if i == target_index else baseline_amplitude
        
        # Generate the WAV bytes for this interval
        wav_bytes = single_tone_wav(
            frequency_hz=float(reference_hz),
            duration_s=duration_s,
            amplitude=amp,
        )
        wav_outputs.append(wav_bytes)
        
    return wav_outputs


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


def student_validate_audio_params(*, amplitude: float, frequency_hz: int) -> bool:
    """Shared 3AFC TODO: implement in `pages/_shared_3afc_student.py`."""
    return shared_student_validate_audio_params(
        amplitude=amplitude,
        stimulus_value=float(frequency_hz),
    )


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
        "- Implement `student_build_amplitude_intervals_audio`.\n"
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
    "How these functions connect: generate 3-interval audio -> collect response -> "
    "update staircase/reversals -> estimate threshold -> compute accuracy -> plot results."
)

try:
    _ = student_build_three_interval_targets(target_index=1)
    _ = student_build_amplitude_intervals_audio(
        baseline_amplitude=float(cfg["reference_amplitude"]["default"]),
        delta_db=float(cfg["adaptive"]["start_level"]),
        reference_hz=int(cfg["reference_frequency_hz"]["default"]),
        target_index=1,
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
        amplitude=float(cfg["reference_amplitude"]["default"]),
        frequency_hz=int(cfg["reference_frequency_hz"]["default"]),
    )
    student_plot_staircase(
        history=[{"Trial": 1, "Level": float(cfg["adaptive"]["start_level"]), "Correct": "Yes"}],
        threshold=float(cfg["adaptive"]["start_level"]),
        y_label="Amplitude Delta (dB)",
        title="Preview Staircase",
    )
    student_plot_staircase_with_threshold(
        history=[{"Trial": 1, "Level": float(cfg["adaptive"]["start_level"]), "Correct": "Yes"}],
        threshold=float(cfg["adaptive"]["start_level"]),
        y_label="Amplitude Delta (dB)",
        title="Preview Staircase",
    )
except NotImplementedError as error:
    st.error(str(error))
    st.warning(
        "Assignment mode is active for this page. Complete "
        "`student_build_amplitude_intervals_audio` in this file and the shared 3AFC "
        "TODOs in `pages/_shared_3afc_student.py`, then reload."
    )
    st.stop()

adaptive = init_adaptive_state(
    "amplitude",
    start_level=float(cfg["adaptive"]["start_level"]),
    min_level=float(cfg["adaptive"]["min_level"]),
    max_level=float(cfg["adaptive"]["max_level"]),
    initial_step=float(cfg["adaptive"]["initial_step"]),
    min_step=float(cfg["adaptive"]["min_step"]),
    max_reversals=int(cfg["adaptive"]["max_reversals"]),
    down=int(cfg["adaptive"]["down"]),
)
trial = get_or_create_trial("amplitude")
current_delta_db = float(adaptive["current_level"])
feedback_key = "amplitude_last_feedback"

with st.container(border=True):
    st.subheader("3AFC Trial")
    baseline_amplitude = st.slider(
        "Reference amplitude",
        min_value=float(cfg["reference_amplitude"]["min"]),
        max_value=float(cfg["reference_amplitude"]["max"]),
        value=float(cfg["reference_amplitude"]["default"]),
        step=float(cfg["reference_amplitude"]["step"]),
        key="amp_reference",
    )
    reference_hz = st.number_input(
        "Reference tone frequency (Hz)",
        min_value=int(cfg["reference_frequency_hz"]["min"]),
        max_value=int(cfg["reference_frequency_hz"]["max"]),
        value=int(cfg["reference_frequency_hz"]["default"]),
        step=int(cfg["reference_frequency_hz"]["step"]),
    )
    ratio = 10 ** (current_delta_db / 20.0)
    target_amplitude = max(0.01, min(0.95, baseline_amplitude * ratio))
    st.caption(
        f"Current adaptive delta: {current_delta_db:.2f} dB | "
        f"Reversals: {len(adaptive['reversals'])}/{adaptive['max_reversals']}"
    )

    play_cols = st.columns(3)
    for idx in range(3):
        amplitude = target_amplitude if idx == trial["target_index"] else baseline_amplitude
        play_cols[idx].audio(
            single_tone_wav(
                frequency_hz=float(reference_hz),
                duration_s=float(cfg["tone_duration_s"]),
                amplitude=amplitude,
            ),
            format="audio/wav",
        )
        play_cols[idx].caption(f"Interval {idx + 1}")

with st.container(border=True):
    st.subheader("Respond")
    render_feedback(feedback_key)
    choice = st.radio("Which interval was louder?", [1, 2, 3], horizontal=True, key="amp_choice")
    submitted = st.button(
        "Submit Response",
        type="primary",
        width="stretch",
        disabled=adaptive["finished"],
    )
    if submitted and not adaptive["finished"]:
        submit_3afc_response(
            state_key="amplitude",
            adaptive=adaptive,
            trial=trial,
            level_used=current_delta_db,
            selected_interval=int(choice),
            feedback_key=feedback_key,
        )

    estimated_db = estimate_threshold(adaptive)
    history = adaptive["history"]
    col_1, col_2 = st.columns(2)
    col_1.metric("Estimated Threshold (dB)", f"{estimated_db:.2f}")
    with col_2:
        render_recent_accuracy_metric(history)

if adaptive["finished"]:
    with st.container(border=True):
        st.subheader("Adaptive Test Complete")
        st.success("Staircase finished. Final estimate and statistics are shown below.")
        history = adaptive["history"]
        render_completion_summary(adaptive, estimated_value=estimated_db, value_label="dB")
        render_staircase_plot(
            history=history,
            estimated_value=estimated_db,
            threshold_label="Estimated Threshold",
            y_label="Amplitude Delta (dB)",
            title="Amplitude Discrimination Adaptive Staircase",
        )

with st.container(border=True):
    st.subheader("Test Controls")
    if st.button("Restart Adaptive Test", width="stretch"):
        reset_adaptive_state("amplitude")
        st.session_state.pop(feedback_key, None)
        st.rerun()
