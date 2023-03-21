FROM python:3.9

ENV CONFIG_DIR=/api/bot_world_config

# set working directory of container
WORKDIR /api

# install dependencies first - leverage cache
# RUN pip install --no-cache-dir --upgrade -r ./requirements.txt
COPY ./requirements.txt .
RUN pip install -r ./requirements.txt

COPY ./fastapi .

CMD ["uvicorn", "recommender_api:app", "--host", "0.0.0.0", "--port", "8000"]



