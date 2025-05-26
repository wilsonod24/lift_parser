import pandas as pd
import streamlit as st 
import parser
import models
from datetime import date
from exporter import export_to_excel as export

def main():
    # Have the user upload the file
    file = st.file_uploader('Upload workout log', type=['txt','csv'])
    if file is not None:
        file_name = file.name
    else:
        file_name = None

    # Convert the file to dataframe
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame()
        st.write("Error", file)

    converted_dict = []   # To store the converted Data

    current_date = date.today()
    # Convert each line of the current csv
    for idx, row in df.iterrows():
        if parser.is_date(row.iloc[0]) is not None:
            current_date = parser.is_date(row.iloc[0])
        if parser.is_exercise_line(row.iloc[0]) and current_date is not None:
            new_rows = parser.parse_exercise(str(row.iloc[0]),date=current_date) #TODO: set date

            for row in new_rows:
                converted_dict.append({
                    'date':row.date,
                    'exercise':row.exercise,
                    'set_number': row.set_number,
                    'reps': row.reps,
                    'weight_lbs': row.weight_lbs,
                    'notes': row.notes,
                    })

    # Convert the dict into a dataframe
    converted_df = pd.DataFrame(converted_dict)
    st.dataframe(converted_df)
    if not converted_df.empty:
        if file_name is not None:
            sheet_name = file_name
        else:
            sheet_name = 'Workout Data'
        excel_data = export(converted_df, sname=sheet_name)
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name="workout_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )


main()    