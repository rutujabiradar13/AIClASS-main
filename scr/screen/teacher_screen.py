import time
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from scr.components.dialog_add_photo import add_photo_dialog
from scr.components.dialog_attendance_result import attendance_result_dialog
from scr.components.dialog_create_subject import create_subject_dialog
from scr.components.dialog_share_subject import share_subject_dialog
from scr.components.dialog_voice_attendance import voice_attendance_dialog
from scr.components.header import header_dashboard
from scr.components.subject_card import subject_card
from scr.database.config import supabase
from scr.database.db import (
    check_teacher_exists,
    create_teacher,
    get_attendance_for_teacher,
    get_teacher_subject,
    teacher_login,
)
from scr.pipelines.face_pipeline import predict_attendance
from scr.ui.base_layout import (
    style_background_dashboard,
    style_base_layout,
)


def teacher_screen():
    style_background_dashboard()
    style_base_layout()

    if "teacher_data" in st.session_state:
        teacher_dashboard()

    elif (
        "teacher_login_type" not in st.session_state
        or st.session_state.teacher_login_type == "login"
    ):
        teacher_screen_login()

    elif st.session_state.teacher_login_type == "register":
        teacher_screen_register()


def teacher_dashboard():
    teacher_data = st.session_state["teacher_data"]

    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        st.subheader(f"Welcome, {teacher_data['name']}")

        if st.button(
            "Logout",
            type="secondary",
            key="loginbackbtm",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.session_state["is_logged_in"] = False
            del st.session_state["teacher_data"]
            st.rerun()

    st.space()

    if "current_teacher_tab" not in st.session_state:
        st.session_state.current_teacher_tab = "take_attendance"

    tab1, tab2, tab3 = st.columns(3)

    with tab1:
        type1 = (
            "primary"
            if st.session_state.current_teacher_tab == "take_attendance"
            else "tertiary"
        )

        if st.button(
            "Take Attendance",
            type=type1,
            width="stretch",
            icon=":material/ar_on_you:",
        ):
            st.session_state.current_teacher_tab = "take_attendance"
            st.rerun()

    with tab2:
        type2 = (
            "primary"
            if st.session_state.current_teacher_tab == "manage_subjects"
            else "tertiary"
        )

        if st.button(
            "Manage Subjects",
            type=type2,
            width="stretch",
            icon=":material/menu_book:",
        ):
            st.session_state.current_teacher_tab = "manage_subjects"
            st.rerun()

    with tab3:
        type3 = (
            "primary"
            if st.session_state.current_teacher_tab == "attendance_records"
            else "tertiary"
        )

        if st.button(
            "Attendance Record",
            type=type3,
            width="stretch",
            icon=":material/assignment:",
        ):
            st.session_state.current_teacher_tab = "attendance_records"
            st.rerun()

    st.divider()

    if st.session_state.current_teacher_tab == "take_attendance":
        teacher_tab_take_attendence()

    if st.session_state.current_teacher_tab == "manage_subjects":
        teacher_tab_manage_subjects()

    if st.session_state.current_teacher_tab == "attendance_records":
        teacher_tab_attendance_records()


def teacher_tab_take_attendence():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    st.subheader("Take AI attendance")

    if "attendance_images" not in st.session_state:
        st.session_state.attendance_images = []

    subjects = get_teacher_subject(teacher_id)

    if not subjects:
        st.warning(
            "You have not created any subject yet. Please create one."
        )
        return

    subject_option = {
        f"{s['name']} - {s['subject_code']}": s["subject_id"]
        for s in subjects
    }

    col1, col2 = st.columns([3, 1])

    with col1:
        select_subject_label = st.selectbox(
            "Select subject",
            options=list(subject_option.keys()),
        )

    with col2:
        if st.button(
            "Add Photos",
            type="primary",
            icon=":material/photo_prints:",
            width="stretch",
        ):
            add_photo_dialog()

    select_subject_id = subject_option[select_subject_label]

    st.divider()

    if st.session_state.attendance_images:
        st.subheader("Added Photos")

        gallery_cols = st.columns(4)

        for idx, img in enumerate(
            st.session_state.attendance_images
        ):
            with gallery_cols[idx % 4]:
                st.image(
                    img,
                    width="stretch",
                    caption=f"Photo {idx + 1}",
                )

    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button(
            "Clear all photos",
            width="stretch",
            type="tertiary",
            icon=":material/delete:",
        ):
            st.session_state.attendance_images = []
            st.rerun()

    with c2:
        has_photos = bool(
            st.session_state.attendance_images
        )

        if st.button(
            "Run face Analysis",
            width="stretch",
            type="secondary",
            icon=":material/analytics:",
            disabled=not has_photos,
        ):
            with st.spinner(
                "Deep scanning classroom photos...."
            ):
                all_detected_ids = {}

                for idx, img in enumerate(
                    st.session_state.attendance_images
                ):
                    img_np = np.array(
                        img.convert("RGB")
                    )

                    detected, _, _ = predict_attendance(
                        img_np
                    )

                    if detected:
                        for sid in detected.keys():
                            student_id = int(sid)

                            all_detected_ids.setdefault(
                                student_id,
                                [],
                            ).append(
                                f"Photo {idx + 1}"
                            )

                enrolled_res = (
                    supabase
                    .table("student_subject")
                    .select("*, students(*)")
                    .eq("subject_id", select_subject_id)
                    .execute()
                )

                enrolled_students = enrolled_res.data

                if not enrolled_students:
                    st.warning(
                        "No students enrolled in this course"
                    )

                else:
                    results = []
                    attendance_to_log = []

                    current_timestamp = datetime.now().strftime(
                        "%Y-%m-%dT%H:%M:%S"
                    )

                    for node in enrolled_students:
                        student = node["students"]

                        sources = all_detected_ids.get(
                            int(student["student_id"]),
                            [],
                        )

                        is_present = len(sources) > 0

                        results.append({
                            "Name": student["name"],
                            "ID": student["student_id"],
                            "sources": (
                                ", ".join(sources)
                                if is_present
                                else "-"
                            ),
                            "status": (
                                "Present"
                                if is_present
                                else "Absent"
                            ),
                        })

                        attendance_to_log.append({
                            "student_id": student["student_id"],
                            "subject_id": select_subject_id,
                            "timestamp": current_timestamp,
                            "is_present": bool(is_present),
                        })

                    attendance_result_dialog(
                        pd.DataFrame(results),
                        attendance_to_log,
                    )

    with c3:
        if st.button(
            "Use Voice Attendance",
            type="primary",
            width="stretch",
            icon=":material/mic:",
        ):
            voice_attendance_dialog(
                select_subject_id
            )


def teacher_tab_manage_subjects():
    teacher_id = st.session_state.teacher_data["teacher_id"]

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Manage Subjects")

    with col2:
        if st.button(
            "Create New Subject",
            width="stretch",
        ):
            create_subject_dialog(teacher_id)

    subjects = get_teacher_subject(teacher_id)

    if subjects:
        for sub in subjects:
            stats = [
                ("Students", sub.get("total_students", 0)),
                ("Classes", sub.get("total_students", 0)),
            ]

            def share_btn(
                subject_name=sub["name"],
                subject_code=sub["subject_code"],
            ):
                if st.button(
                    f"Share code: {subject_name}",
                    key=f"share_{subject_code}",
                    icon=":material/share:",
                ):
                    share_subject_dialog(
                        subject_name,
                        subject_code,
                    )

            st.space()

            subject_card(
                name=sub["name"],
                code=sub["subject_code"],
                section=sub["section"],
                stats=stats,
                footer_callback=share_btn,
            )

            st.divider()

    else:
        st.warning(
            "No Subject Found, Create New Above"
        )


def teacher_tab_attendance_records():
    st.subheader("Attendance Record")

    teacher_id = st.session_state.teacher_data["teacher_id"]

    records = get_attendance_for_teacher(teacher_id)

    if not records:
        return

    data = []

    for record in records:
        timestamp = record.get("timestamp")

        data.append({
            "ts_group": (
                timestamp.split(".")[0]
                if timestamp
                else None
            ),
            "Time": (
                datetime.fromisoformat(timestamp).strftime(
                    "%Y-%m-%d %I:%M %p"
                )
                if timestamp
                else "N'A"
            ),
            "Subjects": record["subjects"]["name"],
            "Subject_code": record["subjects"]["subject_code"],
            "is_present": bool(
                record.get("is_present", False)
            ),
        })

    df = pd.DataFrame(data)

    summary = (
        df.groupby(
            [
                "ts_group",
                "Time",
                "Subjects",
                "Subject_code",
            ]
        )
        .agg(
            Present_count=("is_present", "sum"),
            Total_count=("is_present", "count"),
        )
        .reset_index()
    )

    summary["Total_count"] = (
        summary["Total_count"].astype(str)
        + " Students"
    )

    summary["Attendance stats"] = (
        summary["Present_count"].astype(str)
        + " /"
        + summary["Total_count"]
    )

    display_df = (
        summary
        .sort_values(
            by="ts_group",
            ascending=False,
        )
        [
            [
                "Time",
                "Subjects",
                "Subject_code",
                "Attendance stats",
            ]
        ]
    )

    st.dataframe(
        display_df,
        width="stretch",
        hide_index=True,
    )


def login_teacher(username, password):
    if not username or not password:
        return False

    teacher = teacher_login(
        username,
        password,
    )

    if teacher:
        st.session_state["user_role"] = "teacher"
        st.session_state["teacher_data"] = teacher
        st.session_state["is_logged_in"] = True
        return True

    return False


def teacher_screen_login():
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go Back Home",
            type="secondary",
            key="loginbackbtm",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header(
        "Login using password",
        text_alignment="center",
    )

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter the password",
    )

    st.divider()

    btc1, btc2 = st.columns(2)

    with btc1:
        if st.button(
            "Login",
            type="primary",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
        ):
            if login_teacher(
                teacher_username,
                teacher_password,
            ):
                st.toast("Welcome Back!")
                time.sleep(1)
                st.rerun()
            else:
                st.error(
                    "Invalid username and password combo"
                )

    with btc2:
        if st.button(
            "Register Instead",
            type="primary",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
        ):
            st.session_state.teacher_login_type = "register"


