@echo off

set "nombre_proyecto=tienda"
set "aplicacion_django_principal=core"
set "aplicacion_django_apis=apirest"
set "carpeta_proyectos=C:\ProyectosDjango\"
set "carpeta_proyecto_django=%carpeta_proyectos%%nombre_proyecto%"
set "carpeta_ambiente_virtual=%carpeta_proyectos%%nombre_proyecto%_venv"
set "activacion_ambiente_virtual=%carpeta_proyectos%%nombre_proyecto%_venv\Scripts\activate.bat"

echo.

echo **********************************************************************************
echo Nombe Proyecto Django    : %nombre_proyecto%
echo App principal            : %aplicacion_django_principal%
echo App para API Rest        : %aplicacion_django_apis%
echo Carpeta de proyectos     : %carpeta_proyectos%
echo Carpeta Proyecto Django  : %carpeta_proyecto_django%
echo Ambiente virtual         : %carpeta_ambiente_virtual%
echo Activar ambiente virtual : %activacion_ambiente_virtual%
echo **********************************************************************************

echo.
echo Comenzar proceso de creacion de proyecto...
echo.
echo Actualizando pip y virtualenv a nivel de sistema...
echo.

python -m pip install --upgrade pip
pip install --upgrade virtualenv

if not exist "%carpeta_proyectos%" (
    echo Creando carpeta de proyectos "%carpeta_proyectos%"...
    md "%carpeta_proyectos%"
) else (
    echo.
    echo La carpeta de proyectos "%carpeta_proyectos%" ya esta creada
)

echo.

if exist "%carpeta_ambiente_virtual%" (
    echo Eliminando ambiente virtual "%carpeta_ambiente_virtual%"...
    rd /s /q "%carpeta_ambiente_virtual%"
    if exist "%carpeta_ambiente_virtual%" (
        echo.
        echo El ambiente virtual no pudo ser eliminado, verifique que no este usando la carpeta "%carpeta_ambiente_virtual%"
        echo Esto puede suceder si tiene un terminal abierto que esta usando la carpeta.
        echo Otras veces sucede porque tiene abierto Visual Studio Code, en cuyo caso lo debe cerrar.
        echo.
        echo Terminando instalación debido a que no se pudo eliminar el ambiente virtual...
        exit
    )
    echo.
)

echo Creando ambiente virtual e instalando paquetes Python...
echo.

python -m venv "%carpeta_ambiente_virtual%"
call cd /D "%carpeta_proyectos%"
call %activacion_ambiente_virtual%

python -m pip install --upgrade pip
echo.
pip install django
echo.
pip install pillow
echo.
pip install djangorestframework
echo.
pip install transbank-sdk
echo.
pip install django-extensions
echo.

set /p installPackage=Deseas instalar el paquete cx_Oracle? (S/N): 
echo.

if /i "%installPackage%"=="S" (
    echo Instalando cx_Oracle...
    echo.
    pip install cx_Oracle
    echo La instalacion de cx_Oracle se ha completado.
) else (
    echo No se realizara la instalacion de cx_Oracle.
)

if exist "%carpeta_proyecto_django%" (
    echo.
    echo La carpeta "%carpeta_proyecto_django%" ya existe.
    echo.
    echo Terminando instalacion para no sobreescribir el proyecto Django...
    echo.
    pause
    exit
)

echo.
echo Presiona [ENTER] para crear el proyecto Django
echo.
pause

echo.
echo Creando proyecto "%nombre_proyecto%" con Django
echo.

call django-admin startproject %nombre_proyecto%
call cd %nombre_proyecto%
python manage.py startapp %aplicacion_django_principal%
python manage.py startapp %aplicacion_django_apis%

echo Proyecto Django fue creado, presiona [ENTER] para abrir el proyecto.
echo.
pause

pip freeze > requirements.txt
call code "%carpeta_proyecto_django%"

exit

