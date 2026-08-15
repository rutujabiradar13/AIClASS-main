from datetime import datetime

import pandas as pd
import streamlit as st

from scr.components.dialog_attendance_result import show_attendance_result
from scr.database.config import supabase
from scr.pipelines.voice_pipeline import process_bulk_audio


@st.dialog("Voice attendance")
def voice_attendance_dialog(selected_subject_id):
    st.write(
        "Record audio of students saying 'I am present'. "
        "Then AI will recognize the students."
    )

    audio_data = st.audio_input("Record classroom audio")

    if st.button(
        "Analyze Audio",
        width="stretch",
        type="primary",
    ):
        if not audio_data:
            st.warning("Please record classroom audio first.")
            return

        with st.spinner("Processing Audio data"):
            enrolled_res = (
                supabase
                .table("student_subject")
                .select("*, students(*)")
                .eq("subject_id", selected_subject_id)
                .execute()
            )

            enrolled_students = enrolled_res.data

            if not enrolled_students:
                st.warning("No student enrolled in this course.")
                return

            candidates_dict = {
                int(student["students"]["student_id"]):
                    student["students"]["voice_embeddings"]
                for student in enrolled_students
                if student["students"].get("voice_embeddings") is not None
            }

            if not candidates_dict:
                st.error(
                    "No enrolled students have voice profiles registered."
                )
                return

            audio_bytes = audio_data.read()

            detected_scores = process_bulk_audio(
                audio_bytes,
                candidates_dict,
                threshold=0.65,
            )

            results = []
            attendance_to_log = []

            current_timestamp = datetime.now().strftime(
                "%Y-%m-%dT%H:%M:%S"
            )

            for node in enrolled_students:
                student = node["students"]

                score = detected_scores.get(
                    int(student["student_id"]),
                    0.0,
                )

                is_present = bool(score >= 0.65)

                results.append({
                    "Name": student["name"],
                    "ID": student["student_id"],
                    "sources": score if is_present else "-",
                    "status": "Present" if is_present else "Absent",
                })

                attendance_to_log.append({
                    "student_id": student["student_id"],
                    "subject_id": selected_subject_id,
                    "timestamp": current_timestamp,
                    "is_present": bool(is_present),
                })

            st.session_state.voice_attendance_result = (
                pd.DataFrame(results),
                attendance_to_log,
            )

    if st.session_state.get("voice_attendance_result"):
        st.divider()

        df_results, logs = st.session_state.voice_attendance_result

        show_attendance_result(
            df_results,
            logs,
        )