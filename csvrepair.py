from pprint import pprint
import csv

with open('newsarff2.arff.csv', 'r') as fp:
	full_data = []
	for line in fp:
		cols_data = ['', '']

		line = line.rstrip('\n\r').split(',')
		# line = line.split(',')
		text = ''
		for i in range(len(line)-1):
			text += line[i]
		cols_data[0] = text
		cols_data[1] = line[-1]
		full_data.append(cols_data)
	# lines = fp.readlines()

print(len(full_data), len(full_data[0]))

with open('satire_fake_text.csv', 'w') as outcsv:
	writer = csv.writer(outcsv)
	writer.writerows(full_data)