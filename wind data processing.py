import pandas as pd
import glob

# Function to calculate power based on wind speed
def calculate_power(wind_speed):
    if wind_speed is None or wind_speed < 5:
        return 0
    elif 5 <= wind_speed < 30:
        # Linear increase from 0 watts at 5 m/s to 200 watts at 30 m/s
        return (200 / 25) * (wind_speed - 5)  # (200 - 0) / (30 - 5)
    elif 30 <= wind_speed < 40:
        # Linear decrease from 200 watts at 30 m/s to 100 watts at 40 m/s
        return 200 - (100 / 10) * (wind_speed - 30)  # (200 - 100) / (40 - 30)
    else:  # wind_speed >= 40
        return 0

# Function to read the wind speed data from a single text file
def read_wind_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    # Skip the first two lines and process the rest
    data = []
    for line in lines[2:]:  # Skip the first two header lines
        parts = line.split()  # Split by whitespace
        
        # Extract relevant data
        try:
            julian_day = int(parts[0])  # Julian day
            interval_marker = int(parts[1])  # Interval marker
            temperature = float(parts[2])  # Temperature
            pressure = float(parts[3])  # Pressure
            wind_speed = float(parts[4])  # Wind speed
            wind_direction = float(parts[5])  # Wind direction
            humidity = float(parts[6])  # Humidity
            vertical_temp_diff = float(parts[7])  # Vertical temperature difference
            
            # Handle missing data
            if wind_speed == 444.0:
                wind_speed = None  # Treat missing data as None

            data.append({
                'Julian Day': julian_day,
                'Interval Marker': interval_marker,
                'Temperature': temperature,
                'Pressure': pressure,
                'Wind Speed': wind_speed,
                'Wind Direction': wind_direction,
                'Humidity': humidity,
                'Vertical Temp Diff': vertical_temp_diff
            })
        except (IndexError, ValueError) as e:
            print(f"Error processing line: {line} - {e}")  # Handle potential errors

    return data

# Path to your text files
file_pattern = r"C:\Users\seth\OneDrive - University of Cambridge\IIA\exa\wind data\*-r-.txt"  # Adjust this to your actual file path

# List to hold all data
all_data = []

# Read all matching text files
for file_path in glob.glob(file_pattern):
    wind_data = read_wind_data(file_path)
    all_data.extend(wind_data)

# Create a DataFrame from the collected data
data_df = pd.DataFrame(all_data)

# Now apply the power calculation, skipping rows with missing wind speed
data_df['Power Output'] = data_df['Wind Speed'].apply(calculate_power)

# Save the output to a new CSV file
data_df.to_csv('wind_power_output.csv', index=False)

print("Wind speed data processed and power output calculated.")
