# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 18:19:01 2023

@author: HuntS2
"""

"""
Edited on Tuesday August 8, 2023 by Sawyer Hunt
"""

import pandas as pd
import numpy as np
import streamlit as st
import plotly_express as px


np.random.seed(42)
@st.cache(allow_output_mutation = True)
def get_data():
    df = pd.DataFrame(np.random.randint(0, 100, size = (30, 4)), columns = ["AR 1260", "AR 1254", "AR 1242", "AR 1248"])
    return df
df = get_data()


df.loc[df.index[:10], "Matrix"] = "Water"
df.loc[df.index[10:20], "Matrix"] = "Soil"
df.loc[df.index[20:30], "Matrix"] = "Oil"

df["Units"] = "ug/L"

lat = np.random.uniform(low = 32.8, high = 32.9, size = (30))
long = np.random.uniform(low = -81, high = -80, size = (30))

df["Latitude"] = lat
df["Longitude"] = long


sample = ["S1", "S2", "S3", "S4", "S5", "S6", "S7", "S8", "S9", "S10"]
df.loc[df.index[:10], "Sample"] = sample
df.loc[df.index[10:20], "Sample"] = sample
df.loc[df.index[20:30], "Sample"] = sample


df.set_index("Sample")


st.title("Analytical Dashboard")

st.text("Hello and welcome to the Polychlorinated Biphenyls (PCB) Analytical Dashboard! \nPlease, take some time to interact with the different filters and figures. \nNote: This data was randomly generated using NumPy and does not reflect any \nreal data.")

st.sidebar.header("Filter Options")
samples = st.sidebar.multiselect("Select Sample", df["Sample"].unique())
matrix = st.sidebar.multiselect("Select Matrix", df["Matrix"].unique())


df_selection = df.query("Sample == @samples") 
df_selection2 = df.query("Matrix == @matrix")
df_selection3 = pd.concat([df_selection, df_selection2])
# df_selection3 = df_selection.append(df_selection2)

st.dataframe(df_selection3)


# filtered bar chart
ar1260 = round(df_selection3["AR 1260"].sum(), 2)
ar1254 = round(df_selection3["AR 1254"].sum(), 2)
ar1242 = round(df_selection3["AR 1242"].sum(), 2)
ar1248 = round(df_selection3["AR 1248"].sum(), 2)

bar = px.bar(df_selection3,
             x = ["Total AR 1260", "Total AR 1254", "Total AR 1242", "Total AR 1248"],
             y = [ar1260, ar1254, ar1242, ar1248],
             title = "PCB Totals by Sample/Matrix")
bar.update_layout(xaxis_title = "Analyte", yaxis_title = "Concentration (ug/L)")
st.plotly_chart(bar)


# Map
fig1 = px.scatter_mapbox(df,
                        lat = "Latitude",
                        lon = "Longitude",
                        color = "Matrix",
                        hover_data = ["Sample", "AR 1260", "AR 1254", "AR 1242", "AR 1248"],
                        zoom = 8,
                        title = "PCB Map",
                        labels = {"Latitude" : "Latitude ", "Longitude" : "Longitude "},
                        color_discrete_sequence = ["red", "green", "blue"])
fig1.update_layout(mapbox_style = "open-street-map")
# st.plotly_chart(fig1)


# Radar chart
water = df[df["Matrix"] == "Water"]
radar1 = px.line_polar(water,
                         r = water[["AR 1260", "AR 1254", "AR 1242", "AR 1248"]].mean(),
                         theta = ["AR 1260", "AR 1254", "AR 1242", "AR 1248"],
                         line_close = True,
                         title = "Mean Of PCB Concentrations in Water (ug/L)")
radar1.update_traces(fill = 'toself')
radar1.update_polars(angularaxis_tickcolor = "red", radialaxis_color = "black")
# st.plotly_chart(radar1)


soil = df[df["Matrix"] == "Soil"]
radar2 = px.line_polar(soil,
                         r = np.mean(soil[["AR 1260", "AR 1254", "AR 1242", "AR 1248"]]),
                         theta = ["AR 1260", "AR 1254", "AR 1242", "AR 1248"],
                         line_close = True,
                         title = "Mean Of PCB Concentrations in Soil (ug/L)")
radar2.update_traces(fill = 'toself')
radar2.update_polars(angularaxis_tickcolor = "red", radialaxis_color = "black")
# st.plotly_chart(radar2)


oil = df[df["Matrix"] == "Oil"]
radar3 = px.line_polar(oil,
                         r = np.mean(oil[["AR 1260", "AR 1254", "AR 1242", "AR 1248"]]),
                         theta = ["AR 1260", "AR 1254", "AR 1242", "AR 1248"],
                         line_close = True,
                         title = "Mean Of PCB Concentrations in Oil (ug/L)")
radar3.update_traces(fill = 'toself')
radar3.update_polars(angularaxis_tickcolor = "red", radialaxis_color = "black")
# st.plotly_chart(radar3)


# Summary stats
total1260 = df["AR 1260"].sum()
total1254 = df["AR 1254"].sum()
total1242 = df["AR 1242"].sum()
total1248 = df["AR 1248"].sum()


# tabs
tab1, tab2, tab3 = st.tabs(["Map", "Radar Charts", "Summary Statistics"])
with tab1:
    st.header("Sampling Map")
    st.plotly_chart(fig1)
with tab2:
    st.header("Radar Charts by Matrix")
    st.plotly_chart(radar1)
    st.plotly_chart(radar2)
    st.plotly_chart(radar3)
with tab3:
    st.header("PCB Trends Compared to Last Sampling Event")
    st.metric(label = "AR 1260 Total ug/L", value = total1260, delta = 10, delta_color = "inverse")
    st.metric(label = "AR 1254 Total ug/L", value = total1254, delta = -20, delta_color = "inverse")
    st.metric(label = "AR 1242 Total ug/L", value = total1242, delta = 15, delta_color = "inverse")
    st.metric(label = "AR 1248 Total ug/L", value = total1248, delta = -5, delta_color = "inverse")









