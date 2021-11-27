# Core Pkgs
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# EDA Pkgs
import pandas as pd
import numpy as np

# Other Utilites
import os
import joblib
import hashlib


# Data Viz
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# DB
from managed_db import *

# Password
def generate_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()
# Verify Password/hashes
def verify_hashes(password,hashed_text):
    if generate_hashes(password) == hashed_text:
        return hashed_text
    return False


# GENDER DICTIONARY

feature_names_best = ['Age', 'Sex', 'Steroid', 'Antivirals', 'Fatigue', 'Spiders', 'Ascites','Varices', 'Bilirubin', 'Alk_phosphate', 'Sgot', 'Albumin', 'Protime','Histology']

gender_dict = {"Male": 1, "Female": 2}
feature_dict = {"Yes": 2, "No": 1}

def get_value(val, my_dict):
    for key,value in my_dict.items():
        if val == key:
            return value

def get_key(val, my_dict):
    for key,value in my_dict.items():
        if val == key:
            return key

def get_fvalue(val):
    feature_dict = {"Yes": 2, "No": 1}
    for key,value in feature_dict.items():
        if val == key:
            return value

# Load Model

def load_model(model_file):
	loaded_model = joblib.load(open(os.path.join(model_file),"rb"))
	return loaded_model

html_temp = """
		<div style="background-color:rgb(7, 88, 88);padding:10px;border-radius:10px; margin-bottom: 20px">
		<h1 style="color:rgb(224, 223, 225);text-align:center;">EpApp: Hepatitis B Survival Prediction Web App</h1>
		<h5 style="color:white;text-align:center;">Check your status using physiological parameters</h5>
		</div>
		"""


footer_part = """
		<div style="background-color:rgb(7, 88, 88);padding:10px;border-radius:10px; margin-bottom: 20px">
		<p style="color:rgb(224, 223, 225);text-align:center; font-size: 20px">To know your chance of survival from Hepatis B virus; Sign up, login, and input your physiological health parameters.</p>
        </div>
		"""

