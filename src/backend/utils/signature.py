import base64
import hashlib


def generate_signature(data: str) -> str:
    """Generate OtomaX-style signature dari input string.

    Args:
        data (str): String yang akan di-hash, formatnya harus sesuai.

    Returns:
        str: Signature base64-url-safe
    """
    sha1_bytes = hashlib.sha1(data.encode()).digest()
    b64_encoded = base64.b64encode(sha1_bytes).decode()
    # Format ke base64-url-safe (ganti + dan /, hapus =)
    return b64_encoded.replace("+", "-").replace("/", "_").rstrip("=")


def generate_transaction_signature(
    member_id: str, product: str, dest: str, ref_id: str, pin: str, password: str
) -> str:
    """Generate signature untuk transaksi OtomaX."""
    data = f"OtomaX|{member_id}|{product}|{dest}|{ref_id}|{pin}|{password}"
    return generate_signature(data)


def generate_check_balance_signature(member_id: str, pin: str, password: str) -> str:
    """Generate check balance signature."""
    data = f"OtomaX|CheckBalance|{member_id}|{pin}|{password}"
    return generate_signature(data)
