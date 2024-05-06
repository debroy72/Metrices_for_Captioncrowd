import pandas as pd

# Load the CSV file
df = pd.read_csv('D:/python script for metrices/anonymous_user_interactions.csv')

# Extract the numeric part of the 'User Name' and convert it into an integer for sorting
df['User Number'] = df['User Name'].str.extract('(\d+)').astype(int)

# Sort the DataFrame based on this numeric value
df_sorted = df.sort_values('User Number')

# Remove the temporary 'User Number' column used for sorting
df_sorted.drop('User Number', axis=1, inplace=True)

# Save the sorted DataFrame back to a CSV file
df_sorted.to_csv('sorted_file.csv', index=False)
