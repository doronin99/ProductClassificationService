from fastapi import APIRouter, Depends
from src.core.security import JWTBearer, create_access_token
from dependency_injector.wiring import Provide, inject

from src.core.container import Container
from src.schema.auth_schema import SignIn, SignInResponse, SignUp
from src.schema.user_schema import User
from src.services.auth_service import AuthService

router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@router.post("/sign-in",
             response_model=SignInResponse,
             summary="Sign In",
             description="Sign in and get an access token.")
@inject
async def sign_in(user_info: SignIn, service: AuthService = Depends(Provide[Container.auth_service])):
    """
    Sign in and get an access token.

    Args:
        user_info (SignIn): User credentials for sign-in.
        service (AuthService): Authentication service.

    Returns:
        SignInResponse: Information about the signed-in user.
    """
    response = service.sign_in(user_info)
    access_token, expiration_datetime = create_access_token(response)
    return {"user_info": response,
            "message": "Sign in successful!",
            "access_token": access_token,
            "token_expires": expiration_datetime}


@router.post("/sign-up",
             response_model=User,
             summary="Sign Up",
             description="Sign up and create a new user.")
@inject
async def sign_up(user_info: SignUp, service: AuthService = Depends(Provide[Container.auth_service])):
    """
    Sign up and create a new user.

    Args:
        user_info (SignUp): User information for sign-up.
        service (AuthService): Authentication service.

    Returns:
        User: Information about the newly created user.
    """
    response = service.sign_up(user_info)
    access_token, expiration_datetime = create_access_token(response)
    return {"user_info": response,
            "message": "User registration successful!",
            "access_token": access_token,
            "token_expires": expiration_datetime}


@router.get("/me",
            response_model=User,
            summary="Get Current User",
            description="Get information about the currently authenticated user.")
@inject
async def get_me(current_user: User = Depends(JWTBearer())):
    """
    Get information about the currently authenticated user.

    Args:
        current_user (User): The authenticated user.

    Returns:
        User: Information about the authenticated user.
    """
    return current_user
