import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from base64 import b64encode
from fpdf import FPDF
from tabulate import tabulate
import matplotlib.pyplot as plt

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
    
    df_BER["Coût total effectif"]= df_BER["Coût total effectif"].astype(int)
    
    
    
    #----sum the cout totale effective pour chaque type -----------------
    df_BER_sort = pd.pivot_table(df_BER, index=["Type de réparation"],values=['Coût total effectif'],aggfunc='sum').reset_index()
    #---- sum every type of repartition and show it in a dataframe --------------------------
    value_counts = df_BER["Type de réparation"].value_counts().reset_index()
    
    #---- rename the dataframe of the count of every repartion to new name columns -------------------
    value_counts.rename(columns = {'nombre OT':'Type de réparation','count':'nombre OT'}, inplace = True)
    #value_counts.rename(columns = {'index':'Type de réparation','count':'nombre OT'}, inplace = True)
 
    v1 = str(sum(value_counts["nombre OT"]))
    st.write("Sur **"+str(sum(value_counts["nombre OT"]))+"** OT, la répartition par type d'intervention et son coût sur le dépôt de Bernoussi est comme se suit:")
    #creat a new data frame of description of every repartition type -----------------------------------
    data = data = [[1, "Maintenance"], [2, "Grandes réparations"], [3, "Accidents fautif"],[4, "Accidents sans faute"],[5, "Reformes"],[8, "Garanties"]
                   ,[9, "Matériel"],[51, "Vandalisme"],[62, "Qualité interieur"],[12, "Mauvais usage"],[90,"rien"]]
    
    df_type = pd.DataFrame(data, columns=['Type de réparation', 'Description'])
    # -----------merge three dataframe in one dataframe -----------------------------------------------
    
    

    
    df_p = value_counts[['Type de réparation','nombre OT']].merge(df_BER_sort[['Type de réparation','Coût total effectif']], 
                                    on = 'Type de réparation', 
                                    how = 'left')
    df_1 = df_p[['Type de réparation','nombre OT','Coût total effectif']].merge(df_type[['Type de réparation','Description']], 
                                    on = 'Type de réparation', 
                                    how = 'left')
   
    #df_1 = pd.concat([pd.concat([df_BER_sort, value_counts], axis=1),df_type],  axis=1)
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
    fig1.write_image("images/fig1_bus_BR.jpeg")
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)
    fig2.write_image("images/fig2_bus_BR.jpeg")
    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))+"**DH (Coût garanties exclu)")
    v11=str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))
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
    value_counts.rename(columns = {'nombre OT':'Type de réparation','count':'nombre OT'}, inplace = True)

    #value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    v2 = str(sum(value_counts["nombre OT"]))
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
    fig1.write_image("images/fig1_bus_BN.jpeg")
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))+"**DH (Coût garanties exclu)")
    v22=str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))

    fig2.write_image("images/fig2_bus_BN.jpeg")


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
    value_counts.rename(columns = {'nombre OT':'Type de réparation','count':'nombre OT'}, inplace = True)

    #value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    v3= str(sum(value_counts["nombre OT"]))
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
    fig1.write_image("images/fig1_bus_MA.jpeg")
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))+"**DH (Coût garanties exclu)")
    fig2.write_image("images/fig2_bus_MA.jpeg")
    v33 =str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))





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
    value_counts.rename(columns = {'nombre OT':'Type de réparation','count':'nombre OT'}, inplace = True)

    #value_counts.rename(columns = {'index':'Type de réparation','Type de réparation':'nombre OT'}, inplace = True)
    v4 = str(sum(value_counts["nombre OT"]))
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
    fig1.write_image("images/fig1_bus_MD.jpeg")
    st.write(" la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi est comme se suit:")

    fig2 = px.bar(df_s2 ,x="Description",y="nombre OT",color="nombre OT",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="nombre OT",labels={'Description':'Type de réparation','value':'nombre OT'},height=500,width=900)

    #--------show the figures ---------------------------
    
    st.write(fig2)
    st.write("Le total des dépenses en matière de main d’œuvre et de PDR sorties est de **"+str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))+"**DH (Coût garanties exclu)")
    v44 =str(round(sum(df_s1["Coût total effectif"]) - df_s1.loc[df_s1['Description'].str.contains('Garanties'), 'Coût total effectif'].sum(), 2))
    fig2.write_image("images/fig2_bus_MD.jpeg")

    # type intervention --------------------------------------------------------------------------------------
    st.header('Types des Interventions de Maintenance :')
    st.write("La répartition des OT par types de maintenance est comme se suit :")

    df1 = df1.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df1['Actif'] = pd.to_numeric(df1['Actif'], errors='coerce').astype('Int64')
    df1 = df1.dropna(subset=['Actif'])
    
    df1 = df1.drop(df1[(df1['Actif'] < 32836) | (df1['Actif'] > 33535)].index)


    value_counts = df1["Type de travail"].value_counts().reset_index()
    st.write(value_counts)
    value_counts = value_counts.drop(value_counts[value_counts['index'] == 'GASTO'].index).reset_index(drop=True)

    #value_counts1 = value_counts[value_counts['Type de travail'] != 'GASTO'].reset_index(drop=True)
    

    fig = px.pie(value_counts, names= "index" ,values='Type de travail' ,color="Type de travail")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_intrv.jpeg")

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
    fig2.write_image("images/fig_intrv_prv.jpeg")
    st.write(fig2)

