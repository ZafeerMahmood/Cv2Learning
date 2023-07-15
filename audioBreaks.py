import os
import csv
from datetime import datetime
import wave

def time_to_seconds(time_str):
    try:
        time_components = time_str.split(':')
        minutes = int(time_components[0])
        seconds = int(time_components[1])
        total_seconds = minutes * 60 + seconds
        return total_seconds
    except ValueError:
        return None


def break_wav(csv_file, wav_file):
    try:
        # Get the absolute paths to the files
        csv_path = os.path.abspath(csv_file)
        wav_path = os.path.abspath(wav_file)
    except Exception as e:
        print(e)
        print('Error reading file paths.')

    # Read the CSV file
    try:
        with open(csv_path, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Skip the header row if present

            # Open the WAV file
            with wave.open(wav_path, 'rb') as wav:
                # Get the frame rate and total frames
                frame_rate = wav.getframerate()
                total_frames = wav.getnframes()

                # Initialize the previous end time as the start time of the audio
                prev_end_time = 0

                # Iterate through each row in the CSV
                for row in reader:
                    text = row[1]

                    end_time = time_to_seconds(row[0])  
                    print (end_time,'endtime')# Convert end time to seconds
                    if end_time is None:
                        print(f"Skipping invalid time value for row: {text}")
                        continue

                    # Calculate the start and end frame indices based on the previous end time and current end time
                    start_frame = int(frame_rate * prev_end_time)
                    end_frame = int(frame_rate * end_time)

                    # Adjust the frame indices to fit within the valid range
                    start_frame = max(0, min(start_frame, total_frames))
                    end_frame = max(0, min(end_frame, total_frames))

                    # Set the frame range for the extracted audio
                    frames_to_extract = end_frame - start_frame

                    # Seek to the start frame
                    wav.setpos(start_frame)

                    # Read the frames for the extracted audio
                    frames = wav.readframes(frames_to_extract)

                    # Create an output WAV file for the split audio
                    output_file = f"wav/output_{text}.wav"
                    with wave.open(output_file, 'wb') as split_wav:
                        split_wav.setparams(wav.getparams())
                        split_wav.writeframes(frames)
                    
                    print(f"Split audio exported for row: {text}")

                    # Update the previous end time with the current end time
                    prev_end_time = end_time

    except Exception as e:
        print(e)
        print('Error reading/writing CSV/WAV file.')

# Usage example
csv_file = 'out.csv'
wav_file = 'input_file.wav'
break_wav(csv_file, wav_file)
