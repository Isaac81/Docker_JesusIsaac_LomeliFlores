from datetime import datetime
from pydantic import BaseModel
from pydantic import validator
from pydantic.utils import GetterDict
from peewee import ModelSelect
from typing import Optional, Any


# /// [Post/Departamento]
class DepartamentoBaseModel(BaseModel):
    nombre_departamento: str

    @validator('nombre_departamento')
    def nombre_departamento_validator(cls, nombre_departamento):
        if (len(nombre_departamento) < 3 or len(nombre_departamento) > 25):
            raise ValueError('Longitud del departamento fue del rango 3-25')
        return nombre_departamento
    

# /// [Post/Empleado]
class EmpleadoBaseModel(BaseModel):
    nombre_empleado: str
    appaterno_empleado: str
    apmaterno_empleado: Optional[str]
    direccion_empleado: Optional[str]
    telefono_empleado: str
    cargo: str
    sueldo: float
    usuario: str
    contrasena: str

    @validator('nombre_empleado')
    def nombre_empleado_validator(cls, nombre_empleado):
        if (len(nombre_empleado) < 3 or len(nombre_empleado) > 30):
            raise ValueError('Longitud del nombre fuera del rango 3-30')
        return nombre_empleado
    
    @validator('appaterno_empleado')
    def appaterno_empleado_validator(cls, appaterno_empleado):
        if (len(appaterno_empleado) < 3 or len(appaterno_empleado) > 20):
            raise ValueError('Longitud del apellido paterno fuera del rango 3-20')
        return appaterno_empleado
    
    @validator('apmaterno_empleado')
    def apmaterno_empleado_validator(cls, apmaterno_empleado):
        if apmaterno_empleado is not None:
            if (len(apmaterno_empleado) < 3 or len(apmaterno_empleado) > 20):
                raise ValueError('Longitud del apellido materno fuera del rango 3-20')
        return apmaterno_empleado
    
    @validator('direccion_empleado')
    def direccion_empleado_validator(cls, direccion_empleado):
        if direccion_empleado is not None:
            if (len(direccion_empleado) < 10 or len(direccion_empleado) > 100):
                raise ValueError('Longitud de direccion fuera del rango 10-100')
        return direccion_empleado
    
    @validator('telefono_empleado')
    def telefono_empleado_validator(cls, telefono_empleado):
        if (len(telefono_empleado) != 10):
            raise ValueError('El telefono debe tener 10 digitos')
        return telefono_empleado
    
    @validator('cargo')
    def cargo_validator(cls, cargo):
        if (cargo != 'administrador') and (cargo != 'vendedor'):
            raise ValueError('El cargo solo puede ser administrador o vendedor')
        return cargo
    
    @validator('sueldo')
    def sueldo_validator(cls, sueldo):
        if (sueldo > 85000):
            raise ValueError('El sueldo no puede exceder los 85mil mensuales')
        return sueldo
    
    @validator('usuario')
    def usuario_validator(cls, usuario):
        if (len(usuario) < 3 or len(usuario) > 15):
            raise ValueError('Longitud de usuario fuera del rango 3-15')
        return usuario
    
    @validator('contrasena')
    def contrasena_validator(cls, contrasena):
        if (len(contrasena) < 10 or len(contrasena) > 70):
            raise ValueError('Longitud de contrasena fuera del rango 10-70')
        return contrasena


# /// [Post/Proveedor]
class ProveedorBaseModel(BaseModel):
    nombre_proveedor: str
    direccion_proveedor: Optional[str]
    telefono_proveedor: str

    @validator('nombre_proveedor')
    def nombre_proveedor_validator(cls, nombre_proveedor):
        if (len(nombre_proveedor) < 3 or len(nombre_proveedor) > 40):
            raise ValueError('Longitud del nombre del proveedor fuera del rango 3-40')
        return nombre_proveedor
    
    @validator('direccion_proveedor')
    def direccion_proveedor_validator(cls, direccion_proveedor):
        if direccion_proveedor is not None:
            if (len(direccion_proveedor) < 10 or len(direccion_proveedor) > 100):
                raise ValueError('Longitud de direccion fuera del rango 10-100')
        return direccion_proveedor

    @validator('telefono_proveedor')
    def telefono_proveedor_validator(cls, telefono_proveedor):
        if (len(telefono_proveedor) != 10):
            raise ValueError('El telefono debe tener 10 digitos')
        return telefono_proveedor
    

