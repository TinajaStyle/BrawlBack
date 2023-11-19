from fastapi import Depends, HTTPException, status, WebSocketException
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from datetime import datetime, timedelta
from decouple import config
from db.connections import Connections
from jose import jwt, JWTError
import bcrypt

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/app/signup")


class Security:
    __algorithm = config("ALGORITHM")
    __exp_time = 2
    __key = config("UNLOCK")

    @classmethod
    async def create_token(cls, username: str):
        time = datetime.utcnow() + timedelta(days=cls.__exp_time)
        acces = {"sub": username, "exp": time}
        access_token = jwt.encode(
            claims=acces, algorithm=cls.__algorithm, key=cls.__key
        )
        return {"access_token": access_token, "token_type": "bearer"}

    @classmethod
    async def verify_token(cls, token: Annotated[str, Depends(oauth2_scheme)] = None):
        try:
            username = jwt.decode(token, key=cls.__key, algorithms=cls.__algorithm).get("sub")
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="expired or invalid jwt"
            )
            
        await Connections.is_disable(username)
        return username
    
    @classmethod
    async def verify_token_ws(cls, token:str):
        try:
            username = jwt.decode(token, key=cls.__key, algorithms=cls.__algorithm).get("sub")
        except JWTError:
            raise WebSocketException(
                code = status.WS_1008_POLICY_VIOLATION,
                reason="expired or invalid jwt"
            )     
        await Connections.is_disable(username)
        return username

    @classmethod
    async def get_password_hash(cls, password: str):
        password = password.encode('utf-8')
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password, salt)

    @classmethod
    async def verify_password(cls, password: str, username: str):
        password = password.encode('utf-8')
        hashed_password = await Connections.get_password(username)
        hashed_password = hashed_password.encode('utf-8')
        if not bcrypt.checkpw(password, hashed_password):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="incorrect user or password",
                )