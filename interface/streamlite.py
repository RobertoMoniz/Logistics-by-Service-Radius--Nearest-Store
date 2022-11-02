import streamlit as st
from PIL import Image
import streamlit_authenticator as stauth
import datetime
import requests
import glob
import os
import pandas as pd
from charts import show_evolution,show_heatmap,get_historical_data, show_map
from voronoi import calc_polygons, plot_voronoi
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
               areas_df = pd.DataFrame.from_dict(response.json()['suggested_areas'],orient='index')
               necessary_employees = response.json()['necessary_employees']
               centers_df = pd.DataFrame.from_dict(response.json()['centers'],orient='index').reset_index()
               
               areas_df=areas_df.groupby(by='area_id',as_index=False).count()
               areas_df.columns=['area_id','number of employees']
               
               st.header("Staff analysis")
               st.write("Necessary Employees:\n" + str(necessary_employees))
               st.write("Available Employees:\n" + str(available_employees))
               
               if necessary_employees > available_employees:
                    st.write('Undersized staff')
               elif necessary_employees == available_employees:
                    st.write('Oversized staff')
               else:
                    st.write('Optimal staff')


               
               centers_df.columns=['area_id','latitude','longitude']
               centers_df['area_id']=centers_df['area_id'].astype(int)

               centers_df["polygons"] = calc_polygons(centers_df)

               col1, col2 = st.columns((5,2))
               
               final_df = pd.merge(areas_df,centers_df,on='area_id',how='right')

               final_df['number of employees']=final_df['number of employees'].fillna(0).astype(int)

               with col1:
                    st.header("Area Centers")
                    m=show_map(final_df,hub)[0]
                    plot_voronoi(final_df, m)
                    st_folium(m,height=500,width=600)
               
               with col2:
                    st.header("Allocation")               
                    st.dataframe(show_map(final_df,hub)[1][['color','number of employees']],height=500,width=500)
               


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
               folium_static(show_evolution(df, hub)[0],width=1000,height=700)
            
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