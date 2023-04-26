from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from database import schemas
from reservation import manager
from database.database import get_db
from auth.manager import get_current_user
from datetime import datetime


router = APIRouter(
    prefix="/reservation",
    tags=["Reservation"],
    responses={404: {"description": "Not found"}},
)


@router.post("/create", response_model=schemas.Reservation)
def create_reservation(reservation: schemas.ReservationCreate, db: Session = Depends(get_db)):
    
    reserva_solicitada = manager.convert_datetime(reservation)

    bottom_limit = datetime.strptime('06:00', '%H:%M').time() 
    upper_limit = datetime.strptime('23:00', '%H:%M').time()

    var_inic = str(reserva_solicitada[0]).split(' ')
    horaCompleta_inic = var_inic[1]
    hour_inic = datetime.strptime(horaCompleta_inic, '%H:%M:%S').time()

    var_fim = str(reserva_solicitada[1]).split(' ')
    horaCompleta_fim = var_fim[1]
    hour_fim = datetime.strptime(horaCompleta_fim, '%H:%M:%S').time()

    if (hour_inic < bottom_limit or hour_inic >= upper_limit) or (hour_fim <= bottom_limit or hour_fim > upper_limit):
        raise HTTPException(
            status_code=400, detail="Can't reservate at this hour")

    if reserva_solicitada[0] >= reserva_solicitada[1]:
        raise HTTPException(
            status_code=400, detail="Time start is higher than time end or time start equals to time end")

    existing_reservations = manager.get_reservations_by_area_id(db, reservation.area_id)
    
    for reservas in existing_reservations:
        reservas_feitas = manager.convert_datetime(reservas)
        
        if (reservas_feitas[0] == reserva_solicitada[0] and reservas_feitas[1] == reserva_solicitada[1]) or (reservas_feitas[0] < reserva_solicitada[0] < reservas_feitas[1] or reservas_feitas[0] < reserva_solicitada[1] < reservas_feitas[1]):
            raise HTTPException(
            status_code=400, detail="Reservation date or hour already in use")


    result = manager.create_reservation(db=db, reservation=reservation)
    if result == None:
        raise HTTPException(
            status_code=400, detail="User or Area doesn't exist try again.")
    
    return result


@router.get("/list", response_model=List[schemas.Reservation])
def read_users(db: Session = Depends(get_db)):
    orders = manager.get_all(db)
    return orders


@router.put("/update/{reservation_id}", response_model=schemas.Reservation)
def update_reservation(reservation_id: str, reservation: schemas.ReservationUpdate, db: Session = Depends(get_db)):
    db_reservation = manager.get_reservation_by_id(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found")

    reserva_solicitada = manager.convert_datetime(reservation)

    bottom_limit = datetime.strptime('06:00', '%H:%M').time() 
    upper_limit = datetime.strptime('23:00', '%H:%M').time()

    var_inic = str(reserva_solicitada[0]).split(' ')
    horaCompleta_inic = var_inic[1]
    hour_inic = datetime.strptime(horaCompleta_inic, '%H:%M:%S').time()

    var_fim = str(reserva_solicitada[1]).split(' ')
    horaCompleta_fim = var_fim[1]
    hour_fim = datetime.strptime(horaCompleta_fim, '%H:%M:%S').time()

    if (hour_inic < bottom_limit or hour_inic >= upper_limit) or (hour_fim <= bottom_limit or hour_fim > upper_limit):
        raise HTTPException(
            status_code=400, detail="Can't reservate at this hour")

    if reserva_solicitada[0] >= reserva_solicitada[1]:
        raise HTTPException(
            status_code=400, detail="Time start is higher than time end or time start equals to time end")

    existing_reservations = manager.get_reservations_by_area_id(db, reservation.area_id)
    
    for reservas in existing_reservations:
        reservas_feitas = manager.convert_datetime(reservas)
        
        if (reservas_feitas[0] == reserva_solicitada[0] and reservas_feitas[1] == reserva_solicitada[1]) or (reservas_feitas[0] < reserva_solicitada[0] < reservas_feitas[1] or reservas_feitas[0] < reserva_solicitada[1] < reservas_feitas[1]):
            raise HTTPException(
            status_code=400, detail="Reservation date or hour already in use")


    updated_reservation = manager.update_reservation(db=db, db_reservation=db_reservation, reservation=reservation)
    return updated_reservation



@router.delete("/delete/{reservation_id}")
def delete_reservation(reservation_id: str, db: Session = Depends(get_db)):
    db_reservation = manager.get_reservation_by_id(db, reservation_id=reservation_id)
    if not db_reservation:
        raise HTTPException(
            status_code=404, detail="Reservation not found")
    manager.delete_reservation(db=db, db_reservation = db_reservation)
    return {"message": "Reservation successfully deleted"}

