import streamlit as st
import pandas as pd
from io import BytesIO

st.title("Filtrace Graweb")

file1 = st.file_uploader("FAV", type="xlsx")
file2 = st.file_uploader("aktivní klienti", type="xlsx")
file3 = st.file_uploader("moji_klienti", type="xlsx")

if file1 and file2 and file3:
    # Read the Excel files
    f1 = pd.read_excel(file1)
    f2 = pd.read_excel(file2)
    f3 = pd.read_excel(file3)
    
    # Get all values from column A (0-indexed)
    col_a_f2 = f2.iloc[:, 0].dropna().tolist()
    col_a_f3 = f3.iloc[:, 0].dropna().tolist()
    
    # Filter file1 using column D (3-indexed)
    filtered = f1[f1.iloc[:, 3].isin(col_a_f2) & ~f1.iloc[:, 3].isin(col_a_f3)]
    
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
