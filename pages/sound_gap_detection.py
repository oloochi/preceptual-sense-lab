import streamlit as st

from utils.audio_tools import single_tone_wav
from utils.test_config import load_test_config
from utils.ui import (
    render_instructions,
    render_page_header,
)

st.set_page_config(
    page_title="Pitch Frequency Range Test",
    layout="wide",
)

render_page_header(
    "Pitch Frequency Range Test",
    "Use fine-grained controls to find your audible frequency range between 20 Hz and 20 kHz.",
    "pitch",
)

render_instructions(
    "How To Run This Test",
    (
        "Test tones from low to high frequencies with small frequency steps. Keep "
        "system volume fixed and use a quiet environment."
    ),
    [
        "Use the slider for quick sweeps and number input for exact frequencies.",
        "Increase frequency until you can no longer hear it reliably.",
        "Record the highest clearly audible frequency.",
    ],
)

config = load_test_config()
cfg = config["pitch_range"]


def format_frequency_hz(frequency_hz: int) -> str:
    """Format frequency as Hz under 1 kHz and kHz above 1 kHz."""
    if frequency_hz < 1000:
        return f"{frequency_hz} Hz"
    return f"{frequency_hz / 1000:.2f} kHz"


default_frequency = int(cfg["frequency_hz"]["default"])
default_amplitude = float(cfg["playback_amplitude"]["default"])


def student_estimate_audible_bounds(
    *,
    probe_history_hz: list[int],
    heard_flags: list[bool],
) -> tuple[int, int]:
    """Summarize heard probe frequencies into lower/upper bounds."""
    heard_frequencies = [
        freq for freq, heard in zip(probe_history_hz, heard_flags) if heard
    ]
    
    if not heard_frequencies:
        return (default_frequency, default_frequency)
        
    return (min(heard_frequencies), max(heard_frequencies))


def student_validate_audio_params(*, frequency_hz: int, amplitude: float) -> bool:
    """Ensure requested playback parameters stay within config limits."""
    freq_min = int(cfg["frequency_hz"]["min"])
    freq_max = int(cfg["frequency_hz"]["max"])
    amp_min = float(cfg["playback_amplitude"]["min"])
    amp_max = float(cfg["playback_amplitude"]["max"])
    
    is_freq_valid = freq_min <= frequency_hz <= freq_max
    is_amp_valid = amp_min <= amplitude <= amp_max
    
    return is_freq_valid and is_amp_valid


with st.expander("Assignment TODOs (Edit This Page)"):
    st.markdown(
        "- Implement `student_estimate_audible_bounds` using example probe results.\n"
        "- Implement `student_validate_audio_params` to gate playback inputs."
    )

st.caption(
    "Optional TODO: once the helper functions exist you could show estimated bounds "
    "and validate that playback parameters stay within config limits."
)

# Initialize session state for tracking responses
if "pitch_history_hz" not in st.session_state:
    st.session_state["pitch_history_hz"] = []
if "pitch_heard_flags" not in st.session_state:
    st.session_state["pitch_heard_flags"] = []

with st.container(border=True):
    st.subheader("Tone Playback")
    frequency_hz = st.number_input(
        "Exact test frequency (Hz)",
        min_value=int(cfg["frequency_hz"]["min"]),
        max_value=int(cfg["frequency_hz"]["max"]),
        value=default_frequency,
        step=int(cfg["frequency_hz"]["step"]),
        key="pitch_playback_input",
    )
    amplitude = st.slider(
        "Playback amplitude",
        min_value=float(cfg["playback_amplitude"]["min"]),
        max_value=float(cfg["playback_amplitude"]["max"]),
        value=default_amplitude,
        step=float(cfg["playback_amplitude"]["step"]),
    )
    
    if student_validate_audio_params(frequency_hz=frequency_hz, amplitude=amplitude):
        st.audio(single_tone_wav(frequency_hz=frequency_hz, amplitude=amplitude), format="audio/wav")
        st.caption(f"Current test tone: {format_frequency_hz(int(frequency_hz))}")
    else:
        st.error("Audio parameters are out of configured bounds.")

with st.container(border=True):
    st.subheader("Record Response")
    col1, col2 = st.columns(2)
    
    if col1.button("I heard it", type="primary", use_container_width=True):
        st.session_state["pitch_history_hz"].append(frequency_hz)
        st.session_state["pitch_heard_flags"].append(True)
        st.rerun()
        
    if col2.button("I didn't hear it", use_container_width=True):
        st.session_state["pitch_history_hz"].append(frequency_hz)
        st.session_state["pitch_heard_flags"].append(False)
        st.rerun()

with st.container(border=True):
    st.subheader("Estimated Audible Bounds")
    
    if st.session_state["pitch_history_hz"]:
        lower_bound, upper_bound = student_estimate_audible_bounds(
            probe_history_hz=st.session_state["pitch_history_hz"],
            heard_flags=st.session_state["pitch_heard_flags"],
        )
        
        col_a, col_b = st.columns(2)
        col_a.metric("Lower Bound", format_frequency_hz(lower_bound))
        col_b.metric("Upper Bound", format_frequency_hz(upper_bound))
        
        # Display the log of tested frequencies
        st.caption("Probe History Log")
        history_data = [
            {
                "Trial": idx + 1,
                "Frequency": format_frequency_hz(freq),
                "Heard": "Yes" if heard else "No"
            }
            for idx, (freq, heard) in enumerate(zip(
                st.session_state["pitch_history_hz"], 
                st.session_state["pitch_heard_flags"]
            ))
        ]
        st.dataframe(history_data, use_container_width=True, hide_index=True)
        
        if st.button("Clear History", use_container_width=True):
            st.session_state["pitch_history_hz"].clear()
            st.session_state["pitch_heard_flags"].clear()
            st.rerun()
    else:
        st.info("Play a tone and record your response above to estimate your bounds.")
