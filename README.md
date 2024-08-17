# Desplegando una API FastAPI en AWS Lambda

Este repositorio es un tutorial paso a paso sobre cómo desplegar una aplicación FastAPI en AWS Lambda.

## Tabla de Contenidos
1. [Introducción](#introducción)
2. [Requisitos Previos](#requisitos-previos)
3. [Estructura del Proyecto](#estructura-del-proyecto)
4. [Configuración del Entorno](#configuración-del-entorno)
5. [Despliegue en AWS Lambda](#despliegue-en-aws-lambda)
6. [Referencias](#referencias)

## Introducción

Este tutorial te guiará a través de los pasos necesarios para desplegar una API simple construida con FastAPI en AWS Lambda instalando las dependencias correcondientes segun el proyecto que tenga.

## Requisitos Previos

- Conocimientos básicos de FastAPI y Python.
- Cuenta en AWS con permisos para crear y gestionar recursos de Lambda.
- Python 3.12 o superior.

## Estructura del Proyecto

```plaintext
.
├── test_lambda/
│   ├── router/
│   │   ├── clientRouter.py # Endpoints de cliente
│   ├── schema/
│   │   ├── clientSchema.py # Esquemas Pydantic de cliente
│   ├── main.py  # Código principal de la API FastAPI
│   └── requirements.txt  # Dependencias del proyecto
└── README.md
```

### Despliegue de FastAPI

1. Proyecto de Ejemplo:
     Clona el repositorio para obtener la estructura anterior del proyecto
3. Crear el archivo requirements.txt:
      En este archivo se instalan todas las dependencias que usa el proyecto incluyendo sus versiones usadas. 

    ```bash
    git clone https://github.com/tu-usuario/tu-repositorio.git
    cd tu-repositorio
    ```

