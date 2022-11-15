import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image

st.set_page_config(page_title= 'Gestion kilométrique', page_icon="⛽")
st. title('Gestion kilométrique')


#upload file1 xls

uploaded_file1 =st.file_uploader('Le Kilométrage pour le premiere mois', type=['xlsx','xls','csv'])


#upload file2 xls
uploaded_file2 =st.file_uploader('Le Kilométrage pour le deuxieme mois', type=['xlsx','xls','csv'])



if uploaded_file1 :
    st.markdown('---')
    st.subheader('Le Kilométrage pour le premiere mois')
    #read file python
    df1 = pd.read_excel(uploaded_file1)

    #drop row that have null values
    df1=df1.dropna(how='any',axis=0,subset=['Dernier relevé: Valeur mesurée']) 

    #make column of values km type int
    df1['Dernier relevé: Valeur mesurée'] = df1['Dernier relevé: Valeur mesurée'].astype('int')
    st.dataframe(df1)

if uploaded_file2:
    st.markdown('---')
    st.subheader('Le Kilométrage pour le deuxieme mois')
    #read file python
    df2 = pd.read_excel(uploaded_file2)

    #drop row that have null values
    df2=df2.dropna(how='any',axis=0,subset=['Dernier relevé: Valeur mesurée'])

    #make column of values km type int
    df2['Dernier relevé: Valeur mesurée'] = df2['Dernier relevé: Valeur mesurée'].astype('int')

    #show data frame in table
    st.dataframe(df2)


    #--------------    T1   ------------------------------------------------------------------------------------------

    #RESULT FOR PARC T1
    #catrgory box
    st.header('Le Kilométrage pour PARC T1')
        #merge the two file into one file and make the calculation of km in months
    dfF = df1[['Code du point de mesure','Dernier relevé: Valeur mesurée']].merge(df2[['Code du point de mesure','Dernier relevé: Valeur mesurée']], 
                                    on = 'Code du point de mesure', 
                                    how = 'right')
                                    
    dfF['KM'] = dfF["Dernier relevé: Valeur mesurée_y"] - dfF["Dernier relevé: Valeur mesurée_x"]
    #drop result of T2
    dfF = dfF.drop(labels=range(74, 124))
    
    dfsort =dfF.sort_values(['KM'],ascending=[True])
    # ----PLOT DATAFRAME T1 -------
    fig= px.bar(
    dfsort,
    x='Code du point de mesure',
    y='KM',
    color='KM',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T1</b>'
    )
    st.plotly_chart(fig)

    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM'].max()) +'   KM' )

    #---- moyenne of value of KM
    dfmin = dfF[dfF['KM'] != 0]
    st.write('Moyenne de production : ''   '+ str(int(dfmin['KM'].sum() / dfmin['KM'].count())) +'   KM  ' +'  (hors US qui n’ont pas roulé)' )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfmin['KM'].min()) +'   KM')


    # ---T1--CUMMULE -------------------------------------------
    dfF['KM cumul']= dfF['Dernier relevé: Valeur mesurée_y']
    dfsort_cumul =dfF.sort_values(['KM cumul'],ascending=[True])

    # ----PLOT DATAFRAME T1 cumul -------
    fig= px.bar(
    dfsort_cumul,
    x='Code du point de mesure',
    y='KM cumul',
    color='KM cumul',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T1 cumul</b>'
    )
    st.plotly_chart(fig)

    #----- cumul synthes ---------
    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM cumul'].max()) +'   KM' )

    #---- moyenne of value of KM
    
    st.write('Moyenne de production : ''   '+ str(int(dfF['KM cumul'].sum() / dfF['KM cumul'].count())) +'   KM  ' +'  (hors US qui n’ont pas roulé)' )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfF['KM cumul'].min()) +'   KM')


    #------------------   T2   -----------------------------------------------------------------------

    #RESULT FOR PARC T2
    st.header('Le Kilométrage pour PARC T2')
    #merge the two file into one file and make the calculation of km in months
    dfF = df1[['Code du point de mesure','Dernier relevé: Valeur mesurée']].merge(df2[['Code du point de mesure','Dernier relevé: Valeur mesurée']], 
                                    on = 'Code du point de mesure', 
                                    how = 'right')
                                    
    dfF['KM'] = dfF["Dernier relevé: Valeur mesurée_y"] - dfF["Dernier relevé: Valeur mesurée_x"]
    #drop result of T1
    dfF = dfF.drop(labels=range(0, 74))
    

    dfsort =dfF.sort_values(['KM'],ascending=[True])

        # ---PLOT DATAFRAME-- T2--------
    fig= px.bar(
    dfsort,
    x='Code du point de mesure',
    y='KM',
    color='KM',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T2</b>'
    )
    st.plotly_chart(fig)

    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM'].max()) +'   KM' )

    #---- moyenne of value of KM
    dfmin = dfF[dfF['KM'] != 0]
    st.write('Moyenne de production : ''   '+ str(int(dfmin['KM'].sum() / dfmin['KM'].count())) +'   KM  ' + '  (hors US qui n’ont pas roulé)')

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfmin['KM'].min()) +'   KM')
    #-------------------------------------------------------------------------------------------------------


    # ---T2--CUMMULE -------------------------------------------
    dfF['KM cumul']= dfF['Dernier relevé: Valeur mesurée_y']
    dfsort_cumul =dfF.sort_values(['KM cumul'],ascending=[True])

    
    # ----PLOT DATAFRAME T2 cumul -------
    fig= px.bar(
    dfsort_cumul,
    x='Code du point de mesure',
    y='KM cumul',
    color='KM cumul',
    color_continuous_scale=[' red' , 'yellow' , ' green' ],
    template='plotly_white',
    title =f'<b> Le graphe des KM global parcouru parc T1 cumul</b>'
    )
    st.plotly_chart(fig)

    #----- cumul synthes ---------
    st.subheader('Synthèse des tendances de production par US sur le mois :')
    #--- max value of KM
    st.write('Maximum de production : ''   '+ str(dfF['KM cumul'].max()) +'   KM' )

    #---- moyenne of value of KM
    
    st.write('Moyenne de production : ''   '+ str(int(dfF['KM cumul'].sum() / dfF['KM cumul'].count())) +'   KM  ' +'  (hors US qui n’ont pas roulé)' )

    #----min value of KM 
    st.write('Minimum de production : ''   '+ str(dfF['KM cumul'].min()) +'   KM')