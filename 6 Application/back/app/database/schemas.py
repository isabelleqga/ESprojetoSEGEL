from pydantic import BaseModel, Field
import datetime

class ReservationBase(BaseModel):
    value: int | None = None
    reservation_date: str
    time_start: str
    time_end: str
    justification: str
    reservation_type: str 
    status: str   

class ReservationCreate(BaseModel):
    value: int | None = None
    reservation_date: str
    time_start: str
    time_end: str
    justification: str
    reservation_type: str
    area_id: str
    account_id: str    

    class Config:
        orm_mode = True

class Reservation(ReservationBase):
    area_id: str
    account_id: str

    class Config:
        orm_mode = True


class ReservationUpdate(BaseModel):
    value: int | None = None
    reservation_date: str
    time_start: str
    time_end: str
    justification: str
    reservation_type: str
    status: str
    area_id: str
    account_id: str

class AreaBase(BaseModel):
    name: str

class Area(AreaBase):
    description: str
    available: bool
    lighting: str
    floor_type: str
    covered: str
    photo_url: str
    account_id: str | None = None

    reservations = list[Reservation]

    class Config:
        orm_mode = True

class AreaCreation(AreaBase):
    description: str
    available: bool
    lighting: str
    floor_type: str
    covered: str
    photo_url: str
    account_id: str | None = None

    class Config:
        orm_mode = True

class AreaUpdate(BaseModel):
    name: str 
    description: str 
    available: bool 
    lighting: str
    floor_type: str
    covered: str
    photo_url: str
    account_id: str

    class Config:
        orm_mode = True

class AreaDelete(BaseModel):
    account_id: str

    class Config:
        orm_mode = True


class AccountBase(BaseModel):
    pass

class Account(AccountBase):
    cpf: str
    name: str
    email: str
    hashed_password: str
    user_type: str
    available: bool
    phone_number: str
    

    reservations = list[Reservation]
    areas = list[Area]
    
    
    class Config:
        orm_mode = True

class AccountCreation(AccountBase):
    cpf: str
    name: str
    email: str
    hashed_password: str
    user_type: str
    phone_number: str

    class Config:
        orm_mode = True

class AccountUpdate(BaseModel):
    name: str
    email: str
    hashed_password: str
    phone_number: str
    
    class Config:
        orm_mode = True

class AccountDelete(BaseModel):
    available: bool

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
    user: object


class TokenData(BaseModel):
    email: str | None = None


class AccountInDB(Account):
    hashed_password: str