from collections import Counter
import oead
import json

indexLetters = ["A-","B-","C-","D-","E-","F-","G-","H-","I-","J-"]
indexNumbers = ["1","2","3","4","5","6","7","8"]
allObjects = []

def takeAllData():
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

def oneMapUnit(data):
    for object in data:
        allObjects.append(object['UnitConfigName'])

def allMapUnits(bigData):
    for mapUnit in bigData:
        oneMapUnit(bigData[mapUnit])

def oneGameAnalysis(allObjects):
    allMapUnits(takeAllData())
    allObjects = Counter(allObjects)
    allObjectsFinal = {k: v for k, v in sorted(allObjects.items(), key=lambda item: item[1], reverse = True)}
    with open('AllObjects.json','w') as f:
        f.write(json.dumps(allObjectsFinal, indent = 4))
    totalObjs = 0
    for i in allObjectsFinal:
        totalObjs = totalObjs + allObjectsFinal[i]
    print('Total number of objects in MainField :',totalObjs)

def main():
    if input('Do you want to do a one folder analysis ? Enter y if it\'s the case, or anything else if it\'s not : ') == "y":
        oneGameAnalysis(allObjects)
        return 'Finished counting. Check AllObjects.json.'

if __name__ == "__main__":
  main()