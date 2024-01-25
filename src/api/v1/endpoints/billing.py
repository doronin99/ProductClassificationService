from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import db
from src.core.models import User
from src.core.security import JWTBearer
from src.services.billing_service import BillingService

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


@router.get("/points",
            response_model=int,
            summary="Get User Balance",
            description="Get the current balance of the user's points.")
def get_user_balance(
    user: User = Depends(JWTBearer()),
    db: Session = Depends(db.get_db)
):
    """
    Get the current balance of the user's points.

    Args:
        user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        int: The current balance of the user's points.
    """
    return BillingService.get_user_balance(db, user.id)


@router.post("/deduct",
             response_model=dict,
             summary="Deduct Credits",
             description="Deduct credits from the user's balance for a specific reason.")
def deduct_credits(
    points: int,
    reason: str,
    user: User = Depends(JWTBearer()),
    db: Session = Depends(db.get_db)
):
    """
    Deduct credits from the user's balance for a specific reason.

    Args:
        points (int): The number of points to deduct.
        reason (str): The reason for deducting credits.
        user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        dict: Response indicating success or failure.
    """
    success = BillingService.deduct_credits(db, user.id, points, reason)
    return {"success": success, "message": "Credits deducted successfully." if success else "Failed to deduct credits."}


@router.get("/history",
            response_model=dict,
            summary="Get Billing History",
            description="Get the billing history of the user.")
def get_billing_history(
    user: User = Depends(JWTBearer()),
    db: Session = Depends(db.get_db)
):
    """
    Get the billing history of the user.

    Args:
        user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        dict: Response with billing history entries and message.
    """
    history_entries = BillingService.get_billing_history(db, user.id)
    return {"history_entries": history_entries, "message": "Billing history retrieved successfully."}
