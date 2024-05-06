import pandas as pd

# Adjust the path as needed
file_path = r'D:\python script for metrices\total errors in each videos.xlsx'
try:
    df = pd.read_excel(file_path)
    print(df.head())
except Exception as e:
    print("Error:", e)
