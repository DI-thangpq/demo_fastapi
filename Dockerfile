FROM python:3.11-slim

# Tạo thư mục làm việc
WORKDIR /code

# Cài requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ project
COPY . .

# Cấu hình PYTHONPATH
ENV PYTHONPATH=/code

CMD uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload