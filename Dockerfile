FROM python:3.9-slim
WORKDIR /auth
COPY ./requirements.txt /auth/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /auth/requirements.txt
COPY . /auth
EXPOSE 8071

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8071"]