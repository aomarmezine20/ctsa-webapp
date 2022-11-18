import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from base64 import b64encode
from fpdf import FPDF
import dataframe_image as dfi
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

st.set_page_config(page_title= 'demandes d’interventions (DI)', page_icon="👷‍♂️")
st. title('suivi des demandes d’interventions (DI)')

uploaded_file1 =st.file_uploader('fichier demandes d’interventions', type=['xlsx','xls','csv'])



if uploaded_file1 :
    st.markdown('---')
    st.subheader('fichier demandes d’interventions')
    #read file python
    df = pd.read_excel(uploaded_file1)

    st.dataframe(df)
    #show the numbre of DI
    st.header('Nombre total des DI du mois')
    df['Month'] = pd.DatetimeIndex(df["Date de l'événement"]).month

    st.markdown('le nombre des demandes d’interventions du mois  **'+ str(int(df['Month'].values[0]))+'** est **' +str(df["Code de l'état"].count()) + '** interventions')

    #SHOW the pie of DI 
    st.header('Graphe des états des DI du mois')

    #make AWAITINGREAL = Attente prise en compte and make the calcule 
    df["code de l'état"]=df["Code de l'état"].replace('AWAITINGREAL',"Attente prise en compte",inplace=True)
    fig = px.pie(df, names="Code de l'état")
    st.plotly_chart(fig)
    fig.write_image("images/fig_DI.jpeg")

    #calcule the 10top of Us that have max of DI 
    st.header('Les Top 10 des US sur lesquelles on a plus de de DI')

    #split the column of Matériel du signalement to 4 column one of them is US 
    df[['DI','autre','autre2','autre3']] = df['Matériel du signalement'].str.split(".",expand=True)
    #sort the result
    dfsrt = df.sort_values(['DI'])

    
    #sort and count every us how much DI have 
    dfcount =df['DI'].value_counts().sort_index()
    
    
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

    #drop values of parc T2 
    dfcount_t1 = dfcount[~dfcount.index.isin(parc2())]
    #drop values of parc T1 
    dfcount_t2 = dfcount[~dfcount.index.isin(parc1())]

    #sort another time the list of us of every parc and show top 5 of every parc 
    dfcount_t1 = dfcount_t1.sort_values(ascending=False)
    dfcount_t2 = dfcount_t2.sort_values(ascending=False)

    #show top 5 of every pacr us PARC T1---------------------------------------------------
    st.subheader("5 US/T1")
    st.markdown('**Top 5 des US sur lesquelles on a plus de de DI PARC T1**')
    #convert serie to datafram
    table1=pd.DataFrame(dfcount_t1.head(5))
   #convert table of top 5 us t1 to table
    fig = px.bar(table1, labels={'index':'DI','value':'N° US'},text_auto='')
    
    #convert table of top 5 us t1 to table image
    fig.write_image("images/table_t1.png")
    #plot chart 
    st.plotly_chart(fig)
    
    #show top 5 of every pacr us PARC T2----------------------------------------------------------
    st.subheader("5 US/T2")
    st.markdown('**Top 5 des US sur lesquelles on a plus de de DI PARC T2**')
    
    #convert serie to datafram
    table2=pd.DataFrame(dfcount_t2.head(5))
   #convert table of top 5 us T2 to image
   #convert table of top 5 us t1 to table
    fig = px.bar(table2, labels={'index':'DI','value':'N° US'},text_auto='')
    
    #convert table of top 5 us t1 to table image
    fig.write_image("images/table_t2.png")
    #plot chart 
    st.plotly_chart(fig)
    

    #show top 5 défaillance sujet DI----------------------------------------------------------------
    st.header('Top 5 des défaillance sujet de (DI)')
    dfcount_mtr =df['Matériel du signalement Description'].value_counts()
    

    #convert serie to datafram
    table3=pd.DataFrame(dfcount_mtr.head(5))
   #convert table of matriel deffi to image
   #convert table of top 5 us t1 to table
    
    fig = px.bar(table3, labels={'index':'Matériel du signalement Description','value':'Nbr DI'}, text_auto='')
    #convert table of top 5 us t1 to table image
    fig.write_image("images/table_mtr.png")
    #plot chart 
    st.plotly_chart(fig)
    

    #Top 5 emplacements des défaillances----------------------------------------------------------
    st.header('Top 5 emplacements des défaillances')
    dfcount_emp =df['Point principal associé Description'].value_counts()

    dfcount_emp.to_frame()

    
    #convert serie to datafram
    table4=pd.DataFrame(dfcount_emp.head(5))
    
    fig = px.bar(table4, labels={'index':'Point principal associé Description','value':'Nbr DI'}, text_auto='')
   #convert table of emplacement to image
    fig.write_image("images/table_emp.png")
    #plot chart 
    st.plotly_chart(fig)
    



    #show pdf 

    
    @st.cache
    def gen_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=24)
        pdf.image('images/big_logo.png', 10, 8, 33)
        # Arial bold 15
        pdf.set_font('Arial', 'B', 20)
        # Move to the right
        pdf.cell(40)

        pdf.cell(140, 15, "suivi des demandes d'interventions (DI)", 1, 0, 'C')

        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
        
        pdf.cell(60, 20, 'Nombre total des DI du mois', 'C')
        pdf.ln(15)

        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.cell(60, 20, "* le nombre des demandes d'interventions du mois  "+ str(int(df['Month'].values[0]))+' est ' +str(df["Code de l'état"].count()) + ' interventions', 'C')

        pdf.ln(15)
        
        pdf.set_font('Times', 'B', 25)
        pdf.cell(60, 20, 'Nombre total des DI du mois', 'C')
        pdf.image('images/fig_DI.jpeg', x=5, y=90, w=200,h=150)

        pdf.ln(190)
        pdf.set_font('Times', 'B', 20)
        pdf.cell(60, 20, 'Les Top 10 des US sur lesquelles on a plus de de DI :', 'C')

        pdf.ln(10)
        pdf.set_font('Times', '', 16)
        pdf.cell(10)
        pdf.cell(60, 20, '* Top 5 des US sur lesquelles on a plus de de DI PARC T1', 'C')
        pdf.image('images/table_t1.png', x=30, y=35, w=150,h=100)
        
        pdf.ln(110)
        pdf.set_font('Times', '', 16)
        pdf.cell(10)
        pdf.cell(60, 20, '* Top 5 des US sur lesquelles on a plus de de DI PARC T2', 'C')
        pdf.image('images/table_t2.png', x=30, y=145, w=150,h=100)
        
        

        pdf.ln(155)
        pdf.set_font('Times', 'B', 20)
        
        pdf.cell(60, 60, 'Top 5 des défaillance sujet de (DI) :', 'C')
        pdf.image('images/big_logo.png', 10, 8, 33)
        pdf.image('images/table_mtr.png', x=0, y=50, w=200,h=130)
        
        pdf.ln(165)
        pdf.set_font('Times', 'B', 20)
        pdf.cell(60, 20, 'Top 5 emplacements des défaillances :', 'C')
        pdf.image('images/table_emp.png', x=0, y=188, w=200,h=100) 
        
        return pdf.output(dest='S').encode('latin-1')

    # Embed PDF to display it:
    base64_pdf = b64encode(gen_pdf()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    
    

    # Add a download button:
    st.subheader("Télecharger PDF")
    st.download_button(
        label="Télecharger Resultat PDF",
        data=gen_pdf(),
        file_name="suivi des demandes d'interventions (DI) Ctsa.pdf",
        mime="application/pdf",
    )