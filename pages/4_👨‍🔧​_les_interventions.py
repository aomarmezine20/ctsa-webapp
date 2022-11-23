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
    
    df['US'] = df['Matériel'].str.split('.').str[0]
    

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
    fig.write_image("images/fig_Intrv1.jpeg")
    #make data frame for just nature of intervention and count how much for every values 
    df_intv_count = df_t1["Nature d'intervention"].value_counts()

    #rest index to separate index colomn and make calculation to show every nature of intervention 
    df_intv_count = df_intv_count.reset_index()
    st.header('Suivi de la maintenance préventive ')

    

#----------------case if values of prventif doesn't existe -----------------------------------------------------
    if df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
        st.markdown('  * le nombre des interventions préventives du mois est **'+str(0)+'** ')
    else :
        st.markdown('  * le nombre des interventions préventives du mois est **'+str(int(df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"]))+'** ')
#---------------------------------------------------------------------------------------------------------------------

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
    fig.write_image("images/fig_Intrv2.jpeg")
    
    st.subheader('Taux d’occupation par parc :')
    st.header('Suivi des interventions correctives')
    
    #-------------if is not any values of correctif --------------------------------------------------------------------------------------

    if df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
        st.markdown('  * le nombre des interventions correctives du mois est **'+str(0)+'** ')
    else :

        st.markdown('  * le nombre des interventions correctives du mois est **'+str(int(df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"]))+'** ')
    #------------------------------------------------------------------------------------
    
    st.subheader('La répartition des interventions correctives par priorités :')

    #make a new datafram for just correctif intervention and name it 
    df_t1_cr =df_t1[df_t1["Nature d'intervention"]=='CORRECTIF']

    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t1_cr, names="Priorité")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_Intrv3.jpeg")
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
    fig.write_image("images/fig_Intrv4.jpeg")

    st.subheader("La répartition des interventions correctives en fonction des ‘’Etat’’ :")
    
    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t1_cr, names="Etat")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_Intrv5.jpeg")





#--------------------------------------------PARC T2 ------------------------------------------------------------------------------------
    st.header('-----------------PARC T2------------------')
    st.subheader('Le nombre total d’ordre de travaux')
    st.markdown('  * le nombre des interventions du mois est **'+str(df_t2["Code de l'intervention"].count())+'** ')
    st.subheader('La répartition des interventions de maintenance par type :')
    #plot etat of interventions pie chart 
    fig = px.pie(df_t2, names="Nature d'intervention",color="Nature d'intervention")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_intrv6.jpeg")
    #make data frame for just nature of intervention and count how much for every values 
    df_intv_count2 = df_t2["Nature d'intervention"].value_counts()

    #rest index to separate index colomn and make calculation to show every nature of intervention 
    df_intv_count2 = df_intv_count2.reset_index()
    st.header('Suivi de la maintenance préventive ')

#check if is not any values of preventif -------------------------------------------------------------------
    if df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
        st.markdown('  * le nombre des interventions préventives du mois est **'+str(0)+'** ')
    else :

        st.markdown('  * le nombre des interventions préventives du mois est **'+str(int(df_intv_count2[df_intv_count2['index']=='PREVENTIF']["Nature d'intervention"]))+'** ')
#-----------------------------------------------------------------------------------------------------------------------------------

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
    fig.write_image("images/fig_intrv7.jpeg")
    
    st.subheader('Taux d’occupation par parc :')
    st.header('Suivi des interventions correctives')

    #show nbr of correctif interventions

 #--------------------case if there isn't any values of correctif ------------------------------------
 

    if df_intv_count2[df_intv_count2['index']=='CORRECTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
        st.markdown('  * le nombre des interventions correctives du mois est **'+str(0)+'** ')
    else :

        st.markdown('  * le nombre des interventions correctives du mois est **'+str(int(df_intv_count2[df_intv_count2['index']=='CORRECTIF']["Nature d'intervention"]))+'** ')
#----------------------------------------------------------------------------------------------------

    
    st.subheader('La répartition des interventions correctives par priorités :')

    #make a new datafram for just correctif intervention and name it 
    df_t2_cr =df_t2[df_t2["Nature d'intervention"]=='CORRECTIF']

    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t2_cr, names="Priorité")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_intrv8.jpeg")
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
    fig.write_image("images/fig_intrv9.jpeg")

    st.subheader("La répartition des interventions correctives en fonction des ‘’Etat’’ :")
    
    #plot the datafram in bar chart of every periority and pourcentage
    fig = px.pie(df_t2_cr, names="Etat")
    fig.update_traces(hoverinfo='label+percent', textinfo='value+percent')
    st.plotly_chart(fig)
    fig.write_image("images/fig_intrv10.jpeg")
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
        
        pdf.cell(140, 15, "les statistiques des interventions", 1, 0, 'C')

        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
# ------------------ PARC T1 -----------------------------------------------------------------------------------------------
        pdf.cell(60, 20, '         ----------------- PARC T1 ------------------', 'C')
        pdf.ln(15)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 20, "Le nombre total d'ordre de travaux", 'C')
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.cell(60, 20, '  * le nombre des interventions du mois est '+str(df_t1["Code de l'intervention"].count()), 'C')

        pdf.ln(15)
        pdf.set_font('Times', 'B', 20)
        

        pdf.cell(60, 20, "La répartition des interventions de maintenance par type :", 'C')
        pdf.image('images/fig_Intrv1.jpeg', x=5, y=110, w=200,h=150)
        #footer
        footer(pdf)

        pdf.ln(190)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi de la maintenance préventive:", 'C')
        header(pdf)

        pdf.ln(30)
        pdf.set_font('Times', '', 15)
        pdf.cell(10)
    #--------------------case if there isn't any values of preventif 
        if df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(0), 'C')
        else :
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(int(df_intv_count[df_intv_count['index']=='PREVENTIF']["Nature d'intervention"])), 'C')
    #----------------------------------------------------------------------------------------------------
        pdf.ln(0)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi des interventions préventives :", 'C')
        pdf.image('images/fig_Intrv2.jpeg', x=5, y=80, w=200,h=150)

        footer(pdf)

        pdf.ln(190)
        pdf.set_font('Times', 'B', 20)
        

        pdf.cell(60, 57, "Taux d'occupation par parc :", 'C')
        header(pdf)

        pdf.ln(140)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi des interventions correctives:", 'C')
        pdf.ln(39)
        pdf.cell(10)
        pdf.set_font('Times', '', 15)
    #--------------------case if there isn't any values of correctif ------------------------------------

        if df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(0), 'C')
        else :
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(int(df_intv_count[df_intv_count['index']=='CORRECTIF']["Nature d'intervention"])), 'C')
    #----------------------------------------------------------------------------------------------------
        footer(pdf)
        pdf.ln(0)
        pdf.set_font('Times', 'B', 20)
        
        pdf.ln(120)
        pdf.cell(60, 57, "La répartition des interventions correctives par priorités :", 'C')
        
        pdf.image('images/fig_Intrv3.jpeg', x=5, y=50, w=200,h=150)
        pdf.ln(180)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* FJ ( y compris les FJ prioritaire):","C")
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(120, 20, "Fin de Jour, c'est une panne mineur qui" )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "peut etre planifiée à la fin de l'exploitation de la rame", 'C' )

        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* FT :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-45)
        pdf.cell(20, 20, "Fin de Tour, c'est une panne qui nécessite le rapatriement de la rame " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "à la fin de sa course", 'C' )


        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* HLP :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-42)
        pdf.cell(20, 20, "Haut le Pied, c'est une panne majeur qui nécessite l'évacuation des voyageurs  " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "et le rapatriement immédiat de le rame", 'C' )


        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* RP :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-46)
        pdf.cell(20, 20, "Remorquage/Poussage, c'est une panne majeur qui nécessite l'évacuation   " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "des voyageurs et le rapatriement de la rame en mode US-US soit par remorquage ", 'C' )

        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "[ US menante], soit par poussage [US menée] ou par camion rail-route.", 'C' )

        

        pdf.set_font('Times', 'B', 20)
        pdf.ln(65)
        pdf.cell(10)
        pdf.cell(50, 75, "La répartition des interventions par famille de défaut :", 'C' )

        pdf.image('images/fig_Intrv4.jpeg', x=5, y=65, w=200,h=150)
        header(pdf)
        footer(pdf)

        pdf.set_font('Times', 'B', 20)
        pdf.ln(65)
        pdf.cell(10)
        pdf.cell(50, 75, "La répartition des interventions correctives en fonction ","C")
        pdf.cell(-46)
        pdf.cell(10, 90,"des Etat :", 'C' )
        pdf.image('images/fig_Intrv5.jpeg', x=5, y=65, w=200,h=150)
        
        header(pdf)
        footer(pdf)
