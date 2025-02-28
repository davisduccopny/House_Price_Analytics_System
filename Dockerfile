
FROM python:3.11.5


WORKDIR /app


COPY . .


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080


CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]