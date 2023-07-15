import pandas as pd

# Read the Excel file
try:
    df = pd.read_excel('book1.xlsx')

    # Extract the data from specific rows
    timestamps = df.iloc[1::2, 0].reset_index(drop=True)
    text = df.iloc[::2, 0].reset_index(drop=True)

    # Create a new DataFrame with the extracted data
    new_df = pd.DataFrame({'Time': timestamps, 'Text': text})

    # Save the new DataFrame to a CSV file
    new_df.to_csv('output_file.csv', index=False)

except Exception as e:
    print(e)
    print('Error reading/writing file.')