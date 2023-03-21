from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import LibroProveedor
from schemas import LibroProveedorBaseModel, LibroProveedorResponseModel, LibroProveedorPutModel


router = APIRouter(
    prefix = '/libroproveedor',
    tags=['libroproveedor']
)


@router.get('/')
async def obtener_compras():
    libroproveedor = LibroProveedor.select()
    libroproveedor = [librop for librop in libroproveedor]
    response = parse_obj_as(List[LibroProveedorResponseModel], libroproveedor)

    return response


@router.post('/')
async def crear_compra(libroproveedor: LibroProveedorBaseModel):
    libroproveedor = LibroProveedor.create(
        id_libro = libroproveedor.id_libro,
        id_proveedor = libroproveedor.id_proveedor,
        cantidad = libroproveedor.cantidad,
        fecha_hora = libroproveedor.fecha_hora,
        subtotal = libroproveedor.subtotal
    )

    return { 
                "Compra de " : libroproveedor.id_libro,
                "A: " : libroproveedor.id_proveedor 
            }


@router.get('/{id}')
async def obtener_compra(id: int):
    libroproveedor = LibroProveedor.select().where(LibroProveedor.id == id).first()

    if libroproveedor is None:
        raise HTTPException(status_code=404, detail='ID de compra inexistente')
    
    response = parse_obj_as(LibroProveedorResponseModel, libroproveedor)

    return response


@router.put('/{id}')
async def modificar_departamento(id: int, compra: LibroProveedorPutModel):
    compra_actual = LibroProveedor.select().where(LibroProveedor.id == id).first()

    if compra_actual is None:
        raise HTTPException(status_code=404, detail='ID de compra inexistente')
    
    compra_actual.cantidad = compra.cantidad
    compra_actual.subtotal = compra.subtotal
    
    compra_actual.save()

    return { "Se actualizo la compra" : compra_actual.id }