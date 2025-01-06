FROM continuumio/anaconda3:latest

RUN pip install bokeh==3.6.2

COPY ./bokeh_app /bokeh_app

COPY ./data /data

WORKDIR /bokeh_app

EXPOSE 5006:5006

ENTRYPOINT ["python","main.py"]