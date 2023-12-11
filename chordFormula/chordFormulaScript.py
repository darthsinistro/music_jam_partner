import csv

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            data.append(row)
    return data


#Let's read in the files
chord_path = 'chordFormula/chords.csv'
replace_path = 'chordFormula/replace.csv'

chord_data = read_csv_file(chord_path)
replace_data = read_csv_file(replace_path)

# Let's create a dictionary containing the notes and the ID to replace it with
replace_dict = {rep_row[1]:rep_row[2] for rep_row in replace_data[1:]}

#Let's replace each instance of the python formula with the appropriate index from the replace file

for formula_row in chord_data[1:]:   #Let's loop through each formula
    notes_list = formula_row[3].split('-')  # Turn each formula (from 3rd column) into a list
    modified_list = sorted([replace_dict.get(note,note) for note in notes_list])  # Replace each element and replace it
    formula_row[4] = '-'.join(modified_list) # Now save it back to the 4th column

# Write data to the CSV file, overwriting if it already exists
with open(chord_path, 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile)
    
    # Write each row
    for row in chord_data:
        csv_writer.writerow(row)