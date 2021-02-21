import xml.etree.ElementTree as ET
import os
import random
import re


class Statute:

    path = None
    statuteID = None
    statuteType = None
    documentType = None
    number = None
    year = None
    name = None
    language = None
    documentReferences = None
    enactingClause = None
    chapters = []
    runningSections = None
    sections = []
    referenceParts = None
    signaturePart = None

    def defineNumber(self):
        tags = documentTags()
        documentNumStrLst = []
        tree = ET.parse(self.path)
        root = tree.getroot()
        for elem in tree.iter(tags.get("number")):
            documentNumStrLst.append(elem.text)
        assert(len(documentNumStrLst)==1)
        self.number = documentNumStrLst[0]

    def defineYear(self):
        tags = documentTags()
        documentYearStrLst = []
        tree = ET.parse(self.path)
        root = tree.getroot()
        for elem in tree.iter(tags.get("year")):
            documentYearStrLst.append(elem.text)
        assert(len(documentYearStrLst)==1)
        self.year = documentYearStrLst[0]

    def defineStatuteID(self):
        assert(self.year != None and self.number != None)
        self.statuteID = self.number + "/" + self.year

    def defineStatuteType(self):
        tags = documentTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for elem in tree.iter(tags.get("statuteType")):
            self.statuteType = elem.text
    
    def defineDocumentType(self):
        tags = documentTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for elem in tree.iter(tags.get("documentType")):
            self.documentType = elem.text

    def defineStatuteName(self):
        tags = documentTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for elem in tree.iter(tags.get("name")):
            self.name = elem.text

    def defineEnactingClause(self):
        self.enactingClause = EnactingClause()
        tags = documentTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for enactingClause in tree.iter(tags.get("enactingClause")):
            for content in enactingClause.iter(tags.get("enactingClauseContent")):
                newEnactingClauseSection = EnactingClauseSection()
                newEnactingClauseSection.text = content.text
                self.enactingClause.enactingClauseSections.append(newEnactingClauseSection)

    def defineChapters(self):
        tags = chapterTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for chapter in tree.iter(tags.get("chapter")):
            newChapter = Chapter()
            for identifier in chapter.iter(tags.get("chapterID")):
                newChapter.identifier = identifier.text
            for heading in chapter.iter(tags.get("heading")):
                newChapter.heading = heading.text
            
            self.chapters.append(newChapter)
            
    def defineSections(self):
        #assert (self.runningSections == True)
        tags = sectionTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        for section in tree.iter(tags.get("section")):
            newSection = Section()
            for sectionID in section.iter(tags.get("identifier")):
                newSection.identifier = sectionID.text
            for sectionHeading in section.iter(tags.get("heading")):
                newSection.heading = sectionHeading.text
            newSection.iterableXml = section
            newSection.subsections = self.defineSubsections(aSection = newSection)
            self.sections.append(newSection)
    
    def defineSubsections(self, aSection):
        secTags = sectionTags()
        subTags = subsectionTags()
        paraTags = paragraphTags()
        sectionXML = aSection.iterableXml
        subsectionsLst = []
        position = 1
        for section in sectionXML.iter(secTags.get("section")):
            for element in section:
                print(element.tag)
                if (element.tag == subTags.get("text")):
                    newSubsection = Subsection()
                    newSubsection.text = element.text
                    newSubsection.position = position
                    subsectionsLst.append(newSubsection)
                    position += 1

                elif (element.tag == paraTags.get("paragraphs")):
                    newSubsection = Subsection()
                    newSubsection.paragraphs = self.defineParagraphs(element)
                    newSubsection.position = position
                    subsectionsLst.append(newSubsection)
                    position += 1
        return subsectionsLst
            
            

        '''
        for section in sectionXML.iter(secTags.get("section")):
            for iden in section.iter(secTags.get("identifier")):
                for head in section.iter(secTags.get("heading")):
                    #If it looks like a duck and walks like a duck...
                    if (iden.text == aSection.identifier and head.text == aSection.heading):
                        position = 1
                        #Hmmm
                        paraPosition = 0
                        inParagraph = False
                        for element in section.iter():

                            if (element.tag == subTags.get("text")):

                                if (inParagraph == True):
                                    aSection.position = position
                                    aSection.subsections.append(newSubsection)
                                    position += 1
                                    inParagraph = False

                                newSubsection = Subsection()
                                print("Creating a new subsec")
                                newSubsection.position = position
                                newSubsection.text = element.text
                                aSection.subsections.append(newSubsection)
                                position += 1

                            elif (element.tag == paraTags.get("paragraphs")):
                                inParagraph = True
                                newSubsection = Subsection()
                            
                            elif (element.tag == paraTags.get("paragraphPreamble" and inParagraph == True)):
                                paraPosition = 0
                                newParagraph = Paragraph()
                                newParagraph.position = paraPosition
                                newParagraph.preamble = element.text
                                newParagraph.isPreamble = True
                                newSubsection.paragraphs.append(newParagraph)

                            elif (element.tag == paraTags.get("text") and inParagraph == True):
                                paraPosition += 1
                                newParagraph = Paragraph()
                                newParagraph.position = paraPosition
                                newParagraph.isPreamble = False
                                newParagraph.text = element.text
                                newSubsection.paragraphs.append(newParagraph)

                        if (inParagraph == True):
                            aSection.position = position
                            aSection.subsections.append(newSubsection)

                    else:
                        continue
        '''

    def hasParagraphs(self, iterableSection):
        tags = self.getSectionXMLElements(iterableSection)
        for tag in tags:
            if ("MomenttiKohtaKooste" in str(tag)):
                return True
        return False

    #remove?
    def getSectionXMLElements(self, iterableSection):
        elements = []
        for element in iterableSection.iter():
            elements.append(element.tag)
        return elements

    def defineParagraphs(self, paraRoot):
        paraTags = paragraphTags()
        paraRoot = paraRoot
        position = 1
        paragraphLst = []
        for element in paraRoot.iter():
            if (element.tag == paraTags.get("paragraphPreamble")):
                newParagraph = Paragraph()
                newParagraph.isPreamble = True
                newParagraph.preamble = element.text
                newParagraph.position = position-1
                paragraphLst.append(newParagraph)

            if (element.tag == paraTags.get("text")):
                newParagraph = Paragraph()
                newParagraph.isPreamble = False
                newParagraph.text = element.text
                newParagraph.position = position
                paragraphLst.append(newParagraph)
                position += 1

        return paragraphLst
                         

    def initStatute(self):
        self.defineNumber()
        self.defineYear()       
        self.defineStatuteID()
        self.defineDocumentType()
        self.defineStatuteType()
        self.defineStatuteName()
        self.defineEnactingClause()
        self.defineChapters()
        self.defineSections()
            #for subsection in section.subsections:
                #self.defineParagraphs(aSubsection = subsection)

        #TODO
    
