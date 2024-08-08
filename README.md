# Backend de Buho Bank

Este es el backend del proyecto Buho Bank, desarrollado en Python utilizando FastAPI.

## Configuración del Entorno

### Instalación de Dependencias

#### Windows

```bash
git clone https://github.com/Pinkylml/back_end_BuhoBank.git
cd back_end_BuhoBank

python -m venv env
.\env\Scripts\activate

pip install -r requirements.txt
```

#### Linux y macOS

```bash
git clone https://github.com/Pinkylml/back_end_BuhoBank.git
cd back_end_BuhoBank

python3 -m venv env
source env/bin/activate

pip install -r requirements.txt
```

## Ejecución del Servidor

Para ejecutar el servidor de desarrollo:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
ten en cuenta que debes estar en la carpeta back_end_BuhoBank/ para que funcione el codigo, si estas dentro de app usa el siguiente:


```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
## Documentación de la API

Una vez que el servidor esté en ejecución, puedes acceder a la documentación de la API en:

```
http://localhost:8000/docs
```

Aquí podrás probar los endpoints y explorar la funcionalidad del backend de Buho Bank.
