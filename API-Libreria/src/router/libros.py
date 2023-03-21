from pydantic import parse_obj_as
from PIL import Image
import io
from fastapi import APIRouter, HTTPException
from fastapi import Depends
from fastapi import File, UploadFile
from typing import List

from config.database import Libros
from schemas import LibroBaseModel, LibroResponseModel, LibroPutModel


router = APIRouter(
    prefix = '/libros',
    tags=['libros']
)


@router.get('/')
async def obtener_libros():
    libros = Libros.select()
    libros = [libro for libro in libros]
    response = parse_obj_as(List[LibroResponseModel], libros)

    return response


@router.post('/')
async def crear_libro(libro: LibroBaseModel):
    if Libros.select().where(Libros.id == libro.id).exists():
        return HTTPException(409, 'El id del producto ya existe')
    
    libro = Libros.create(
        id = libro.id,
        id_departamento = libro.id_departamento,
        id_proveedor = libro.id_proveedor,
        titulo = libro.titulo,
        autor = libro.autor,
        editorial = libro.editorial,
        precio_compra = libro.precio_compra,
        precio_venta = libro.precio_venta,
        unidades_existentes = libro.unidades_existentes
    )

    return { "LibroCreado" : libro.id }


@router.post("/{id}")
async def crear_libro(id: int, img: UploadFile = File(...)):
    if not Libros.select().where(Libros.id == id).exists():
        raise HTTPException(409, 'El id del libro no existe')
    
    data = await img.read()
    image = Image.open(io.BytesIO(data))
    image.save("static/" + str(id) + ".png")

    return "Imagen creada"


@router.get('/id/{id}')
async def obtener_libro(id: int):
    libro = Libros.select().where(Libros.id == id).first()

    if libro is None:
        raise HTTPException(status_code=404, detail='ID de libro inexistente')
    
    response = parse_obj_as(LibroResponseModel, libro)

    return response


@router.get('/titulo/{titulo}')
async def obtener_libro_titulo(titulo: str):
    libros = Libros.select().where(Libros.titulo ** ('%' + titulo + '%'))
    libros = [libro for libro in libros]
    response = parse_obj_as(List[LibroResponseModel], libros)
    
    return response


@router.put('/{id}')
async def modificar_libro(id: int, libro: LibroPutModel):
    libro_actual = Libros.select().where(Libros.id == id).first()

    if libro_actual is None:
        raise HTTPException(status_code=404, detail='ID de libro inexistente')
    
    libro_actual.id_departamento = libro.id_departamento
    libro_actual.id_proveedor = libro.id_proveedor
    libro_actual.titulo = libro.titulo
    libro_actual.autor = libro.autor
    libro_actual.editorial = libro.editorial
    libro_actual.precio_compra = libro.precio_compra
    libro_actual.precio_venta = libro.precio_venta
    libro_actual.unidades_existentes = libro.unidades_existentes

    libro_actual.save()

    return { "LibroActualizado" : id }


@router.delete('/{id}')
async def eliminar_libro(id: int):
    libro = Libros.select().where(Libros.id == id).first()

    if libro is None:
        raise HTTPException(status_code=404, detail='Libro inexistente')
    
    libro.delete_instance()

    return { "LibroEliminado" : id }