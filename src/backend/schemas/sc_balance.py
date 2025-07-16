"""Schema untuk operasi balance publik dan utilitas signature.

Hasan Maki and Copilot
"""

from pydantic import BaseModel, Field

class BalanceCheckRequest(BaseModel):
    """Request schema untuk cek saldo member tanpa signature.

    Args:
        name (str): Nama member.
        pin (str | None): PIN member (opsional).
        password (str | None): Password member (opsional).

    Hasan Maki and Copilot
    """
    name: str = Field(..., min_length=6)
    pin: str | None = None
    password: str | None = None

class BalanceCheckWithSignRequest(BaseModel):
    """Request schema untuk cek saldo member dengan signature.

    Args:
        name (str): Nama member.
        sign (str): Signature hasil hash.

    Hasan Maki and Copilot
    """
    name: str = Field(..., min_length=6)
    sign: str
