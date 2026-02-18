from ..models.User import User
from ..utils.password import hash_password

def get_user_by_email(db, email: str):
    return db.query(User).filter(User.email == email).first()

def get_user_by_id(db, user_id: int) -> User | None:
    return db.query(User).filter(User.user_id == user_id).first()

def update_user_password(db, user: User, new_password: str):
    user.password_hash = hash_password(new_password)
    user.is_first_login = False
    db.flush()
    db.refresh(user)
    return user


def create_user(
    db,
    *,
    email: str,
    password_hash: str,
    role: str
) -> User:
    user = User(
        email=email,
        password_hash=password_hash,
        role=role,
        is_first_login=True,
    )
    db.add(user)
    db.flush()
    db.refresh(user)
    return user