import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import datetime
import requests
import glob
import os
import pandas as pd
from charts import show_evolution,show_heatmap,get_historical_data
from streamlit_folium import st_folium, folium_static

@st.cache
def load_logo():
     logo = Image.open('logo.PNG')
     return logo

# Define layout basico da página
st.set_page_config(
    page_title="Best Allocation | Le Wagon MVP",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        #'Get Help': 'https://www.extremelycoolapp.com/help',
        #'Report a bug': "https://www.extremelycoolapp.com/bug",
        'About': "# Best Alloction. v0\n" + "This is the first version of the app"
    }
)
col1, col2, col3 = st.columns((3,1,1))

st.sidebar.image(load_logo(), use_column_width=True)


def module_selection():
     
     st.sidebar.write('## Menu')
     tipo_produto_traduzido = st.sidebar.radio("Select the module", ('Demmand Heatmap', 'Demmand Evolution', 'Best Allocation'))

     if tipo_produto_traduzido == 'Demmand Heatmap':
          demmand_heamap()
     elif tipo_produto_traduzido == 'Demmand Evolution':
          demmand_evolution()
     elif tipo_produto_traduzido == 'Best Allocation':
          demmand_prediction()
 
def demmand_prediction():
     with st.form("my_form"):

          st.sidebar.write("")

          hub = st.sidebar.selectbox('Hubs: ', 
                                     ('Alphaville',
                                      'Barra',
                                      'Brasília',
                                      'Cabo Frio',
                                      'Campinas',
                                      'Curitiba',
                                      'Recife',
                                      'São Bernardo do Campo',
                                      'São Cristóvão',
                                      'Tatuapé',
                                      'Vila Olímpia',
                                      'Vitória'))

          available_employees = st.sidebar.number_input(label="Number of available employees:",min_value=1)
               

          date = st.sidebar.date_input("Date: ",datetime.date(day=datetime.date.today().day,
                                   month=datetime.date.today().month, year=datetime.date.today().year),
                                   min_value=datetime.date.today())
          with st.sidebar:

               submitted = st.form_submit_button("Analyze")
          if submitted:
               st.sidebar.write("Hub: ", hub)
               st.sidebar.write("Number of employees: ",  available_employees)
               date_br = f'{date.day}/{date.month}/{date.year}'
               st.sidebar.write('Date: ', date_br)
               url = f'https://best-allocation-eiwjbu3z3a-uc.a.run.app/optimize?hub={hub}&date={date_br}&available_employees={available_employees}&work_hours=8&service_time=0.5&conversion_rate=0.2'
               response = requests.get(url)
               areas = response.json()['suggested_areas']
               necessary_employees = response.json()['necessary_employees']
               centers = response.json()['centers']
               dicionario = {0: 0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0, 10:0, 11:0, 12:0, 13:0, 14:0, 15:0}
               for i in areas:
                    demanda = areas[i]['area_id']
                    dicionario[demanda] = dicionario[demanda] + 1
               df = pd.DataFrame.from_dict(dicionario, orient='index', columns=['demanda'])
               df = df.reset_index()
               df = df.rename(columns={'index':'area'})
               #df = df.set_index('area')
               hide_dataframe_row_index = """
                    <style>
                    .row_heading.level0 {display:none}
                    .blank {display:none}
                    </style>
                    """

               # Inject CSS with Markdown
               st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

               # Display an interactive table
               st.dataframe(df)

def demmand_evolution():
     with st.form("my_form"):

          st.sidebar.write("")

          hub = st.sidebar.selectbox('Hubs: ', 
                                     ('Alphaville',
                                      'Barra',
                                      'Brasília',
                                      'Cabo Frio',
                                      'Campinas',
                                      'Curitiba',
                                      'Recife',
                                      'São Bernardo do Campo',
                                      'São Cristóvão',
                                      'Tatuapé',
                                      'Vila Olímpia',
                                      'Vitória'))
          
          start_date = st.sidebar.date_input("Start date: ",datetime.date(day=1,
                                   month=datetime.date.today().month, year=datetime.date.today().year-1),
                                             min_value=datetime.date(day=1,
                                   month=datetime.date.today().month, year=datetime.date.today().year-2))
          
          end_date = st.sidebar.date_input("End date: ",datetime.date.today(),
                         max_value=datetime.date.today())

          with st.sidebar:

               submitted = st.form_submit_button("Show Evolution")
          if submitted:
               st.sidebar.write("Hub escolhido: ", hub)
               start_date = f'{start_date.day}/{start_date.month}/{start_date.year}'
               end_date = f'{end_date.day}/{end_date.month}/{end_date.year}'
               #url = f'https://best-allocation-eiwjbu3z3a-uc.a.run.app/historic?hub={hub}&start_date={start_date}&end_date={end_date}'
               df = get_historical_data(hub,start_date,end_date)
               folium_static(show_evolution(df, hub),width=1000,height=700)
            
def demmand_heamap():
     with st.form("heatmap"):

          st.sidebar.write("")

          hub = st.sidebar.selectbox('Área desejada: ', 
                                     ('Alphaville',
                                      'Barra',
                                      'Brasília',
                                      'Cabo Frio',
                                      'Campinas',
                                      'Curitiba',
                                      'Recife',
                                      'São Bernardo do Campo',
                                      'São Cristóvão',
                                      'Tatuapé',
                                      'Vila Olímpia',
                                      'Vitória'))
          
          start_date = st.sidebar.date_input("Start date: ",datetime.date(day=1,
                                   month=datetime.date.today().month, year=datetime.date.today().year-1),
                                             min_value=datetime.date(day=1,
                                   month=datetime.date.today().month, year=datetime.date.today().year-2))
          
          end_date = st.sidebar.date_input("End date: ",datetime.date.today(),
                         max_value=datetime.date.today())

          with st.sidebar:

               submitted = st.form_submit_button("Show Heatmap")
          if submitted:
               st.sidebar.write("Hub: ", hub)
               start_date = f'{start_date.day}/{start_date.month}/{start_date.year}'
               end_date = f'{end_date.day}/{end_date.month}/{end_date.year}'
               #url = f'https://best-allocation-eiwjbu3z3a-uc.a.run.app/historic?hub={hub}&start_date={start_date}&end_date={end_date}'
               df = get_historical_data(hub,start_date,end_date)
               st_folium(show_heatmap(df, hub),width=1000)
#               st.markdown(show_heatmap(df, hub), unsafe_allow_html =True)    
                  
module_selection()