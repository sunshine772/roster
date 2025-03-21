# Player selection

## Build the solution
Esta solución requiere Python 3.10 y Poetry 1.1 instalados. 
Para construir la solución, simplemente instala las dependencias de Python: 
```shell
poetry install
```

## Run solution locally
Para preparar la solución localmente (migrar la base de datos local - SQLite), ejecuta este comando (solo necesita ejecutarse una vez):
```shell
poetry run python manage.py migrate my_app
```

Para ejecutar la solución localmente (iniciar el servidor en el puerto 3000), simplemente ejecuta este comando:
```shell
poetry run python manage.py runserver 3000
```

Por favor, ignora los mensajes de error sobre migraciones no aplicadas al ejecutar el servidor. El proyecto se inicializa a partir de una plantilla de aplicación Django que incluye aplicaciones irrelevantes  (e.g. `admin`, `auth`, ... etc).

## Run tests
Para ejecutar las pruebas, simplemente ejecuta este comando:
```shell
poetry run python manage.py test --noinput my_app.tests
```
