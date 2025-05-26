import pandas as pd 
from io import BytesIO

def export_to_excel(workout_data: pd.DataFrame, sname='Workout Data'):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        workout_data.to_excel(writer, index=False, sheet_name=sname)
        output.seek(0)
    return output
