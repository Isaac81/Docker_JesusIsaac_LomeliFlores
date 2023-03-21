from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from config.database import database as connection
from config.database import *


from router import departamentos
from router import empleados
from router import proveedores
from router import libros
from router import ventas
from router import libroproveedor
from router import libroventa


app = FastAPI(
    title='API-Libreria',
    description='API para proyecto Libreria SSPIS',
    version='1.0.3'
)


origins = [
    'http://localhost:5173',
    'http://127.0.0.1:5173',
    'http://localhost:5174',
    'http://127.0.0.1:5174',
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(departamentos.router)
app.include_router(empleados.router)
app.include_router(proveedores.router)
app.include_router(libros.router)
app.include_router(ventas.router)
app.include_router(libroproveedor.router)
app.include_router(libroventa.router)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.on_event("startup")
def startup():
    if connection.is_closed():
        connection.connect()
    print('Iniciando API server')

    connection.create_tables([  Departamentos,
                                Empleados,
                                Proveedores,
                                Libros,
                                Ventas,
                                LibroProveedor,
                                LibroVenta   ])

@app.on_event("shutdown")
def shutdown():
    if not connection.is_closed():
        connection.close()
    print('Cerrando API server')


@app.get('/')
async def root():
    return {'root': 'hola'}