# /// [Post/Libro]
class LibroBaseModel(BaseModel):
    id: int
    id_departamento: int
    id_proveedor: int
    titulo: str
    autor: str
    editorial: str
    precio_compra: float
    precio_venta: float
    unidades_existentes: int

    @validator('id')
    def id_validator(cls, id):
        if (len(str(id)) == 9 or len(str(id)) == 13):
            return id 
        else:  
            raise ValueError('Los ISBN solo pueden tener 9 o 13 digitos')
    
    @validator('titulo')
    def titulo_validator(cls, titulo):
        if (len(titulo) == 0 or len(titulo) > 100):
            raise ValueError('El titulo debe tener una longitud entre 1 y 100')
        return titulo
    
    @validator('autor')
    def autor_validator(cls, autor):
        if (len(autor) < 3 or len(autor) > 50):
            raise ValueError('Longitud de autor fuera del rango 3-50')
        return autor
    
    @validator('editorial')
    def editorial_validator(cls, editorial):
        if(len(editorial) < 3 or len(editorial) > 50):
            raise ValueError('Longitud de editorial fuera del rango 3-50')
        return editorial
    
    @validator('precio_compra')
    def precio_compra_validator(cls, precio_compra):
        if(precio_compra < 0 or precio_compra > 99998):
            raise ValueError('No se pueden comprar ejemplares por menos de 0 o mas de 99998')
        return precio_compra
    
    @validator('precio_venta')
    def precio_venta_validator(cls, precio_venta):
        if(precio_venta < 0 or precio_venta > 99999):
            raise ValueError('No se pueden vender ejemplares por menos de 0 o mas de 99999') 
        return precio_venta
    
    @validator('unidades_existentes')
    def unidades_existentes_validator(cls, unidades_existentes):
        if(unidades_existentes > 9999):
            raise ValueError('No se pueden almacenar mas de 9999 ejemplares de un titulo')
        return unidades_existentes


# /// [Post/Venta]
class VentaBaseModel(BaseModel):
    monto_total: float
    fecha_hora: datetime
    id_empleado: int
    
    @validator('monto_total')
    def monto_total_validator(cls, monto_total):
        if(monto_total < 0 or monto_total > 99999):
            raise ValueError('Una venta no puede tener un monto menor a 0 o mayor a 99999')
        return monto_total
    

# /// [Post/LibroProveedor]
class LibroProveedorBaseModel(BaseModel):
    id_libro: int
    id_proveedor: int
    cantidad: int
    fecha_hora: datetime
    subtotal: float

    @validator('cantidad')
    def cantidad_validator(cls, cantidad):
        if(cantidad == 0):
            raise ValueError('No se pueden realizar compras con ningun ejemplar')
        return cantidad
    
    @validator('subtotal')
    def subtotal_validator(cls, subtotal):
        if(subtotal < 0):
            raise ValueError('No se pueden realizar compras con costo a favor del cliente')
        return subtotal
    

# /// [Post/LibroVenta]    
class LibroVentaBaseModel(BaseModel):
    id_libro: int
    id_venta: int
    cantidad: int
    subtotal: float

    @validator('cantidad')
    def cantidad_validator(cls, cantidad):
        if(cantidad == 0):
            raise ValueError('No se pueden realizar ventas con ningun ejemplar')
        return cantidad
    
    @validator('subtotal')
    def subtotal_validator(cls, subtotal):
        if(subtotal < 0):
            raise ValueError('No se pueden realizar ventas con costo a favor del cliente')
        return subtotal



# /// [Response/Inicio]
class PeeweeGetterDict(GetterDict):
    def get(self, key: Any, default: Any = None):
        res = getattr(self._obj, key, default)
        
        if isinstance(res, ModelSelect):
            return list(res)

        return res


# /// [Response/Departamento]
class DepartamentoResponseModel(BaseModel):
    id: int
    nombre_departamento: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReferenciaDepartamentoResponseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReferenciaProveedorResponseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Response/Empleado]
