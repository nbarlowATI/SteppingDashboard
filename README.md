# SteppingDashboard

Bokeh dashboard for displaying weekly step counts.
Based largely on series of blog posts and corresponding Github repo by Will Koehrsen:

https://towardsdatascience.com/data-visualization-with-bokeh-in-python-part-iii-a-complete-dashboard-dc6a86aa6e23
https://github.com/WillKoehrsen/Bokeh-Python-Visualization/

### How to run natively

You will need a relatively recent python version, and pip, installed:
```
pip install -r bokeh_app/requirements.txt
```
This should install the necessary python packages (basically pandas and bokeh).
Then you can run with
```
bokeh serve --show bokeh_app
```
and point your browser to ```http://localhost:5006/bokeh_app```

### How to run with docker

If you have docker installed and running, you can do
```
docker build -t stepdash -f Dockerfile .
docker run -p 5006:5006 -it stepdash
```
and again, point your browser to ```http://localhost:5006/bokeh_app```
