

class parseDict:

    def __init__(self, personName: str, rawDict: dict):
        self.__dict = rawDict
        self.__name = personName
    
    def relations(self, rawDict):
        relationsList = []
        properLen = 3
        positions = {
            'spouse': 0,
            'child': 1,
            'earliest ancestor': 2
            }

        for relation, person2Name in rawDict.items():
            
            pos = positions[relation.lower()]
            if len(relationsList) < pos + 1:
                dependentPosition = len(relationsList) + 1
            else:
                dependentPostion = pos
            relationsList += ['' for i in range(dependentPosition)]+[person2Name]

        relationsList += ['' for i in range(properLen-len(relationsList))]

        if not relationsList[positions['earliest ancestor']] == None:
            relationsList[positions['earliest ancestor']] = 'no'
        else:
            relationsList[positions['earliest ancestor']] = 'yes'

        return relationsList
    
    def run(self):
        csvList = [self.__name]
        genderPos = 4

        for key, value in self.__dict.items():
            if key == 'relations':
                csvList += self.relations(value)
            elif key == 'gender':
                if not len(csvList) > genderPos:
                    csvList += ['' for i in range(genderPos-len(csvList))] + [value]
                else:
                    csvList.append(value)
                    
        return ';'.join(csvList)


class parseText:

    def __init__(self, csvText):
        self.__text = csvText

    def run(self):
        sections = self.__text.split(';')
        if len(sections) < 5:
            return -1
        marks = {
            0: 'personName',
            1: 'spouse',
            2: 'parentName',
            3: 'is Earliest Ancestor',
            4: 'gender'
            }
        personName, spouse, parentName, isEarliestAncestor, gender = sections

        relations = {}
        if not spouse == '':
            relations['spouse'] = spouse

        if not parentName == '':
            relations['parent'] = parentName

        if not isEarliestAncestor == 'no':
            relations['earliest ancestor'] = None

        return {personName: {'relations': relations, 'gender': gender}}
        

