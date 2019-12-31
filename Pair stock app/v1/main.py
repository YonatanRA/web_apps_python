# librerias
from flask import Flask
from flask import render_template
from flask import request



import matplotlib
matplotlib.use('agg')

import os
import pandas as pd



# constantes
CARTERA=10000
DIAS_ATRAS=90
INDICE=['^DJI']
STOCKS=['BA','GS','UNH','MMM','HD','AAPL','MCD','IBM','CAT','TRV']
PATH=os.path.dirname(os.path.abspath(__file__))


# variables globales
stock_data=None

app = Flask(__name__)



# funcion para preparar los datos, todos los csv en una pivot table
# devuelve un dataframe
def data():
    stock_data=[]

    for e in INDICE+STOCKS:
        src=os.path.join(PATH, 'data/'+ e +'.csv')
        df=pd.read_csv(src)
        df['Symbol']=e
        df=df[['Symbol', 'Date', 'Adj Close']]
        stock_data.append(df)

    stock_data=pd.concat(stock_data)

    stock_data=stock_data.pivot('Date','Symbol')
    stock_data.columns=stock_data.columns.droplevel()
    stock_data=stock_data.tail(90)

    return (stock_data)



# antes del primer request, haz la pivot table
@app.before_first_request
def startup():
    global stock_data
    stock_data=data()




# funcion para microservicio
# todo, salvo el html, esta aqui
@app.route('/', methods=['POST', 'GET'])
def main():
    if request.method=='POST':   # para html, subida
        cartera=request.form['cartera']
        if cartera=='':  cartera=10000

        # calcula el spread
        stock1='^DJI'
        distancias={}

        serie1=stock_data[stock1].pct_change().cumsum()

        for stock2 in list(stock_data):
            if (stock1!=stock2):
                serie2=stock_data[stock2].pct_change().cumsum()
                diff=list(serie2-serie1)
                distancias[stock2]=diff[-1]


        # stock mas debil y stock mas fuerte
        debil=min(distancias.items(), key=lambda x: x[1])
        fuerte=max(distancias.items(), key=lambda x: x[1])


        # sentido del trade
        corto=fuerte[0]
        corto_ult=stock_data[fuerte[0]][-1]

        largo=debil[0]
        largo_ult=stock_data[debil[0]][-1]


        # se renderiza el html
        return render_template('index.html',
                               corto=corto,
                               largo=largo,
                               corto_ult=round(corto_ult,2),
                               size_corto=round((float(cartera)*.5)/corto_ult,2),
                               largo_ult=round(largo_ult,2),
                               size_largo=round((float(cartera)*.5)/largo_ult,2),
                               cartera=cartera)



    else:   # parametros por defecto


        return render_template('index.html',
                               corto='Nada',
                               largo='Nada',
                               corto_ult=0,
                               size_corto=0,
                               largo_ult=0,
                               size_largo=0,
                               cartera=CARTERA)