result_temp ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
	<img src="https://bit.ly/3cyaPF9" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>	
	<p style="text-align:justify;color:white">{} % probalibilty that Patient {}s</p>
	</div>
	"""

result_temp2 ="""
	<div style="background-color:#464e5f;padding:10px;border-radius:10px;margin:10px;">
	<h4 style="color:white;text-align:center;">Algorithm:: {}</h4>
	<img src="https://bit.ly/3x6M1xF/{}" alt="Avatar" style="vertical-align: middle;float:left;width: 50px;height: 50px;border-radius: 50%;" >
	<br/>
	<br/>	
	<p style="text-align:justify;color:white">{} % probalibilty that Patient {}s</p>
	</div>
	"""

prescriptive_message_temp ="""
	<div style="background-color:#207DAE;overflow-x: auto; padding:10px;border-radius:5px;margin:10px;">
		<h3 style="text-align:justify;color:white;padding:10px">Recommended Life style Approach</h3>        
		<ul>
		<li style="text-align:justify;color:white;padding:10px">Reduce Stress Level</li>
		<li style="text-align:justify;color:white;padding:10px">Totally Avoid Alcohol</li>
		<li style="text-align:justify;color:white;padding:10px">Exercise Regularly</li>
		<li style="text-align:justify;color:white;padding:10px">Avoid Inhaling Fumes from Toxic Chemicals</li>
		<li style="text-align:justify;color:white;padding:10px">Eat Healthy Foods</li>
		<ul>
		<h3 style="text-align:justify;color:white;padding:10px">Recommended Medical Approach</h3>
		<ul>
		<li style="text-align:justify;color:white;padding:10px">Always Go For Checkups</li>
		<li style="text-align:justify;color:white;padding:10px">Always consult Your Doctor</li>		
		<ul>
	</div>
	"""


descriptive_message_temp ="""
	<div style="background-color:rgb(194, 217, 235);overflow-x: auto; padding:10px;border-radius:5px;margin-bottom:30px;">
		<h3 style="text-align:justify;color:#101242;padding:10px">Do You Know:</h3>
		<p style="font-size: 20px;">WHO estimated that in 2019, the number of people living with chronic hepatitis B was 296 million, with a record of 1.5 million new infections every year. The estimated number of deaths from hepatitis B in 2019 was 820,000.
        To increase your chance of survival from acute and chronic Hepatitis B virus, you need to diagnose yourself constantly.</p>
	</div>
	"""



def main():
    """Hepatitis B Mortality Prediction App"""

    
    #st.title("Disease Mortality Prediction App")
    st.markdown(html_temp.format('royalblue'),unsafe_allow_html=True)

    menu = ["Home", "Login", "SignUp"]
    sub_menu = ["Prediction"]

    choice = st.sidebar.selectbox("Menu",menu)
    if choice == "Home":
        st.subheader("Home")
        #st.text("What is Hepatitis?")
        st.markdown(descriptive_message_temp,unsafe_allow_html=True)        
        st.markdown(footer_part,unsafe_allow_html=True)
        
        

        

    
    elif choice == "Login":
        username = st.sidebar.text_input("Username")
        password = st.sidebar.text_input("Password", type="password")
        if st.sidebar.checkbox("Login"):
            create_usertable()
            hashed_pswd = generate_hashes(password)
            result = login_user(username, verify_hashes(password, hashed_pswd))
            ### if password == "12345"
            if result:
                st.success('Welcome {}'.format(username))

                activity = st.selectbox("Activity", sub_menu)

                                   
                    
                # PREDICTION
                if activity == "Prediction":
                    st.subheader("Predictive Analytics")

                    Age = st.number_input("Age", 7, 80)
                    Sex = st.radio("Sex", tuple(gender_dict.keys()))
                    Steroid = st.radio("Do you take Steriod?", tuple(feature_dict.keys()))
                    Antivirals = st.radio("Do you take Antivirals?", tuple(feature_dict.keys()))
                    Fatigue = st.radio("Do you Have Fatigue?", tuple(feature_dict.keys()))
                    Spiders = st.radio("Do you have Spiders Naevi?", tuple(feature_dict.keys()))
                    Ascites = st.selectbox("Ascites", tuple(feature_dict.keys()))
                    Varices = st.selectbox("Varices", tuple(feature_dict.keys()))
                    Bilirubin = st.number_input("Bilirubin", 0.0, 0.8)
                    Alk_phosphate= st.number_input("Alkaline Phosphate Content", 0.8, 296.0)
                    Sgot = st.number_input("Sgot", 0.0, 648.0)
                    Albumin = st.number_input("Albumin", 0.0, 6.4)
                    Protime = st.number_input("Prothromin Time", 0.0, 100.0)
                    Histology = st.selectbox("Histology", tuple(feature_dict.keys()))
                    
                    #Age', 'Sex', 'Steroid', 'Antivirals', 'Fatigue', 'Spiders', 'Ascites','Varices',
                     #'Bilirubin', 'Alk_phosphate', 'Sgot', 'Albumin', 'Protime','Histology'
                    feature_list = [Age,get_value(Sex,gender_dict),get_fvalue(Steroid),get_fvalue(Antivirals),
                    get_fvalue(Fatigue), get_fvalue(Spiders),get_fvalue(Ascites),get_fvalue(Varices),
                    Bilirubin,Alk_phosphate,Sgot,Albumin,
                    int(Protime),get_fvalue(Histology)]

                    st.write(feature_list)

                    pretty_result = {"Age": Age,"Sex": Sex, "Antivirals": Antivirals, "Fatigue": Fatigue, "Spiders": Spiders,
                                    "Ascites":Ascites, "Varices":Varices, "Bilirubin": Bilirubin, "Alk_phosphate":
                                    Alk_phosphate, "Sgot": Sgot, "Albumin": Albumin, "Protime": Protime, "Histology": Histology}
                    
                    st.json(pretty_result)
                    single_sample = np.array(feature_list).reshape(1, -1)

                    # Model Choice
                    model_choice = st.selectbox("Select Model", ["Prediction Score"])
                    if st.button('Predict'):
                        if model_choice == "Prediction Score":
                            loaded_model = load_model("models/knn_hepB_model.pkl")
                            prediction = loaded_model.predict(single_sample)
                            pred_prob = loaded_model.predict_proba(single_sample)                            
                            
                          
                        if prediction == 1:
                            st.warning("Patient Chance of Survival is Low")
                            pred_probability_score = {"Low":pred_prob[0][0]*100,"High":pred_prob[0][1]*100}
                            st.subheader("Predicton Probability Score")
                            st.json(pred_probability_score)
                            st.markdown(prescriptive_message_temp,unsafe_allow_html=True) 
                            
                        else:
                            st.success("Patient Chance of Survival is High")
                            pred_probability_score = {"Low":pred_prob[0][0]*100,"High":pred_prob[0][1]*100} 
                            st.subheader("Predicton Probability Score")
                            st.json(pred_probability_score)
                            st.markdown(prescriptive_message_temp,unsafe_allow_html=True)
                            

                
            
            else:
                st.warning("Incorrect Username/Password")  

    
    elif choice == "SignUp":
        new_username = st.text_input("Username")
        new_password = st.text_input("Password", type='password')   

        confirm_password = st.text_input("Confirm Password",type='password')
        if new_password == confirm_password:
            st.success("Password Confirmed")     
        

        else:
            st.warning("Passwords not the same")
        
        if st.button("Submit"):
            create_usertable()
            hashed_new_password = generate_hashes(new_password)
            add_userdata(new_username,hashed_new_password)
            st.success("You have successfully created a new account")
            st.info("Login to Get Started")
        

if __name__ == '__main__':
    main()