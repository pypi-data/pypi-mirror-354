# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from datetime import datetime
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ......_models import BaseModel

__all__ = ["Eip155PrepareProxiedOrderResponse", "Fee", "OrderTypedData", "PermitTypedData"]


class Fee(BaseModel):
    fee_in_eth: float
    """
    The quantity of the fee paid via payment token in
    [ETH](https://ethereum.org/en/developers/docs/intro-to-ether/#what-is-ether).
    """

    fee_in_wei: str
    """
    The quantity of the fee paid via payment token in
    [wei](https://ethereum.org/en/developers/docs/intro-to-ether/#denominations).
    """

    type: Literal["SPONSORED_NETWORK", "NETWORK", "TRADING", "ORDER", "PARTNER_ORDER", "PARTNER_TRADING"]
    """Type of fee."""


class OrderTypedData(BaseModel):
    domain: object
    """Domain separator for the typed data."""

    message: object
    """Message to be signed.

    Contains the actual data that will be signed with the wallet.
    """

    primary_type: str = FieldInfo(alias="primaryType")
    """Primary type of the typed data."""

    types: object
    """Types used in the typed data."""


class PermitTypedData(BaseModel):
    domain: object
    """Domain separator for the typed data."""

    message: object
    """Message to be signed.

    Contains the actual data that will be signed with the wallet.
    """

    primary_type: str = FieldInfo(alias="primaryType")
    """Primary type of the typed data."""

    types: object
    """Types used in the typed data."""


class Eip155PrepareProxiedOrderResponse(BaseModel):
    id: str
    """ID of the EvmPreparedProxiedOrder."""

    deadline: datetime
    """Deadline for the prepared order to be placed."""

    fees: List[Fee]
    """Fees involved in the order. Provided here as a reference."""

    order_typed_data: OrderTypedData
    """
    [EIP-712](https://eips.ethereum.org/EIPS/eip-712) typed data to be signed with a
    wallet.
    """

    permit_typed_data: PermitTypedData
    """
    [EIP-712](https://eips.ethereum.org/EIPS/eip-712) typed data to be signed with a
    wallet.
    """
