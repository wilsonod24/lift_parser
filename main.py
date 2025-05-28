import pandas as pd
import streamlit as st 
import parser
from datetime import date
import plotly.express as px
from exporter import export_to_excel as export

def convert_dataframe(file):
    """Takes in a file (CSV or TXT) and returns the workout data as a dataframe"""

    # Convert the file to dataframe
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.DataFrame()
        st.write("Error", file)

    converted_dict = []   # To store the converted Data

    current_date = date.today()     # Set default date

    # Convert each line of the current csv
    for idx, row in df.iterrows():
        if parser.is_date(row.iloc[0]) is not None:
            
            # Change the current date based on the current line
            current_date = parser.is_date(row.iloc[0])  

        if parser.is_exercise_line(row.iloc[0]) and current_date is not None:

            # Parse the exercise line into a list of sets
            new_rows = parser.parse_exercise(str(row.iloc[0]),date=current_date)

            # Add the Exercise sets to the dictionary of sets
            for row in new_rows:
                converted_dict.append({
                    'date':row.date,
                    'exercise':row.exercise,
                    'set_number': row.set_number,
                    'reps': row.reps,
                    'weight_lbs': row.weight_lbs,
                    'notes': row.notes,
                    })

    # Convert the dict into a dataframe and return it
    return pd.DataFrame(converted_dict)

def calculate_1rm(reps:float, weight_lbs: float):
    """Calculates the one rep max based on weight in pounds and reps performed"""
    return weight_lbs / (1.0278 - 0.0278 * reps)

def plot_interactive(df: pd.DataFrame):
    """Plots the interactive line plot based on the dataframe passed in"""

    # Clean inputs
    df['reps'] = pd.to_numeric(df['reps'], errors='coerce')
    df['weight_lbs'] = pd.to_numeric(df['weight_lbs'], errors='coerce')
    df = df.dropna(subset=['reps', 'weight_lbs'])

    # drop sets without weights input
    df = df[(df['weight_lbs'] != 0) & (df['exercise'] != 'dips')]

    # Group each exercise by date and exercise
    df = df.groupby(['date', 'exercise'], as_index=False).agg({'reps': 'max', 'weight_lbs': 'max'})

    # Add 1rm column
    df['one_rep_max'] = df.apply(lambda row: calculate_1rm(row['reps'], row['weight_lbs']), axis=1)

    # Create the plot in plotly express
    fig = px.line(df, x='date', y='one_rep_max',color='exercise',markers=True,title='one rep max progression by exercise'.title())

    # Plot the data to the streamlit front end
    st.plotly_chart(fig)

def main():
    # Have the user upload the file
    file = st.file_uploader('Upload workout log: see sample below for formatting', type=['txt','csv'])

    # Sample to show formatting
    st.text('Example formatting for parsing:'.title())  
    st.dataframe(pd.read_csv('push_data.txt').head())   
        
    # Convert the dataframe
    converted_df = convert_dataframe(file)

    required_cols = ['date', 'reps', 'weight_lbs']

    all_exist = all(col in converted_df.columns for col in required_cols)
    if all_exist:
        # Plot the data
        plot_interactive(converted_df)

    # Display the converted DF
    st.dataframe(converted_df)

    # Allow user to download converted DF as xlsx file
    if not converted_df.empty:


        sheet_name = 'Workout Excel Data'
        excel_data = export(converted_df, sname=sheet_name)

        # Download button for the user to export the data
        st.download_button(
            label="Download Excel file",
            data=excel_data,
            file_name="workout_data.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

main()    