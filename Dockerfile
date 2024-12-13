FROM python:3

WORKDIR /onepc

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
EXPOSE 8000

RUN python manage.py migrate
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]