class EmpleadoResponseModel(BaseModel):
    id: int
    nombre_empleado: str
    appaterno_empleado: str
    apmaterno_empleado: Optional[str]
    direccion_empleado: Optional[str]
    telefono_empleado: str
    cargo: str
    sueldo: float
    usuario: str
    contrasena: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Response/Proveedor]
class ProveedorResponseModel(BaseModel):
    id: int
    nombre_proveedor: str
    direccion_proveedor: Optional[str]
    telefono_proveedor: str

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Response/Libro]
class LibroResponseModel(BaseModel):
    id: int
    id_departamento: ReferenciaDepartamentoResponseModel
    id_proveedor: ReferenciaProveedorResponseModel
    titulo: str
    autor: str
    editorial: str
    precio_compra: float
    precio_venta: float
    unidades_existentes: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReferenciaLibroResponseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


#/// [Response/Venta]
class VentaResponseModel(BaseModel):
    id: int
    monto_total: float
    fecha_hora: datetime
    id_empleado: int    

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class ReferenciaVentaResponseModel(BaseModel):
    id: int

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Response/LibroProveedor]
class LibroProveedorResponseModel(BaseModel):
    id: int
    id_libro: ReferenciaLibroResponseModel
    id_proveedor: ReferenciaProveedorResponseModel
    cantidad: int
    fecha_hora: datetime
    subtotal: float

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Response/LibroVenta]
class LibroVentaResponseModel(BaseModel):
    id: int
    id_libro: ReferenciaLibroResponseModel
    id_venta: ReferenciaVentaResponseModel
    cantidad: int
    subtotal: float

    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


# /// [Put/Inicio]
# /// [Put/Departamento]
# Igual al PostModel


# /// [Put/Empleado]
# Igual al PostModel


#/// [Put/Proveedor]
# Igual al PostModel


# /// [Put/Libro]
class LibroPutModel(BaseModel):
    id_departamento: int
    id_proveedor: int
    titulo: str
    autor: str
    editorial: str
    precio_compra: float
    precio_venta: float
    unidades_existentes: int
    
    @validator('titulo')
    def titulo_validator(cls, titulo):
        if (len(titulo) == 0 or len(titulo) > 100):
            raise ValueError('El titulo debe tener una longitud entre 1 y 100')
        return titulo
    
    @validator('autor')
    def autor_validator(cls, autor):
        if (len(autor) < 3 or len(autor) > 50):
            raise ValueError('Longitud de autor fuera del rango 3-50')
        return autor
    
    @validator('editorial')
    def editorial_validator(cls, editorial):
        if(len(editorial) < 3 or len(editorial) > 50):
            raise ValueError('Longitud de editorial fuera del rango 3-50')
        return editorial
    
    @validator('precio_compra')
    def precio_compra_validator(cls, precio_compra):
        if(precio_compra < 0 or precio_compra > 99998):
            raise ValueError('No se pueden comprar ejemplares por menos de 0 o mas de 99998')
        return precio_compra
    
    @validator('precio_venta')
    def precio_venta_validator(cls, precio_venta):
        if(precio_venta < 0 or precio_venta > 99999):
            raise ValueError('No se pueden vender ejemplares por menos de 0 o mas de 99999') 
        return precio_venta
    
    @validator('unidades_existentes')
    def unidades_existentes_validator(cls, unidades_existentes):
        if(unidades_existentes > 9999):
            raise ValueError('No se pueden almacenar mas de 9999 ejemplares de un titulo')
        return unidades_existentes


# /// [Put/Venta]
class VentaPutModel(BaseModel):
    monto_total: float

    @validator('monto_total')
    def monto_total_validator(cls, monto_total):
        if(monto_total < 0 or monto_total > 99999):
            raise ValueError('Una venta no puede tener un monto menor a 0 o mayor a 99999')
        return monto_total
    

# /// [Put/LibroProveedor]
class LibroProveedorPutModel(BaseModel):
    cantidad: int
    subtotal: float

    @validator('cantidad')
    def cantidad_validator(cls, cantidad):
        if(cantidad == 0):
            raise ValueError('No se pueden realizar compras con ningun ejemplar')
        return cantidad
    
    @validator('subtotal')
    def subtotal_validator(cls, subtotal):
        if(subtotal < 0):
            raise ValueError('No se pueden realizar compras con costo a favor del cliente')
        return subtotal
    

# /// [Put/LibroVenta]
# Igual al PostModel