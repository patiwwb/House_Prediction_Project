import streamlit as st
import pickle
import numpy as np

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

model = data["model"]
sc = data["scaler"]

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
    

def show_predict_page():
    st.title("Home Price Prediction")

    st.write("""### We need some information to predict the price""")

    bedrooms = st.slider("bedrooms", 0, 5, 1)
    bathrooms = st.slider("bathrooms", 0, 5, 1)
    sqft_living = st.slider(label='sqflt_living',min_value=0.0,max_value=5000.0,value=1000.0,step=100.0)
    sqft_lot = st.slider(label='sqflt_lot',min_value=0.0,max_value=5000.0,value=1000.0,step=100.0)
    floors = st.slider("floors", 0, 5, 1)
    waterfront = st.slider("waterfront", 0, 5, 1)
    view =st.slider("view", 0, 5, 1)
    condition = st.slider("condition", 0, 5, 1)
    sqft_above = st.slider(label='sqflt_above',min_value=0.0,max_value=5000.0,value=1000.0,step=100.0)
    sqft_basement = st.slider(label='sqflt_basement',min_value=0.0,max_value=5000.0,value=1000.0,step=100.0)
    year_built = st.slider(label='year_built',min_value=1930,max_value=2021,value=1960,step=1)
    year_renovation = st.slider(label='year_renovation',min_value=1930,max_value=2021,value=1960,step=1)
    street= st.text_input("street")
    city = st.text_input("city")
    statezip = st.text_input("statezip")
    country = st.text_input("country")

    ok = st.button("Calculate Salary")
    if ok:
        values = process_input(sc,bedrooms,bathrooms,sqft_living,sqft_lot,floors,waterfront,view,condition,
                  sqft_above,sqft_basement,year_built,year_renovation,street,city,statezip,country)
       
        prediction=model.predict(values)
        st.subheader(f"The estimated price is ${prediction[0]:.2f}")