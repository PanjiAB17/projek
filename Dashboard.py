import streamlit as st
import pandas as pd
import numpy as np

pages = {
   "Dashboard": [

        st.Page("Home.py", title="Home"),
        st.Page("Report.py", title="Report"),
        st.Page("Activity.py", title="Activity"),
        st.Page("Notification.py", title="Notification"),
        st.Page("Setting.py", title="Setting"),
        
    ],
    
}

pg = st.navigation(pages)
pg.run()
