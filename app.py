import streamlit as st
import pandas as pd
import os
from io import BytesIO

#Set up our app
st.set_page_config(page_title="📊 Smart Data Processor", layout="wide")
st.title("🛠️ Data Refinery")
st.write("Easily convert, clean, and visualize your CSV and Excel files for better insights. 📈")

uploaded_files = st.file_uploader("📂 Drag & drop or select your CSV/Excel files:", type=["csv","xlsx"], accept_multiple_files=True )

if uploaded_files:
    for file in uploaded_files:
        file_extension = os.path.splitext(file.name)[-1].lower()

        if file_extension == ".csv":
            df = pd.read_csv(file)
        elif file_extension == ".xlsx":
            df = pd.read_excel(file)
        else:
            st.error("⚠️ Unsupported format detected! Please provide a valid CSV or Excel file.")
            continue
        #Display info about the file
        st.write(f"📝 Filename: {file.name}")
        st.write(f"📏 Size:  {file.size/1024}")

        #Show five rows of our dataframe
        st.write("👀 Data Snapshot")
        st.dataframe(df.head())

        #Options for Data Cleaning
        st.subheader("🛠️ Clean & Optimize Data")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1,col2 = st.columns(2)

            with col1:
                if st.button(f"🗑️ Deduplicate {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.success("✅ Duplicate entries successfully removed!")
            with col2:
                if st.button(f"📉 Fill Missing Data in {file.name}"):
                    numeric_cols = df.select_dtypes(include=['number']).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.success("✅ Missing values filled using column-wise mean.") 
        st.subheader("🎯 Choose Columns for Processing")
        columns = st.multiselect(f"Choose Columns for {file.name}", df.columns, default=df.columns)
        df = df[columns]
        #Create some visualisation
        st.subheader("📈 Visualize Your Data")
        if st.checkbox(f"📊 Enable Graphs for {file.name}"):
            st.bar_chart(df.select_dtypes(include='number').iloc[:,:2])

        #Covert the file CSV to Excel
        st.subheader("🔄 Convert File Format")
        conversion_type = st.radio(f"🛠️ Choose Output Format for {file.name} to: ",["CSV", "Excel"], key=file.name)
        if st.button(f"Convert {file.name}"):
            buffer = BytesIO()
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)  
                file_name =file.name.replace(file_extension,".csv") 
                mime_type = "text/csv"
            elif conversion_type   == "Excel":
                df.to_excel(buffer, index=False)  
                file_name = file.name.replace(file_extension,".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  
            buffer.seek(0)

            #Download Button
            st.download_button(
                label=f"📥 Download {file_name} as {conversion_type}",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

            st.success("🎉 Processing complete!")





                