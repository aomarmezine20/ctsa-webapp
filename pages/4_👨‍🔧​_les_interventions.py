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
    st.header('-----------------PARC T1------------------')
    st.subheader('Le nombre total d’ordre de travaux')
    st.markdown('  * le nombre des interventions du mois est **'+str(df_t1["Code de l'intervention"].count())+'** ')
    st.subheader('La répartition des interventions de maintenance par type :')
    #plot etat of interventions pie chart 
    fig = px.pie(df_t1, names="Nature d'intervention",color="Nature d'intervention")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_DI.jpeg")
    #make data frame for just nature of intervention and count how much for every values 
    df_intv_count = df_t1["Nature d'intervention"].value_counts()

    #rest index to separate index colomn and make calculation to show every nature of intervention 
    df_intv_count = df_intv_count.reset_index()
    st.header('Suivi de la maintenance préventive ')
    st.markdown('  * le nombre des interventions préventives du mois est **'+str(int(df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"]))+'** ')
    st.subheader('Suivi des interventions préventives :')
    #make a new datafram for just perventif intervention and name it 
    df_t1_prv =df_t1[df_t1["Nature d'intervention"]=='PREVENTIF']
    
    #calcule every gamme how much have of status for every type of status and name it df_t1_prv2
    df_t1_prv2 =df_t1_prv[["Gamme de maintenance à l'origine de l'intervention",'Etat']].value_counts().reset_index()
    
    #plot the datafram in bar chart 
    fig = px.bar(df_t1_prv2,x="Gamme de maintenance à l'origine de l'intervention", y=df_t1_prv2[0],color='Etat', text_auto='',labels={
                     "0": "Etat",})

    #plot it 
    st.plotly_chart(fig)
    
    st.subheader('Taux d’occupation par parc :')
    st.header('Suivi des interventions correctives')
    #show nbr of correctif interventions
    st.markdown('  * le nombre des interventions correctives du mois est **'+str(int(df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"]))+'** ')
    st.subheader('La répartition des interventions correctives par priorités :')

    #make a new datafram for just correctif intervention and name it 
    df_t1_cr =df_t1[df_t1["Nature d'intervention"]=='CORRECTIF']

    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t1_cr, names="Priorité")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    #explaine every priority key of chart
    st.markdown("* **FJ ( y compris les FJ prioritaire):** Fin de Jour, c’est une panne mineur qui peut etre planifiée à la fin de l’exploitation de la rame")
    st.markdown("* **FT :** Fin de Tour, c’est une panne qui nécessite le rapatriement de la rame à la fin de sa course")
    st.markdown("* **HLP :** Haut le Pied, c’est une panne majeur qui nécessite l’évacuation des voyageurs et le rapatriement immédiat de le rame")
    st.markdown("* **RP :** Remorquage/Poussage, c’est une panne majeur qui nécessite l’évacuation des voyageurs et le rapatriement de la rame en mode US-US soit par remorquage [ US menante], soit par poussage [US menée] ou par camion rail-route.")
    
    #make new datafram of famille des defaut count
    st.subheader("La répartition des interventions par famille de défaut :")
    df_t1_cr2 =df_t1_cr[["Famille de défaut"]].value_counts().reset_index()
    #plot this datafrm in bar chart
    fig = px.bar(df_t1_cr2,x="Famille de défaut",y=df_t1_cr2[0], text_auto='',labels={
                     "0": "Nbr des OT",})

    st.plotly_chart(fig)

    st.subheader("La répartition des interventions correctives en fonction des ‘’Etat’’ :")
    
    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t1_cr, names="Etat")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)





#--------------------------------------------PARC T2 ------------------------------------------------------------------------------------
    st.header('-----------------PARC T2------------------')
    st.subheader('Le nombre total d’ordre de travaux')
    st.markdown('  * le nombre des interventions du mois est **'+str(df_t2["Code de l'intervention"].count())+'** ')
    st.subheader('La répartition des interventions de maintenance par type :')
    #plot etat of interventions pie chart 
    fig = px.pie(df_t2, names="Nature d'intervention",color="Nature d'intervention")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_DI.jpeg")
    #make data frame for just nature of intervention and count how much for every values 
    df_intv_count2 = df_t2["Nature d'intervention"].value_counts()

    #rest index to separate index colomn and make calculation to show every nature of intervention 
    df_intv_count2 = df_intv_count2.reset_index()
    st.header('Suivi de la maintenance préventive ')
    st.markdown('  * le nombre des interventions préventives du mois est **'+str(int(df_intv_count2[df_intv_count2['index']=='PREVENTIF']["Nature d'intervention"]))+'** ')
    st.subheader('Suivi des interventions préventives :')
    #make a new datafram for just perventif intervention and name it 
    df_t2_prv =df_t2[df_t2["Nature d'intervention"]=='PREVENTIF']
    
    #calcule every gamme how much have of status for every type of status and name it df_t1_prv2
    df_t2_prv2 =df_t2_prv[["Gamme de maintenance à l'origine de l'intervention",'Etat']].value_counts().reset_index()
    
    #plot the datafram in bar chart 
    fig = px.bar(df_t2_prv2,x="Gamme de maintenance à l'origine de l'intervention", y=df_t2_prv2[0],color='Etat', text_auto='',labels={
                     "0": "Etat",})

    #plot it 
    st.plotly_chart(fig)
    
    st.subheader('Taux d’occupation par parc :')
    st.header('Suivi des interventions correctives')
    #show nbr of correctif interventions
    st.markdown('  * le nombre des interventions correctives du mois est **'+str(int(df_intv_count2[df_intv_count2['index']=='CORRECTIF']["Nature d'intervention"]))+'** ')
    st.subheader('La répartition des interventions correctives par priorités :')

    #make a new datafram for just correctif intervention and name it 
    df_t2_cr =df_t2[df_t2["Nature d'intervention"]=='CORRECTIF']

    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t2_cr, names="Priorité")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    #explaine every priority key of chart
    st.markdown("* **FJ ( y compris les FJ prioritaire):** Fin de Jour, c’est une panne mineur qui peut etre planifiée à la fin de l’exploitation de la rame")
    st.markdown("* **FT :** Fin de Tour, c’est une panne qui nécessite le rapatriement de la rame à la fin de sa course")
    st.markdown("* **HLP :** Haut le Pied, c’est une panne majeur qui nécessite l’évacuation des voyageurs et le rapatriement immédiat de le rame")
    st.markdown("* **RP :** Remorquage/Poussage, c’est une panne majeur qui nécessite l’évacuation des voyageurs et le rapatriement de la rame en mode US-US soit par remorquage [ US menante], soit par poussage [US menée] ou par camion rail-route.")
    
    #make new datafram of famille des defaut count
    st.subheader("La répartition des interventions par famille de défaut :")
    df_t2_cr2 =df_t2_cr[["Famille de défaut"]].value_counts().reset_index()
    #plot this datafrm in bar chart
    fig = px.bar(df_t2_cr2,x="Famille de défaut",y=df_t2_cr2[0], text_auto='',labels={
                     "0": "Nbr des OT",})

    st.plotly_chart(fig)

    st.subheader("La répartition des interventions correctives en fonction des ‘’Etat’’ :")
    
    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t2_cr, names="Etat")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)