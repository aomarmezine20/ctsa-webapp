import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from base64 import b64encode
from fpdf import FPDF

st.set_page_config(page_title= 'Répartition des OT et des coûts par dépôt :', page_icon="./images/big_logo.png")
st. title('Répartition des OT et des coûts par dépôt :')





hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#upload file1 xls

uploaded_file1 =st.file_uploader("Fichier D'extraction", type=['xlsx','xls','csv'])
uploaded_file2 =st.file_uploader("Fichier D'extraction PDR", type=['xlsx','xls','csv'])


#---- remove list pagees
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
#-------  MENUUUU -----------------
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
with st.sidebar:
    selected = option_menu("Reporting Tram", ["Home","Gestion kilométrique", "Demandes d’interventions (DI)","les interventions","Pièces de rechange"], 
        icons=["bi-house-door","bi-graph-up-arrow", "bi-clipboard-check","bi-wrench", "gear"], menu_icon="bi-arrow-right-square", default_index=1)
 
   
if selected == "Home" :
    switch_page("HOME")

if selected == "Demandes d’interventions (DI)" :
    switch_page("demandes d’interventions (di)")

if selected == "les interventions" :
   switch_page("\u200b les interventions")

elif selected == "Pièces de rechange" :
    switch_page("\u200a pièces de rechange")


with st.sidebar:
    selected = option_menu("Reporting Bus", ["Répartition des OT "], 
        icons=['house','gear'], menu_icon="bi-arrow-right-square", default_index=0)
    

