import pandas as pd
import matplotlib.pyplot as plt

# Paths to your files
user_interactions_path = 'D:/python script for metrices/user_interactions.csv'
errors_for_calc_final_path = 'D:/python script for metrices/errorsforcalcfinal.xlsx'

# Load DataFrames
user_interactions_df = pd.read_csv(user_interactions_path)
errors_for_calc_final_df = pd.read_excel(errors_for_calc_final_path)

# Diagnostic prints to verify initial data load
print("User Interactions - First few rows:")
print(user_interactions_df.head())
print("\nErrors for Calc Final - First few rows:")
print(errors_for_calc_final_df.head())

# Preprocessing: Lowercase and strip for consistency
user_interactions_df['Clicked Word'] = user_interactions_df['Clicked Word'].str.strip().str.lower()
user_interactions_df['Video Name'] = user_interactions_df['Video Name'].str.strip().str.lower()
errors_for_calc_final_df['Clicked Word'] = errors_for_calc_final_df['Clicked Word'].str.strip().str.lower()
errors_for_calc_final_df['Video Name'] = errors_for_calc_final_df['Video Name'].str.strip().str.lower()

# Merge DataFrames on 'Clicked Word' and 'Video Name'
merged_df = pd.merge(user_interactions_df, errors_for_calc_final_df, 
                     on=['Clicked Word', 'Video Name'], 
                     how='inner')

print("\nMerged DataFrame size:", merged_df.shape)

# Check if merged_df is not empty to proceed
if not merged_df.empty:
    # Create a list of all matching entries (if needed for further processing)
    user_error_list = list(merged_df[['User Name', 'Error type']].itertuples(index=False, name=None))
    print("\nFull User Error List:")
    for entry in user_error_list:
        print(entry)

    # Aggregate data based on 'Error type'
    error_type_counts = merged_df['Error type'].value_counts()

    # Plotting the aggregated data
    error_type_counts.plot(kind='bar', figsize=(12, 6))
    plt.title('Error Type Distribution Across All User Interactions')
    plt.xlabel('Error Type')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()
else:
    print("\nNo matching entries found across all user interactions.")
