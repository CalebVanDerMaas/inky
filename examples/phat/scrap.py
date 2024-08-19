# Appending to a file
with open('example.txt', 'a') as file:
    file.write("This line will be added to the end of the file.\n")

# Open the file in read mode
with open('example.txt', 'r') as file:
    lines = file.readlines()  # Read all lines into a list
    last_30_lines = lines[-30:]  # Slice the last 30 lines

# Now you can work with last_30_lines
for line in last_30_lines:
    print(line.strip())  # Print each line without the trailing newline