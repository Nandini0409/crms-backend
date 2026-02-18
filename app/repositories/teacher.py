from app.models.Teacher import Teacher
from sqlmodel import Session, select
from sqlalchemy import func
from app.models.User import User


def count_total_teachers(db: Session) -> int:
    statement = select(func.count(Teacher.teacher_id))
    result = db.exec(statement)
    return result.one()



def create_teacher(
    db,
    *,
    user_id,
    name: str,
    phone: str | None
) -> Teacher:
    teacher = Teacher(
        user_id=user_id,
        name=name,
        phone=phone,
    )
    db.add(teacher)
    db.flush()
    db.refresh(teacher)
    return teacher

def get_teacher_by_user_id(db, user_id):
    return (
        db.query(Teacher)
        .filter(Teacher.user_id == user_id)
        .first()
    )



def get_all_teachers(db: Session) :
    statement = (
        select(Teacher, User)
        .join(User, Teacher.user_id == User.user_id)
    )

    results = db.exec(statement).all()

    teachers = []

    for teacher, user in results:
        print(teacher)
        teachers.append({
            "teacher_id": teacher.teacher_id,
            "name": teacher.name,
            "phone": teacher.phone,
            "email": user.email,
            "created_at": teacher.created_at
        })

    return teachers


def get_teacher_by_id(db, teacher_id: int) -> Teacher | None:
    return db.query(Teacher).filter(Teacher.teacher_id == teacher_id).first()