# Sử dụng Python image làm base
FROM python:3.11.5

# Đặt thư mục làm việc cho ứng dụng
WORKDIR /app

# Sao chép các file vào container
COPY . .

# Cài đặt các yêu cầu
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8080

# Chạy Streamlit
CMD ["streamlit", "run", "main.py", "--server.port=8080", "--server.address=0.0.0.0"]