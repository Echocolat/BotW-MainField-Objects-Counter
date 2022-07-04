from collections import Counter
import oead
import json
import dictdiffer

indexLetters = ["A-","B-","C-","D-","E-","F-","G-","H-","I-","J-"]
indexNumbers = ["1","2","3","4","5","6","7","8"]
allObjects = []

def takeAllDataOneFile():
    allData = {}
    for let in indexLetters:
        for numb in indexNumbers:
            dyn = '_Dynamic.smubin'
            sta = '_Static.smubin'
            for i in [dyn,sta]:
                file = 'Map Units\\' + let + numb + '\\' + let + numb + i
                with open(file,'rb') as f:
                    allData[let + numb + i] = oead.byml.from_binary(oead.yaz0.decompress(f.read()))['Objs']
    return allData

def takeAllDataComparison(folder):
    allData = {}
    for let in indexLetters:
        for numb in indexNumbers:
            dyn = '_Dynamic.smubin'
            sta = '_Static.smubin'
            for i in [dyn,sta]:
                file = 'Comparison\\' + folder + '\\' + let + numb + '\\' + let + numb + i
                with open(file,'rb') as f:
                    allData[let + numb + i] = oead.byml.from_binary(oead.yaz0.decompress(f.read()))['Objs']
    return allData

def oneMapUnit(data):
    for object in data:
        allObjects.append(object['UnitConfigName'])

def allMapUnits(bigData):
    for mapUnit in bigData:
        oneMapUnit(bigData[mapUnit])

def oneGameAnalysis(allObjects):
    allMapUnits(takeAllDataOneFile())
    allObjects = Counter(allObjects)
    allObjectsFinal = {k: v for k, v in sorted(allObjects.items(), key=lambda item: item[1], reverse = True)}
    with open('AllObjects.json','w') as f:
        f.write(json.dumps(allObjectsFinal, indent = 4))
    totalObjs = 0
    for i in allObjectsFinal:
        totalObjs = totalObjs + allObjectsFinal[i]
    print('Total number of objects in MainField :',totalObjs)

def comparison():
    finalString = {}
    allData1 = takeAllDataComparison('Map Units 1')
    allData2 = takeAllDataComparison('Map Units 2')
    allObjects1, allObjects2 = [], []
    for mapUnit in allData1:
        for object in allData1[mapUnit]:
            allObjects1.append(object['UnitConfigName'])
    for mapUnit in allData2:
        for object in allData2[mapUnit]:
            allObjects2.append(object['UnitConfigName'])
    allObjects1 = Counter(allObjects1)
    allObjects2 = Counter(allObjects2)
    allObjectsFinal1 = {k: v for k, v in sorted(allObjects1.items(), key = lambda item: item[1], reverse = True)}
    allObjectsFinal2 = {k: v for k, v in sorted(allObjects2.items(), key = lambda item: item[1], reverse = True)}
    for diff in list(dictdiffer.diff(allObjectsFinal1,allObjectsFinal2)):
        if diff[0] == 'remove':
            for i in range(len(diff[2])):
                finalString[diff[2][i][0]] = f'Found {diff[2][i][0]} in first folder and not in the second one, {diff[2][i][1]} of them.'
        elif diff[0] == 'add':
            for i in range(len(diff[2])):
                finalString[diff[2][i][0]] = f'Found {diff[2][i][0]} in second folder and not in the first one, {diff[2][i][1]} of them.'
        elif diff[0] == 'change':
            finalString[diff[1]] = f'Found {diff[1]} in both folders. {diff[2][0]} of them in the first, {diff[2][1]} of them in the second.'
    with open('comparison.json','w') as f:
        f.write(json.dumps(finalString, indent = 4))
            

def main():
    if input('Do you want to do a one folder analysis ? Enter y if it\'s the case, or anything else if it\'s not : ') == "y":
        oneGameAnalysis(allObjects)
    elif input('Do you want to do a comparison between two folders ? Enter y if yes, anything else if no : ') == 'y':
        comparison()
    input('Press Enter to exit...')

if __name__ == "__main__":
  main()