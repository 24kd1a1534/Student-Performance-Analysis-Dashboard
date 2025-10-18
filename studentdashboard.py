
import streamlit as st
import pandas as pd
import plotly.express as px
def load_data():
    df = pd.read_excel("C:\\Users\\sachi\\Downloads\\student_performance_100.xlsx")
    df["Total Score"] = df[["Math Score", "Reading Score", "Writing Score"]].mean(axis=1)
    df["Read+Write"] = df["Reading Score"] + df["Writing Score"]
    return df

df = load_data()
st.sidebar.header("Filter Options")
ethnicity = st.sidebar.multiselect("Ethnicity", df["Ethnicity"].unique(), df["Ethnicity"].unique())
gender = st.sidebar.multiselect("Gender", df["Gender"].unique(), df["Gender"].unique())
education = st.sidebar.multiselect("Parental Education", df["Parental Education"].unique(), df["Parental Education"].unique())
prep = st.sidebar.multiselect("Test Preparation", df["Test Preparation"].unique(), df["Test Preparation"].unique())

filtered_df = df[
    (df["Ethnicity"].isin(ethnicity)) &
    (df["Gender"].isin(gender)) &
    (df["Parental Education"].isin(education)) &
    (df["Test Preparation"].isin(prep))
]
st.title("Student Performance Analysis Dashboard")
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Student Count", len(filtered_df))
col2.metric("Avg Math", f"{filtered_df['Math Score'].mean():.2f}")
col3.metric("Avg Reading", f"{filtered_df['Reading Score'].mean():.2f}")
col4.metric("Avg Writing", f"{filtered_df['Writing Score'].mean():.2f}")
col5.metric("Avg Total", f"{filtered_df['Total Score'].mean():.2f}")
fig1 = px.bar(filtered_df, x="Ethnicity", y="Total Score", color="Ethnicity", title="Total Score by Ethnicity")
gender_avg = filtered_df.groupby("Gender")["Total Score"].mean().reset_index()
fig2 = px.pie(gender_avg, names="Gender", values="Total Score", title="Average Total Score by Gender")
edu_avg = filtered_df.groupby("Parental Education")["Total Score"].mean().reset_index()
fig3 = px.bar(edu_avg, x="Parental Education", y="Total Score", color="Parental Education", title="Avg Total Score by Parental Education")
prep_count = filtered_df["Test Preparation"].value_counts().reset_index()
prep_count.columns = ["Test Preparation", "Count"]
fig4 = px.pie(prep_count, names="Test Preparation", values="Count", title="Test Preparation Completion")
fig5 = px.bar(filtered_df, x="Student ID", y="Read+Write", title="Reading + Writing Score by Student")
c1,c2=st.columns(2)
with c1:
    st.plotly_chart(fig3, use_container_width=True)
with c2:
    st.plotly_chart(fig2, use_container_width=True)
c3,c4=st.columns(2)
with c1:
    st.plotly_chart(fig1, use_container_width=True)
with c2:
    st.plotly_chart(fig4, use_container_width=True)

st.plotly_chart(fig5, use_container_width=True)