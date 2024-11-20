
import streamlit as st
import pandas as pd
import matplotlib as plt
from datetime import date
#from prophet import Prophet
#from prophet.plot import plot_plotly
from plotly import graph_objs as go
import matplotlib.dates as mdates


st.title("Forecasting :material/timeline:")


def cargar(csv):
    df = pd.read_csv(csv)
    df.reset_index(drop=True,inplace=True)
    return df

histo = cargar('../App/hist_mensual.csv')
histo_dia = cargar('../App/hist_diario.csv')
pred = cargar('../App/predicciones.csv')

st.subheader('Datos Historicos (2022 - 2024)')
st.write(histo)

def plot_historic(df,m):
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=df['Fecha'], y=df['Numero total de viajes']))
	fig.layout.update(title={
            'text': f'Número de viajes {m}',  # Texto del título
            'x': 0.5,  # Centra el título (0 es izquierda, 1 es derecha)
            'xanchor': 'center',  # Asegura el centrado exacto
            'yanchor': 'top'      # Posiciona el título en la parte superior
        },
        title_font={
            'size': 24  # Cambia el tamaño de la letra
        }, xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)

plot_historic(histo_dia,'diario')	
plot_historic(histo,'mensual')

st.subheader('Predicciones (2024 - 2026)')

st.markdown(
    """
    <p style="text-align: justify;">
    Puedes predecir de septiembre de 2024 (1 mes) a febrero del 2026 (18 meses)
    </p>
    """, 
    unsafe_allow_html=True
)

n_months = st.slider('Meses:', 1, 18)

st.write(pred[:n_months])
plot_historic(pred[:n_months],'futuros')