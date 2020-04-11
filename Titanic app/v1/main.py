from flask import Flask
from flask import render_template
from flask import request
from flask import Markup

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

import io
import os
import base64

import numpy as np
from numpy import genfromtxt
from sklearn.linear_model import LogisticRegression as LogReg
from sklearn.model_selection import train_test_split as tts
 

# necesario en pythonanywhere
PATH=os.path.dirname(os.path.abspath(__file__))


# default inicial
EMBARKED='Southampton'
FARE=33
AGE=30
GENDER='Female'
TITLE='Mrs.'
CLASS='Second'
CABIN='C'
SIBSP=0
PARCH=0


# inicializando variables
tasa_media=0



# modelo 
logreg=LogReg()



# flask app
app=Flask(__name__)



# antes del primer request...
@app.before_first_request
def startup():
    global tasa_media, logreg
    
    data=genfromtxt(PATH+'/data/titanic.csv', delimiter=',')
    
    tasa_media=(np.mean([e[0] for e in data])*100)

    
    logreg.fit([e[1:] for e in data], [e[0] for e in data])  # se entrena una vez antes de arrancar
    
    

    
# main app
@app.route("/", methods=['POST', 'GET'])
def main():
    model_results=''
    
    if request.method=='POST':
        s_embarked=request.form['s_embarked']
        s_fare=request.form['s_fare']
        s_age=request.form['s_age']
        s_gender=request.form['s_gender']
        s_title=request.form['s_title']
        s_class=request.form['s_class']
        s_cabin=request.form['s_cabin']
        s_sibsp=request.form['s_sibsp']
        s_parch=request.form['s_parch']
        
        # se reasigna para prediccion
        age=int(s_age)
        isfemale=1 if s_gender=='Female' else 0
        sibsp=int(s_sibsp)
        parch=int(s_parch)
        fare=int(s_fare)
        
        
        # puerto de embarque
        embarked_Q=1
        embarked_S=0
        embarked_Unknown=0 
        embarked_nan=0
        if (s_embarked[0]=='Q'):
            embarked_Q = 1
        if (s_embarked[0]=='S'):
            embarked_S = 1
            
        
        # clase
        pclass_Second=0
        pclass_Third=0
        pclass_nan=0
        if (s_class=='Second'):
            pclass_Second=1
        if (s_class=='Third'):
            pclass_Third=1
            
            
        
        # titulo
        title_Master=0
        title_Miss=0
        title_Mr=0
        title_Mrs=0
        title_Rev=0
        title_Unknown=0
        title_nan=0
        if (s_title=='Master.'):
            title_Master=1
        if (s_title=='Miss.'):
            title_Miss=1
        if (s_title=='Mr.'):
            title_Mr=1
        if (s_title=='Mrs.'):
            title_Mrs=1
        if (s_title=='Rev.'):
            title_Master=1
        if (s_title=='Unknown'):
            title_Unknown=1
            
            
        # cabina
        cabin_B=0
        cabin_C=0  
        cabin_D=0  
        cabin_E=0
        cabin_F=0
        cabin_G=0
        cabin_T=0
        cabin_Unknown=0
        cabin_nan=0
        if (s_cabin=='B'):
            cabin_B=1
        if (s_cabin=='C'):
            cabin_C=1
        if (s_cabin=='D'):
            cabin_D=1
        if (s_cabin=='E'):
            cabin_E=1
        if (s_cabin=='F'):
            cabin_F=1
        if (s_cabin=='G'):
            cabin_G=1
        if (s_cabin=='T'):
            cabin_T=1
        if (s_cabin=='Unknown'):
            cabin_Unknown=1
            
            
        
        # pasajero
        pasajero=[[age, sibsp, parch, fare, isfemale, 
                   pclass_Second, pclass_Third, pclass_nan, 
                   cabin_B, cabin_C, cabin_D, cabin_E, cabin_F, cabin_G,
                   cabin_T, cabin_Unknown, cabin_nan, embarked_Q, 
                   embarked_S, embarked_Unknown, embarked_nan, 
                   title_Master, title_Miss, title_Mr, title_Mrs, 
                   title_Rev, title_Unknown, title_nan]]
        
        
        # prediccion
        y_prob=logreg.predict_proba(pasajero)
        
        # plot
        with plt.xkcd():
            plt.figure()
            plt.bar(range(2),[tasa_media, y_prob[0][1]*100],
                    align='center', color=['y', 'b'], alpha=0.5)
            
            plt.xticks(range(2), ['Tasa Supervivencia media', 'Pasajero'])
            plt.axhline(tasa_media, color='r')
            plt.ylim([0,100])
            plt.ylabel('Probabilidad Supervivencia')
            plt.title('¿Sobrevivirá tu pasajero? \n '+'¡{:.2f}% de probabilidad!'.format(y_prob[0][1]*100))
            img=io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            plot_url=base64.b64encode(img.getvalue()).decode()
            
        
        return render_template('index.html',
            model_results=model_results,
            model_plot=Markup('<img src="data:image/png;base64,{}">'.format(plot_url)),
            s_embarked=s_embarked,
            s_fare=s_fare,
            s_age=s_age,
            s_gender=s_gender,
            s_title=s_title,
            s_class=s_class,
            s_cabin=s_cabin,
            s_sibsp=s_sibsp,
            s_parch=s_parch)
    
    
    
    else:
        # parametros por defecto
        return render_template('index.html',
            model_results = '',
            model_plot = '',
            s_embarked=EMBARKED,
            s_fare=FARE,
            s_age=AGE,
            s_gender=GENDER,
            s_title=TITLE,
            s_class=CLASS,
            s_cabin=CABIN,
            s_sibsp=SIBSP,
            s_parch=PARCH)
    
    
    
    
# solo para local 
if __name__=='__main__':
    app.run(debug=True)
    
    
    
    
    
       
    
