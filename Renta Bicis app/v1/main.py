from flask import Flask
from flask import render_template
from flask import request

import pandas as pd
import os
    
# inicia Flask
app = Flask(__name__)



# directorio base
PATH=os.path.dirname(os.path.abspath(__file__))
#PATH=''
# coeficientes
coefs=None

# valores medios como datos de entrada
input_data=None


@app.before_first_request
def startup():
    global coefs
   # path_cofs=os.path.join()
    coefs=pd.read_csv(PATH+'/data/coefs.csv')\
            .set_index('carac')\
            .to_dict()['coef']
    
    global input_data
    input_data=pd.read_csv(PATH+'/data/means.csv', 
                           names=['carac', 'coef'])\
                 .set_index('carac')\
                 .to_dict()['coef']
    

# cuando carga, son los valores por defecto
# se va a predecir sobre 4 caracteristicas, pero se necesita evaluar
# con todas.
@app.route("/", methods=['POST', 'GET'])
def main():
    return render_template('index.html',
                           
            holiday=input_data['holiday'],
            hr=input_data['hr'],
            yr=input_data['yr'],
            hum=input_data['hum'],
            temp=input_data['temp'],
            atemp=input_data['atemp'],
            windspeed=input_data['windspeed'],
            season_1=1,
            season_2=0,
            season_3=0,
            season_4=0,
            weathersit_1=input_data['weathersit_1'],
            weathersit_2=input_data['weathersit_2'],
            weathersit_3=input_data['weathersit_3'],
            weathersit_4=input_data['weathersit_4'],
            weekday_1=input_data['weekday_1'],
            weekday_2=input_data['weekday_2'],
            weekday_3=input_data['weekday_3'],
            weekday_4=input_data['weekday_4'],
            weekday_5=input_data['weekday_5'],
            weekday_6=input_data['weekday_6'],
            weekday_0=input_data['weekday_0'],
            sum_hr_1=input_data['sum_hr_1'],
            sum_hr_2=input_data['sum_hr_2'],
                        
                           
            coef_intercept=coefs['intercept'],
            coef_holiday=coefs['holiday'],
            coef_hr=coefs['hr'],
            coef_yr=coefs['yr'],
            coef_hum=coefs['hum'],
            coef_temp=coefs['temp'],
            coef_atemp=coefs['atemp'],
            coef_windspeed=coefs['windspeed'],
            coef_season_1=coefs['season_1'],
            coef_season_2=coefs['season_2'],
            coef_season_3=coefs['season_3'],
            coef_season_4=coefs['season_4'],
            coef_weathersit_1=coefs['weathersit_1'],
            coef_weathersit_2=coefs['weathersit_2'],
            coef_weathersit_3=coefs['weathersit_3'],
            coef_weathersit_4=coefs['weathersit_4'],
            coef_weekday_1=coefs['weekday_1'],
            coef_weekday_2=coefs['weekday_2'],
            coef_weekday_3=coefs['weekday_3'],
            coef_weekday_4=coefs['weekday_4'],
            coef_weekday_5=coefs['weekday_5'],
            coef_weekday_6=coefs['weekday_6'],
            coef_weekday_0=coefs['weekday_0'],
            coef_sum_hr_1=coefs['sum_hr_1'],
            coef_sum_hr_2=coefs['sum_hr_2'])




# para ejecutar en local
if __name__=='__main__':
      app.run(debug=True)
