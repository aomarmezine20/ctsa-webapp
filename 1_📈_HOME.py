import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from streamlit_option_menu import option_menu




st.set_page_config(page_title= 'Ctsa Web app', page_icon="./images/big_logo.png",menu_items={})
st. title('Welcome')
#------------- hide footer 
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#---- remove list pages 
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)

image = Image.open('images/big_logo.png')


col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    st.image(image,width=380)

with col3:
    st.write(' ')












import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
with st.sidebar:
    selected = option_menu("Reporting Tram", ["Home","Gestion kilométrique", "Demandes d’interventions (DI)","les interventions","Pièces de rechange"], 
        icons=["bi-house-door","bi-graph-up-arrow", "bi-clipboard-check","bi-wrench", "gear"], menu_icon="bi-arrow-right-square", default_index=0)
 
   
if selected == "Gestion kilométrique" :
   switch_page("gestion kilométrique")

if selected == "Demandes d’interventions (DI)" :
    switch_page("demandes d’interventions (di)")

if selected == "les interventions" :
   switch_page("\u200b les interventions")

elif selected == "Pièces de rechange" :
    switch_page("\u200a pièces de rechange")


with st.sidebar:
    selected = option_menu("Reporting Bus", ["Répartition des OT", 'Rapport 2'], 
        icons=['house', 'gear'], menu_icon="bi-arrow-right-square", default_index=1)
if selected == "Répartition des OT" :
    switch_page("Reporting_bus")