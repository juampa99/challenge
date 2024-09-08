FROM python:3.10.12-bookworm
# FROM ubuntu/python:3.10-22.04_stable

WORKDIR /code
COPY ./backend /code
# COPY ./requirements.txt /code/requirements.txt
# RUN ls && false
RUN apt update
# RUN apt install python3-commandnotfound
RUN pip install --no-cache-dir --upgrade -r ./requirements.txt

CMD ["python3", "-m", "uvicorn", "app:app", "--forwarded-allow-ips='*'", "--host", "0.0.0.0", "--workers", "3"]

