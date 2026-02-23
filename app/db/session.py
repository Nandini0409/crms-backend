from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings
from app.models.User import User
from app.models.Teacher import Teacher
from app.models.Student import Student
from app.models.Batch import Batch
from app.models.Attendance import Attendance
from app.models.Enrollment import Enrollment
from app.models.Fee import Fee
from app.models.Payment import Payment
from app.models.TeacherBatch import TeacherBatch
from sqlalchemy.pool import NullPool

engine = create_engine(
    settings.database_url,
    pool_pre_ping=True,
    poolclass=NullPool,  
)

def get_session():
    session = Session(engine)
    try:
        yield session
        session.commit()     
    except Exception:
        session.rollback()  
        raise
    finally:
        session.close()

