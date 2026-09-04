"""Shared TODOs for all 3AFC assignment pages.

Why this file exists:
- All 3AFC pages use the same staircase, accuracy, and plotting patterns.
- Shared logic is implemented here once and reused by all 3AFC pages.

Used by:
- pages/sound_gap_detection.py
- pages/amplitude_threshold.py
- pages/pitch_threshold.py

Implementation expectations:
- Keep return types exactly as annotated.
- Prefer small, pure functions with no Streamlit state mutations.
- Validate/clamp values to avoid invalid outputs.
"""
import matplotlib.pyplot as plt
import streamlit as st


def shared_student_apply_reversal_update(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Apply one 2-down/1-up staircase update."""
    safe_down_n = max(1, down_n)
    
    if not is_correct:
        next_level = current_level + step
        next_streak = 0
    else:
        next_streak = correct_streak + 1
        if next_streak >= safe_down_n:
            next_level = current_level - step
            next_streak = 0
        else:
            next_level = current_level
            
    next_level = max(min_level, min(max_level, next_level))
    return next_level, next_streak


def shared_student_plot_staircase(
    history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """Plot the staircase trace for the given history."""
    if not history:
        return

    trials = [row.get("Trial", i + 1) for i, row in enumerate(history)]
    levels = [row.get("Level", 0.0) for row in history]
    corrects = [row.get("Correct") == "Yes" for row in history]

    fig, ax = plt.subplots(figsize=(8, 4))
    
    ax.plot(trials, levels, color="black", alpha=0.4, zorder=1)
    
    c_x = [t for i, t in enumerate(trials) if corrects[i]]
    c_y = [l for i, l in enumerate(levels) if corrects[i]]
    i_x = [t for i, t in enumerate(trials) if not corrects[i]]
    i_y = [l for i, l in enumerate(levels) if not corrects[i]]

    ax.scatter(c_x, c_y, color="green", label="Correct", zorder=2)
    ax.scatter(i_x, i_y, color="red", label="Incorrect", zorder=2)
    
    ax.axhline(threshold, color="blue", linestyle="--", label="Estimated Threshold", zorder=1)

    ax.set_xlabel("Trial")
    ax.set_ylabel(y_label)
    ax.set_title(title)
    ax.legend()
    ax.grid(True, linestyle=":", alpha=0.6)

    st.pyplot(fig)


def shared_student_build_three_interval_targets(*, target_index: int) -> list[bool]:
    """Build a length-3 target mask with exactly one `True` entry."""
    return [i == target_index for i in range(3)]


def shared_student_update_staircase_state(
    *,
    current_level: float,
    step: float,
    is_correct: bool,
    correct_streak: int,
    down_n: int,
    min_level: float,
    max_level: float,
) -> tuple[float, int]:
    """Reusable helper that keeps staircase behavior consistent."""
    return shared_student_apply_reversal_update(
        current_level=current_level,
        step=step,
        is_correct=is_correct,
        correct_streak=correct_streak,
        down_n=down_n,
        min_level=min_level,
        max_level=max_level,
    )


def shared_student_estimate_threshold_from_reversals(
    *, reversals: list[float], fallback_level: float, tail_count: int = 4
) -> float:
    """Estimate threshold using the trailing reversal points."""
    if len(reversals) >= tail_count and tail_count > 0:
        return sum(reversals[-tail_count:]) / tail_count
    return fallback_level


def shared_student_compute_recent_accuracy(history: list[dict], window: int = 12) -> float:
    """Compute a trailing percent-correct accuracy metric."""
    if not history:
        return 0.0
        
    recent_trials = history[-window:]
    correct_count = sum(1 for row in recent_trials if row.get("Correct") == "Yes")
    return (correct_count / len(recent_trials)) * 100.0


def shared_student_validate_audio_params(*, amplitude: float, stimulus_value: float) -> bool:
    """Validate amplitude and stimulus-specific numeric values."""
    return (0.0 <= amplitude <= 1.0) and (stimulus_value > 0.0)


def shared_student_plot_staircase_with_threshold(
    *, history: list[dict], threshold: float, y_label: str, title: str
) -> None:
    """Wrapper that draws the staircase and highlights the threshold."""
    shared_student_plot_staircase(
        history=history,
        threshold=threshold,
        y_label=y_label,
        title=title,
    )
