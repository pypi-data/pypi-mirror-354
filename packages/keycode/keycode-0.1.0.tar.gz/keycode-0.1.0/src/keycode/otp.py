import pyotp
import time


def get_otp(secret: str) -> tuple[str, int]:
    """Get the current OTP and the time remaining."""
    totp = pyotp.TOTP(secret)
    otp = totp.now()
    time_remaining = int(totp.interval - (time.time() % totp.interval))
    return otp, time_remaining
