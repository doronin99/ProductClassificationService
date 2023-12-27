from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.core.container import Container
from src.core.dependencies import get_current_active_user
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
    return service.sign_in(user_info)


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
    return service.sign_up(user_info)


@router.get("/me",
            response_model=User,
            summary="Get Current User",
            description="Get information about the currently authenticated user.")
@inject
async def get_me(current_user: User = Depends(get_current_active_user)):
    """
    Get information about the currently authenticated user.

    Args:
        current_user (User): The authenticated user.

    Returns:
        User: Information about the authenticated user.
    """
    return current_user