#--------------------------------------------TESTING------------------------------------------------



    def printSectionTags(self, aSection):
        secTags = sectionTags()
        subTags = subsectionTags()
        paraTags = paragraphTags()
        sectionXML = aSection.iterableXml
        print("-----------------------------------------------------------------")
        print("ID: " + self.statuteID)
        for section in sectionXML.iter(secTags.get("section")):
            for element in section:
                print(element.tag)
        print("-----------------------------------------------------------------")

    def printProperties(self):
        print("ID: " + self.statuteID + "\n")
        print("Dokumentin tyyppi: " + self.documentType + "\n")
        print("Säädöksen tyyppi: " + self.statuteType + "\n")
        print("Säädöksen nimi: " + self.name + "\n")

        print("Johtolause: ")
        for section in self.enactingClause.enactingClauseSections:
            print(section.text)
        for section in self.sections:
            for subsection in section.subsections:
                print("MOMENTTI: " + subsection.text)

    def printSectionXMLTags(self):
        secTags = sectionTags()
        subTags = subsectionTags()
        tree = ET.parse(self.path)
        root = tree.getroot()
        print("ID: " + self.statuteID) 
        for section in tree.iter(secTags.get("section")):
            for iterObj in section.iter():
                print(iterObj)

    def printStatute(self):
        print("ID: " + self.statuteID)
        for section in self.sections:
            if (section.heading != None):
                if (section.identifier == None):
                    print("\n\nEI PYKÄLÄTUNNUSTA: " + section.text)
                elif (section.identifier != None):
                    print("\n\n" + section.identifier + " " + section.heading + ": \n" )
            elif (section.heading == None and section.identifier != None):
                print(section.identifier + ": \n")
            elif (section.identifier == None):
                print("EI PYKÄLÄTUNNUSTA EIKÄ OTSIKKOA \n")

            for subsection in section.subsections:
                if (subsection.position != None and subsection.text != None):
                    print(str(subsection.position) + ". mom: " + subsection.text + "\n")
                elif(subsection.position != None and subsection.text == None and len(subsection.paragraphs)>0):
                    for paragraph in subsection.paragraphs:
                        if (paragraph.isPreamble == True):
                            print("Johtolause: " + paragraph.preamble + "\n")
                        elif (paragraph.isPreamble == False):
                            print("Pos. " + str(paragraph.position) + paragraph.text +"\n")
                        else:
                             (print("\n\nWHAAAAAAAAAAAAAAAAAAT\n\n"))

    def printSectionHeadings(self):
        print(self.statuteID)
        for section in self.sections:
            if (section.heading != None):
                print(section.heading + "\n")
            elif (section.heading == None):
                print("Pykälällä ei otsikkoa")

    def printParagraphs(self):
        for section in self.sections:
            for subsection in section.subsections:
                if (subsection.paragraphs != None):
                    print("addsfdsfsadf" + str(subsection.position))
                    for paragraph in subsection.paragraphs:
                        assert(paragraph.isPreamble != None)
                        if (paragraph.isPreamble == True):
                            print("Momentin (nro: " + str(paragraph.position) + ") esipuhe: " + paragraph.text + "\n")
                        elif (paragraph.isPreamble == False):
                            print(str(paragraph.position) + ". kohta: " + paragraph.text + "\n")


