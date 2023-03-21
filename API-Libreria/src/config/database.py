from peewee import *
from datetime import datetime
from decouple import config
import hashlib


base = config('basededatos', '')
usuario = config('usuario', default='user')
passw = config('pass', default='clase')
host = config('host', default='localhost')
puerto = config('puerto', default=5000)

database = PostgresqlDatabase(base,
                              user = usuario,
                              password = passw,
                              host = host,
                              port = puerto)


class Departamentos(Model):
    id = AutoField(primary_key=True)
    nombre_departamento = CharField(max_length=25, unique=True)

    def __str__(self) -> str:
        return self.id

    class Meta:
        database = database
        table_name = 'departamentos'


class Empleados(Model):
    id = AutoField(primary_key=True)
    nombre_empleado = CharField(max_length=30)
    appaterno_empleado = CharField(max_length=20)
    apmaterno_empleado = CharField(max_length=20, null=True)
    direccion_empleado = CharField(max_length=100, null=True)
    telefono_empleado = FixedCharField(max_length=10)
    cargo = CharField(max_length=40)
    sueldo = DecimalField(decimal_places=2, max_digits=7)
    usuario = CharField(max_length=15, unique=True)
    contrasena = TextField()

    def __str__(self) -> str:
        return self.id

    class Meta:
        database = database
        table_name = 'empleados'


class Proveedores(Model):
    id = AutoField(primary_key=True)
    nombre_proveedor = CharField(max_length=40)
    direccion_proveedor = CharField(max_length=100, null=True)
    telefono_proveedor = FixedCharField(max_length=10)

    def __str__(self) -> str:
        return self.id

    class Meta:
        database = database
        table_name = 'proveedores'


class Libros(Model):
    id = BigIntegerField(primary_key=True)
    id_departamento = ForeignKeyField(Departamentos, backref='departamentos', db_column='id_departamento')
    id_proveedor = ForeignKeyField(Proveedores, backref='proveedores', db_column='id_proveedor')
    titulo = CharField(max_length=100)
    autor = CharField(max_length=50)
    editorial = CharField(max_length=50)
    precio_compra = DecimalField(decimal_places=2, max_digits=7)
    precio_venta = DecimalField(decimal_places=2, max_digits=7)
    unidades_existentes = IntegerField()

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        database = database
        table_name = 'libros'


class Ventas(Model):
    id = BigAutoField(primary_key=True)
    monto_total = DecimalField(decimal_places=2, max_digits=7)
    fecha_hora = DateTimeField(default=datetime.now)
    id_empleado = ForeignKeyField(Empleados, backref='empleados', db_column='id_empleado')

    def __str__(self) -> str:
        return self.id

    class Meta:
        database = database
        table_name = 'ventas'


class LibroProveedor(Model):
    id = AutoField(primary_key=True)
    id_libro = ForeignKeyField(Libros, backref='libros', db_column='id_libro')
    id_proveedor = ForeignKeyField(Proveedores, backref='proveedores', db_column='id_proveedor')
    cantidad = IntegerField()
    fecha_hora = DateTimeField(default=datetime.now)
    subtotal = DecimalField(decimal_places=2, max_digits=7)

    def __str__(self) -> str:
        return self.id
    
    class Meta:
        database = database
        table_name = 'libro_proveedor'
                                   

class LibroVenta(Model):
    id = AutoField(primary_key=True)
    id_libro = ForeignKeyField(Libros, backref='libros', db_column='id_libro')
    id_venta = ForeignKeyField(Ventas, backref='ventas', db_column='id_venta')
    cantidad = IntegerField()
    subtotal = DecimalField(decimal_places=2, max_digits=7)

    def __str__(self) -> str:
        return self.id

    class Meta:
        database = database
        table_name = 'libro_venta'