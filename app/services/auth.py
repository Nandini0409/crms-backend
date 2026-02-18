from ..repositories.user import (
    get_user_by_email, 
    update_user_password,
    get_user_by_id
)
from app.repositories.student import get_student_by_user_id
from app.repositories.teacher import get_teacher_by_user_id
from ..utils.password import verify_password
from ..utils.jwt import create_access_token
from app.core.exception import AuthError
import logging

logger = logging.getLogger(__name__)




def get_my_profile_service(db, user):
    user = get_user_by_id(db, user.user_id)
    if not user:
        raise AuthError(
            code="USER_NOT_FOUND",
            user_message="User profile not found"
        )

    if user.role == "student":
        student = get_student_by_user_id(db, user.user_id)
        if not student:
            raise AuthError(
                code="STUDENT_NOT_FOUND",
                user_message="Student profile not found"
            )

        return {
            "name": student.name,
            "email": user.email,
            "role": user.role
        }

    elif user.role == "teacher":
        teacher = get_teacher_by_user_id(db, user.user_id)
        if not teacher:
            raise AuthError(
                code="TEACHER_NOT_FOUND",
                user_message="Teacher profile not found"
            )

        return {
            "name": teacher.name,
            "email": user.email,
            "role": user.role
        }

    # elif user.role == "admin":
    #     admin = get_admin_by_user_id(db, user.user_id)
    #     if not admin:
    #         raise AuthError(
    #             code="ADMIN_NOT_FOUND",
    #             user_message="Admin profile not found"
    #         )

    #     return {
    #         "name": admin.name,
    #         "email": user.email,
    #         "role": user.role
    #     }

    else:
        raise AuthError(
            code="INVALID_ROLE",
            user_message="Invalid user role"
        )






def login_service(data, db):
    user = get_user_by_email(db, data.email)
    if not user:
        logger.warning(
            "Invalid login attempt - user not found",
            extra={"email": data.email},
        )
        raise AuthError(
            code="INVALID_CREDENTIALS",
            user_message="Invalid email or password",
            dev_message=f"User not found for email: {data.email}",
        )

    if not verify_password(data.password, user.password_hash):
        logger.warning(
            "Invalid login attempt - password mismatch",
            extra={"user_id": str(user.user_id)},
        )
        raise AuthError(
            code="INVALID_CREDENTIALS",
            user_message="Invalid email or password",
            dev_message=f"Password mismatch for user_id: {user.user_id}",
        )

    print(user.is_first_login)
    if user.is_first_login:
        logger.info(
            "First login detected",
            extra={"user_id": str(user.user_id)},
        )
        return {
                "user_id": user.user_id,
                "role": user.role,
                "email": user.email,
                "force_password_change": True,
            }
    

    access_token = create_access_token(
        data={"user_id": str(user.user_id), "role": user.role}
    )

    logger.info(
        "User logged in successfully",
        extra={"user_id": str(user.user_id)},
    )

    return {
            "user_id": user.user_id,
            "email": user.email,
            "role": user.role,
            "access_token": access_token,
        }
    




def force_change_password_service(data, db):
    user = get_user_by_email(db, data.email)
    if not user:
        logger.warning(
            "Force change password attempt - user not found",
            extra={"email": data.email},
        )
        raise AuthError(
            code="USER_NOT_FOUND",
            user_message="User not found",
            dev_message=f"User not found for email: {data.email}",
        )

    if not verify_password(data.current_password, user.password_hash):
        logger.warning(
            "Force change password attempt - current password mismatch",
            extra={"user_id": str(user.user_id)},
        )
        raise AuthError(
            code="INVALID_CREDENTIALS",
            user_message="Current password is incorrect",
            dev_message=f"Current password mismatch for user_id: {user.user_id}",
        )

    updated_user = update_user_password(db, user, data.new_password)

    access_token = create_access_token(
        data={"user_id": str(updated_user.user_id), "role": updated_user.role}
    )

    logger.info(
        "Password changed successfully",
        extra={"user_id": str(updated_user.user_id)},
    )

    return {
            "user_id": updated_user.user_id,
            "role": updated_user.role,
            "access_token": access_token,
            "force_password_change": False,
        }
