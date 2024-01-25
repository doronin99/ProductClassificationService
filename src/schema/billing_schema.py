from pydantic import BaseModel
from datetime import datetime


class BillingHistory(BaseModel):
    BillingHistoryID: int
    BillingID: int
    PointsChanged: int
    Reason: str
    ChangedAt: datetime
