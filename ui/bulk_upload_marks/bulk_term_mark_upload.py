import streamlit as st
import pandas as pd
from ui.session import initialize_session_state

initialize_session_state()

def bulk_term_mark():
        
        st.title("Bulk Upload Term Marks")

        try:
            uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
            if uploaded_file is not None:
                # Read file
                if uploaded_file.name.endswith("csv"):
                    df = pd.read_csv(uploaded_file)
            else:
                df = pd.read_excel(uploaded_file)
                st.dataframe(df)  # preview
        except:
            st.markdown("upload file")

        if st.button("Upload to Database"):
            st.session_state['records'] = df.to_dict(orient="records")
  