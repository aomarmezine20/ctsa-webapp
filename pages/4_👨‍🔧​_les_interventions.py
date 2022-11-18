import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
import matplotlib.pyplot as plt
from PIL import Image
from base64 import b64encode
from fpdf import FPDF


st.set_page_config(page_title= 'les interventions)', page_icon="👨‍🔧")
st. title('les statistiques des interventions')

uploaded_file1 =st.file_uploader('fichier des interventions', type=['xlsx','xls','csv'])


if uploaded_file1 :
    st.markdown('---')
    st.subheader('fichier d’interventions')
    #read file python
    df = pd.read_excel(uploaded_file1)

    st.dataframe(df)

    df[['US','autre','autre2','autre3']] = df['Matériel'].str.split(".",expand=True)

    #creat list of T1 parc 
    def parc1() :
        T=[]
        for i in range (0,10):
            T.append('US00'+str(i))
        for i in range(10,75):
            T.append('US0'+str(i))
        return(T)
    #creat list of parc T2
    def parc2():
        T=[]
        for i in range(75,100):
            T.append('US0'+str(i))
        for i in range(100,125):
            T.append('US'+str(i))
        return(T)
        
    df_t1 = df[df['US'].isin(parc1())]
    df_t2 = df[df['US'].isin(parc2())]
#-----------------PARC T1 --------------------------------------------------------------------------------------------------------------------------
    st.header('---------------------------PARC T1------------------')
    st.subheader('Le nombre total d’ordre de travaux')
    st.markdown('  * le nombre des interventions du mois est **'+str(df_t1["Code de l'intervention"].count())+'** ')
    st.subheader('Le nombre total d’ordre de travaux ')
    #plot etat of interventions pie chart 
    fig = px.pie(df_t1, names="Nature d'intervention",color="Nature d'intervention")
    st.plotly_chart(fig)
    fig.write_image("images/fig_DI.jpeg")

    df_intv_count = df_t1["Nature d'intervention"].value_counts()
    
    st.dataframe(df_intv_count)
    df_intv_count = df_intv_count.reset_index()
    st.subheader('Suivi de la maintenance préventive ')
    st.markdown('  * le nombre des interventions préventives du mois est **'+str(int(df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"]))+'** ')
    st.subheader('Suivi des interventions préventives :')

    df_t1_prv =df_t1[df_t1["Nature d'intervention"]=='PREVENTIF']
    

    df_t1_prv2 =df_t1_prv[["Gamme de maintenance à l'origine de l'intervention",'Etat']].value_counts().reset_index()
    

    fig = px.bar(df_t1_prv2,x="Gamme de maintenance à l'origine de l'intervention", y=df_t1_prv2[0],color='Etat', text_auto='',labels={
                     "0": "Etat",})

    
    st.plotly_chart(fig)
    st.subheader('Taux d’occupation par parc :')