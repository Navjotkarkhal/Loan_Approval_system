import streamlit as st
import numpy as np
import pandas as pd
import pickle
import base64

@st.cache_data
def load_model():
    return pickle.load(open('Random_Forest1.sav', 'rb'))

@st.cache_data
def get_fvalue(val):
    feature_dict = {"No": 1, "Yes": 2}
    return feature_dict.get(val)

def get_value(val, my_dict):
    return my_dict.get(val)

app_mode = st.sidebar.selectbox("Choose Page", ["Home", "Prediction"])

if app_mode == 'Home':    
    st.title('Loan Prediction')    
    data = pd.read_csv('loan_dataset.csv')    
    st.write(data.head())    
    st.bar_chart(data[['ApplicantIncome', 'LoanAmount']].head(20))

elif app_mode == 'Prediction':
    st.title('Loan Eligibility Prediction')
    

    Gender = st.selectbox('Gender', ['Male', 'Female'])
    Married = st.selectbox('Married', ['Yes', 'No'])
    Dependents = st.selectbox('Dependents', ['0', '1', '2', '3+'])
    Education = st.selectbox('Education', ['Graduate', 'Not Graduate'])
    Self_Employed = st.selectbox('Self Employed', ['Yes', 'No'])
    ApplicantIncome = st.number_input('Applicant Income', min_value=0)
    CoapplicantIncome = st.number_input('Coapplicant Income', min_value=0)
    LoanAmount = st.number_input('Loan Amount (in thousands)', min_value=0.0)
    Loan_Amount_Term = st.selectbox('Loan Amount Term', [360, 180, 120, 60])
    Credit_History = st.selectbox('Credit History', [1.0, 0.0])
    Property_Area = st.selectbox('Property Area', ['Urban', 'Semiurban', 'Rural'])

    gender_dict = {'Male': 1, 'Female': 0}
    edu_dict = {'Graduate': 1, 'Not Graduate': 0}
    prop_dict = {'Urban': 2, 'Semiurban': 1, 'Rural': 0}

    if st.button("Predict"):
        loaded_model = load_model()

        feature_list = [
            ApplicantIncome,
            CoapplicantIncome,
            LoanAmount,
            Loan_Amount_Term,
            Credit_History,
            gender_dict.get(Gender, 0),
            get_fvalue(Married),
            int(Dependents.replace('+', '')),
            edu_dict.get(Education, 0),
            get_fvalue(Self_Employed),
            prop_dict.get(Property_Area, 0)
        ]

        single_sample = np.array(feature_list).reshape(1, -1)
        prediction = loaded_model.predict(single_sample)

        # Load GIFs
        # file_yes = open("6m-rain.gif", "rb")
        # data_url_yes = base64.b64encode(file_yes.read()).decode()
        # file_yes.close()

        # file_no = open("green-cola-no.gif", "rb")
        # data_url_no = base64.b64encode(file_no.read()).decode()
        # file_no.close()

        if prediction[0] == 0:
            st.error('According to our calculations, you will not get the loan.')
            st.image('denied.png')
          
        else:
            st.success('Congratulations! You will get the loan.')
            st.image('icon.png  ')
            
