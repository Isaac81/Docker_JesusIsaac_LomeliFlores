# Universidad de Guadalajara - Centro Universitario de Ciencias Exactas e Ingenierias
## Departamento de ciencias computacionales
Computacion Tolerante a fallas - Seccion D06

Profesor: *Lopez Franco Michel Emanuel*

Alumno: *Lomeli Flores Jesus Isaac*

## Docker

### Introducción

<p align="justify">
 En algunas ocasiones se debe desarrollar con multiples proyectos al mismo tiempo con distintas bibliotecas, lenguajes, entornos, dependencias de distintos sistemas
  operativos. Lo que resulta tedioso si se tiene que estar cambiando entre maquinas virtuales, sin mencionar la cantidad de recursos que estas consumiran. Docker
  soluciona estos problemas de una manera sencilla y optima.
</p>

### Desarrollo

<p align="justify">
  Para este proyecto es necesaria la creación de una red personalizada en docker debido a que se utilizaran dos contenedores, uno para la base de datos en postgresql y otro con la API en FastAPI para consumir la base de datos. Para la creación de dicha red se utiliza el comando que esta debajo.
</p>


```
docker network create redlibreria
```


<p align="justify">
Se ingresa el siguiente comando en una terminal. Dicho comando creara un contenedor con una imagen de postgresql con la base de datos "libreria" con el usuario postgres y una contraseña. Así mismo mapeara el puerto del contenedor que sera el 5432 (puerto por defecto de postgresql) al del localhost 4500.
</p>

```
docker container run -p 4500:5432 --name database --net redlibreria -e POSTGRES_USER=postgres -e POSTGRES_PASSWORD=class123456 -e POSTGRES_DB=libreria -d postgres
```
![Contenedor de la base de datos](/Imagenes/20230320215135.png)


<p align="justify">
Una vez creado el contenedor se retornara el id completo del contenedor. Para ver si el contenedor creado esta corriendo existen múltiples opciones, una de ellas es escribir el siguiente comando en la terminal que mostrara todos los contenedores activos.
</p>

```
docker ps
```

![Estado en consola](/Imagenes/20230320184814.png)

<p align="justify">
Si se esta utilizando docker en windows, otra forma de verificar el estado del contenedor es con docker desktop en la seccion de contenedores.
</p>

![Estado en Docker Desktop](/Imagenes/20230320185336.png)

<p align="justify">
Para crear el contenedor de la API es necesario crear un Dockerfile en la raiz del proyecto, cuya estructura se muestra en la siguiente imagen junto con el contenido del Dockerfile.
</p>

![Estructura y dockerfile](/Imagenes/20230320215311.png)


<p align="justify">
Después de crear el Dockerfile se debe ingresar el siguiente comando para crear la imagen de docker.
</p>

```
docker build -t apilibreria .
```

![Creación de la imagen](/Imagenes/20230320194055.png)

<p align="justify">
El siguiente paso es crear el contenedor de la API con la imagen que se creo en el paso anterior para lo cual se ingresa el siguiente comando en la terminal lo que a su vez ejecutara a la API.
</p>


```
docker run -d --name contenedorapilibreria --net redlibreria -p 8005:8000 apilibreria
```

<p align="justify">
Para comprobar que la API sea accesible desde el localhost se ingresa a la dirección http://localhost:8005/docs , dirección que corresponde a la documentación de la API.
</p>

![Documentacion de la API](/Imagenes/20230320215753.png)

### Conclusión

<p align="justify">
Se logro comprender el funcionamiento y proceso para implementar un proyecto con multiples contenedores, asi como la utilidad de docker que resulta ser la mejor opcion
  para el trabajo colaborativo pues elimina los problemas de compatibilidad y dependencias, ademas de ahorrar recursos pues solo corre una imagen del sistema operativo
  la cual sera utilizada por todos lo contenedores que la necesiten, eliminando sistemas operativos duplicados.
</p>