#---------------   PARC  T2  -----------------------------------------------------------------------------------------------------------
        pdf.ln(65)
        pdf.cell(10)
        pdf.ln(30)
        pdf.set_font('Arial', 'B', 25)
        header(pdf)
        pdf.cell(60, 20, '         ----------------- PARC T2 ------------------', 'C')
        pdf.ln(15)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 20, "Le nombre total d'ordre de travaux", 'C')
        pdf.set_font('Times', '', 15)
        pdf.ln(15)
        pdf.cell(10)
        pdf.cell(60, 20, '  * le nombre des interventions du mois est '+str(df_t2["Code de l'intervention"].count()), 'C')

        pdf.ln(15)
        pdf.set_font('Times', 'B', 20)
        

        pdf.cell(60, 20, "La répartition des interventions de maintenance par type :", 'C')
        pdf.image('images/fig_intrv6.jpeg', x=5, y=110, w=200,h=150)
        #footer
        footer(pdf)

        pdf.ln(190)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi de la maintenance préventive:", 'C')
        header(pdf)

        pdf.ln(30)
        pdf.set_font('Times', '', 15)
        pdf.cell(10)
    #--------------------case if there isn't any values of preventif ------------------------------------

        if df_intv_count2[df_intv_count2['index']=='PREVENTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(0), 'C')
        else :
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(int(df_intv_count2[df_intv_count2['index']=='PREVENTIF']["Nature d'intervention"])), 'C')
    #------------------------------------------------------------------------------------------------------------

        pdf.ln(0)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi des interventions préventives :", 'C')
        pdf.image('images/fig_intrv7.jpeg', x=5, y=80, w=200,h=150)

        footer(pdf)

        pdf.ln(190)
        pdf.set_font('Times', 'B', 20)
        

        pdf.cell(60, 57, "Taux d'occupation par parc :", 'C')
        header(pdf)

        pdf.ln(140)
        pdf.set_font('Times', 'B', 25)
        

        pdf.cell(60, 57, "Suivi des interventions correctives:", 'C')
        pdf.ln(39)
        pdf.cell(10)
        pdf.set_font('Times', '', 15)
    #--------------------case if there isn't any values of correctif ------------------------------------

        if df_intv_count2[df_intv_count2['index']=='CORRECTIF']["Nature d'intervention"].empty :
         #show nbr of correctif interventions
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(0), 'C')
        else :
            pdf.cell(60, 20, '  * le nombre des interventions préventives du mois est '+str(int(df_intv_count2[df_intv_count2['index']=='CORRECTIF']["Nature d'intervention"])), 'C')
        #------------------------------------------------------------- ------------------------------------

        footer(pdf)
        pdf.ln(0)
        pdf.set_font('Times', 'B', 20)
        
        pdf.ln(120)
        pdf.cell(60, 57, "La répartition des interventions correctives par priorités :", 'C')
        
        pdf.image('images/fig_intrv8.jpeg', x=5, y=50, w=200,h=150)
        pdf.ln(180)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* FJ ( y compris les FJ prioritaire):","C")
        pdf.cell(20)
        pdf.set_font('Times', '', 15)
        pdf.cell(120, 20, "Fin de Jour, c'est une panne mineur qui" )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "peut etre planifiée à la fin de l'exploitation de la rame", 'C' )

        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* FT :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-45)
        pdf.cell(20, 20, "Fin de Tour, c'est une panne qui nécessite le rapatriement de la rame " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "à la fin de sa course", 'C' )


        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* HLP :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-42)
        pdf.cell(20, 20, "Haut le Pied, c'est une panne majeur qui nécessite l'évacuation des voyageurs  " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "et le rapatriement immédiat de le rame", 'C' )


        pdf.ln(10)
        pdf.cell(10)
        pdf.set_font('Times', 'B', 15)
        pdf.cell(60, 20, "* RP :","C")
        pdf.set_font('Times', '', 15)
        pdf.cell(-46)
        pdf.cell(20, 20, "Remorquage/Poussage, c'est une panne majeur qui nécessite l'évacuation   " )
        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "des voyageurs et le rapatriement de la rame en mode US-US soit par remorquage ", 'C' )

        pdf.ln(5)
        pdf.cell(15)
        pdf.cell(60, 20, "[ US menante], soit par poussage [US menée] ou par camion rail-route.", 'C' )

        

        pdf.set_font('Times', 'B', 20)
        pdf.ln(65)
        pdf.cell(10)
        pdf.cell(50, 75, "La répartition des interventions par famille de défaut :", 'C' )

        pdf.image('images/fig_intrv9.jpeg', x=5, y=65, w=200,h=150)
        header(pdf)
        footer(pdf)

        pdf.set_font('Times', 'B', 20)
        pdf.ln(65)
        pdf.cell(10)
        pdf.cell(50, 75, "La répartition des interventions correctives en fonction ","C")
        pdf.cell(-46)
        pdf.cell(10, 90,"des Etat :", 'C' )
        pdf.image('images/fig_intrv10.jpeg', x=5, y=65, w=200,h=150)
        footer(pdf)


        return pdf.output(dest='S').encode('latin-1')

    # Embed PDF to display it:
    base64_pdf = b64encode(gen_pdf()).decode("utf-8")
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="400" type="application/pdf">'
    #to show pdf in page 
    # st.markdown(pdf_display, unsafe_allow_html=True)
    
    

    # Add a download button:
    st.subheader("Télecharger PDF")
    st.download_button(
        label="Télecharger Resultat PDF",
        data=gen_pdf(),
        file_name="suivi les interventions  Ctsa.pdf",
        mime="application/pdf",
    )