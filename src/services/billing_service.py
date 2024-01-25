from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.core.models import User, BillingHistory


class BillingService:
    @staticmethod
    def get_user_balance(db: Session, user_id: int):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            return user.billing.points
        return None

    @staticmethod
    def deduct_credits(db: Session, user_id: int, points: int, reason: str):
        user = db.query(User).filter(User.id == user_id).first()
        if user:
            if user.billing.points >= points:
                user.billing.points -= points
                db.commit()

                # Log the transaction in billing history
                billing_history = BillingHistory(
                    user_id=user_id,
                    points_changed=-points,
                    reason=reason
                )
                db.add(billing_history)
                db.commit()

                return True
            else:
                raise HTTPException(status_code=400, detail="Insufficient credits")
        else:
            raise HTTPException(status_code=404, detail="User not found")

    @staticmethod
    def get_billing_history(db: Session, user_id: int):
        return db.query(BillingHistory).filter(BillingHistory.user_id == user_id).all()
