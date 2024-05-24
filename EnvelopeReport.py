# -*- coding: utf-8 -*-
"""
Created on Wed May 15 13:58:19 2024

@author: BCLEM
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings




warnings.filterwarnings('ignore')



st.set_page_config(page_title="Docusign Envelope Report", page_icon=":bar_chart:",layout="wide")

st.title(" :bar_chart: Docusign Envelope Dashboard")
st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

#user can upload file
fl = st.file_uploader(":file_folder: Upload a file", type=(["csv","txt","xlsx","xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_csv(filename)
else:
  os.chdir("J:/Corporate Functions/Docusign/Reports/Monthly Reports/2024/Apr/")
  df = pd.read_csv("Envelope Report.csv")
  
col1, col2 = st.columns((2))
df["Sent On (Date)"] = pd.to_datetime(df["Sent On (Date)"])

#Getting the min and max date
startDate = pd.to_datetime(df["Sent On (Date)"]).min()
endDate = pd.to_datetime(df["Sent On (Date)"]).max()

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))
    
with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Sent On (Date)"] >= date1) & (df["Sent On (Date)"] <= date2)].copy()


#Create Account Dropdown
st.sidebar.header("Accounts: ")
account = st.sidebar.multiselect("Choose your Account", df["Account"].unique())
if not account:
    df2 = df.copy()
else:
    df2 = df[df["Account"].isin (account)]
    
#Create for Sender
sender_name = st.sidebar.multiselect("Choose Sender", df2["Sender Name"].unique())
if not sender_name:
    df2 = df.copy()
else:
    df2 = df[df["Sender Name"].isin (sender_name)]
    
#filter database on Account and Sender Name
if not account and not sender_name:
    filtered_df = df
elif not sender_name:
    filtered_df = df[df["Account"].isin(account)]
elif not account:
    filtered_df = df[df["Sender Name"].isin(sender_name)]
    
envelopes_sent = int(filtered_df['Sent On (Date)'].count())
total_pages = int(filtered_df['# of Pages'].sum())
total_recipients = int(filtered_df['# of Recipients'].sum())








## Main Page
left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Envelopes Sent:")
    st.subheader(envelopes_sent)
with middle_column:
    st.subheader("Total Pages:")
    st.subheader(total_pages)
with right_column:
    st.subheader("Total Recipients")
    st.subheader(total_recipients)
    
    
    
    

st.markdown("---")


#Changes Sent On Date to Month
filtered_df['Sent On (Date)'] = pd.to_datetime(
    filtered_df['Sent On (Date)'], format='%m').dt.month_name()


#Create bar chart for envelopes

df_envelopes = filtered_df.groupby(
   filtered_df["Sent On (Date)"])["Envelope ID"].count().sort_values()

fig = px.bar(
    df_envelopes,
    x = df_envelopes.index, 
    y = "Envelope ID",
    orientation="v",
    title="<b> # of Envelopes</b>",
   
)
st.plotly_chart(fig,use_container_width=True, height = 200)

st.markdown("---")

#create bar chart for pages
df_pages = filtered_df.groupby(
   filtered_df["Sent On (Date)"])["# of Pages"].sum().sort_values()

fig = px.bar(
    df_pages,
    x = df_pages.index, 
    y = "# of Pages",
    orientation="v",
    title="<b> # of Pages</b>",
   
)
st.plotly_chart(fig,use_container_width=True, height = 200)

st.markdown("---")

#create bar chart for recipients
#df_pages = filtered_df.groupby(
   #filtered_df["Sent On (Date)"])["# of Recipients"].sum().sort_values()

#fig = px.bar(
   # df_pages,
    #x = df_pages.index, 
   # y = "# of Recipients",
    #orientation="v",
   # title="<b> # of Recipients</b>",
   
#)
#st.plotly_chart(fig,use_container_width=True, height = 200)



