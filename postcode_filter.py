# Filter postcodes to only have rows where type=pobox or blank

import csv

input_file = "australian_postcodes.csv"  # Change to your CSV filename
output_file = "po_box_only.csv"

# Open the input CSV and create an output CSV with filtered rows
with open(input_file, mode="r", newline="", encoding="utf-8") as infile, \
     open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
    
    reader = csv.DictReader(infile)
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    
    writer.writeheader()  # Write header to output file
    
    for row in reader:
        if row["type"] == "Post Office Boxes" or row["type"].strip() == "":
            writer.writerow(row)  # Write row if it meets the condition

print(f"Filtered rows saved to {output_file}")
