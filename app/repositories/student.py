from app.models.Student import Student
from app.models.User import User
from sqlmodel import Session, select
from sqlalchemy import func


def count_total_students(db: Session) -> int:
    statement = select(func.count(Student.student_id))
    result = db.exec(statement)
    return result.one()



def create_student(
    db,
    *,
    user_id,
    name: str,
    phone: str | None
) -> Student:
    student = Student(
        user_id=user_id,
        name=name,
        phone=phone,
    )
    db.add(student)
    db.flush()
    db.refresh(student)
    return student



def get_all_students(db: Session):
    statement = (
        select(Student, User)
        .join(User, Student.user_id == User.user_id)
    )

    results = db.exec(statement).all()

    students = []

    for student, user in results:
        students.append({
            "student_id": student.student_id,
            "name": student.name,
            "phone": student.phone,
            "email": user.email,
            "created_at": student.created_at
        })

    return students


def get_student_by_id(db, student_id: int) -> Student | None:
    return db.query(Student).filter(Student.student_id == student_id).first()


def get_student_by_user_id(db, user_id):
    return (
        db.query(Student)
        .filter(Student.user_id == user_id)
        .first()
    )
