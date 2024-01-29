# ToDo-List Challenge - Instrucciones de uso

## Requisitos
- [Python 3.12.X](https://www.python.org/downloads/)
- [Git 2.39.X](https://git-scm.com/downloads)
- OPCIONAL: [Docker](https://www.docker.com/)

## Instalación
- 1) Abra una terminal e ingrese "mkdir proyect" para crear la carpeta del proyecto
- 2) Párese sobre la carpeta creada con "cd proyect" donde instalará el proyecto
- 3) Clone el repositorio ingresando "git clone -b mdr-todo-list-challenge https://github.com/invera/todo-challenge"
- 4) Párese sobre el proyecto con "cd ./todo-challenge/challenge"
- 5) Instale los módulos adicionales ingresando "pip install -r requirements.txt"

## Configuración
- 1) Dentro de la carpeta "challenge" cree un archivo llamado ".env" y ábralo con un editor de texto.
- 2) Escriba "SECRET_KEY=clave_secreta" donde "clave_secreta" debe ser reemplazado por cual fuera la clave secreta que desee para encriptar toda infromación sensible del proyecto.
- 3) Guarde el archivo y ciérrelo

## Ejecución
- 1) Sobre la misma terminal utilizada para la instalación, ingrese el comando "py manage.py runserver" y ya tendrá listo el proyecto en funcionamiento

## Instalación Docker
- 1) Siga los pasos 1 al 4 de la instalación principal.
- 2) En la misma terminal, ingrese el comando "docker compose up --build" para construir el ambiente en el que se ejecutará el proyecto

## Configuración Docker
- 1) Dentro de la carpeta "challenge" cree un archivo llamado ".env" y ábralo con un editor de texto.
- 2) Escriba "SECRET_KEY=<clave_secreta>" donde "<clave_secreta>" debe ser reemplazado por cual fuera la clave secreta que desee para encriptar toda infromación sensible del proyecto.
- 3) Además, tendrá que definir las siguientes variables, para las que así como a "SECRET_KEY" tendrá que asignar valores:
    - DEBUG=1
    - SQL_ENGINE=django.db.backends.postgresql
    - SQL_DATABASE=todo_challenge
    - SQL_USER=todo_challenge
    - SQL_PASSWORD=todo_challenge
    - SQL_HOST=db
    - SQL_PORT=5432
    - DJANGO_SUPERUSER_PASSWORD=<contraseña_superusuario>
    - DEFAULT_ADMIN_PASSWORD=<contraseña_superusuario>
    - DEFAULT_ADMIN_EMAIL=<email_superusuario>
    - DEFAULT_ADMIN_USERNAME=<nombre_superusuario>
- 4) Guarde el archivo y ciérrelo

## Ejecución Docker
- 1) Sobre la misma terminal utilizada para la instalación opcional, ingrese el comando "docker compose up" y ya estará listo

## Utilización / Pruebas
Una vez ejecutado el proyecto, puede realizar peticiones HTTP a los siguientes enlaces para cada una de las acciones indicadas.
Lo que verá a continuación son comandos en terminales UNIX y/o PowerShell que generarán esas solicitudes HTTP y puede ingresarlos en una terminal para probarlos.

### Request
`POST /api/user/` Crear un usuario
- UNIX
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}' http://127.0.0.1:8000/api/user/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"username":"test","password":"test" }'
```
### Response
```
    HTTP/1.1 201 OK
    { username: test, password: ... }
```

### Request
`POST /api/token/` Iniciar sesión con credenciales
- UNIX
```
curl -X POST -H "Content-Type: application/json" -d '{"username":"test","password":"test"}' http://127.0.0.1:8000/api/token/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token/" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"username":"test","password":"test"}'
```
### Response
```
    HTTP/1.1 201 OK
    { refresh: <refresh_token> access: <access_token> }
```

### Request
`POST /api/token/refresh` Actualizar el token access
- UNIX
```
curl -X POST -H "Content-Type: application/json" -d '{"refresh":"<refresh_token>"}' http://127.0.0.1:8000/api/token/refresh
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/token/" -Method Post -Headers @{ "Content-Type" = "application/json" } -Body '{"refresh":"<refresh_token>"}'
```
### Response
```
    HTTP/1.1 201 OK
    { access: <access_token> }
```

### Request
`PUT/PATCH /api/user/` Cambiar los datos del usuario
- UNIX
```
curl -X PUT -H "Content-Type: application/json" -d '{"username":"<username>","password":"password"}' http://127.0.0.1:8000/api/user/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/" -Method Put -Headers @{ "Content-Type" = "application/json" } -Body '{"username":"<username>","password":"password"}'
```
### Response
```
    HTTP/1.1 201 OK
    { access: <access_token> }
```
