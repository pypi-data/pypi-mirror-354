# src/stratio/api/models/customer.py
from typing import Optional

from pydantic import BaseModel, field_serializer

from models.dynamodb import DynamoModel
from models.globals import SubscriptionActionEnum


class SubscriberBase(BaseModel):
    """
    Base representation of a subscriber.
    """

    # mandatory attributes
    customerIdentifier: str
    productCode: str
    # optional attributes
    customerAWSAccountID: Optional[str] = None
    companyName: Optional[str] = None
    contactEmail: Optional[str] = None
    contactPhone: Optional[str] = None
    created: Optional[str] = None
    subscriptionAction: Optional[SubscriptionActionEnum] = None
    subscriptionExpired: Optional[bool] = None
    successfullyRegistered: Optional[bool] = None
    successfullySubscribed: Optional[bool] = None
    isFreeTrialTermPresent: Optional[bool] = None

    @field_serializer("subscriptionAction")
    def serialize_subscription_action(self, v: Optional[SubscriptionActionEnum]) -> Optional[str]:
        return v.value if v is not None else None


class Subscriber(SubscriberBase, DynamoModel):
    """
    Cluster-hub representation of a subscriber.
    """

    # Required fields
    contactName: str


class SubscriberList(BaseModel):
    """
    List of base subscribers query with source and optional error message.
    """

    source: str
    items: list[SubscriberBase]
    error: Optional[str] = None
