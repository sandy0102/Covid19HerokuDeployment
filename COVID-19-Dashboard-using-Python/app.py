from flask import Flask, render_template, send_file, make_response
from coronaIndia import table, plot1, plot2, plot3, top20, bedslowest, datewise, ageWise, malefemaleratio, total,icmr,positive,icmrlabs
from flask import *
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

app = Flask(__name__)

@app.route('/')
def show_tables():
    tableDisplay = table()
    figureDisplay1 = plot1()
    figureDisplay2=plot2()
    figureDisplay3=plot3()
    top20fig = top20()
    bedsLowestCount = bedslowest()
    dateWise = datewise()
    ageWiseDate = ageWise()
    maleFemaleRatio = malefemaleratio()
    icmrdata=icmr()
    totals=total()
    positives=positive()
    icmrlabData=icmrlabs()
    return render_template('index.html',  returnList = tableDisplay, figure1=figureDisplay1, figure2=figureDisplay2,figure3=figureDisplay3,
                    top20list=top20fig, bedsLowest=bedsLowestCount, dateWiseData=dateWise,
                    ageWiseData=ageWiseDate, maleFemale=maleFemaleRatio, total_data=totals,icmr_data=icmrdata, pos=positives,icmr_lab=icmrlabData)
    

if __name__ == "__main__":
    app.jinja_env.cache = {}
    app.run(debug=True)