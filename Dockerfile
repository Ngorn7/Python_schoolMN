# ==============================
# 1️⃣ Base image# ==============================
FROM python:3.12-slim
# Prevent Python from buffering output
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
# Working directory
WORKDIR /app
# ==============================
# 2️⃣ Install dependencies
# ==============================
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
# ==============================
# 3️⃣ Copy project files
# ==============================
COPY . /app/
# ==============================
# 4️⃣ Run migrations + start server
# ==============================
# Run migrations when container starts
CMD ["sh", "-c", "python manage.py migrate && gunicorn SU43_44_POS.wsgi:application --bind 0.0.0.0:8000"]
# Expose Django port
EXPOSE 8000