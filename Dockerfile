# Sử dụng image Python chính thức
FROM python:3.12-slim

# Đặt thư mục làm việc
WORKDIR /app

# Sao chép file requirements.txt vào container
COPY requirements.txt .

# Cài đặt các thư viện từ requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Sao chép mã nguồn của bạn vào container
COPY . .

# Mở cổng ứng dụng
EXPOSE 5000

# Lệnh để chạy ứng dụng
CMD ["python", "main.py"]
