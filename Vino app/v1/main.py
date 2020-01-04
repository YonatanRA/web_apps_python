# librerias
from flask import Flask
from flask import render_template
from flask import request
from flask import jsonify

import logging

import os

import pandas as pd
import numpy as np

import pickle




# inicia flask
app=Flask(__name__)



# modelo 
gbc=None


# variables, caracteristicas
var=None
 
 
# ruta absoluta
PATH=os.path.dirname(os.path.abspath(__file__))
    

# para cargar las imagenes
def imagen_vino(color, calidad):
    if color==0:
        color_str='blanco'
    else:
        color_str='tinto'
    return('/static/images/vino_' +color_str+'_'+str(calidad)+'.jpg')




# antes del primer request
@app.before_first_request
def startup():
    global gbc
    gbc=pickle.load(open(PATH+'/data/gbc.p','rb'))
    global var
    var=pd.read_csv(PATH+'/data/vino_data.csv').drop('quality', axis=1).columns



# manejo de errores
@app.errorhandler(500)
def server_error(e):
    logging.exception('algun error...')
    return """
    And internal error <pre>{}</pre>
    """.format(e), 500



# conexion a traves de ruta
@app.route('/backend', methods=['POST', 'GET'])
def backend():
    # requests
    req=[request.args.get(e.replace(' ', '_')) for e in var]
    
    # nuevos datos
    n_data={k:v for k,v in zip(var, req)}
    n_data['color']=int(request.args.get('color'))
    
    X_pred=pd.DataFrame.from_dict(n_data, orient='index').T

    # prediccion
    prob=gbc.predict_proba(X_pred)

    pred=[3,6,9][np.argmax(prob[0])]
    
    return jsonify({'prediccion':pred, 
                    'imagen': imagen_vino(n_data['color'], pred)})


# principal
@app.route("/", methods=['POST', 'GET'])
def main():
    logging.warning('index!')
    # carga por defecto
    return render_template('index.html', 
                           prediccion=1, 
                           imagen=PATH+'/static/images/vino_tinto_6.jpg')





# solo en local
if __name__=='__main__':
    app.run(debug=True)
