import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image
from base64 import b64encode
from fpdf import FPDF

st.set_page_config(page_title= 'Gestion kilométrique', page_icon="./images/big_logo.png")
st. title('Gestion kilométrique')





hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
#upload file1 xls

uploaded_file1 =st.file_uploader('Le Kilométrage pour le premiere mois', type=['xlsx','xls','csv'])


#upload file2 xls
uploaded_file2 =st.file_uploader('Le Kilométrage pour le deuxieme mois', type=['xlsx','xls','csv'])

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
    selected = option_menu("Reporting Bus", ["Rapport 1", 'Rapport 2'], 
        icons=['house', 'gear'], menu_icon="bi-arrow-right-square", default_index=1)


if uploaded_file1 :
    st.markdown('---')
    st.subheader('Le Kilométrage pour le premiere mois')
    #read file python
    df1 = pd.read_excel(uploaded_file1)

    #drop row that have null values
    df1=df1.dropna(how='any',axis=0,subset=['Valeur mesurée']) 

    #make column of values km type int
    df1['Valeur mesurée'] = df1['Valeur mesurée'].astype('int')
    st.dataframe(df1)

if uploaded_file2:
    st.markdown('---')
    st.subheader('Le Kilométrage pour le deuxieme mois')
    #read file python
    df2 = pd.read_excel(uploaded_file2)
    df1 = pd.read_excel(uploaded_file1)
    df1=df1.dropna(how='any',axis=0,subset=['Valeur mesurée']) 

    #make column of values km type int
    df1['Valeur mesurée'] = df1['Valeur mesurée'].astype('int')

    #drop row that have null values
    df2=df2.dropna(how='any',axis=0,subset=['Valeur mesurée'])

    #make column of values km type int
    df2['Valeur mesurée'] = df2['Valeur mesurée'].astype('int')

    #show data frame in table
    st.dataframe(df2)


    #--------------    T1   ------------------------------------------------------------------------------------------

    #RESULT FOR PARC T1
    #catrgory box
    st.header('Le Kilométrage pour PARC T1')
        #merge the two file into one file and make the calculation of km in months
    dfF1 = df1[['Point de mesure','Valeur mesurée']].merge(df2[['Point de mesure','Valeur mesurée']], 
                                    on = 'Point de mesure', 
                                    how = 'left')
    dfF1['KM'] = dfF1["Valeur mesurée_y"] - dfF1["Valeur mesurée_x"]


    def parc1() :
        T=[]
        for i in range (0,10):
            T.append('PM-US00'+str(i))
        for i in range(10,75):
            T.append('PM-US0'+str(i))
        return(T)
    #creat list of parc T2
    def parc2():
        T=[]
        for i in range(75,100):
            T.append('PM-US0'+str(i))
        for i in range(100,125):
            T.append('PM-US'+str(i))
        return(T)
    #drop result of T2
    
    dfF1 = dfF1[~dfF1["Point de mesure"].isin(parc2())]
    
    dfsort =dfF1.sort_values(['KM'],ascending=[True])
    # ----PLOT DATAFRAME T1 -------
    fig= px.bar(
    dfsort,
    x='Point de mesure',
    y='KM',
    color='KM',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T1</b>'
    )
    
    st.plotly_chart(fig)
    fig.update_layout(
    autosize=True,
    width=1300,
    height=700)
    fig.write_image("images/fig_T1.jpeg")

    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF1['KM'].max()) +'   KM' )

    #---- moyenne of value of KM
    dfmin1 = dfF1[dfF1['KM'] != 0]
    st.write('Moyenne de production : ''   '+ str(int(dfmin1['KM'].sum() / dfmin1['KM'].count())) +'   KM  ' +'  (hors US qui n’ont pas roulé)' )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfmin1['KM'][dfmin1['KM']>20].min()) +'   KM')


    # ---T1--CUMMULE -------------------------------------------
    dfF1['KM cumul']= dfF1['Valeur mesurée_y']
    dfsort_cumul =dfF1.sort_values(['KM cumul'],ascending=[True])

    # ----PLOT DATAFRAME T1 cumul -------
    fig= px.bar(
    dfsort_cumul,
    x='Point de mesure',
    y='KM cumul',
    color='KM cumul',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T1 cumul</b>'
    )
    st.plotly_chart(fig)
    fig.update_layout(
    autosize=True,
    width=1300,
    height=700)
    fig.write_image("images/fig_T1cumul.jpeg")

    #----- cumul synthes ---------
    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF1['KM cumul'].max()) +'   KM' )

    #---- moyenne of value of KM
    
    st.write('Moyenne de production : ''   '+ str(int(dfF1['KM cumul'].sum() / dfF1['KM cumul'].count())) +'   KM  ' +"  (hors US qui n'ont pas roulé)" )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfF1['KM cumul'][dfF1['KM cumul']>20].min()) +'   KM')


    #------------------   T2   -----------------------------------------------------------------------

    #RESULT FOR PARC T2
    st.header('Le Kilométrage pour PARC T2')
    #merge the two file into one file and make the calculation of km in months
    dfF = df1[['Point de mesure','Valeur mesurée']].merge(df2[['Point de mesure','Valeur mesurée']], 
                                    on = 'Point de mesure', 
                                    how = 'right')
                                    
    dfF['KM'] = dfF["Valeur mesurée_y"] - dfF["Valeur mesurée_x"]
    #drop result of T1
    dfF = dfF[~dfF["Point de mesure"].isin(parc1())]
    

    dfsort =dfF.sort_values(['KM'],ascending=[True])

        # ---PLOT DATAFRAME-- T2--------
    fig= px.bar(
    dfsort,
    x='Point de mesure',
    y='KM',
    color='KM',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T2</b>'
    )
    
    st.plotly_chart(fig)
    fig.update_layout(
    autosize=True,
    width=1100,
    height=700)
    fig.write_image("images/fig_T2.jpeg")

    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM'].max()) +'   KM' )

    #---- moyenne of value of KM
    dfmin = dfF[dfF['KM'] != 0]
    st.write('Moyenne de production : ''   '+ str(int(dfmin['KM'].sum() / dfmin['KM'].count())) +'   KM  ' + '  (hors US qui n’ont pas roulé)')

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfmin['KM'][dfmin['KM']>20].min()) +'   KM')
    #-------------------------------------------------------------------------------------------------------


    # ---T2--CUMMULE -------------------------------------------
    dfF['KM cumul']= dfF['Valeur mesurée_y']
    dfsort_cumul =dfF.sort_values(['KM cumul'],ascending=[True])

    
    # ----PLOT DATAFRAME T2 cumul -------
    fig= px.bar(
    dfsort_cumul,
    x='Point de mesure',
    y='KM cumul',
    color='KM cumul',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T2 cumul</b>'
    )
    st.plotly_chart(fig)
    fig.update_layout(
    autosize=True,
    width=1100,
    height=700)
    fig.write_image("images/fig_T2cumul.jpeg")

    #----- cumul synthes ---------
    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM cumul'].max()) +'   KM' )

    #---- moyenne of value of KM
    
    st.write('Moyenne de production : ''   '+ str(int(dfF['KM cumul'].sum() / dfF['KM cumul'].count())) +'   KM  ' +'  (hors US qui n’ont pas roulé)' )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfF['KM cumul'][dfF['KM cumul']>20].min()) +'   KM')


    def footer(pdf):
        #footer
        pdf.set_y(266)
        # Select Arial italic 8
        pdf.set_font('Arial', 'I', 12)
        # Print centered page number
        pdf.cell(0, 10, 'Page %s' % pdf.page_no(), 0, 0, 'C')

    def header(pdf):
        pdf.image('images/big_logo.png', 10, 8, 33)

    #---------print pdf--------------------------------------------------------------------------
    @st.cache
    def gen_pdf():
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Helvetica", size=24)
        header(pdf)
        # Arial bold 15
        pdf.set_font('Arial', 'B', 20)
        # Move to the right
        pdf.cell(70)
        # Title
        pdf.cell(75, 15, 'Gestion kilométrique', 1, 0, 'C')
        # Line break
        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
        
        pdf.cell(60, 20, 'Le Kilométrage pour PARC T1', 'C')
        # Line break
        pdf.ln(15)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.cell(60, 20, 'Le Kilométrage pour PARC T1', 'C')
        #-------------T1 -------------------------------------------------
        # Line break
        pdf.ln(15)
        pdf.cell(0)
        pdf.image('images/fig_T1.jpeg', x=5, y=69, w=206,h=150)
        # Line break
        pdf.ln(150)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.cell(60, 20, 'Synthèse des tendances de production par US sur le mois :', 'C')

        pdf.ln(15)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Maximum de production : ''   '+ str(dfF1['KM'].max()) +'   KM', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Moyenne de production : ''   '+ str(int(dfmin1['KM'].sum() / dfmin1['KM'].count())) +'   KM  ' +"  (hors US qui n'ont pas roulé)", 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Minimum de production : ''   '+ str(dfmin1['KM'].min()) +'   KM', 'C')
        footer(pdf)
        #------------T1 cumul -------------------------------------------
        pdf.ln(70)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.image('images/fig_T1cumul.jpeg', x=5, y=30, w=206,h=150)
        header(pdf)
        

        pdf.ln(170)
        pdf.cell(10)
        pdf.cell(60, 20, 'Synthèse des tendances de production par US sur le mois :', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Maximum de production : ''   '+ str(dfF1['KM cumul'].max()) +'   KM', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Moyenne de production : ''   '+ str(int(dfF1['KM cumul'].sum() / dfF1['KM cumul'].count())) +'   KM  ' +"  (hors US qui n'ont pas roulé)", 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Minimum de production : ''   '+ str(dfF1['KM cumul'].min()) +'   KM', 'C')
        
        footer(pdf)
        pdf.ln(100)
        pdf.set_font('Arial', 'B', 25)
        pdf.ln(100)
        pdf.cell(70, 65, 'Le Kilométrage pour PARC T2', 'C')
        header(pdf)
        #----------------T2-----------------------------------------------------------
        pdf.ln(40)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.image('images/fig_T2.jpeg', x=5, y=49, w=206,h=150)
        header(pdf)
        pdf.ln(150)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.cell(60, 20, 'Synthèse des tendances de production par US sur le mois :', 'C')

        pdf.ln(15)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Maximum de production : ''   '+ str(dfF['KM'].max()) +'   KM', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Moyenne de production : ''   '+ str(int(dfmin['KM'].sum() / dfmin['KM'].count())) +'   KM  ' +"  (hors US qui n'ont pas roulé)", 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Minimum de production : ''   '+ str(dfmin['KM'].min()) +'   KM', 'C')
        footer(pdf)

        #------------T2 cumul ----------------------------------------------------

        pdf.ln(70)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(10)
        pdf.image('images/fig_T2cumul.jpeg', x=5, y=30, w=206,h=150)
        header(pdf)
        

        pdf.ln(170)
        pdf.cell(10)
        pdf.cell(60, 20, 'Synthèse des tendances de production par US sur le mois :', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Maximum de production : ''   '+ str(dfF['KM cumul'].max()) +'   KM', 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Moyenne de production : ''   '+ str(int(dfF['KM cumul'].sum() / dfF['KM cumul'].count())) +'   KM  ' +"  (hors US qui n'ont pas roulé)", 'C')

        pdf.ln(10)
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(60, 20,  '* Minimum de production : ''   '+ str(dfF['KM cumul'].min()) +'   KM', 'C')
        footer(pdf)
        
        
        return pdf.output(dest='S').encode('latin-1')

        # Line break
        
    # Embed PDF to display it:
    base64_pdf = b64encode(gen_pdf()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    #st.markdown(pdf_display, unsafe_allow_html=True)

    # Add a download button:

    st.subheader("Télecharger PDF")
    st.download_button(
        label="Télecharger Resultat PDF",
        data=gen_pdf(),
        file_name="Gestion kilométrique Ctsa.pdf",
        mime="application/pdf",
    )