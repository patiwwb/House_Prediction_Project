import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go


@st.cache
def load_data():
    df0 = pd.read_csv(r"C:\Users\chlan\Desktop\New stuff\House_Prediction_Project\data.csv")
    df0.drop_duplicates()
    df0.drop(columns=['date'],inplace = True)
    
    num_cols = []
    cat_cols = []
    for i in df0.columns:
        if df0[i].dtypes == 'O':
            cat_cols.append(i)
        else:
            num_cols.append(i)
    
    for i in num_cols:
        df0[i]=df0[i].astype(float)
        
    df0 = df0[(
                (df0['price'] <= 1000000) & 
                (df0['price'] > 150000) & 
                (df0['bathrooms'] <= 6) & 
                (df0['condition'] > 2) & 
                (df0['sqft_living'] > 800) & 
                (df0['bedrooms'] >= 1) & 
                (df0['bedrooms'] <= 4.5) 
                )]
    df0 = df0[df0['price']!=0]
    
    return df0

df = load_data()

def show_explore_page():
    st.title("Explore House Prices")

    st.write(
        """
    ### Kaggle dataset 
    """
    )
    
    fig = px.histogram(df, x="price",
                   marginal="box", # or violin, rug
                   hover_data=df.columns)
    


    st.write("""#### Distribution of prices""")

    st.plotly_chart(fig)

    st.write(
        """
    ### City frequency
    """
    )

    fig1 = plt.figure(figsize=(25, 6))
    
    plt.subplot(1,2,1)
    plt1 = df.city.value_counts().plot(kind='bar')
    plt.title('City Histogram')
    plt1.set(xlabel = 'City', ylabel='Frequency')

    st.pyplot(fig1)
    