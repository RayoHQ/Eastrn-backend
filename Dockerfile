# 베이스 이미지 선택
FROM python:3.11

# 작업 디렉터리 설정
WORKDIR /app

# Poetry 설치
RUN curl -sSL https://install.python-poetry.org | python3 -

# 환경변수 설정 (Poetry가 가상 환경을 사용하지 않도록 설정)
ENV POETRY_VIRTUALENVS_CREATE=false

# Poetry 의존성 파일 복사
COPY pyproject.toml poetry.lock ./

# requirements.txt 생성
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

# 필요한 패키지 설치
RUN pip install --no-cache-dir -r requirements.txt

# 애플리케이션 코드 복사
COPY app.py .

# 실행 명령어 설정
CMD ["python", "app.py"]
