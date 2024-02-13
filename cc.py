import pandas as pd
import subprocess

df = pd.read_csv('data_configuration.csv', delimiter=';')

# Filter rows where NameConf is "conf1"
filtered_df = df[df['NameConf'] == 'conf1']

# Extract the PathPupilLabs column values (without index)
path_pupil_labs = filtered_df['PathPupilLabs'].values.item()

# Print the result
print(path_pupil_labs)


try:
    subprocess.Popen([path_pupil_labs])
    print(f"Pupil capture launched from path: {path_pupil_labs}")
except FileNotFoundError:
    print("Invalid path to Pupil Labs executable")