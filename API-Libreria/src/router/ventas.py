from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import Ventas
from schemas import VentaBaseModel, VentaResponseModel


router = APIRouter(
    prefix = '/ventas',
    tags=['ventas']
)


@router.get('/')
async def obtener_ventas():
    ventas = Ventas.select()
    ventas = [venta for venta in ventas]
    response = parse_obj_as(List[VentaResponseModel], ventas)

    return response


@router.post('/')
async def crear_venta(venta: VentaBaseModel):
    venta = Ventas.create(
        monto_total = venta.monto_total,
        fecha_hora = venta.fecha_hora,
        id_empleado = venta.id_empleado
    )

    return { "Venta creada" : venta.id }


@router.get('/{id}')
async def obtener_venta(id: int):
    venta = Ventas.select().where(Ventas.id == id).first()

    if venta is None:
        raise HTTPException(status_code=404, detail='ID de venta inexistente')
    
    response = parse_obj_as(VentaResponseModel, venta)

    return response


@router.put('/{id}')
async def modificar_venta(id: int, venta: VentaBaseModel):
    venta_actual = Ventas.select().where(Ventas.id == id).first()

    if venta_actual is None:
        raise HTTPException(status_code=404, detail='ID de venta inexistente')
    
    venta_actual.monto_total = venta.monto_total
    venta_actual.fecha_total = venta.fecha_total
    venta_actual.id_empleado = venta.id_empleado
    
    venta_actual.save()

    return { "Se actualizo la venta" : venta_actual.id }


@router.delete('/{id}')
async def eliminar_venta(id: int):
    venta = Ventas.select().where(Ventas.id == id).first()

    if venta is None:
        raise HTTPException(status_code=404, detail='Venta inexistente')
    
    venta.delete_instance()

    return { "Se elimino la venta" : id }



