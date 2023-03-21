from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import Departamentos
from schemas import DepartamentoBaseModel, DepartamentoResponseModel


router = APIRouter(
    prefix = '/departamentos',
    tags=['departamentos']
)


@router.get('/')
async def obtener_departamentos():
    departamentos = Departamentos.select()
    departamentos = [departamento for departamento in departamentos]
    response = parse_obj_as(List[DepartamentoResponseModel], departamentos)

    return response


@router.post('/')
async def crear_departamento(departamento: DepartamentoBaseModel):
    departamento_busqueda = Departamentos.select().where(Departamentos.nombre_departamento == departamento.nombre_departamento).first()
    if departamento_busqueda is not None:
        raise HTTPException(status_code=404, detail='Nombre de departamento duplicado')
    
    departamento = Departamentos.create(
        nombre_departamento=departamento.nombre_departamento
    )

    return { "id" : departamento.id }


@router.get('/id/{id}')
async def obtener_departamento(id: int):
    departamento = Departamentos.select().where(Departamentos.id == id).first()

    if departamento is None:
        raise HTTPException(status_code=404, detail='ID de departamento inexistente')
    
    response = parse_obj_as(DepartamentoResponseModel, departamento)

    return response


@router.get('/nombre/{nombre}')
async def obtener_departamento_nombre(nombre: str):
    departamentos = Departamentos.select().where(Departamentos.nombre_departamento ** ('%' + nombre + '%'))
    departamentos = [departamento for departamento in departamentos]
    response = parse_obj_as(List[DepartamentoResponseModel], departamentos)
    
    return response


@router.put('/{id}')
async def modificar_departamento(id: int, departamento: DepartamentoBaseModel):
    departamento_actual = Departamentos.select().where(Departamentos.id == id).first()
    departamento_busqueda = Departamentos.select().where(Departamentos.nombre_departamento == departamento.nombre_departamento).first()
    if departamento_actual is None:
        raise HTTPException(status_code=404, detail='ID de departamento inexistente')
    
    if departamento_busqueda is not None:
        raise HTTPException(status_code=404, detail='El nombre de departamento ya existe')
    
    departamento_actual.nombre_departamento = departamento.nombre_departamento
    
    departamento_actual.save()

    return { "Id_modificado" : departamento_actual.id }


@router.delete('/{id}')
async def eliminar_departamento(id: int):
    departamento = Departamentos.select().where(Departamentos.id == id).first()

    if departamento is None:
        raise HTTPException(status_code=404, detail='Departamento inexistente')
    
    departamento.delete_instance()

    return { "Id_eliminado" : id }