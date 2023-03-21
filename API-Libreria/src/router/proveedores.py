from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import Proveedores
from schemas import ProveedorBaseModel, ProveedorResponseModel


router = APIRouter(
    prefix = '/proveedores',
    tags=['proveedores']
)

@router.get('/')
async def obtener_proveedores():
    proveedores = Proveedores.select()
    proveedores = [proveedor for proveedor in proveedores]
    response = parse_obj_as(List[ProveedorResponseModel], proveedores)

    return response


@router.post('/')
async def crear_proveedor(proveedor: ProveedorBaseModel):
    proveedor = Proveedores.create(
        nombre_proveedor = proveedor.nombre_proveedor,
        direccion_proveedor = proveedor.direccion_proveedor,
        telefono_proveedor = proveedor.telefono_proveedor
    )

    return { "Proveedor creado" : proveedor.id }


@router.get('/id/{id}')
async def obtener_proveedor(id: int):
    proveedor = Proveedores.select().where(Proveedores.id == id).first()

    if proveedor is None:
        raise HTTPException(status_code=404, detail='ID de proveedor inexistente')
    
    response = parse_obj_as(ProveedorResponseModel, proveedor)

    return response


@router.get('/nombre/{nombre}')
async def obtener_proveedor_nombre(nombre: str):
    proveedores = Proveedores.select().where(Proveedores.nombre_proveedor ** ('%' + nombre + '%'))
    proveedores = [proveedor for proveedor in proveedores]
    response = parse_obj_as(List[ProveedorResponseModel], proveedores)
    
    return response


@router.put('/{id}')
async def modificar_proveedor(id: int, proveedor: ProveedorBaseModel):
    proveedor_actual = Proveedores.select().where(Proveedores.id == id).first()

    if proveedor_actual is None:
        raise HTTPException(status_code=404, detail='ID de proveedor inexistente')
    
    proveedor_actual.nombre_proveedor = proveedor.nombre_proveedor
    proveedor_actual.direccion_proveedor = proveedor.direccion_proveedor
    proveedor_actual.telefono_proveedor = proveedor.telefono_proveedor

    proveedor_actual.save()

    return { "Se actualizo el proveedor" : proveedor_actual.id }


@router.delete('/{id}')
async def eliminar_proveedor(id: int):
    proveedor = Proveedores.select().where(Proveedores.id == id).first()

    if proveedor is None:
        raise HTTPException(status_code=404, detail='Proveedor inexistente')
    
    proveedor.delete_instance()

    return { "Se elimino el proveedor" : id }