import csv
datafile = open('satire_tone_data_run_4.csv', 'r')
datareader = csv.reader(datafile, delimiter=',')
data = []
for row in datareader:
    data.append(row)    
#print(data[0])
#print (data)

newfeatures = [['C', 'D', 'F', 'H', 'N', 'P', 'R', 'S']]
with open('satireThemes', 'r') as fp:
    for line in fp:
        insfeat = []
        #print(line)
        for thm in newfeatures[0]:
            if thm in line:
                insfeat.append(1)
            else:
                insfeat.append(0)
        newfeatures.append(insfeat)
        #print(insfeat)

with open('fakeNewsThemes', 'r') as fp:
    for line in fp:
        insfeat = []
        #print(line)
        for thm in newfeatures[0]:
            if thm in line:
                insfeat.append(1)
            else:
                insfeat.append(0)
        newfeatures.append(insfeat)
        #print(insfeat)

new_data = []
for i in range(len(newfeatures)):
    new_ins = data[i][:-1]+newfeatures[i]+[data[i][-1]]
    new_data.append(new_ins)

print(len(newfeatures))
with open('satire_tone_data_them.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(new_data)
