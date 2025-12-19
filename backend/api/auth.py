"""
인증 관련 API 라우터
"""
from fastapi import APIRouter, HTTPException
from datetime import datetime
import logging

from models.schemas import (
    LoginRequest,
    LoginResponse,
    ErrorResponse
)
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

router = APIRouter(
    tags=["Authentication"]
)


@router.post(
    "/login",
    response_model=LoginResponse,
    responses={
        401: {"model": ErrorResponse, "description": "인증 실패"}
    },
    summary="로그인",
    description="사용자 로그인 및 JWT 토큰 발급"
)
def login(request: LoginRequest):
    """
    ## 로그인 API

    사용자 인증 후 JWT 토큰을 발급합니다.

    **예시 요청:**
    ```json
    {
      "email": "user@example.com",
      "password": "your_secure_password"
    }
    ```
    """
    try:
        logger.info(f"로그인 시도: {request.email}")

        # AuthService를 통해 사용자 인증
        user = AuthService.authenticate_user(request.email, request.password)

        if not user:
            raise HTTPException(
                status_code=401,
                detail={
                    "success": False,
                    "error": {
                        "code": "UNAUTHORIZED",
                        "message": "이메일 또는 비밀번호가 올바르지 않습니다",
                        "timestamp": datetime.now().isoformat()
                    }
                }
            )

        # Access Token 생성
        token_data = AuthService.create_access_token(user)

        return {
            "success": True,
            "data": token_data
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"로그인 실패: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "로그인 처리 중 오류 발생",
                    "details": {"error": str(e)},
                    "timestamp": datetime.now().isoformat()
                }
            }
        )


@router.post(
    "/refresh",
    summary="토큰 갱신",
    description="만료된 토큰을 갱신합니다"
)
def refresh_token():
    """
    ## 토큰 갱신 API

    Refresh token을 사용하여 새로운 access token을 발급받습니다.

    **예시 요청:**
    ```json
    {
      "refresh_token": "your_refresh_token"
    }
    ```
    """
    # TODO: Refresh token 검증 및 새 토큰 발급
    return {
        "success": True,
        "message": "Token refresh not implemented yet"
    }
