import datetime
import random

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Daily Activity")
st.title("Daily Activity")

if "df" not in st.session_state:

 
    np.random.seed(42)

 
    issue_descriptions = [
        "Mengumpulkan data dari berbagai sumber",
        "Mengumpulkan dan Membersihkan Data",
        "Menganalisis Data",
        "Membuat Laporan dan Visualisasi",
        "Mengidentifikasi Kebutuhan Data",
        "Mengembangkan dan Menerapkan Model",
        "Mengintegrasikan Data",
        "Mengoptimalkan Proses",
        "Mengkomunikasikan Hasil",
        "Mengelola Data",
        "Membuat dashboard dan report untuk memantau kinerja bisnis",
        "Mengembangkan dan menerapkan sistem pengumpulan data",
        "Mengidentifikasi dan mengatasi masalah data",
        "Membuat rekomendasi untuk perbaikan proses bisnis",
        "Mengkolaborasi dengan tim lain untuk mengembangkan solusi bisnis",
       
    ]

    data = {
        "ID": [f"TICKET-{i}" for i in range(1100, 1000, -1)],
        "Tugas": np.random.choice(issue_descriptions, size=100),
        "Status": np.random.choice(["Open", "In Progress", "Closed"], size=100),
        "Priority": np.random.choice(["High", "Medium", "Low"], size=100),
        "Date Submitted": [
            datetime.date(2025, 1, 1) + datetime.timedelta(days=random.randint(0, 182))
            for _ in range(100)
        ],
    }
    df = pd.DataFrame(data)

   
    st.session_state.df = df



st.header("Tambahkan Tugas")

with st.form("add_ticket_form"):
    Tugas = st.text_area("New Task")
    priority = st.selectbox("Priority", ["High", "Medium", "Low"])
    submitted = st.form_submit_button("Submit")

if submitted:
    
    recent_ticket_number = int(max(st.session_state.df.ID).split("-")[1])
    today = datetime.datetime.now().strftime("%m-%d-%Y")
    df_new = pd.DataFrame(
        [
            {
                "ID": f"TICKET-{recent_ticket_number+1}",
                "Tugas": Tugas,
                "Status": "Open",
                "Priority": priority,

                "Date Submitted": today,
            }
        ]
    )

    st.write("Ticket submitted! Here are the ticket details:")
    st.dataframe(df_new, use_container_width=True, hide_index=True)
    st.session_state.df = pd.concat([df_new, st.session_state.df], axis=0)


st.header("Existing tickets")
st.write(f"Number of tickets: `{len(st.session_state.df)}`")

edited_df = st.data_editor(
    st.session_state.df,
    use_container_width=True,
    hide_index=True,
    column_config={
        "Status": st.column_config.SelectboxColumn(
            "Status",
            help="Ticket status",
            options=["Open", "In Progress", "Closed"],
            required=True,
        ),

        "Priority": st.column_config.SelectboxColumn(
            "Priority",
            help="Priority",
            options=["High", "Medium", "Low"],
            required=True,

    ),

    },

    
    disabled=["ID", "Date Submitted"],
)


st.header("Statistics")

col1, col2, col3 = st.columns(3)
num_open_tickets = len(st.session_state.df[st.session_state.df.Status == "Open"])
col1.metric(label="Number of open tickets", value=num_open_tickets, delta=10)
col2.metric(label="First response time (hours)", value=5.2, delta=-1.5)
col3.metric(label="Average resolution time (hours)", value=16, delta=2)

st.write("")
st.write("##### Ticket status per month")
status_plot = (
    alt.Chart(edited_df)
    .mark_bar()
    .encode(
        x="month(Date Submitted):O",
        y="count():Q",
        xOffset="Status:N",
        color="Status:N",
    )
    .configure_legend(
        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)
st.altair_chart(status_plot, use_container_width=True, theme="streamlit")

st.write("##### Current ticket priorities")
priority_plot = (
    alt.Chart(edited_df)
    .mark_arc()
    .encode(theta="count():Q", color="Priority:N")
    .properties(height=300)
    .configure_legend(

        orient="bottom", titleFontSize=14, labelFontSize=14, titlePadding=5
    )
)

st.altair_chart(priority_plot, use_container_width=True, theme="streamlit")