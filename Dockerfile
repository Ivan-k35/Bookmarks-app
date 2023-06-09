FROM python:3.9

# Установить рабочую директорию в контейнере
WORKDIR /app

# Установить переменные среды
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установить зависимости
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Копировать проект
COPY . /app/

# Стандартная команда для запуска Django приложения
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]