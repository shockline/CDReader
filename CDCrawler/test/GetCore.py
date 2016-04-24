

def dealWithContent(content):
    posDict={}
    negDict={}
    for posWord in posList:
        count=content.count(posWord)
        if count > 0:
            posDict[posWord] = count
    for negWord in negList:
        count=content.count(negWord)
        if count > 0:
            negDict[negWord] = count
    for key, value in posDict.items():
        content=content.replace(key, '<span style="font-size:18px;font-weight: bold; color: #000;background-color:rgba(0, 
100, 0, 0.49);" title="正面短语">'+key+"</span>")

    for key, value in negDict.items():
        content=content.replace(key, '<span style="font-size:18px;font-weight: bold;  color: #000;background-color: #d9534
f;" title="负面短语">'+key+"</span>")
    
    return json.dumps({"data":content, "poswords":posDict, "negwords":negDict})
