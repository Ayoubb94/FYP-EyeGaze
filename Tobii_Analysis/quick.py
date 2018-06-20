import csv

with open('data','r') as f_in:
    with open('data_out', 'w') as f_out:
        writer = csv.writer(f_out, delimiter=' ', lineterminator='\n')
        reader = csv.reader(f_in, delimiter=' ')

        result = []
        # read headers
        row = next(reader)
        # add new header to list of headers
        row.append('Col5')
        result.append(row)

        for row in reader:
            # add new column values
            row.append(row[0])
            result.append(row)

        writer.writerows(result)

data_out