import dlib
import numpy as np
import face_recognition_models
import streamlit as st
from sklearn.svm import SVC

from scr.database.db import get_all_students


@st.cache_resource
def load_dlib_models():
    detector = dlib.get_frontal_face_detector()

    sp = dlib.shape_predictor(
        face_recognition_models.pose_predictor_model_location()
    )

    facerec = dlib.face_recognition_model_v1(
        face_recognition_models.face_recognition_model_location()
    )

    return detector, sp, facerec


def get_face_embeddings(image_np):
    detector, sp, facerec = load_dlib_models()

    faces = detector(image_np, 3)
    encodings = []

    for face in faces:
        shape = sp(image_np, face)

        descriptor = facerec.compute_face_descriptor(
            image_np,
            shape,
            1
        )

        encodings.append(np.array(descriptor))

    return encodings


def get_trained_model():
    X = []
    y = []

    student_db = get_all_students()

    if not student_db:
        return None

    for student in student_db:
        embedding = student.get("face_embedding")

        if embedding:
            X.append(np.array(embedding))
            y.append(student.get("student_id"))

    if len(X) == 0:
        return None

    if len(set(y)) == 1:
        return {
            "clf": None,
            "X": X,
            "y": y
        }

    clf = SVC(
        kernel="linear",
        probability=True,
        class_weight="balanced"
    )

    try:
        clf.fit(X, y)

    except ValueError as e:
        st.error(f"Model training failed: {e}")
        return None

    return {
        "clf": clf,
        "X": X,
        "y": y
    }


def train_classifier():
    st.cache_resource.clear()

    model_data = get_trained_model()

    return bool(model_data)


def predict_attendance(class_image_np):
    encodings = get_face_embeddings(class_image_np)

    detected_student = {}

    model_data = get_trained_model()

    if not model_data:
        return detected_student, [], len(encodings)

    clf = model_data["clf"]
    X_train = model_data["X"]
    y_train = model_data["y"]

    all_students = sorted(list(set(y_train)))

    for encoding in encodings:

        if len(all_students) >= 2:
            predicted_id = int(
                clf.predict([encoding])[0]
            )
        else:
            predicted_id = int(all_students[0])

        student_embedding = X_train[
            y_train.index(predicted_id)
        ]

        best_match_score = np.linalg.norm(
            student_embedding - encoding
        )

        resemblance_threshold = 0.8

        if best_match_score <= resemblance_threshold:
            detected_student[predicted_id] = True

    return (
        detected_student,
        all_students,
        len(encodings)
    )


def check_duplicate_face(face_image_np):
    encodings = get_face_embeddings(face_image_np)

    if len(encodings) == 0:
        return False, None, None

    if len(encodings) > 1:
        return False, None, None

    new_encoding = np.asarray(encodings[0])

    model_data = get_trained_model()

    if not model_data:
        return False, None, None

    X_train = np.asarray(model_data["X"])
    y_train = np.asarray(model_data["y"])

    if len(X_train) == 0:
        return False, None, None

    distances = np.linalg.norm(
        X_train - new_encoding,
        axis=1
    )

    best_index = int(np.argmin(distances))
    best_distance = float(distances[best_index])

    existing_student_id = int(
        y_train[best_index]
    )

    registration_threshold = 0.60

    if best_distance <= registration_threshold:
        return (
            True,
            existing_student_id,
            best_distance
        )

    return (
        False,
        None,
        best_distance
    )