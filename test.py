# Open the file in read mode ('r')
with open('conf.txt', 'r') as file:
    # Read each line in the file and store it in a list
    paths = [line.strip().split('=')[1].strip() for line in file]

# Now 'paths' is a list of paths
image_folder_path = paths[0]
data_folder_path = paths[1]
config_folder_path = paths[2]

# Print the paths
print(image_folder_path)
print(data_folder_path)
print(config_folder_path)