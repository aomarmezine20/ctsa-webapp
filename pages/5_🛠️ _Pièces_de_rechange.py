import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from base64 import b64encode
from fpdf import FPDF


st.set_page_config(page_title= 'suivi des Pièces de rechange', page_icon="./images/big_logo.png")
st. title('Suivi des Pièces de rechange')
#------------- hide footer 
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)

#----- remove list pages
st.markdown("<style> ul {display: none;} </style>", unsafe_allow_html=True)
#-------  MENUUUU -----------------
import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_extras.switch_page_button import switch_page
with st.sidebar:
    selected = option_menu("Reporting Tram", ["Home","Gestion kilométrique", "Demandes d’interventions (DI)","les interventions","Pièces de rechange"], 
        icons=["bi-house-door","bi-graph-up-arrow", "bi-clipboard-check","bi-wrench", "gear"], menu_icon="bi-arrow-right-square", default_index=4)
 
   
if selected == "Gestion kilométrique" :
   switch_page("gestion kilométrique")

if selected == "Demandes d’interventions (DI)" :
    switch_page("demandes d’interventions (di)")

if selected == "les interventions" :
   switch_page("\u200b les interventions")

if selected == "Home" :
    switch_page("HOME")

with st.sidebar:
    selected = option_menu("Reporting Bus", ["Rapport 1", 'Rapport 2'], 
        icons=['house', 'gear'], menu_icon="bi-arrow-right-square", default_index=1)



#upload file1 xls

uploaded_file1 =st.file_uploader('fichier des sorties PDR MR', type=['xlsx','xls','csv'])


#upload file2 xls
uploaded_file2 =st.file_uploader('fichier des interventions', type=['xlsx','xls','csv'])


    
    

