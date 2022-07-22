FROM python:3.10-buster

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY backend/requirements.txt requirement-backend.txt
RUN pip3 install -r requirement-backend.txt


RUN pip install torch-scatter -f https://data.pyg.org/whl/torch-1.11.0+cpu.html
RUN pip install torch-sparse -f https://data.pyg.org/whl/torch-1.11.0+cpu.html
RUN pip install torch-cluster -f https://data.pyg.org/whl/torch-1.11.0+cpu.html
RUN pip install torch-spline-conv -f https://pytorch-geometric.com/whl/torch-1.11.0+cpu.html
RUN pip install  torch-geometric -f https://data.pyg.org/whl/torch-1.11.0+cpu.html
# RUN pip3 install -q torch-scatter -f https://data.pyg.org/whl/torch-1.9.0+cu111.html
# torch-geometric -f https://pytorch-geometric.com/whl/torch-1.8.0+cu101.html

RUN pip3 install GitPython openpyxl networkx
# RUN pip3 install 


RUN echo "redofefegetetetfefefeteee"

COPY backend/run.py backend/run.py
COPY . .


COPY backend/.env backend/.env

WORKDIR /backend

EXPOSE 443


CMD ["python", "run.py"]
# CMD ["gunicorn", "--config", "gunicorn-cfg.py", "run:app"]


# udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1
# docker build --platform=linux/amd64 -t udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1-amd . && docker push udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1-amd
# docker run -p 5050:5050  udsdatasciencedopingdetection.azurecr.io/ds-graph-api:v1

# gunicorn --config gunicorn-cfg.py run:app