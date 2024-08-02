import pandas as pd
import streamlit as st
# from datetime import datetime, timedelta
# from streamlit_date_picker import date_range_picker, PickerType

from my_data import get_user_medical_records, get_user_information, calc_age
from analysis_diagrams import plot_line_data, plot_gauge, systolic_pressure_color, diastolic_pressure_color, saturation_color, heart_rate,general_pressure_color


# DEFAULT VALUE 1 
# userID = 1
# Get user id with the parameters of the other page
userID = st.query_params["user_id"]

# Load data from the especific user
user_info_df = get_user_information(userID)
medical_records_df = get_user_medical_records(userID)


#* Check if the user exists
if user_info_df.empty:
    st.header(":'(")
    st.header(f"El usuario no existe")
    st.stop()

# User basic information
username = user_info_df.loc[0,"username"]
f_name = user_info_df.loc[0,"first_name"]
l_name = user_info_df.loc[0,"last_name"]
age = calc_age(user_info_df)

#* Check if the user has data (funcion st.stop() para no ejecutar el resto del codigo)
if medical_records_df.empty:
    st.header(":'(")
    st.header(f"No hay registros medicos del usuario: {username}")
    st.stop()


# Medical DATA
# Calc Last_record index
last_index = medical_records_df.shape[0] - 1
last_record = medical_records_df.loc[last_index]
last_systolic_rate = last_record["systolic_pressure"]
last_diastolic_rate = last_record["diastolic_pressure"]
last_heart_rate = last_record["heart_rate"]
last_saturation = last_record["saturation"]
last_record_date = last_record["event_date"]

last_diagnostic = general_pressure_color(last_systolic_rate,last_diastolic_rate)[1]


# page configuration
st.set_page_config(
    page_title=f"Presión arterial y ritmo cardiaco usuario: {username}",
    layout="wide"
    )

st.title("Presión Arterial y Ritmo Cardiaco")

st.subheader(f"Ususario: {username}")

st.markdown(f"Estos son los datos médicos sanguineos de la paciente **{f_name} {l_name}** de \
            **{age}** años de edad.")

st.header(f"Diagnóstico última medición {last_record_date}: {last_diagnostic.upper()}")

# * 1. Gauge Charts

suffix= " mmHg"
heart_rate_suffix = " bpm"
saturation_suffix = " %"

last_systolic_color = systolic_pressure_color(last_systolic_rate)
last_diastolic_color = diastolic_pressure_color(last_diastolic_rate)
last_heart_rate_color = heart_rate(last_heart_rate)
last_saturation_color = saturation_color(last_saturation)


systolic_gauge = plot_gauge(
    indicator_number=last_systolic_rate,
    indicator_color=last_systolic_color,
    indicator_suffix=suffix,
    indicator_title="Presión Sistólica"
)

diastolic_gauge = plot_gauge(
    indicator_number=last_diastolic_rate,
    indicator_color=last_diastolic_color,
    indicator_suffix=suffix,
    indicator_title="Presión Diastólica"
)

heart_rate_gauge = plot_gauge(
    indicator_number=last_heart_rate,
    indicator_color=last_heart_rate_color[0],
    indicator_suffix=heart_rate_suffix,
    indicator_title="Pulsaciones"
)

sturation_gauge = plot_gauge(
    indicator_number=last_saturation,
    indicator_color=last_saturation_color[0],
    indicator_suffix=saturation_suffix,
    indicator_title="Saturación",
    max_bound=100 
)

col1, col2, col3, col4 = st.columns(4)
col1.plotly_chart(systolic_gauge, use_container_width=True)
col2.plotly_chart(diastolic_gauge, use_container_width=True)
col3.plotly_chart(heart_rate_gauge, use_container_width=True)
col4.plotly_chart(sturation_gauge, use_container_width=True)



#! reviewing date range picker

# st.markdown("### 4. Month Range Picker")
# default_start, default_end = datetime.now() - timedelta(days=30), datetime.now()
# refresh_value = timedelta(days=30)
# date_range_string = date_range_picker(picker_type=PickerType.month,
#                                       start=default_start, end=default_end,
#                                       key='month_range_picker',
#                                       refresh_button={'is_show': True, 'button_name': 'Refresh Last 1 Month',
#                                                       'refresh_value': refresh_value})
# if date_range_string:
#     start, end = date_range_string
#     st.write(f"Month Range Picker [{start}, {end}]")

# ! finish


st.header(f"Consolidado de medición año 2024")

# * Line charts

# crear una pestaña para cada medida
tab1, tab2, tab3, tab4 = st.tabs(["P. Sistolica", "P. Diastolica", "Pulsaciones", "Saturacion"])

systolic_chart = plot_line_data(medical_records_df, "event_date", "systolic_pressure", "presion sistolica")
diastolic_chart = plot_line_data(medical_records_df, "event_date", "diastolic_pressure", "presion diastolica")
heart_rate_chart = plot_line_data(medical_records_df, "event_date", "heart_rate", "pulsaciones")
saturation_chart = plot_line_data(medical_records_df, "event_date", "saturation", "saturacion")

# Tablas donde muestren toda la informacion general de cada registro
with tab1:
    # actual, average, max, min, standard deviation
    record = medical_records_df["systolic_pressure"]
    data_table = [{"Valor Actual": last_systolic_rate, 
               "Valor Promedio": record.mean(), 
               "Valor Maximo": record.max(),
               "Valor Minimo": record.min(), 
               "Desviacion Estandard": record.std()}]

    # Plot table and chart
    st.dataframe(data_table, hide_index=True)
    st.plotly_chart(systolic_chart, use_container_width=True)
    
with tab2:
    # actual, average, max, min, standard deviation
    record = medical_records_df["diastolic_pressure"]
    data_table = [{"Valor Actual": last_diastolic_rate, 
               "Valor Promedio": record.mean(), 
               "Valor Maximo": record.max(),
               "Valor Minimo": record.min(), 
               "Desviacion Estandard": record.std()}]

    # Plot table and chart
    st.dataframe(data_table, hide_index=True)
    st.plotly_chart(diastolic_chart, use_container_width=True)

with tab3:
    # actual, average, max, min, standard deviation
    record = medical_records_df["heart_rate"]
    data_table = [{"Valor Actual": last_heart_rate, 
                    "Valor Promedio": record.mean(), 
                    "Valor Maximo": record.max(),
                    "Valor Minimo": record.min(), 
                    "Desviacion Estandard": record.std()}]

    # Plot table and chart
    st.dataframe(data_table, hide_index=True)
    st.plotly_chart(heart_rate_chart, use_container_width=True)

with tab4:
    # actual, average, max, min, standard deviation
    record = medical_records_df["saturation"]
    data_table = [{"Valor Actual": last_saturation, 
               "Valor Promedio": record.mean(), 
               "Valor Maximo": record.max(),
               "Valor Minimo": record.min(), 
               "Desviacion Estandard": record.std()}]

    # Plot table and chart
    st.dataframe(data_table, hide_index=True)
    st.plotly_chart(saturation_chart, use_container_width=True)


# * Display tables
st.header("Tabla registros año 2024")
# st.dataframe(user_info_df)
st.dataframe(
    # Drop columns
    medical_records_df.drop(["id","user_id"], axis=1).sort_values(by="event_date", ascending=False),
    use_container_width=True)