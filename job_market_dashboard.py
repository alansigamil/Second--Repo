import streamlit as st
import pandas as pd
import plotly.express as px
import os

csv_file = r"C:\Users\Alansi Gamil\Desktop\My project\Jobs and Salaries in Data field 2024\jobs_in_data_2024.csv"

@st.cache_data
def load_data(file_path):
    if not os.path.exists(file_path):
        st.error(f"File not found: {file_path}")
        st.stop()
    return pd.read_csv(file_path)

def filter_data(data, location=None, experience=None, work_setting=None, min_salary=None):
    filtered_data = data.copy()
    if location:
        filtered_data = filtered_data[filtered_data['company_location'] == location]
    if experience:
        filtered_data = filtered_data[filtered_data['experience_level'] == experience]
    if work_setting:
        filtered_data = filtered_data[filtered_data['work_setting'] == work_setting]
    if min_salary:
        filtered_data = filtered_data[filtered_data['salary_in_usd'] >= min_salary]
    return filtered_data

st.title("Job Market Data Analysis Dashboard")

jobs_data = load_data(csv_file)

st.sidebar.header("Filter Jobs")
location = st.sidebar.selectbox("Select Location", options=["All"] + jobs_data['company_location'].unique().tolist())
experience = st.sidebar.selectbox("Select Experience Level", options=["All"] + jobs_data['experience_level'].unique().tolist())
work_setting = st.sidebar.selectbox("Select Work Setting", options=["All"] + jobs_data['work_setting'].unique().tolist())
min_salary = st.sidebar.slider("Minimum Salary (USD)", min_value=0, max_value=int(jobs_data['salary_in_usd'].max()), value=0)

filtered_data = filter_data(
    jobs_data,
    location=None if location == "All" else location,
    experience=None if experience == "All" else experience,
    work_setting=None if work_setting == "All" else work_setting,
    min_salary=min_salary
)

st.header("Filtered Jobs Data")
st.write(f"Showing {len(filtered_data)} jobs")
st.dataframe(filtered_data)

st.header("Visualizations")

st.subheader("Salary Distribution")
fig1 = px.histogram(
    filtered_data,
    x='salary_in_usd',
    nbins=30,
    title="Salary Distribution (in USD)",
    labels={'salary_in_usd': 'Salary in USD'},
    template='plotly_white'
)
st.plotly_chart(fig1)

st.subheader("Employment Types Proportion")
employment_type_counts = filtered_data['employment_type'].value_counts()
fig2 = px.pie(
    values=employment_type_counts.values,
    names=employment_type_counts.index,
    title="Employment Types Proportion",
    template='plotly_white'
)
st.plotly_chart(fig2)

st.subheader("Top 10 Job Locations")
location_counts = filtered_data['company_location'].value_counts().head(10)
fig3 = px.bar(
    location_counts,
    x=location_counts.index,
    y=location_counts.values,
    title="Top 10 Job Locations by Count",
    labels={'x': 'Company Location', 'y': 'Job Count'},
    template='plotly_white'
)
st.plotly_chart(fig3)

# Salary by Experience Level
st.subheader("Salary by Experience Level")
fig4 = px.box(
    filtered_data,
    x='experience_level',
    y='salary_in_usd',
    title="Salary Distribution by Experience Level",
    labels={'experience_level': 'Experience Level', 'salary_in_usd': 'Salary in USD'},
    template='plotly_white'
)
st.plotly_chart(fig4)
