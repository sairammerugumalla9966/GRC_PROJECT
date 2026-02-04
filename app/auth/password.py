from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def _truncate_password(password: str) -> str:
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        password_bytes = password_bytes[:72]
    return password_bytes.decode("utf-8", errors="ignore")

def hash_password(password: str) -> str:
    safe_password = _truncate_password(password)
    return pwd_context.hash(safe_password)

def verify_password(password: str, hashed: str) -> bool:
    safe_password = _truncate_password(password)
    return pwd_context.verify(safe_password, hashed)
