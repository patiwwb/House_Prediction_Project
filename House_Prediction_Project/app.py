from flask import Flask, render_template, request
from flask import jsonify
import requests
import pickle
import numpy as np
import os
app = Flask(__name__)

with open('saved_steps.pkl', 'rb') as file:
    data = pickle.load(file)
model = data["model"]
sc = data["scaler"]



@app.route('/',methods=['GET'])
def Home():
    return render_template('index.html')


d = {'Auburn': 0,
 'Beaux Arts Village': 1,
 'Bellevue': 2,
 'Black Diamond': 3,
 'Bothell': 4,
 'Burien': 5,
 'Carnation': 6,
 'Clyde Hill': 7,
 'Covington': 8,
 'Des Moines': 9,
 'Duvall': 10,
 'Enumclaw': 11,
 'Fall City': 12,
 'Federal Way': 13,
 'Inglewood-Finn Hill': 14,
 'Issaquah': 15,
 'Kenmore': 16,
 'Kent': 17,
 'Kirkland': 18,
 'Lake Forest Park': 19,
 'Maple Valley': 20,
 'Medina': 21,
 'Mercer Island': 22,
 'Milton': 23,
 'Newcastle': 24,
 'Normandy Park': 25,
 'North Bend': 26,
 'Pacific': 27,
 'Preston': 28,
 'Ravensdale': 29,
 'Redmond': 30,
 'Renton': 31,
 'Sammamish': 32,
 'SeaTac': 33,
 'Seattle': 34,
 'Shoreline': 35,
 'Skykomish': 36,
 'Snoqualmie': 37,
 'Snoqualmie Pass': 38,
 'Tukwila': 39,
 'Vashon': 40,
 'Woodinville': 41,
 'Yarrow Point': 42}

def process_input(scaler,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,
                  sqft_above,sqft_basement,yr_built,yr_reno,street,city,statezip,country):
    X = np.array([[bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,sqft_above,sqft_basement,yr_built,yr_reno,street,city,statezip,country]])
    l = [0]*56
    l = np.array(l)
    l =l.reshape(1,l.shape[0])
    X = X[0][:-2]
    city = X[-1]
    X = X[:-2]
    zeros = [0]*43
    zeros = np.array(zeros)
    zeros = zeros.reshape(1,zeros.shape[0])
    X =np.append(X,zeros)
    X[d[city]]=1
    X[:12]=scaler.transform([X[:12]])
    return [X]
    

@app.route("/predict", methods=['POST'])
def predict():
    if request.method == 'POST':
        bedrooms = float(request.form['Bedrooms'])
        bathrooms = float(request.form['Bathrooms'])
        sqft_living = float(request.form['Bedrooms'])
        sqft_lot = float(request.form['Bedrooms'])
        floors = float(request.form['Bedrooms'])
        waterfront = float(request.form['Bedrooms'])
        view = float(request.form['Bedrooms'])
        condition = float(request.form['Bedrooms'])
        sqft_above = float(request.form['Bedrooms'])
        sqft_basement = float(request.form['Bedrooms'])
        year_built = float(request.form['Bedrooms'])
        year_renovation = float(request.form['Bedrooms'])
        street = str(request.form['street'])
        city = str(request.form['city'])
        statezip = str(request.form['statezip'])
        country = str(request.form['Country'])
        
        values = process_input(sc,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,
                  sqft_above,sqft_basement,year_built,year_renovation,street,city,statezip,country)
       
        prediction=model.predict(values)
        output=round(prediction[0],2)
        if output<0:
            return render_template('index.html',prediction_texts="Sorry you cannot sell this house")
        else:
            return render_template('index.html',prediction_text="You Can Sell The House at {}".format(output))
    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)