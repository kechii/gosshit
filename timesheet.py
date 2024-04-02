import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO

def main():
    st.title("Timesheet App")
    
    # Timesheet form
    st.header("Timesheet Form")
    name = st.text_input("Name")
    time_in = st.time_input("Time In")
    time_out = st.time_input("Time Out")
    
    if st.button("Submit"):
        # Save data to a DataFrame
        data = {
            "Name": [name],
            "Time In": [time_in],
            "Time Out": [time_out],
            "Date": [datetime.now().date()]
        }
        df = pd.DataFrame(data)
        
        # Append data to existing DataFrame if it exists, else create a new one
        if 'timesheet_data' not in st.session_state:
            st.session_state.timesheet_data = df
        else:
            st.session_state.timesheet_data = pd.concat([st.session_state.timesheet_data, df], ignore_index=True)
        
        st.success("Data submitted successfully!")
    
    # Display report
    if 'timesheet_data' in st.session_state:
        st.header("Timesheet Report")
        st.table(st.session_state.timesheet_data)
        
        # Export report to Excel
        if st.button("Export Report to Excel"):
            excel_file = BytesIO()
            writer = pd.ExcelWriter(excel_file, engine="openpyxl")
            st.session_state.timesheet_data.to_excel(writer, index=False, sheet_name="Timesheet")
            writer.save()
            excel_file.seek(0)
            st.download_button(
                label="Download Excel Report",
                data=excel_file,
                file_name="timesheet_report.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

if __name__ == "__main__":
    main()