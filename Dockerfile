FROM python:3.10-buster

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
# RUN pip3 install torch-scatter torch-sparse torch-geometric


COPY . .

EXPOSE 5050

CMD [ "python3", "backend/app.py"]


# udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1
# docker build --platform=linux/amd64 -t udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1-amd . && docker push udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1-amd
# docker run -p 5050:5050  udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1