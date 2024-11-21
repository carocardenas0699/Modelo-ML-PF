
import streamlit as st
import pandas as pd
from plotly import graph_objs as go
from streamlit_option_menu import option_menu

st.markdown(
    """
    <div style="display: flex; align-items: center; justify-content: center;">
        <h1 style="margin-right: 0px;">Business Intelligence</h1>
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" style="width: 50px; height: 50px;">
            <path d="M22,21H2V3H4V19H6V10H10V19H12V6H16V19H18V14H22V21Z" fill="#367884" />
        </svg>
    </div>
    """,
    unsafe_allow_html=True
)

pred = pd.read_csv('../App/pred.csv')
n_months = pred.shape[0]

if n_months == 30:
     st.warning('No has seleccionado un numero de meses para predecir')
else:
    st.markdown("""
    En esta seccion podras realizar un analisis de negocio con base en el comportamiento del mercado de la ciudad a partir de:
    - Evaluacion de costos
    - Impacto ambiental
    """)

total_usd = pred['Ingreso total (USD)'].sum()  # Sumar los ingresos en USD de los primeros meses seleccionados
total_pas = pred['Numero total de pasajeros'].sum()
total_dist = pred['Distancia total recorrida (mi)'].sum() 
total_dur = pred['Duración total recorrido (min)'].sum() / 60  # Sumar el número de viajes de los primeros meses seleccionados
dias_pred = n_months*30

st.header(f'Estimaciones para {n_months-30} meses de operacion')

st.subheader('Demanda futura en NYC')

col, col3 = st.columns(2, gap='large', vertical_alignment='center')

with col:
    total_viajes = pred['Numero total de viajes'][30:].sum()
    st.metric(f"Numero total de viajes en {n_months-30} meses:", f"{total_viajes:,}")

with col:
    viajes_dia = total_viajes/dias_pred
    st.metric(f"Numero aproximado de viajes diarios:", f"{int(viajes_dia):,}")

with col3:
    viajes_veh = 20
    veh_dia = (viajes_dia / viajes_veh ) * 1.1
    st.metric(f"Numero aproximado de vehiculos necesarios:", f"{int(veh_dia):,}")

st.markdown('***')

st.subheader('Qué porcentaje de la demanda te gustaria cubrir?')
per_d = st.slider('Porcentaje:', 0, 100, key='per_d')
per_d = per_d / 100

co4, col5 = st.columns(2, gap='large', vertical_alignment='center')

with co4:
    viajes_dia_cubrir = viajes_dia*per_d
    st.metric(f"Cubririas estos viajes diarios:", f"{int(viajes_dia_cubrir):,}")

with col5:
    vehiculos_necesarios = veh_dia*per_d

    st.metric(f"Necesitarias este numero de vehiculos:", f"{int(vehiculos_necesarios):,}")

st.markdown('***')

st.subheader('Selecciona el porcentaje de vehiculos electricos 🍃')
per = st.slider('Porcentaje:', 0, 100, key='per')
per = per / 100

st.markdown('#### Tu flota estaria compuesta por:')

col1, col2 = st.columns(2, gap='large', vertical_alignment='center')

with col1:
    veh_cov = vehiculos_necesarios*(1-per)
    st.metric(f"Vehiculos convencionales:", f"{int(veh_cov):,}")

with col2:
    veh_ele = vehiculos_necesarios*per
    st.metric(f"Vehiculos electricos", f"{int(veh_ele):,}")

st.markdown("***")

st.subheader('Selecciona el modelo del vehiculo convencional que quisieras adquirir 🚕')

eleccion2 = None

col1, col2, col3 = st.columns(3)

with col1:
    st.image('./images/Usado.jpg', width= 350)

with col2:
    st.image('./images/Nuevo.jpg', width= 350)

with col3:
    opcion = ['Usado', 'Nuevo']
    estado = st.radio('Estado del vehiculo', opcion)


st.markdown('***')

st.subheader('Selecciona el modelo del vehiculo electrico que quisieras adquirir 🚙')

evs = pd.read_csv('../App/EVs models.csv', index_col='ID')

eleccion1 = None

col1, col2, col3 = st.columns(3)
col4, col5, col6 = st.columns(3)

with col1:
    st.image('./images/Veh1.jpg')
    if st.button("Elegir", key="grupo1_Opcion 1"):
        eleccion1 = 1
with col2:
    st.image('./images/Veh2.jpg')
    if st.button("Elegir", key="grupo1_Opcion 2"):
        eleccion1 = 2
with col3:
    st.image('./images/Veh3.jpg')
    if st.button("Elegir", key="grupo1_Opcion 3"):
        eleccion1 = 3
with col4:
    st.image('./images/Veh4.jpg')
    if st.button("Elegir", key="grupo1_Opcion 4"):
        eleccion1 = 4
with col5:
    st.image('./images/Veh5.jpg')
    if st.button("Elegir", key="grupo1_Opcion 5"):
        eleccion1 = 5
with col6:
    st.image('./images/Veh6.jpg')
    if st.button("Elegir", key="grupo1_Opcion 6"):
        eleccion1 = 6

if eleccion1:

    nombre = evs['Brand_Model'][eleccion1]
    precio_veh_ele = evs['PriceUSD'][eleccion1]
    eff = evs['Efficiency_WhKm'][eleccion1]

    st.write(f'Elegiste el vehiculo electrico: {nombre}')

    st.markdown('***')

    dist_diaria = total_dist / dias_pred

    col1, col2 = st.columns(2, gap='large', vertical_alignment='top')

    co2 = total_dist*(411/1000000)*(1-per)
    co2_dia = dist_diaria*(411/1000000)*(1-per)
    cost_gas = (dist_diaria/40)*3.42*(1-per)
    cons_kw = ((dist_diaria*per*1.60934)*eff)/1000
    cost_kw = cons_kw*0.2

    if estado == 'Usado':
        precio_conv = 15000
    else:
        precio_conv = 27500

    cost_veh_conv = veh_cov*precio_conv
    cost_veh_ele = precio_veh_ele*veh_ele
    cost_veh = cost_veh_ele + cost_veh_conv

    with col1:
        st.subheader('Inversion Inicial 💵')
        st.metric("Costo de vehiculos convencionales (USD)", f"${cost_veh_conv:,.2f}")
        st.metric("Costo de vehiculos electricos (USD)", f"${cost_veh_ele:,.2f}")
        st.metric("Costo total de la flota (USD)", f"${cost_veh:,.2f}")

    with col2:
        st.subheader('Gasto Operacional ⛽')
        st.metric("Costo de gasolina (USD)", f"${cost_gas:,.2f}")
        st.metric("Costo de watts (USD)", f"${cost_kw:,.2f}")
        st.metric("Costo total de combustible en un dia (USD)", f"${(cost_kw+cost_gas):,.2f}")

    st.markdown('***')

    st.subheader('Impacto ambiental 🌎')
    st.metric("Emisiones de CO2 en un dia (ton)", f"{co2_dia:,.2f}")
    st.metric(f"Total emisiones de CO2 en {n_months-30} meses (ton)", f"{co2:,.2f}")
else:
    st.warning('Debes seleccionar un vehiculo electrico')
