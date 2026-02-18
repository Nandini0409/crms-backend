from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from app.core.exception import AuthError, BusinessError
from app.utils.jwt import decode_access_token
from app.repositories.user import get_user_by_id
from app.db.session import get_session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db=Depends(get_session),
):
    print("in the get user fucniton")
    payload = decode_access_token(token)
    user_id = payload.get("user_id")
    if not user_id:
        raise AuthError(
            code="INVALID_TOKEN",
            user_message="Invalid authentication token",
        )

    user = get_user_by_id(db, user_id)
    if not user:
        raise AuthError(
            code="USER_NOT_FOUND",
            user_message="User not found",
        )

    return user



def admin_require(
    current_user=Depends(get_current_user)
):
    if current_user.role != "admin":
        raise BusinessError(
            code="FORBIDDEN",
            user_message="You are not allowed to perform this action",
            dev_message=f"User role is {current_user.role}",
            status_code=403
        )

    return current_user



def teacher_require(
        current_user=Depends(get_current_user)
):
    if current_user.role != "teacher":
        raise BusinessError(
            code="FORBIDDEN",
            user_message="You are not allowed to perform this action",
            dev_message=f"User role is {current_user.role}",
            status_code=403
        )

    return current_user




def student_require(
        current_user=Depends(get_current_user)
):
    print("in student check function")
    if current_user.role != "student":
        raise BusinessError(
            code="FORBIDDEN",
            user_message="You are not allowed to perform this action",
            dev_message=f"User role is {current_user.role}",
            status_code=403
        )

    return current_user