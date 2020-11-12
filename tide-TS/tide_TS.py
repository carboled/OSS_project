#!/usr/bin/python

firstline = 4

time = []
tideState = []
moonState = []
date = []
elevation = []
repeated = False
#year = 2018
prev_element = ''
ji = 0
with open('Tidal_data.txt') as xtide_file:
    for lineNum, line in enumerate(xtide_file, 1):
        ji += 1
        #print("Line: %i, Lenght: %i" % (ji, len(line)))
        temp = line.strip().split()
        if lineNum < firstline and temp[0] in ['January', 'February', 'March', 'April',  'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']:
            year = int(temp[1])
            #print(year)
        if lineNum > firstline and len(line) == 77:
            #a = type(temp[0][0])
            i = 0
            spaces = 0
            is_set = False
            splitList = []
            for c in range(len(line)):
                if line[c] != ' ' and not is_set:
                    for i in range(spaces // 10):
                        splitList.append('H9999')
                        splitList.append('9999')
                    is_set = True
                    i = c
                elif line[c] == ' ' and is_set:
                    splitList.append(line[i:c])
                    is_set = False
                    spaces = 0
                elif line[c] == ' ':
                    spaces += 1
                elif c == len(line) - 1 and is_set:
                    splitList.append(line[i:c])

            moon = ''
            if splitList[0][0].isdigit() or splitList[0] in ['LQtr', 'New', 'FQtr', 'Full']:
                if splitList[0][0].isdigit():
                    repeat_Check = splitList[-1] + '-%i' % year
                else:
                    repeat_Check = splitList[-1] + '-%i' % year

                # Check if repeated data
                if len(date) > 1 and repeat_Check == date[-1]:
                    repeated = True
                else:
                    repeated = False
                    for element in splitList:
                        if element == '01-01':# and prev_element == '12-31':
                            pass
                        if element[0].isdigit():
                            if element == '01-01' and prev_element == '12-31':
                                year += 1
                            date.append(element + '-%i' % year)
                            time.append([])
                            elevation.append([])
                            tideState.append([])
                            moonState.append(moon)
                            moon = ''
                            prev_element = element
                        else:
                            moon = element
            # if value lines
            elif splitList[0][0] in ['H', 'L'] and not repeated:
                iter = 0
                for element in splitList:
                    if element[0] in ['H', 'L']:
                        if element[1:] != '9999':
                            time[iter - 7].append(element[1:3] + ':' + element[3:])
                            tideState[iter - 7].append(element[0])
                        
                    else:
                        if element != '9999':
                            elevation[iter - 7].append(element)
                        iter += 1
print('Input file has been read...')
import csv
print('Writing time series to file TS-%i.csv ...'% year)
with open('TS-%i.csv' % year, 'w') as outputfile:
    outputwriter = csv.writer(outputfile, delimiter=';', quoting=csv.QUOTE_MINIMAL)
    outputwriter.writerow(['Date', 'Time', 'Elevation', 'tideState'])
    for d in range(len(date)):
            for t1 in range(len(time[d])):
                outputwriter.writerow([date[d], time[d][t1], elevation[d][t1], tideState[d][t1]])
print('Time series have been generated.')