# PDR -------------------------------------------------------------------------------------------------

    df1 = df1.sort_values(by='Actif')
    
    # select the rows that meet the condition
    df1['Actif'] = pd.to_numeric(df1['Actif'], errors='coerce').astype('Int64')
    df1 = df1.dropna(subset=['Actif'])
    
    df1 = df1.drop(df1[(df1['Actif'] < 32836) | (df1['Actif'] > 33535)].index)

    #--------------------------------------------------------------------------------------------
    df_PDR_sort = pd.pivot_table(df1, index=["Actif"],values=['Coût total effectif'],aggfunc='sum').reset_index().astype(int)
    df_PDR_sort = df_PDR_sort.sort_values(by='Coût total effectif',ascending=True)
    
    df_PDR_sort = df_PDR_sort.tail(10)
    
  
    df_PDR_sort["Actif"]=df_PDR_sort["Actif"].astype(str)
    # -------------------------------------------------------------------------------------
    st.subheader('Top 10 des dépenses par bus :')
    fig2 = px.bar(df_PDR_sort ,x="Actif",y="Coût total effectif",color="Coût total effectif",color_continuous_scale=[ ' green','yellow' ,' red'  ],text="Coût total effectif",labels={'Description':'Type de réparation','value':'nombre OT'},title="Top 10 des dépenses par bus :")
    st.write(fig2)
    fig2.write_image("images/fig_top_10.jpeg")

    #------------------------------------------------------------------------------------------------
    st.subheader('Top 10 des PDR par coût :')
    
    df_Cout_sort = pd.pivot_table(df2, index=["Article","Description"],values=['Coût ligne',"Quantité"],aggfunc='sum').reset_index()
    
    df_Cout_sort = df_Cout_sort.sort_values(by='Coût ligne',ascending=True)
    df_Cout_sort = df_Cout_sort.tail(11)
    df_Cout_sort = df_Cout_sort.sort_values(by='Coût ligne',ascending=False)
    df_Cout_sort = df_Cout_sort.drop(df_Cout_sort[df_Cout_sort['Article'] == 'GOIL'].index).reset_index(drop=True)
    df_Cout_sort["Quantité"]=df_Cout_sort["Quantité"].values.astype(int)
    st.table(df_Cout_sort)


    fig, ax = plt.subplots(figsize=(8, 6))
    ax.axis('off')  # Turn off the axis labels
    ax.axis('tight')  # Set the layout tightly
    table = ax.table(cellText=df_Cout_sort.values, colLabels=df_Cout_sort.columns, loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(3,3)
    plt.savefig('images/table_image.png', bbox_inches='tight', pad_inches=0.2)
    
    #------------------PDF ---------------------------------------------------------------------

    def footer(pdf):
        #footer
        pdf.set_y(266)
        # Select Arial italic 8
        pdf.set_font('Arial', 'I', 12)
        # Print centered page number
        pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')

    

    def header(pdf):
        pdf.image('images/Casabus-logo.png', 0, 8, 52)
    def header2(pdf):
        pdf.image('images/big_logo.png', 164, 8, 33)
    @st.cache
    def gen_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Helvetica", size=24)
        header(pdf)
        header2(pdf)
        pdf.set_font('Arial', 'B', 20)
        # Move to the right
        pdf.cell(50)
        
        pdf.cell(100, 16, "Reporting CASA Bus", 1, 0, 'C')

        
        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
# ------------------ Dépôt Bernoussi-----------------------------------------------------------------------------------------------
        pdf.cell(60, 20, '----------------- Dépôt Bernoussi ------------------', 'C')
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(60, 20, "Sur "+v1+" OT, la répartition par type d'intervention et son coût sur le dépôt de Bernoussi", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "est comme se suit:", 'C')

        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig1_bus_BR.jpeg', x=5, y=75, w=200,h=130)

        footer(pdf)
        pdf.ln(400)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 80, "la répartition par type d'intervention et nombre d'OT sur le dépôt de Bernoussi ", 'C')
        pdf.ln(38)
        pdf.cell(60, 20, "est comme se suit:", 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig2_bus_BR.jpeg', x=5, y=75, w=200,h=130)
        pdf.ln(145)
        pdf.cell(60, 20, "Le total des dépenses en matière de main d'oeuvre et de PDR sorties est de "+v11 + "DH", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "(Coût garanties exclu)", 'C')

        footer(pdf)

        pdf.ln(190)
  #------------------------ depot BENMSIK ----------------------------------------------------------------------------
        
        # Move to the right
        
        
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(50)
        pdf.cell(60, 20, '                     Dépôt BENMSIK ', 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(10)
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(60, 20, "Sur "+v2+" OT, la répartition par type d'intervention et son coût sur le dépôt de BENMSIK", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "est comme se suit:", 'C')

        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig1_bus_BN.jpeg', x=5, y=75, w=200,h=130)

        footer(pdf)
        pdf.ln(400)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 80, "la répartition par type d'intervention et nombre d'OT sur le dépôt de BENMSIK ", 'C')
        pdf.ln(38)
        pdf.cell(60, 20, "est comme se suit:", 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig2_bus_BN.jpeg', x=5, y=75, w=200,h=130)
        pdf.ln(145)
        pdf.cell(60, 20, "Le total des dépenses en matière de main d'oeuvre et de PDR sorties est de "+v22+" DH", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "(Coût garanties exclu)", 'C')
        footer(pdf)

        pdf.ln(145)

#----------------------------------depot MAARIF -----------------------------------------------------------
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(50)
        pdf.cell(60, 20, '                     Dépôt MAARIF ', 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(10)
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(60, 20, "Sur "+v3+" OT, la répartition par type d'intervention et son coût sur le dépôt de MAARIF", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "est comme se suit:", 'C')

        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig1_bus_MA.jpeg', x=5, y=75, w=200,h=130)

        footer(pdf)
        pdf.ln(400)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 80, "la répartition par type d'intervention et nombre d'OT sur le dépôt de MAARIF ", 'C')
        pdf.ln(38)
        pdf.cell(60, 20, "est comme se suit:", 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig2_bus_MA.jpeg', x=5, y=75, w=200,h=130)
        pdf.ln(145)
        pdf.cell(60, 20, "Le total des dépenses en matière de main d'oeuvre et de PDR sorties est de "+v33+" DH", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "(Coût garanties exclu)", 'C')
        footer(pdf)

        pdf.ln(145)
#(------------------------------ depot MEDINA --------------------------------------)
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(50)
        pdf.cell(60, 20, '                     Dépôt MEDIOUNA ', 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(10)
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(60, 20, "Sur "+v4+" OT, la répartition par type d'intervention et son coût sur le dépôt de MEDIOUNA", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "est comme se suit:", 'C')

        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig1_bus_MD.jpeg', x=5, y=75, w=200,h=130)

        footer(pdf)
        pdf.ln(400)
        
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 80, "la répartition par type d'intervention et nombre d'OT sur le dépôt de MEDIOUNA ", 'C')
        pdf.ln(38)
        pdf.cell(60, 20, "est comme se suit:", 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig2_bus_MD.jpeg', x=5, y=75, w=200,h=130)
        pdf.ln(145)
        pdf.cell(60, 20, "Le total des dépenses en matière de main d'oeuvre et de PDR sorties est de "+v44+" DH", 'C')
        pdf.ln(7)
        pdf.cell(60, 20, "(Coût garanties exclu)", 'C')
        footer(pdf)

        pdf.ln(145)

        pdf.set_font('Arial', 'B', 25)
        pdf.ln(50)
        pdf.cell(60, 65, 'Types des Interventions de Maintenance :', 'C')
        header(pdf)
        header2(pdf)
        pdf.set_font('Times', '', 15)
        pdf.ln(33)
        pdf.cell(60, 20, "La répartition des OT par types de maintenance est comme se suit :", 'C')
        pdf.ln(7)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_intrv.jpeg', x=30, y=65, w=140,h=100)
        pdf.ln(15)
        pdf.ln(69)
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(60, 20, "a. Interventions préventives :", 'C')
        pdf.ln(15)
        footer(pdf)
        pdf.image('images/fig_intrv_prv.jpeg', x=5, y=165, w=170,h=100)
        pdf.ln(145)
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(50)
        pdf.cell(60, 65, 'Top 10 des dépenses par bus :', 'C')
        header(pdf)
        header2(pdf)
        pdf.ln(50)
        pdf.image('images/fig_top_10.jpeg', x=5, y=50, w=200,h=130)
        pdf.ln(50)
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(40)
        pdf.cell(60, 65, 'Top 10 des PDR par coût :', 'C')
        
        pdf.image('images/table_image.png', x=5, y=195, w=195,h=80)
        
        return pdf.output(dest='S').encode('latin-1')



    base64_pdf = b64encode(gen_pdf()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    #to show pdf in page 
    
    #st.markdown(pdf_display, unsafe_allow_html=True)
    # Add a download button:
    st.subheader("Télecharger PDF")
    st.download_button(
        label="Télecharger Resultat PDF",
        data=gen_pdf(),
        file_name="Reporting CASA Bus.pdf",
        mime="application/pdf",
    )


    