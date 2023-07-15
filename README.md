# cv2 basic learning projects

idea
    1. make script to test if the user face is screen center or not
    2. make a script to draw landmarks on person body.
    3. make a script to calculate the angles between hip and head or hip and neck.


# projects requirements 

    1.opencv-python
    2.mediapipe


# project deatails

1. takes a video input draws a green box around the face and write center or not centered simple (change the threshold accrodingly )

    ![screenshot1](https://github.com/ZafeerMahmood/Cv2Learning/blob/main/screenshots/ss1.png)

2. draws landmark on person body and calculate if the back is straight or not then angles between (shoulder and hip)
    ![sreenshot2](https://github.com/ZafeerMahmood/Cv2Learning/blob/main/screenshots/ss2.png)

3. added a new Script to clean data copies for youtube transcipt to 

    ```py
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
    ```