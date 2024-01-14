# Gloppiness code 
# Gloppiness of Personal Care Products
# Shijian Wu
# 1st version: 11-2023
# 2nd version: 01-2024

# Import packages
import cv2 as cv
import numpy as np
import pandas as pd
#import Image from PIL
from PIL import Image
from matplotlib import pyplot as plt 
from matplotlib.lines import Line2D
from scipy.signal import savgol_filter 
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)
import os
import cv2


# This function select the region of interest (ROI)
def select_roi(event, x, y, flags, param):
    global refPt, cropping, frame

    if event == cv.EVENT_LBUTTONDOWN:
        refPt = [(x, y)]
        cropping = True
    elif event == cv.EVENT_LBUTTONUP:
        refPt.append((x, y))
        cropping = False

        # Draw a rectangle around the region of interest
        cv.rectangle(frame, refPt[0], refPt[1], (255), 2)
        cv.imshow("frame", frame)


# Directory containing your input files
input_directory = 'Videos/demo_videos'
output_directory = 'Results/raw_diameter'  # This can be the same as the input directory if desired

# Get a list of all .avi files in the directory
all_files = os.listdir(input_directory)
avi_files = [f for f in all_files if f.endswith('.avi')]


# Display all .avi files and ask the user to select which to process
print("Available videos:")
for idx, file in enumerate(avi_files, 1):
    print(f"{idx}. {file}")

# Ask the user for their choice
selected_indices = input("Enter the numbers of the videos to process (separated by space): ")
selected_indices = [int(i) for i in selected_indices.split()]

# Filter the list of files to only include the selected ones
selected_files = [avi_files[i - 1] for i in selected_indices if 1 <= i <= len(avi_files)]



for file_name in selected_files:
    
    # Global variables
    refPt = []
    cropping = False
    
    # Construct full file path
    input_path = os.path.join(input_directory, file_name)

    # Construct output path (change .txt to .csv)
    output_path = os.path.join(output_directory, os.path.splitext(file_name)[0] + '.csv')

    # Open video using OpenCV (assuming you want to process it in some way)
    cap = cv2.VideoCapture(input_path)
    ret, frame = cap.read()
    #  frame = np.rot90(frame)
    clone = frame.copy()
    cv.namedWindow("frame")
    cv.setMouseCallback("frame", select_roi)
    
    while True:
        cv.imshow("frame", frame)
        key = cv.waitKey(1) & 0xFF

        # If the 'r' key is pressed, reset the cropping region
        if key == ord("r"):
            frame = clone.copy()

        # If the 'c' key is pressed, break from the loop to process the ROI
        elif key == ord("c"):
            break

    cv.destroyAllWindows()


    # Initialize an empty list to store the flattened image data
    # data = []
    filament_diameter = []
    if len(refPt) == 2:
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            roi = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]    
            roi = np.rot90(roi)

            # Apply Canny edge detection to the ROI
            edges = cv2.Canny(roi, 10, 100)

            ###############################################
            rows, cols = len(edges), len(edges[0])
            left_edges, right_edges = [0]*rows, [0]*rows

            for i in range(0, rows, 1):
                if np.all(edges[i] == 0):
                    left_edges[i] = 0

                for j in range(cols):
                    if edges[i][j] == 255:
                        left_edges[i] = j
                        break

            for i in range(0, rows, 1):
                if np.all(edges[i] == 0):
                    right_edges[i] = 0
                for j in range(cols-1, -1, -1):
                    if edges[i][j] == 255:
                        right_edges[i] = j
                        break

            filament_diameter.append(np.subtract(right_edges, left_edges))
            ###################################################################       
            cv2.imshow("Edges in ROI", edges)
            cv2.imshow("Video", frame)

            key = cv2.waitKey(30) & 0xFF
            if key == 27:  # ESC key
                break

    cap.release()
    cv2.destroyAllWindows()

    df_filament_diameter = pd.DataFrame(filament_diameter).T
    df_filament_diameter.shape
    df_filament_diameter.to_csv(output_path, index=False)
    



# function to trim trailing zeros
def trim_trailing_zeros(series):
    for i in reversed(range(len(series))):
        if series.iat[i] != 0:   # !=
            return series.iloc[:i+1]
    return pd.Series(dtype='float64')

# Function to remove last n non-NaN values
def remove_last_n(df, n):
    for col in df.columns:
        # Get non-NA indices
        non_na_indices = df[col].dropna().index
        
        # If there are less than 'n' non-NAs, continue
        if len(non_na_indices) < n:
            continue

        # Get last 'n' non-NA indices
        last_n_indices = non_na_indices[-n:]

        # Set last 'n' non-NAs to NaN
        df.loc[last_n_indices, col] = np.nan

    return df

def find_local_peak(series, threshold):
    for i in range(1, len(series)-1):  # Skip first and last element
        if series[i] > threshold and series[i-1] < series[i] > series[i+1]:
            return series.index[i]
    return np.nan  # Return NaN if no peak is found




# Directory containing your CSV files
input_directory = 'Results/raw_diameter'
output_directory = 'Results/rupture_time'

# Get a list of all .csv files in the directory
all_files = os.listdir(input_directory)
csv_files = [f for f in all_files if f.endswith('.csv')]

# Display all .csv files and ask the user to select which to process
print("Available CSV files:")
for idx, file in enumerate(csv_files, 1):
    print(f"{idx}. {file}")

# Ask the user for their choice
selected_indices = input("Enter the numbers of the CSV files to process (separated by space): ")
selected_indices = [int(i) for i in selected_indices.split()]

# Filter the list of files to only include the selected ones
selected_files = [csv_files[i - 1] for i in selected_indices if 1 <= i <= len(csv_files)]

# Initialize an empty list to hold individual DataFrames
dfs = []

# Loop through and read each selected CSV into a DataFrame
for file_name in selected_files:
    # Existing processing code for each file...
    
    # Construct full file path
    input_path = os.path.join(input_directory, file_name)

    # Construct output path (change .txt to .csv)
    output_path = os.path.join(output_directory, os.path.splitext(file_name)[0] + '.csv')
    
    file_path = os.path.join(input_directory, file_name)
    df1 = pd.read_csv(file_path)
    print(type(df1))
    ######################################
    df2 = df1.apply(trim_trailing_zeros)
    df2 = df2.rolling(window=5, min_periods=1).mean()
    # Remove the last 2 non-NAs (Replace 2 with 100 for your case)
    df3 = remove_last_n(df2, 100)
    df3 = df2
    min_values = df3.min()
    df_min_values = min_values.to_frame()
    df_smoothed_min_values = df_min_values.rolling(window=3).mean()

    # Calculate the derivative (difference)
    df_diff = abs(df_smoothed_min_values.diff())
    # Find first local peak larger than 3 for all columns
    peak_indices = df_diff.apply(find_local_peak, args=(0.2,), axis=0)
    
    rupture_time = (df1.shape[1]-np.int64(peak_indices))/200
    dfs.append({"File Name": file_name, "Value": rupture_time[0]})

    print("Rupture Frame is:", (df1.shape[1]-np.int64(peak_indices))/200)

# # Create a DataFrame from the results
# dfs.append({"File Name": file_name, "Avg.": pd.DataFrame(dfs).mean()})
results_df = pd.DataFrame(dfs)

# Save the results to a new CSV file
results_df.to_csv(output_path, index=False)