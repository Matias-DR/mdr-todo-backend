# ToDo-List Challenge - Instrucciones de uso

## Requisitos
- [Python 3.12.X](https://www.python.org/downloads/)
- [Git 2.39.X](https://git-scm.com/downloads)
- [Docker](https://www.docker.com/)

## Instalación
- 1) Abra una terminal e ingrese "mkdir <nombre_carpeta>" (para terminales en UNIX y PowerShell en Windows >=10) para crear la carpeta del proyecto
- 2) Párese sobre la carpeta creada con "cd <nombre_carpeta>" donde instalará el proyecto
- 3) Clone el repositorio ingresando "git clone https://github.com/Matias-DR/mdr-todo-challenge"
- 4) Párese sobre el proyecto con "cd ./mdr-todo-challenge/challenge"

## Configuración
- 1) Dentro de la carpeta "challenge" cree un archivo llamado ".env" y ábralo con un editor de texto.
- 2) Escriba "SECRET_KEY=clave_secreta" donde "clave_secreta" debe ser reemplazado por cual fuera la clave secreta que desee para encriptar toda infromación sensible del proyecto.
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

## Ejecución
- 1) Ingrese el comando "docker compose up --build" para construir el ambiente en el que se ejecutará el proyecto
- 2) Ejecute con el comando "docker compose up" y ya podrá consumir la aplicación

## Documentación
Una vez levantado el proyecto, puede relevar todos los endpoints disponibles por la aplicación ingresando a "http://127.0.0.1:8000/api/schema/redoc/".
Además, puede probar cada uno de los endpoint ingresando a "http://127.0.0.1:8000/api/schema/swagger-ui/".
Por útlimo, si desea documentar y probar cada endpoint de manera personalizada en aplicaciones externas, ingrese a "http://127.0.0.1:8000/api/schema/" para exportar las configuraciones a un archivo "api.yaml" que contendrá la colección de endpoints.

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
    {
        "pk":2,
        "password":"<hash>",
        "username":"test"
    }
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
    HTTP/1.1 200 OK
    { access: <access_token> }
```

### Request
`GET /api/user/` Obtener los datos del usuario
- UNIX
```
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/user/<pk>/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/<pk>/" -Method Put -Headers @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    {
        "pk":2,
        "password":"<hash>",
        "username":"test"
    }
```

### Request
`PUT/PATCH /api/user/` Cambiar los datos del usuario
- UNIX
```
curl -X PUT -H "Content-Type: application/json" -d '{"username":"test2","password":"test2"}' http://127.0.0.1:8000/api/user/<pk>/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/<pk>/" -Method Put -Headers @{ "Content-Type" = "application/json" } -Body '{"username":"test2","password":"test2"}'
```
### Response
```
    HTTP/1.1 200 OK
    {
        "password": "test2",
        "username": "test2"
    }
```

### Request
`DELETE /api/user/` Eliminar el usuario
- UNIX
```
curl -X DELETE -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/user/<pk>/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/user/<pk>/" -Method Delete -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 204 No Content
```

### Request
`POST /api/task/` Crear un una tarea (requiere token)
- UNIX
```
curl -X POST -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"title":"test","description":"test"}' http://127.0.0.1:8000/api/task/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/" -Method Post -Headers @{
    "Content-Type" = "application/json"
    "Authorization" = "Bearer <access_token>"
} -Body '{"title":"test","description":"test" }'
```
### Response
```
    HTTP/1.1 201 Created
    {
        "completed": false,
        "description": "test",
        "title": "test"
    }
```

### Request
`GET /api/task/` Obtener los datos de una tarea
- UNIX
```
curl -X GET -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/task/<pk_task>
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/<pk_task>" -Method Get -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    {
        "completed": false,
        "description": "test",
        "title": "test"
    }
```

### Request
`GET /api/task/` Obtener los datos de todas las tareas del usuario autenticado
- UNIX
```
curl -X GET -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/token/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/<pk_task>" -Method Get -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    [
        {
            "completed": true,
            "description": "test",
            "title": "test"
        },
        {
            "completed": false,
            "description": "test_modified",
            "title": "test_modified"
        }
    ]
```

### Request
`PUT/PATCH /api/task/` Modificar los datos de una tarea
- UNIX
```
curl -X PUT -H "Content-Type: application/json" -H "Authorization: Bearer <access_token>" -d '{"title":"test_modified","description":"test_modified"}' http://127.0.0.1:8000/api/task/<pk_task>/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/<pk_task>/" -Method Put -Headers @{
    "Authorization" = "Bearer <access_token>"
    "Content-Type" = "application/json"
} -Body '{"title":"test_modified","description":"test_modified" }'
```
### Response
```
    HTTP/1.1 200 OK
    {
        "completed": false,
        "description": "test_modified",
        "title": "test_modified"
    }
```

### Request
`PUT/PATCH /api/user/` Eliminar una tarea
- UNIX
```
curl -X DELETE -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/task/<pk_task>/
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/<pk_task>/" -Method Delete -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 204 No Content
```

### Request
`PUT/PATCH /api/task/` Marcar una tarea como completa
- UNIX
```
curl -X PUT -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/task/<pk_task>/complete
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task/<pk_task>/complete" -Method Put -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    {
        "completed": true,
        "description": "test",
        "title": "test"
    }
```

### Request
`GET /api/task/` Buscar una tarea por título o descripción
- UNIX
```
curl -X GET -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/task?search=<texto_a_buscar>
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task?search=<texto_a_buscar>" -Method Get -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    [
        {
            "completed": false,
            "description": "test",
            "title": "test"
        },
        {
            "completed": true,
            "description": "test2",
            "title": "test2"
        },
    ]
```

### Request
`GET /api/task/` Buscar una tarea por fecha y estado (completa o incompleta)
- UNIX
```
curl -X GET -H "Authorization: Bearer <access_token>" http://127.0.0.1:8000/api/task?complete=(True|False)&created=<yyyy-mm-dd>
```
- PowerShell
```
Invoke-RestMethod -Uri "http://127.0.0.1:8000/api/task?complete=(True|False)&created=<yyyy-mm-dd>" -Method Get -Headers @{
    "Authorization" = "Bearer <access_token>"
}
```
### Response
```
    HTTP/1.1 200 OK
    [
        {
            "completed": false,
            "description": "test",
            "title": "test"
        },
        {
            "completed": true,
            "description": "test2",
            "title": "test2"
        },
    ]
```
