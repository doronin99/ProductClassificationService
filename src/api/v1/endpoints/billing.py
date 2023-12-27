from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.core.database import db
from src.core.dependencies import get_current_user
from src.core.models import User
from src.schema.billing_schema import BillingHistory
from src.services.billing_service import BillingService

router = APIRouter(
    prefix="/billing",
    tags=["billing"],
)


@router.get("/points",
            response_model=int,
            summary="Get User Balance",
            description="Get the current balance of the user's points.")
def get_user_balance(user: User = Depends(get_current_user), db: Session = Depends(db.get_db)):
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
             response_model=bool,
             summary="Deduct Credits",
             description="Deduct credits from the user's balance for a specific reason.")
def deduct_credits(points: int, reason: str, user: User = Depends(get_current_user), db: Session = Depends(db.get_db)):
    """
    Deduct credits from the user's balance for a specific reason.

    Args:
        points (int): The number of points to deduct.
        reason (str): The reason for deducting credits.
        user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        bool: True if credits were successfully deducted, False otherwise.
    """
    return BillingService.deduct_credits(db, user.id, points, reason)


@router.get("/history",
            response_model=list[BillingHistory],
            summary="Get Billing History",
            description="Get the billing history of the user.")
def get_billing_history(user: User = Depends(get_current_user), db: Session = Depends(db.get_db)):
    """
    Get the billing history of the user.

    Args:
        user (User): The authenticated user.
        db (Session): The database session.

    Returns:
        List[BillingHistory]: The list of billing history entries.
    """
    return BillingService.get_billing_history(db, user.id)
