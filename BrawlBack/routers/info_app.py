from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
from schemas.info import Token
from security.dependence import Security
from db.connections import Connections

router = APIRouter(prefix="/app", tags=["app"])

responss = {
    424: {"description":"cant connect with database"},
    403: {"description": "Not enough privileges"},
}

@router.post("/signup", response_model=Token, 
             status_code=status.HTTP_201_CREATED,
             responses={**responss,400:{"description": 
                 "insecure password or user already used"}})
async def signup(form: Annotated[OAuth2PasswordRequestForm, Depends()],
                 response: Response):
    if len(form.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="insecure password"
        )
    if await Connections.if_user(form.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="user already used"
        )
    password = await Security.get_password_hash(form.password)
    await Connections.insert_user(form.username, password)
    response.status_code = status.HTTP_201_CREATED
    return await Security.create_token(form.username)

@router.post("/login", response_model=Token, 
             status_code=status.HTTP_200_OK,
             responses={**responss,
                        400:{"description":"incorrect user or password"}})
async def login(form: Annotated[OAuth2PasswordRequestForm, Depends()]):
    if not await Connections.if_user(form.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="incorrect user or password"
        )
    await Security.verify_password(form.password, form.username)
    return await Security.create_token(form.username)