def register_teacher(
    teacher_username,
    teacher_name,
    teacher_password,
    teacher_password_confirm,
):
    if (
        not teacher_username
        or not teacher_name
        or not teacher_password
        or not teacher_password_confirm
    ):
        return False, "All fields are required!"

    if check_teacher_exists(teacher_username):
        return False, "Username already taken"

    if teacher_password != teacher_password_confirm:
        return False, "Passwords do not match"

    try:
        create_teacher(
            teacher_username,
            teacher_password,
            teacher_name,
        )

        return True, "Successfully Created! Login Now"

    except Exception as e:
        st.error(f"Error: {e}")
        return False, str(e)


def teacher_screen_register():
    c1, c2 = st.columns(
        2,
        vertical_alignment="center",
        gap="xxlarge",
    )

    with c1:
        header_dashboard()

    with c2:
        if st.button(
            "Go Back Home",
            type="secondary",
            key="registerbackbtn",
            shortcut="control+backspace",
        ):
            st.session_state["login_type"] = None
            st.rerun()

    st.header("Register your profile")

    st.space()
    st.space()

    teacher_username = st.text_input(
        "Enter username",
        placeholder="ananyaroy",
    )

    teacher_name = st.text_input(
        "Enter your name",
        placeholder="ananya",
    )

    teacher_password = st.text_input(
        "Enter password",
        type="password",
        placeholder="Enter the password",
    )

    teacher_password_confirm = st.text_input(
        "Confirm your password",
        type="password",
        placeholder="Enter the password again",
    )

    st.divider()

    btc1, btc2 = st.columns(2)

    with btc1:
        if st.button(
            "Register Now",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
        ):
            success, message = register_teacher(
                teacher_username,
                teacher_name,
                teacher_password,
                teacher_password_confirm,
            )

            if success:
                st.success(message)

                time.sleep(2)

                st.session_state.teacher_login_type = "login"
                st.rerun()

            else:
                st.error(message)

    with btc2:
        if st.button(
            "Login Instead",
            icon=":material/passkey:",
            shortcut="control+enter",
            width="stretch",
        ):
            st.session_state.teacher_login_type = "login"
            st.rerun()