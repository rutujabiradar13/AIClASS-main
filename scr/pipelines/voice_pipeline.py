import io

import librosa
import numpy as np
import streamlit as st
from resemblyzer import VoiceEncoder, preprocess_wav


@st.cache_resource
def load_voice_encoder():
    return VoiceEncoder()


def get_voice_embedding(audio_bytes):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True,
        )

        if audio is None or len(audio) == 0:
            st.error("No audio detected.")
            return None

        wav = preprocess_wav(audio)

        if len(wav) < 16000:
            st.warning("Please record at least 1 second of speech.")
            return None

        embedding = encoder.embed_utterance(wav)

        return embedding.tolist()

    except Exception as e:
        st.error(f"Voice recognition error: {e}")
        return None


def identify_speaker(
    new_embedding,
    candidates_dict,
    threshold=0.65,
    margin=0.08,
):
    if new_embedding is None or not candidates_dict:
        return None, 0.0

    new_embedding = np.asarray(
        new_embedding,
        dtype=np.float32,
    )

    new_norm = np.linalg.norm(new_embedding)

    if new_norm == 0:
        return None, 0.0

    new_embedding = new_embedding / new_norm

    scores = []

    for sid, stored_embedding in candidates_dict.items():
        if stored_embedding is None:
            continue

        try:
            stored_embedding = np.asarray(
                stored_embedding,
                dtype=np.float32,
            )

            if stored_embedding.shape != new_embedding.shape:
                st.warning(
                    f"Invalid embedding size for student {sid}"
                )
                continue

            stored_norm = np.linalg.norm(stored_embedding)

            if stored_norm == 0:
                continue

            stored_embedding = stored_embedding / stored_norm

            similarity = float(
                np.dot(
                    new_embedding,
                    stored_embedding,
                )
            )

            scores.append((int(sid), similarity))

        except Exception as e:
            st.warning(
                f"Could not compare student {sid}: {e}"
            )

    if not scores:
        return None, 0.0

    scores.sort(
        key=lambda x: x[1],
        reverse=True,
    )

    best_sid, best_score = scores[0]

    second_score = (
        scores[1][1]
        if len(scores) > 1
        else -1.0
    )

    if best_score < threshold:
        st.warning(
            f"No confident match. "
            f"Best score = {best_score:.3f}, "
            f"required = {threshold:.2f}"
        )
        return None, 0.0

    if len(scores) > 1:
        score_difference = best_score - second_score

        if score_difference < margin:
            st.warning(
                "Voice match is ambiguous. "
                "Best and second-best scores are too close."
            )
            return None, 0.0

    st.success(
        f"Speaker identified: Student {best_sid} "
        f"({best_score:.3f})"
    )

    return best_sid, best_score


def process_bulk_audio(
    audio_bytes,
    candidates_dict,
    threshold=0.65,
):
    try:
        encoder = load_voice_encoder()

        audio, sr = librosa.load(
            io.BytesIO(audio_bytes),
            sr=16000,
            mono=True,
        )

        if audio is None or len(audio) == 0:
            st.error("No audio detected.")
            return {}

        duration = len(audio) / sr

        if duration < 1.0:
            st.warning(
                "Please record at least 1 second of speech."
            )
            return {}

        wav = preprocess_wav(audio)

        if wav is None or len(wav) == 0:
            st.error("Could not preprocess audio.")
            return {}

        embedding = encoder.embed_utterance(wav)

        sid, score = identify_speaker(
            embedding.tolist(),
            candidates_dict,
            threshold=threshold,
            margin=0.08,
        )

        if sid is None:
            st.warning("No confident speaker identified.")
            return {}

        return {
            int(sid): float(score)
        }

    except Exception as e:
        st.error(f"Bulk processing error: {e}")
        return {}