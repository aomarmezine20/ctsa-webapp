import streamlit as st # pip install streamlit
import pandas as pd # pip install pandas
import plotly.express as px # pip install plotly-express
from PIL import Image

st.set_page_config(page_title= 'Excel Plotter', page_icon="📈")
st. title('Welcome')



image = Image.open('images/big_logo.png')


col1, col2, col3 = st.columns(3)

with col1:
    st.write('')

with col2:
    st.image(image,width=380)

with col3:
    st.write(' ')

