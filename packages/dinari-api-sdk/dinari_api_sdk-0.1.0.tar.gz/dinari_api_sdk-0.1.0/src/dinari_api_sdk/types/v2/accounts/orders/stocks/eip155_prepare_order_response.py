# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List
from typing_extensions import Literal

from ......_models import BaseModel

__all__ = ["Eip155PrepareOrderResponse", "Fee", "TransactionData"]


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


class TransactionData(BaseModel):
    abi: object
    """
    [JSON ABI](https://docs.soliditylang.org/en/v0.8.30/abi-spec.html#json) of the
    smart contract function encoded in the transaction. Provided for informational
    purposes.
    """

    args: object
    """Arguments to the smart contract function encoded in the transaction.

    Provided for informational purposes.
    """

    contract_address: str
    """Smart contract address that the transaction should call."""

    data: str
    """Hex-encoded function call."""


class Eip155PrepareOrderResponse(BaseModel):
    fees: List[Fee]
    """Fees included in the order transaction. Provided here as a reference."""

    transaction_data: List[TransactionData]
    """
    List of contract addresses and call data for building transactions to be signed
    and submitted on chain. Transactions should be submitted on chain in the order
    provided in this property.
    """