exclude_values = ['910']
if uploaded_file1 :
    st.markdown('---')
    st.subheader("Reporting Bus" )
    df1 = pd.read_excel(uploaded_file1,engine='openpyxl')
    st.write(df1)
    st.subheader("Reporting Bus PDR" )
    df2 = pd.read_excel(uploaded_file2,engine='openpyxl')
    st.write(df2)


    st.header('------------------Dépôt Bernoussi------------------')
    

    #----creat DATAFRAME FOR JUST BERNOSSI DEPOT -----------------
    df_BER = df1[df1['Intervention'].str.startswith('BER')]
    df_BER = df_BER.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df_BER['Actif'] = pd.to_numeric(df_BER['Actif'], errors='coerce').astype('Int64')
    df_BER = df_BER.dropna(subset=['Actif'])
    
    df_BER = df_BER.drop(df_BER[(df_BER['Actif'] < 32836) | (df_BER['Actif'] > 33535)].index)
    
    
    
    
    
    #----sum the cout totale effective pour chaque type -----------------
    df_BER_sort = pd.pivot_table(df_BER, index=["Type de réparation"],values=['Coût total effectif'],aggfunc='sum').reset_index()
    #---- sum every type of repartition and show it in a dataframe --------------------------
    value_counts = df_BER["Type de réparation"].value_counts().reset_index()
    
    #---- rename the dataframe of the count of every repartion to new name columns -------------------
    value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    st.write("Sur **"+str(sum(value_counts["nombre OT"]))+"** OT, la répartition par type d'intervention et son coût sur le dépôt de Bernoussi est comme se suit:")
    #creat a new data frame of description of every repartition type -----------------------------------
    data = data = [[1, "Maintenance"], [2, "Grandes réparations"], [3, "Accidents fautif"],[4, "Accidents sans faute"],[5, "Reformes"],[8, "Garanties"]
                   ,[9, "Matériel"],[51, "Vandalisme"],[62, "Qualité interieur"],[12, "Mauvais usage"],[90,"rien"]]
    
    df_type = pd.DataFrame(data, columns=['Type de réparation', 'Description'])
    # -----------merge three dataframe in one dataframe -----------------------------------------------
    
    df_1 = pd.merge(pd.merge(df_BER_sort, value_counts,on='Type de réparation'),df_type, on="Type de réparation")
    #-------change the type of reaparion count to str 
    df_1["Type de réparation"]=df_1["Type de réparation"].values.astype(str)



    #remove type rien in Description 
    df_1 = df_1.drop(df_1[df_1["Description"] == "rien" ].index)
    
    #-------sort the the maine dataframe in two dataframe every dataframe sorted in defirent way -------------------
    df_s1 =df_1.sort_values(['Coût total effectif'],ascending=[True])
    df_s2 =df_1.sort_values(['nombre OT'],ascending=[True])


    #--------- plot the two sorted dataframe one for cout totale effectif and the other for nombre Ot-----
    fig1 = px.bar(df_s1 ,x="Description",y="Coût total effectif",color="Coût total effectif",text="Coût total effectif",labels={'Description':'Type de réparation','value':'Coût total effectif'},height=500,width=900)
    st.write(fig1)
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]), 2))+"**DH")

    #--------------------------------------------------------------------------------------
    st.header('------------------Dépôt BENMSIK------------------')
    

    #----creat DATAFRAME FOR JUST BERNOSSI DEPOT -----------------
    df_BEN = df1[df1['Intervention'].str.startswith('BEN')]

    df_BEN = df_BEN.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df_BEN['Actif'] = pd.to_numeric(df_BEN['Actif'], errors='coerce').astype('Int64')
    df_BEN = df_BEN.dropna(subset=['Actif'])
    
    df_BEN = df_BEN.drop(df_BEN[(df_BEN['Actif'] < 32836) | (df_BEN['Actif'] > 33535)].index)
    
    #----sum the cout totale effective pour chaque type -----------------
    df_BEN_sort = pd.pivot_table(df_BEN, index=["Type de réparation"],values=['Coût total effectif'],aggfunc='sum').reset_index().astype(int)
    #---- sum every type of repartition and show it in a dataframe --------------------------
    value_counts = df_BEN["Type de réparation"].value_counts().reset_index()
    
    #---- rename the dataframe of the count of every repartion to new name columns -------------------
    value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    st.write("Sur **"+str(sum(value_counts["nombre OT"]))+"** OT, la répartition par type d'intervention et son coût sur le dépôt de BENMSIK est comme se suit:")
    #creat a new data frame of description of every repartition type -----------------------------------
    data = data = [[1, "Maintenance"], [2, "Grandes réparations"], [3, "Accidents fautif"],[4, "Accidents sans faute"],[5, "Reformes"],[8, "Garanties"]
                   ,[9, "Matériel"],[51, "Vandalisme"],[62, "Qualité interieur"],[12, "Mauvais usage"],[90,"rien"]]
    
    df_type = pd.DataFrame(data, columns=['Type de réparation', 'Description'])
    # -----------merge three dataframe in one dataframe -----------------------------------------------
    
    df_1 = pd.merge(pd.merge(df_BEN_sort, value_counts,on='Type de réparation'),df_type, on="Type de réparation")
    #-------change the type of reaparion count to str 
    df_1["Type de réparation"]=df_1["Type de réparation"].values.astype(str)

    #remove type rien in Description 
    df_1 = df_1.drop(df_1[df_1["Description"] == "rien" ].index)
    
    #-------sort the the maine dataframe in two dataframe every dataframe sorted in defirent way -------------------
    df_s1 =df_1.sort_values(['Coût total effectif'],ascending=[True])
    df_s2 =df_1.sort_values(['nombre OT'],ascending=[True])

    #--------- plot the two sorted dataframe one for cout totale effectif and the other for nombre Ot-----
    fig1 = px.bar(df_s1 ,x="Description",y="Coût total effectif",color="Coût total effectif",text="Coût total effectif",labels={'Description':'Type de réparation','value':'Coût total effectif'},height=500,width=900)
    st.write(fig1)
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]), 2))+"**DH")





    #--------------------------------------------------------------------------------------
    st.header('------------------Dépôt MAARIF------------------')
    

    #----creat DATAFRAME FOR JUST BERNOSSI DEPOT -----------------
    df_MAA = df1[df1['Intervention'].str.startswith('MAA')]


    df_MAA = df_MAA.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df_MAA['Actif'] = pd.to_numeric(df_MAA['Actif'], errors='coerce').astype('Int64')
    df_MAA = df_MAA.dropna(subset=['Actif'])
    
    df_MAA = df_MAA.drop(df_MAA[(df_MAA['Actif'] < 32836) | (df_MAA['Actif'] > 33535)].index)
    
    #----sum the cout totale effective pour chaque type -----------------
    df_MAA_sort = pd.pivot_table(df_MAA, index=["Type de réparation"],values=['Coût total effectif'],aggfunc='sum').reset_index().astype(int)
    #---- sum every type of repartition and show it in a dataframe --------------------------
    value_counts = df_MAA["Type de réparation"].value_counts().reset_index()
    
    #---- rename the dataframe of the count of every repartion to new name columns -------------------
    value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    st.write("Sur **"+str(sum(value_counts["nombre OT"]))+"** OT, la répartition par type d'intervention et son coût sur le dépôt de MAARIF est comme se suit:")
    #creat a new data frame of description of every repartition type -----------------------------------
    data = data = [[1, "Maintenance"], [2, "Grandes réparations"], [3, "Accidents fautif"],[4, "Accidents sans faute"],[5, "Reformes"],[8, "Garanties"]
                   ,[9, "Matériel"],[51, "Vandalisme"],[62, "Qualité interieur"],[12, "Mauvais usage"],[90,"rien"]]
    
    df_type = pd.DataFrame(data, columns=['Type de réparation', 'Description'])
    # -----------merge three dataframe in one dataframe -----------------------------------------------
    
    df_1 = pd.merge(pd.merge(df_MAA_sort, value_counts,on='Type de réparation'),df_type, on="Type de réparation")
    #-------change the type of reaparion count to str 
    df_1["Type de réparation"]=df_1["Type de réparation"].values.astype(str)



    #remove type rien in Description 
    df_1 = df_1.drop(df_1[df_1["Description"] == "rien" ].index)
    
    #-------sort the the maine dataframe in two dataframe every dataframe sorted in defirent way -------------------
    df_s1 =df_1.sort_values(['Coût total effectif'],ascending=[True])
    df_s2 =df_1.sort_values(['nombre OT'],ascending=[True])

    #--------- plot the two sorted dataframe one for cout totale effectif and the other for nombre Ot-----
    fig1 = px.bar(df_s1 ,x="Description",y="Coût total effectif",color="Coût total effectif",text="Coût total effectif",labels={'Description':'Type de réparation','value':'Coût total effectif'},height=500,width=900)
    st.write(fig1)
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]), 2))+"**DH")
    






    #--------------------------------------------------------------------------------------
    st.header('------------------Dépôt MEDIOUNA------------------')
    

    #----creat DATAFRAME FOR JUST BERNOSSI DEPOT -----------------
    df_MED = df1[df1['Intervention'].str.startswith('MAA')]


    df_MED = df_MED.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df_MED['Actif'] = pd.to_numeric(df_MED['Actif'], errors='coerce').astype('Int64')
    df_MED = df_MED.dropna(subset=['Actif'])
    
    df_MED = df_MED.drop(df_MED[(df_MED['Actif'] < 32836) | (df_MED['Actif'] > 33535)].index)
    
    #----sum the cout totale effective pour chaque type -----------------
    df_MED_sort = pd.pivot_table(df_MED, index=["Type de réparation"],values=['Coût total effectif'],aggfunc='sum').reset_index().astype(int)
    #---- sum every type of repartition and show it in a dataframe --------------------------
    value_counts = df_MED["Type de réparation"].value_counts().reset_index()
    
    #---- rename the dataframe of the count of every repartion to new name columns -------------------
    value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    st.write("Sur **"+str(sum(value_counts["nombre OT"]))+"** OT, la répartition par type d'intervention et son coût sur le dépôt de MEDIOUNA est comme se suit:")
    #creat a new data frame of description of every repartition type -----------------------------------
    data = data = [[1, "Maintenance"], [2, "Grandes réparations"], [3, "Accidents fautif"],[4, "Accidents sans faute"],[5, "Reformes"],[8, "Garanties"]
                   ,[9, "Matériel"],[51, "Vandalisme"],[62, "Qualité interieur"],[12, "Mauvais usage"],[90,"rien"]]
    
    df_type = pd.DataFrame(data, columns=['Type de réparation', 'Description'])
    # -----------merge three dataframe in one dataframe -----------------------------------------------
    
    df_1 = pd.merge(pd.merge(df_MED_sort, value_counts,on='Type de réparation'),df_type, on="Type de réparation")
    #-------change the type of reaparion count to str 
    df_1["Type de réparation"]=df_1["Type de réparation"].values.astype(str)


    #remove type rien in Description 
    df_1 = df_1.drop(df_1[df_1["Description"] == "rien" ].index)
    
    #-------sort the the maine dataframe in two dataframe every dataframe sorted in defirent way -------------------
    df_s1 =df_1.sort_values(['Coût total effectif'],ascending=[True])
    df_s2 =df_1.sort_values(['nombre OT'],ascending=[True])

    #--------- plot the two sorted dataframe one for cout totale effectif and the other for nombre Ot-----
    fig1 = px.bar(df_s1 ,x="Description",y="Coût total effectif",color="Coût total effectif",text="Coût total effectif",labels={'Description':'Type de réparation','value':'Coût total effectif'},height=500,width=900)
    st.write(fig1)
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]), 2))+"**DH")
    

    # type intervention --------------------------------------------------------------------------------------
    st.header('Types des Interventions de Maintenance :')
    st.write("La répartition des OT par types de maintenance est comme se suit :")

    df1 = df1.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df1['Actif'] = pd.to_numeric(df1['Actif'], errors='coerce').astype('Int64')
    df1 = df1.dropna(subset=['Actif'])
    
    df1 = df1.drop(df1[(df1['Actif'] < 32836) | (df1['Actif'] > 33535)].index)


    value_counts = df1["Type de travail"].value_counts().reset_index()
    
    

    fig = px.pie(value_counts, names= "index" ,values='Type de travail' ,color="Type de travail")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)

    #intervention preventives -----------------------------------------------------------------------------------
    st.subheader('a. Interventions préventives :')

    value_counts = df1["Description"].value_counts().reset_index()
    value_c = value_counts[value_counts['index'].str.startswith("MT15")]
    MT15=sum(value_c["Description"])
    value_cNT = value_counts[value_counts['index'].str.startswith("MTKM")]
    MTKM=sum(value_cNT["Description"])

    data = [["MT15", MT15],["MTKM",MTKM]]
    
    df_type = pd.DataFrame(data, columns=['type', 'Nombre'])
    fig2 = px.bar(df_type ,x="type",y="Nombre",color="Nombre",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="Nombre",labels={'Description':'Type de réparation','value':'nombre OT'},height=400,width=700,title="VISITES PREVENTIVES")

    st.write(fig2)

