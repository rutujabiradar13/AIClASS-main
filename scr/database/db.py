from scr.database.config import supabase
import bcrypt


def hash_pass(pwd):
    salt = bcrypt.gensalt()   # DO NOT add .decode() here
    hashed = bcrypt.hashpw(pwd.encode("utf-8"), salt)
    return hashed.decode("utf-8")


def check_pass(pwd, hashed):
    return bcrypt.checkpw(pwd.encode(), hashed.encode())


def check_teacher_exists(username):
    response =supabase.table("teacher").select("username").eq("username", username).execute()
    return len(response.data) > 0


def create_teacher(username, password, name):
    data = {"username" : username, "password":hash_pass(password), "name":name }
    response = supabase.table("teacher").insert(data).execute()
    return response.data


def teacher_login(username, password):
    response = supabase.table("teacher").select("*").eq("username", username).execute()
    if response.data:
        teacher = response.data[0]
        if check_pass(password, teacher['password']):
            return teacher

    return None


def get_all_students():
    response =supabase.table('students').select("*").execute()
    return response.data


def create_student(new_name, face_embedding, voice_embedding):
    data = {'name': new_name, 'face_embedding': face_embedding, 'voice_embeddings':voice_embedding}
    response = supabase.table('students').insert(data).execute()
    return response.data


def create_subject(subject_code, name, section, teacher_id):
    data = {"subject_code": subject_code, "name":name, "section":section, "teacher_id":teacher_id}
    response = supabase.table("subjects").insert(data).execute()
    return response.data


def get_teacher_subject(teacher_id):
    response = supabase.table("subjects").select("*, student_subject(count), attendance_log(timestamp)").eq("teacher_id", teacher_id).execute()
    subjects = response.data

    for sub in subjects:
        student_subject = sub.get("student_subject", [])
        sub["total_students"] = student_subject[0].get("count", 0) if student_subject else 0
        attendance = sub.get('attendance_log', [])
        unique_session = len(set(log["timestamp"] for log in attendance))
        sub['total_classes'] = unique_session

        sub.pop("student_subject",None)
        sub.pop('attendance_log', None)

    return subjects


def enroll_student_to_subject(student_id, subject_id):
    data = {
        "student_id": student_id,
        "subject_id": subject_id
    }

    try:
        response = (
            supabase
            .table("student_subject")
            .insert(data)
            .execute()
        )

        print("ENROLLMENT RESPONSE:", response.data)

        return response.data

    except Exception as e:
        print("ENROLLMENT ERROR:", e)
        return None


def unenroll_student_to_subject(student_id, subject_id):
    data = {'student_id': student_id, 'subject_id': subject_id}
    response = supabase.table('student_subject').delete(data).eq('student_id', student_id).eq('subject_id', subject_id).execute()
    return response.data


def get_students_subject(student_id):
    response = supabase.table('student_subject').select('*,subjects(*)').eq('student_id', student_id).execute()
    return response.data


def get_students_attendance(student_id):
    response = supabase.table('attendance_log').select('*,subjects(*)').eq('student_id', student_id).execute()
    return response.data


def create_attendance(logs):
    response = supabase.table('attendance_log').insert(logs).execute()
    return response.data


def get_attendance_for_teacher(teacher_id):
    response = supabase.table('attendance_log').select("*, subjects!inner(*)").eq('subjects.teacher_id', teacher_id).execute()
    return response.data