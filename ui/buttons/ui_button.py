import streamlit as st
import pandas as pd


def button_upload():
    try:
            uploaded_file = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx"])
            if uploaded_file is not None:
                # Read file
                if uploaded_file.name.endswith("csv"):
                    df = pd.read_csv(uploaded_file)
                    
                    # df["dateofbirth"] = pd.to_datetime(df["dateofbirth"], format="%d%m%Y").dt.strftime("%Y-%m-%d")
                    # Handle date of birth (assuming ddmmyyyy format in CSV)
                #if "dateofbirth" in df.columns:
                       # df["dateofbirth"] = pd.to_datetime(df["dateofbirth"], format="%d%m%Y", errors="coerce").dt.strftime("%Y-%m-%d")

                # Convert numeric fields to string
                for col in ["pincode", "contactnumber", "aadhar","dateofbirth"]:
                        if col in df.columns:
                                df[col] = df[col].astype(str)
                    
            else:
                df = pd.read_excel(uploaded_file)
                
                st.dataframe(df)  # preview
    except:
            st.markdown("upload file")

    if st.button("Upload to Database"):
            st.session_state['records'] = df.to_dict(orient="records")