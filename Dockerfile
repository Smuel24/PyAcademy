# Usa imagen base de Python 3.13
FROM python:3.13-slim

# Establece variables de entorno
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Establece el directorio de trabajo
WORKDIR /app

# Instala dependencias del sistema (ACTUALIZADO)
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia requirements.txt
COPY requirements.txt .

# Instala dependencias Python
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copia el proyecto completo
COPY . .

# Ejecuta migraciones y crea archivos estáticos
RUN python manage.py collectstatic --noinput || true

# Expone el puerto
EXPOSE 8000

# Comando para ejecutar el servidor
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]