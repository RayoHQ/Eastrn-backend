# 기본 이미지를 Python 3.9을 사용
FROM python:3.9-slim

# 시스템 의존성 설치 (Graphviz)
RUN apt-get update && apt-get install -y \
    graphviz \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉토리 생성 및 설정
WORKDIR /app

# requirements.txt 복사
COPY requirements.txt /app/

# 의존성 설치
RUN pip install --no-cache-dir -r requirements.txt

# .env 파일을 복사 (필요한 경우)
COPY .env /app/.env

# 애플리케이션 코드 복사
COPY . /app

# PYTHONPATH 환경변수 설정 (app 디렉토리가 Python 모듈로 인식되도록)
ENV PYTHONPATH=/app

# 환경변수 설정 (필요한 경우 추가)
ENV PYTHONUNBUFFERED=1

# 컨테이너 시작 시 실행할 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
