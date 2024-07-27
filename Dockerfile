#Elegir la version de python
FROM python:3.12.4

#Declarar variables de entorno
ENV SMTP_APP_PASSWORD_GOOGLE="jmij jmjq zwpv tprf"

#Preparar el directorio de trabajo
WORKDIR /code

#Copiarlos requerimientos base
COPY ./requirements.txt /code/requirements.txt

#Instalar dependencias
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#Copiar el codigo 
COPY ./app /code/app

#Usar el comando para correr el servicio uvicorn app:main.app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]