# PDR -------------------------------------------------------------------------------------------------

    df2 = df2.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df2['Actif'] = pd.to_numeric(df2['Actif'], errors='coerce').astype('Int64')
    df2 = df2.dropna(subset=['Actif'])
    
    df2 = df2.drop(df2[(df2['Actif'] < 32836) | (df2['Actif'] > 33535)].index)

    #--------------------------------------------------------------------------------------------

    df_PDR_sort = pd.pivot_table(df2, index=["Actif"],values=['Coût ligne'],aggfunc='sum').reset_index().astype(int)
    df_PDR_sort = df_PDR_sort.sort_values(by='Coût ligne',ascending=True)
    
    df_PDR_sort = df_PDR_sort.tail(10)

  
    df_PDR_sort["Actif"]=df_PDR_sort["Actif"].astype(str)
    # -------------------------------------------------------------------------------------
    st.subheader('Top 10 des dépenses par bus :')
    fig2 = px.bar(df_PDR_sort ,x=df_PDR_sort["Actif"].astype(str),y="Coût ligne",color="Coût ligne",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="Coût ligne",labels={'Description':'Type de réparation','value':'nombre OT'},title="Top 10 des dépenses par bus :")
    st.write(fig2)

    #------------------------------------------------------------------------------------------------
    st.subheader('Top 10 des PDR par coût :')
    
    df_Cout_sort = pd.pivot_table(df2, index=["Article","Description"],values=['Coût ligne',"Quantité"],aggfunc='sum').reset_index()
    
    df_Cout_sort = df_Cout_sort.sort_values(by='Coût ligne',ascending=True)
    df_Cout_sort = df_Cout_sort.tail(10)
    df_Cout_sort = df_Cout_sort.sort_values(by='Coût ligne',ascending=False)
    df_Cout_sort["Quantité"]=df_Cout_sort["Quantité"].values.astype(int)
    st.table(df_Cout_sort)
    