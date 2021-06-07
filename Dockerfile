FROM 502937263541.dkr.ecr.eu-west-1.amazonaws.com/traveltek/uvicorn-gunicorn-fastapi-python3.8:0.1.0

COPY requirements.txt Makefile setup.py ./
RUN make install

COPY ./app /app/app
