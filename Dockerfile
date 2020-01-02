FROM continuumio/anaconda3:latest

RUN pip install bokeh==1.4.0

COPY ./bokeh_app /bokeh_app

WORKDIR /bokeh_app

EXPOSE 5006:5006

ENTRYPOINT ["bokeh","serve","--show","."]