import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Provize pro IMPnet")

file1 = st.file_uploader("Faktury Vydané GRAWEB", type="xlsx")
file2 = st.file_uploader("Klienti IMP netu", type="xlsx")
file3 = st.file_uploader("Původní klienti GRAWEBu", type="xlsx")

if file1 and file2 and file3:
    # Read the Excel files
    f1 = pd.read_excel(file1)
    f2 = pd.read_excel(file2)
    f3 = pd.read_excel(file3)
    
    # Get all values from column A, convert to integer
    col_a_f2 = pd.to_numeric(f2.iloc[:, 0], errors='coerce').dropna().astype(int).tolist()
    col_a_f3 = pd.to_numeric(f3.iloc[:, 0], errors='coerce').dropna().astype(int).tolist()
    
    # Filter file1 using column D, convert to integer but keep index aligned
    col_d_f1 = pd.to_numeric(f1.iloc[:, 3], errors='coerce')
    filtered = f1[col_d_f1.isin(col_a_f2) & ~col_d_f1.isin(col_a_f3)]
    
    if len(filtered) > 0:
        st.write(f"Sample filtered data (first 5 rows):")
        st.dataframe(filtered)
    
    # Save to Excel in memory
    output = BytesIO()
    filtered.to_excel(output, index=False, engine='openpyxl')
    output.seek(0)  # move pointer to start of the file
    
    # Provide download button
    st.download_button(
        label="Download Filtered Excel",
        data=output,
        file_name="filtered.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    
    st.success(f"Filtered {len(filtered)} rows successfully!")
