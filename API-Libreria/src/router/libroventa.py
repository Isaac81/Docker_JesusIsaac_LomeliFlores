from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import LibroVenta
from schemas import LibroVentaBaseModel, LibroVentaResponseModel


router = APIRouter(
    prefix = '/libroventa',
    tags=['libroventa']
)


@router.get('/')
async def obtener_libroventa_all():
    libroventa = LibroVenta.select()
    libroventa = [venta for venta in libroventa]
    response = parse_obj_as(List[LibroVentaResponseModel], libroventa)

    return response


@router.post('/')
async def crear_libroventa(libroventa: LibroVentaBaseModel):
    libroventa = LibroVenta.create(
        id_libro = libroventa.id_libro,
        id_venta = libroventa.id_venta,
        cantidad = libroventa.cantidad,
        subtotal = libroventa.subtotal
    )

    return { "Venta creada" : libroventa.id }


@router.get('/{id}')
async def obtener_libroventa(id: int):
    libroventa = LibroVenta.select().where(LibroVenta.id == id).first()

    if libroventa is None:
        raise HTTPException(status_code=404, detail='ID de venta de libro inexistente')
    
    response = parse_obj_as(LibroVentaResponseModel, libroventa)

    return response


@router.put('/{id}')
async def modificar_libroventa(id: int, venta:LibroVentaBaseModel):
    venta_actual = LibroVenta.select().where(LibroVenta.id == id).first()

    if venta_actual is None:
        raise HTTPException(status_code=404, detail='ID de venta de libro inexistente')
    
    venta_actual.id_libro = venta.id_libro
    venta_actual.id_venta = venta.id_venta
    venta_actual.cantidad = venta.cantidad
    venta_actual.subtotal = venta.subtotal
    
    venta_actual.save()

    return { "Se actualizo la venta del libro" : venta_actual.id }