if uploaded_file2 and uploaded_file2:

    st.markdown('---')
    st.subheader('fichier des sorties PDR MR')

    
    #read file python
    df1 = pd.read_excel(uploaded_file1,engine="openpyxl")
    st.write(df1)
    
    st.markdown('---')
    st.subheader('fichier d’interventions')


    #read file python
    df2 = pd.read_excel(uploaded_file2)
    st.write(df2)
    
    #make a new datafram contain spesefic elements that we want
    df = df1[["Code de l'intervention",'MOVEMENTQUANTITY',"Code Article","Type OT","Description Article"]].merge(df2[["Code de l'intervention",'Matériel']], 
                                    on = "Code de l'intervention", 
                                    how = 'inner')

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
    

    #split column of materiel to new columns contain just ud
    df['US'] = df['Matériel'].str.split('.').str[0]
    #just the colum start with P.MR
    df_starts_with_pm = df[df['Code Article'].str.startswith('P.MR')]

    
    #change quantity of pdr to int
    df["MOVEMENTQUANTITY"] = df["MOVEMENTQUANTITY"].astype(int)

    #split the big datafram to two for each parc
    df_t1 = df[df['US'].isin(parc1())]
    df_starts_with_pm_t1 =df_starts_with_pm[df_starts_with_pm['US'].isin(parc1())]
    df_t2 = df[df['US'].isin(parc2())]
    df_starts_with_pm_t2 =df_starts_with_pm[df_starts_with_pm['US'].isin(parc2())]
    
    
    #parc T1  ------------------------------------------------------------------------------------------------------------------------
    st.header('-----------------PARC T1------------------')
    #----- Top 20 piece ------------------------------------------------
    st.subheader('Top 20 des pièces consommées parc T1 PMR: ')
    df_starts_with_pm_t1qnt = df_starts_with_pm_t1[["Code Article", "MOVEMENTQUANTITY"]]
    df_starts_with_pm_t1qnt = pd.pivot_table(df_starts_with_pm_t1qnt, index=["Code Article"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    #sort another time the list of us of every parc and show top 20 of every parc 
    df_starts_with_pm_t1qnt = df_starts_with_pm_t1qnt.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_starts_with_pm_t1qnt = df_starts_with_pm_t1qnt.tail(20)
    
    #plot the result in bar chart
    fig = px.bar(df_starts_with_pm_t1qnt,x="Code Article",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_1_1.jpeg")

    #-------- 
    st.subheader('Top 20 des pièces consommées parc T1  : ')

    df_t1_qnt = df_t1[["Code Article", "MOVEMENTQUANTITY"]]
    df_t1_qnt = pd.pivot_table(df_t1_qnt, index=["Code Article"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    #sort another time the list of us of every parc and show top 20 of every parc 
    df_t1_qnt = df_t1_qnt.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_t1_qnt = df_t1_qnt.tail(20)
    
    #plot the result in bar chart
    fig = px.bar(df_t1_qnt,x="Code Article",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_1.jpeg")


    #----------- top 10 us consommablle of piece -------------------------------------
    st.subheader('Top 10 US à haute consommation de PDR parc T1: ')
    df_t1_us = df_t1[["US", "MOVEMENTQUANTITY"]]
    df_t1_us = pd.pivot_table(df_t1_us, index=["US"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    df_t1_us = df_t1_us.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_t1_us = df_t1_us.tail(10)

    #plot the result in bar chart
    fig = px.bar(df_t1_us,x="US",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_2.jpeg")
    
    #------- repartition par type --------------------------------------------
    st.subheader('Répartition des sorties PDR en fonction des types OT parc T1: ')
    df_t1_type = df_t1[["Type OT", "MOVEMENTQUANTITY"]]
    df_t1_type["MOVEMENTQUANTITY"] = abs(df_t1_type['MOVEMENTQUANTITY'])
    
    df_t1_type = pd.pivot_table(df_t1_type, index=["Type OT"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    df_t1_type = df_t1_type.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)

    fig = px.pie(df_t1_type, names= "Type OT" ,values='MOVEMENTQUANTITY' ,color="MOVEMENTQUANTITY")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)

    fig.write_image("images/fig_piece_3.jpeg")





    #parc T2  ------------------------------------------------------------------------------------------------------------------------
    st.header('-----------------PARC T2------------------')
    #----- Top 20 piece ------------------------------------------------
    st.subheader('Top 20 des pièces consommées parc T2 PMR: ')
    df_starts_with_pm_t2qnt = df_starts_with_pm_t2[["Code Article", "MOVEMENTQUANTITY"]]
    df_starts_with_pm_t2qnt = pd.pivot_table(df_starts_with_pm_t2qnt, index=["Code Article"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    #sort another time the list of us of every parc and show top 20 of every parc 
    df_starts_with_pm_t2qnt = df_starts_with_pm_t2qnt.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_starts_with_pm_t2qnt = df_starts_with_pm_t2qnt.tail(20)
    
    #plot the result in bar chart
    fig = px.bar(df_starts_with_pm_t2qnt,x="Code Article",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_4_1.jpeg")


    st.subheader('Top 20 des pièces consommées parc T2: ')
    df_t2_qnt = df_t2[["Code Article", "MOVEMENTQUANTITY"]]
    df_t2_qnt = pd.pivot_table(df_t2_qnt, index=["Code Article"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    #sort another time the list of us of every parc and show top 20 of every parc 
    df_t2_qnt = df_t2_qnt.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_t2_qnt = df_t2_qnt.tail(20)
    
    #plot the result in bar chart
    fig = px.bar(df_t2_qnt,x="Code Article",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_4.jpeg")

    #----------- top 10 us consommablle of piece -------------------------------------
    st.subheader('Top 10 US à haute consommation de PDR parc T2: ')
    df_t2_us = df_t2[["US", "MOVEMENTQUANTITY"]]
    df_t2_us = pd.pivot_table(df_t2_us, index=["US"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    df_t2_us = df_t2_us.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)
    df_t2_us = df_t2_us.tail(10)

    #plot the result in bar chart
    fig = px.bar(df_t2_us,x="US",y='MOVEMENTQUANTITY', text_auto='')

    st.plotly_chart(fig)
    #save it in image
    fig.write_image("images/fig_piece_5.jpeg")
    
    #------- repartition par type --------------------------------------------
    st.subheader('Répartition des sorties PDR en fonction des types OT parc T2: ')
    df_t2_type = df_t2[["Type OT", "MOVEMENTQUANTITY"]]
    df_t2_type["MOVEMENTQUANTITY"] = abs(df_t2_type['MOVEMENTQUANTITY'])
    
    df_t2_type = pd.pivot_table(df_t2_type, index=["Type OT"],values=['MOVEMENTQUANTITY'],aggfunc='sum').reset_index()

    df_t2_type = df_t2_type.sort_values(by = ["MOVEMENTQUANTITY"],ascending=False)

    fig = px.pie(df_t2_type, names= "Type OT" ,values='MOVEMENTQUANTITY' ,color="MOVEMENTQUANTITY")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)

    fig.write_image("images/fig_piece_6.jpeg")

    
    st.subheader("Chercher description des articles")
    # Demander à l'utilisateur d'entrer le code de l'article
    code = st.text_input("Entrez le code de l'article")

    # Rechercher la description correspondante
    result = df.loc[df['Code Article'] == code, 'Description Article']

    # Afficher la description de l'article
    if not result.empty:
        st.write(f"Description de l'article : {result.iloc[0]}")
    else:
        st.write(f"Aucune description trouvée pour l'article '{code}'")
    






    def footer(pdf):
        #footer
        pdf.set_y(266)
        # Select Arial italic 8
        pdf.set_font('Arial', 'I', 12)
        # Print centered page number
        pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')

    def header(pdf):
        pdf.image('images/big_logo.png', 10, 8, 33)


    

#-------------------- Pdf ---------------------------------------------------------------------------------------------------

    @st.cache
    def gen_pdf():
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Helvetica", size=24)
        header(pdf)
        # Arial bold 15
        pdf.set_font('Arial', 'B', 20)
        # Move to the right
        pdf.cell(40)
        
        pdf.cell(140, 15, "Suivi des Pièces de rechange", 1, 0, 'C')

        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
# ------------------ PARC T1 -----------------------------------------------------------------------------------------------
        pdf.cell(60, 20, '         ----------------- PARC T1 ------------------', 'C')
        pdf.ln(15)
        pdf.set_font('Times', 'B', 25)

        pdf.cell(60, 20, "Top 20 des pièces consommées parc T1:", 'C')
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_1.jpeg', x=5, y=80, w=200,h=150)

        footer(pdf)
        pdf.ln(400)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 80, "Top 10 US à haute consommation de PDR parc T1:", 'C')
        header(pdf)

        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_2.jpeg', x=5, y=60, w=200,h=150)
        footer(pdf)


        pdf.ln(190)
        pdf.set_font('Times', 'B', 23)
        
        #ploot in pdf taux of occupation
        pdf.cell(60, 57, "Répartition des sorties PDR en fonction des types", 'C')
        pdf.ln(10)
        pdf.cell(60, 57, " OT parc T1:", 'C')
        header(pdf)
        pdf.image('images/fig_piece_3.jpeg', x=5, y=65, w=200,h=150)
        footer(pdf)

        pdf.ln(190)
        #--------------T2 ------------------------------------------------
        
        pdf.ln(30)
        header(pdf)
        pdf.set_font('Arial', 'B', 25)
        pdf.cell(60, 20, '         ----------------- PARC T2 ------------------', 'C')
        pdf.ln(15)
        pdf.set_font('Times', 'B', 25)

        pdf.cell(60, 20, "Top 20 des pièces consommées parc T2:", 'C')
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_4.jpeg', x=5, y=80, w=200,h=150)

        footer(pdf)
        pdf.ln(200)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 80, "Top 10 US à haute consommation de PDR parc T2:", 'C')
        header(pdf)

        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_5.jpeg', x=5, y=60, w=200,h=150)
        footer(pdf)


        pdf.ln(190)
        pdf.set_font('Times', 'B', 23)
        
        #ploot in pdf taux of occupation
        pdf.cell(60, 57, "Répartition des sorties PDR en fonction des types", 'C')
        pdf.ln(10)
        pdf.cell(60, 57, " OT parc T2:", 'C')
        header(pdf)
        pdf.image('images/fig_piece_6.jpeg', x=5, y=65, w=200,h=150)
        footer(pdf)

        pdf.ln(200)
        pdf.set_font('Times', 'B', 25)
        pdf.cell(60, 80, "Top 20 des pièces consommées parc T1  PMR:", 'C')
        header(pdf)

        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_1_1.jpeg', x=5, y=60, w=200,h=150)
        footer(pdf)

        pdf.ln(200)
        pdf.set_font('Times', 'B', 25)
        pdf.cell(60, 80, "Top 20 des pièces consommées parc T2 PMR:", 'C')
        header(pdf)

        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.image('images/fig_piece_4_1.jpeg', x=5, y=60, w=200,h=150)
        footer(pdf)




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
        file_name="Suivi des Pièces de rechange  Ctsa.pdf",
        mime="application/pdf",
    )