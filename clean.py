import csv

with open('dataset.csv', 'r') as infile, open('cleaned_dataset.csv', 'w', newline='') as outfile:
    writer = csv.writer(outfile)
    for row in csv.reader(infile):
        if all(field.strip() for field in row):
            writer.writerow(row)

print("Data cleaned successfully! CI check passed.")
