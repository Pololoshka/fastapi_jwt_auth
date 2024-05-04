from datetime import UTC, datetime, timedelta

from jose import jwt
from passlib.context import CryptContext

from src.settings import AuthenticationSettings


class AuthenticateHandler:
    def __init__(self, pwd_context: CryptContext, auth_settings: AuthenticationSettings) -> None:
        self.pwd_context = pwd_context
        self.settings = auth_settings

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return self.pwd_context.verify(secret=plain_password, hash=hashed_password)  # type: ignore[no-any-return]

    def create_access_token(self, data: dict, *, expires_delta: timedelta | None = None) -> str:
        to_encode = data.copy()
        delta = expires_delta or timedelta(minutes=self.settings.access_token_expire_minutes)
        expire = datetime.now(UTC) + delta
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, self.settings.secret_key, algorithm=self.settings.algorithm)  # type: ignore[no-any-return]
