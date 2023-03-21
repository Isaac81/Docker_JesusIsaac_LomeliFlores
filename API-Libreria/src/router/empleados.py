from pydantic import parse_obj_as
from fastapi import APIRouter, HTTPException
from typing import List

from config.database import Empleados
from schemas import EmpleadoBaseModel, EmpleadoResponseModel

router = APIRouter(
    prefix = '/empleados',
    tags = ['empleados']
)


@router.get('/')
async def obtener_empleados():
    empleados = Empleados.select()
    empleados = [empleado for empleado in empleados]
    response = parse_obj_as(List[EmpleadoResponseModel], empleados)

    return response


@router.post('/')
async def crear_empleado(empleado: EmpleadoBaseModel):
    usuario_busqueda = Empleados.select().where(Empleados.usuario == empleado.usuario).first()
    if usuario_busqueda is not None:
        raise HTTPException(status_code=404, detail='Ya existe el usuario')
    
    empleado = Empleados.create(
        nombre_empleado = empleado.nombre_empleado,
        appaterno_empleado = empleado.appaterno_empleado,
        apmaterno_empleado = empleado.apmaterno_empleado,
        direccion_empleado = empleado.direccion_empleado,
        telefono_empleado = empleado.telefono_empleado,
        cargo = empleado.cargo,
        sueldo = empleado.sueldo,
        usuario = empleado.usuario,
        contrasena = empleado.contrasena
    )

    return { "Empleado_creado" : empleado.id }


@router.get('/id/{id}')
async def obtener_empleado(id: int):
    empleado = Empleados.select().where(Empleados.id == id).first()

    if empleado is None:
        raise HTTPException(status_code=404, detail='ID de empleado inexistente')
    
    response = parse_obj_as(EmpleadoResponseModel, empleado)

    return response


@router.get('/nombre/{nombre}')
async def obtener_empleado_nombre(nombre: str):
    empleados = Empleados.select().where(Empleados.nombre_empleado ** ('%' + nombre + '%'))
    empleados = [empleado for empleado in empleados]
    response = parse_obj_as(List[EmpleadoResponseModel], empleados)
    
    return response


@router.put('/{id}')
async def modificar_empleado(id: int, empleado: EmpleadoBaseModel):
    usuario_busqueda = Empleados.select().where(Empleados.usuario == empleado.usuario).first()
    empleado_actual = Empleados.select().where(Empleados.id == id).first()

    if empleado is None:
        raise HTTPException(status_code=404, detail='ID de empleado inexistente')
    
    if usuario_busqueda is not None:
        raise HTTPException(status_code=404, detail='El usuario ya existe')

    empleado_actual.nombre_empleado = empleado.nombre_empleado
    empleado_actual.appaterno_empleado = empleado.appaterno_empleado
    empleado_actual.apmaterno_empleado = empleado.apmaterno_empleado
    empleado_actual.direccion_empleado = empleado.direccion_empleado
    empleado_actual.telefono_empleado = empleado.telefono_empleado
    empleado_actual.cargo = empleado.cargo
    empleado_actual.sueldo = empleado.sueldo
    empleado_actual.usuario = empleado.usuario
    empleado_actual.contrasena = empleado.contrasena

    empleado_actual.save()

    return { "Id_modificado" : empleado_actual.id}


@router.delete('/{id}')
async def eliminar_empleado(id: int):
    empleado = Empleados.select().where(Empleados.id == id).first()

    if empleado is None:
        raise HTTPException(status_code=404, detail='Empleado inexistente')
    
    empleado.delete_instance()

    return { "Id_eliminado" : empleado.id }