class Chapter:

    identifier = None
    number = None
    heading = None 
    sections = None

    def defineNumber(self):
        assert(identifier != None)


class Section:
    
    def __init__(self):
        pass

    sectionID = None
    identifier = None
    classification = None
    heading = None
    subsections = []
    #Iterable element tree object rooted in the current section. 
    iterableXml = None

    #--------------TESTING------------------

    def getTreeElements(self):
        elements = []
        for element in self.iterableXml.iter():
            elements.append(element.tag)
        return (elements)


class Subsection:

    def __init__(self):
        pass

    position = None
    paragraphs = []
    text = None
    iterableXml = None

class Paragraph:

    def __init__(self):
        pass

    isPreamble = None
    preamble = None
    position = None 
    text = None

class EnactingClause:

    enactingClauseSections = []

class EnactingClauseSection:

    text = None

class SignaturePart:

    date = None
    signatories = None 

class Signator:

    rank = None
    name = None 

###############
class Picture:

    pictureID = None
    text = None

def documentTags():
    
    documentType = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiNimi"
    #tyyppikoodi = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiKoodi"
    number = "{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}AsiakirjaNroTeksti"
    year = "{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}ValtiopaivavuosiTeksti"
    #name = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}NimekeTeksti"
    #viiteteksti = "{http://www.vn.fi/skeemat/sisaltoelementit/2010/04/27}ViiteTeksti"
    #---------------------------------------------------------------------------------------------
    enactingClause = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Johtolause" #--->
    enactingClauseContent = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosKappaleKooste"
    #---------------------------------------------------------------------------------------------
    statuteType = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadostyyppiKooste"
    name = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimekeKooste"

    tagDic = {"documentType":documentType, "number":number, "year":year, "statuteType":statuteType, "name":name, "enactingClause":enactingClause, 
    "enactingClauseContent":enactingClauseContent}

    return tagDic

def chapterTags():

    chapterID = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}LukuTunnusKooste"
    chapter = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Luku" #???
    heading = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosOtsikkoKooste"

    tagDic = {"chapterID":chapterID, "chapter":chapter, "heading":heading}
    return tagDic

def sectionTags():

    section = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Pykala" #Huom. ei tekstisisältöä
    identifier = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}PykalaTunnusKooste"
    heading = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosOtsikkoKooste"

    tagDic = {"section":section, "identifier":identifier, "heading":heading}
    return tagDic

def subsectionTags():

    text = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKooste"

    tagDic = {"text":text}
    return tagDic

def paragraphTags():
    paragraphs = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}KohdatMomentti"#??--->

    paragraphPreamble = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiJohdantoKooste"
    text = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKohtaKooste"

    tagDic ={"paragraphPreamble":paragraphPreamble, "text":text, "paragraphs":paragraphs}
    return tagDic 

def signaturePartTags():

    date = "{http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27}PaivaysKooste"
    #----
    signator = "{http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27}Allekirjoittaja" #Huom. ei tekstisisältöä
    #--->
    person = "{http://www.vn.fi/skeemat/organisaatiokooste/2010/02/15}Henkilo" #Huom. ei teksisisältöä

    tagDic = {"date":date,"signator":signator,"person":person}
    return tagDic

def signatorTags():
    rank = "{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}AsemaTeksti"
    name = "{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}SukuNimi"

    tagDic = {"rank":rank, "name":name}
    return tagDic



    
    #-----------------------------------------------------------------------------------------
    #kappaleKooste = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosKappaleKooste"
    #-------------------------------viivat-------------------------------------------
    #katkoviiva = "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}Katkoviiva"
    #palstaviiva = "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}Palstaviiva"
    #lihava = "{http://www.vn.fi/skeemat/sisaltoelementit/2010/04/27}LihavaTeksti"
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}table
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}tgroup
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}colspec
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}colspec
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}tbody
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}row
    #{http://www.vn.fi/skeemat/taulukkokooste/2010/04/27}entry

#Lists all files in cwd and in subfolders

def filesToIgnore():
    filenames = ["pyxml.py", "pyxml2.py", "sem.xml"]
    return filenames

def allFilePaths():
    filePaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (name in filesToIgnore()):
                continue
            else:
                filePaths.append(os.path.join(root, name))
    return filePaths

def randomFilePath():
    filePaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if (name in filesToIgnore()):
                continue
            else:
                filePaths.append(os.path.join(root, name))
    randomFile = filePaths[random.randint(0, len(filePaths)-1)]
    return randomFile

def createStatute(path):
    newStatute = Statute()
    newStatute.path = path

    return newStatute







path = randomFilePath()
stat = createStatute(path)
stat.initStatute()
stat.printStatute()
