import sys
import xmltodict

def parseLog(file):
    global count
    file = sys.argv[1]
    handler = open(file).read()
    dicter = xmltodict.parse(handler)

    count = 0

    for key in dicter.keys():
        function(key,dicter[key],"root")



def function(objectName,orderedDict,nodeLine):
    #print(objectName)
    #get children and attributes
    banned_words = ["center", "bottom", "right", "left", "top","children", "font","columnConstraints","rowConstraints"]
    pos_enum = ["BASELINE_CENTER","BASELINE_LEFT","BASELINE_RIGHT","BOTTOM_CENTER","BOTTOM_LEFT","BOTTOM_RIGHT","CENTER","CENTER_LEFT","CENTER_RIGHT","TOP_CENTER","TOP_LEFT","TOP_RIGHT"]
    stroke_type_enum = ["CENTERED","INSIDE","OUTSIDE"]
    priority_enum = ["ALWAYS","SOMETIMES","NEVER"]

    children = []
    attributes = dict()
    include = True
    try:
        if type(orderedDict) is not list:
            for attr in orderedDict.keys():
                if("@" in attr) and ("xmlns" not in attr):
                    attributes[attr]=orderedDict[attr]
            for child in orderedDict.keys():
                if "@" not in child:
                    children.append(child)
        elif type(orderedDict) is list:
            for odict in orderedDict:
                function(objectName,odict,nodeLine)
                include = False
    except:

        print("Parsing Error")

    if objectName not in banned_words and include:
        global count
        print("// Node Line: "+nodeLine)
        varName = objectName[0].lower() + objectName[1:] + str(count)
        print(objectName + " " +varName +" = new "+ objectName +"();")
        for attr in attributes.keys():
            edited_attr = attr
            if attributes[attr] in pos_enum:
                attributes[attr] = "Pos."+attributes[attr]
            elif attributes[attr] in stroke_type_enum:
                attributes[attr] = "StrokeType."+attributes[attr]
            elif attributes[attr] in priority_enum:
                attributes[attr] = "Priority."+attributes[attr]
            elif " " in attributes[attr]:
                attributes[attr] = "\""+attributes[attr]+"\""
            if "." in attr:
                edited_attr = attr[attr.find("."):]

            methodName = "set"+edited_attr[1].upper() + edited_attr[2:]
            print(varName + "."+methodName+"(" + attributes[attr] +");")
        print("")
        count += 1

    #Checks to see if there any "children"
    if children and include:
        #If so loop through children recursively calling this function
        for child in children:
            function(child,orderedDict[child],nodeLine +"->" +objectName)


if __name__ == "__main__":
    #parseLog(sys.argv[1])
    parseLog("NEWGARDENFXML.fxml")
