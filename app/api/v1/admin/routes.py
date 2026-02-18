from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.request import (
    CreateStudentRequest,
    CreateTeacherRequest,
    CreateBatchRequest,
    CreateEnrollmentRequest, 
    AssignTeacherBatchRequest, 
    CreateFeeRequest,
    CreatePaymentRequest
)
from app.schemas.base import(
    APIResponse
)
from app.services.admin import (
    get_dashboard_data_service,
    create_student_service,
    create_teacher_service,
    get_all_students_service,
    get_all_teachers_service,
    create_batch_service,
    get_all_batch_service,
    enroll_student_service,
    assign_teacher_batch_service, 
    create_fee_service,
    get_batch_fee_service,
    create_payment_service,
    get_all_payment_service,
    get_teachers_with_batchid_service,
    get_students_with_batchid_service
)
from app.db.session import get_session
from app.core.deps import admin_require


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)




@router.get("/dashboard", response_model=APIResponse)
def get_dashboard_data_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_dashboard_data_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }


@router.post("/student", response_model=APIResponse)
def create_student_route(
    data: CreateStudentRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require),
):
    result = create_student_service(db, data)
    return {
        "success": True,
        "message": "Student created successfully",
        "detail": result
    }


@router.get("/student", response_model=APIResponse)
def get_all_student_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    print("hii")
    result = get_all_students_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }


@router.post("/teacher", response_model=APIResponse)
def create_teacher_route(
    data: CreateTeacherRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = create_teacher_service(db, data)
    return {
        "success": True,
        "message": "Teacher created successfully",
        "detail": result
    }


@router.get("/teacher", response_model=APIResponse)
def get_all_teachers_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_all_teachers_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }







@router.post("/batch", response_model=APIResponse)
def create_batch_route(
    data: CreateBatchRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require),
):
    result = create_batch_service(db, data)
    return {
        "success": True,
        "message": "Batch created successfully",
        "detail": result
    }



@router.get("/batch", response_model=APIResponse)
def get_all_batch_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_all_batch_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }


@router.get("/batch/{batch_id}/teachers", response_model=APIResponse)
def get_teachers_with_batchid_route(
    batch_id,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_teachers_with_batchid_service(db, batch_id)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }



@router.get("/batch/{batch_id}/students", response_model=APIResponse)
def get_students_with_batchid_route(
    batch_id,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_students_with_batchid_service(db, batch_id)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }





@router.post("/enrollment", response_model=APIResponse)
def enroll_student_route(
    data: CreateEnrollmentRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = enroll_student_service(db, data)
    return {
        "success": True,
        "message": "Enrollment successful.",
        "detail": result
    }




@router.post("/teacher-batch", response_model=APIResponse)
def assign_teacher_batch_route(
    data: AssignTeacherBatchRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = assign_teacher_batch_service(db, data)
    return {
        "success": True,
        "message": "Assigned teacher to batch successfully.",
        "detail": result
    }



@router.post("/fees", response_model=APIResponse)
def create_fees_route(
    data: CreateFeeRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = create_fee_service(db, data)
    return {
        "success": True,
        "message": "Added fee record successfully.",
        "detail": result
    }




@router.get("/fees", response_model=APIResponse)
def get_batch_fee_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_batch_fee_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }




@router.post("/payments", response_model=APIResponse)
def create_payments_route(
    data: CreatePaymentRequest,
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = create_payment_service(db, data)
    return {
        "success": True,
        "message": "Added payment record successfully.",
        "detail": result
    }




@router.get("/payments", response_model=APIResponse)
def get_all_payment_route(
    db: Session = Depends(get_session),
    _=Depends(admin_require)
):
    result = get_all_payment_service(db)
    return {
        "success": True,
        "message": "Successful response",
        "detail": result
    }



