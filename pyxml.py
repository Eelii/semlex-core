import xml.etree.ElementTree as ET
import os
import random
import re

#tree = ET.parse('country_data.xml')
#root = tree.getroot()




class Laki:
    
    lawNumber = None
    lawYear = None
    lawID = None
    lawName = None
    pykalat = []
    luvut = []

    def __init__(self, path):
        self.path = path
    
    def addPykala(self, pykala):
        self.pykalat.append(pykala)

    def defineLawNumber(self):
        self.lawNumber = getAsiakirjaNro(self.path)

    def defineLawYear(self):
        self.lawYear = getVuosi(self.path)
    
    def defineLawID(self):
        self.lawID = getId(self.path)
    
    def defineLawName(self):
        self.lawName = getLakiKokoNimi(self.path)
    #EI
    def defineParagraphs(self):
        self.pykalat = getPykalat(self.path)
    
    def printLaki(self):
        print("\n\n\n"+ str(self.lawName))
        print("\nTunnus: " + str(self.lawID) +"\n")
        print("------------------------------------------------------")
        for pykala in self.pykalat:
            pykala.printPykala()

class Luku:

    def __init__(self, nro, pykalat):
        self.nro = nro
        self.pykalat = pykalat

class Pykala: 

    momentit = []
    nro = None
    tunnus = None
    otsikko = None
    
    def addMomentti(momentti):
        momentit.append(momentti)
    
    def printPykala(self):
        try:
            print("\n\n" + str(self.nro) + " § " + self.otsikko)
            for momentti in self.momentit:
                print("\n")
                momentti.printMomentti()
        except:
            print("\n" + str(self.nro) + " § ")
            for momentti in self.momentit:
                print("\n")
                momentti.printMomentti()





class Momentti:

    kohdat = []

    def __init__(self, sija, sisalto):
        self.sija = sija 
        self.sisalto = sisalto
    
    def printMomentti(self):
        print(self.sisalto)

class Kohta:

    def __init__():
        pass

def listFiles():
    filesList = os.listdir()
    return filesList

#Lists all files in cwd and in subfolders
def listAllFilePaths():
    filePaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if ("pyxml.py" in name):
                continue
            else:
                filePaths.append(os.path.join(root, name))
    return filePaths

def getRandomFilePath():
    filePaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in files:
            if ("pyxml.py" in name):
                continue
            else:
                filePaths.append(os.path.join(root, name))
    randomFile = filePaths[random.randint(0, len(filePaths)-1)]
    return randomFile

def listDirPaths():
    dirPaths = []
    for root, dirs, files in os.walk(".", topdown=False):
        for name in dirs:
            dirPaths.append(os.path.join(root, name))
    return dirPaths
    
def containsDirs(folder):
    containsDirs = False
    for aThing in folder:
        path = os.path.join(os.getcwd(), aThing)
        if(os.path.isdir(path)==True):
            containsDirs = True
            break
    return containsDirs

def createLaw(path):
    law = Laki(path)
    law.defineLawNumber()
    law.defineLawYear()
    law.defineLawID()
    law.defineLawName()
    law.defineParagraphs()
    return law

#TODO + katkoviivat ja palstaviivat
def removeCursiveTags(path):
    cursiveTag = "</saa:SaadosKursiiviKooste>"
    cursiveTag2 = "<saa:SaadosKursiiviKooste>"
    with open(path, 'r') as file:
        filedata = file.read()

    filedata = filedata.replace(cursiveTag, "")
    filedata = filedata.replace(cursiveTag2, "")

    with open(path, 'w') as file:
        file.write(filedata)

def preprocessAllXmlFiles():
    filepaths = listAllFilePaths()
    for filepath in filepaths:
        (print("Prosessoidaan tiedostoa: " + str(filepath)))
        removeCursiveTags(filepath)
    
def getLawList():
    listOfLaws = []
    filepaths = listAllFilePaths()
    for filepath in filepaths:
        law = createLaw(filepath)
        listOfLaws.append(law)
    return listOfLaws


def getTags():
    #-----------------------------identifiointiosa------------------------------------
    asiakirjatyyppi = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiNimi"
    tyyppikoodi = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiKoodi"
    asiakirjanro = "{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}AsiakirjaNroTeksti"
    vuosi = "{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}ValtiopaivavuosiTeksti"
    asiakirjanimi = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}NimekeTeksti"
    viiteteksti = "{http://www.vn.fi/skeemat/sisaltoelementit/2010/04/27}ViiteTeksti"
    #----------------------------------säädös-----------------------------------------
    saadostyyppi = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadostyyppiKooste"
    saadosnimi = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimekeKooste"
    kappaleKooste = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosKappaleKooste"
    #TODO
    johtolause = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Johtolause"
    #--------------------------------luku---------------------------------------------
    luku = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Luku"
    lukuOtsikko = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosOtsikkoKooste"
    lukuTunnus = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}LukuTunnusKooste"
    #--------------------------------pykalistö----------------------------------------
    pykala = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Pykala" #Huom. ei tekstisisältöä
    pykalaTunnus = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}PykalaTunnusKooste"
    otsikko = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosOtsikkoKooste"
    #--------------------------------momentti-----------------------------------------
    momentti = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKooste"
    #--------------------------------kohta--------------------------------------------
    kohtaJohdanto = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiJohdantoKooste"
    momenttiKohta = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKohtaKooste" #????
    #-------------------------------viivat-------------------------------------------
    katkoviiva = "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}Katkoviiva"
    palstaviiva = "{http://www.vn.fi/skeemat/sisaltokooste/2010/04/27}Palstaviiva"
    #-------------------------------allekirjoitusosa---------------------------------------
    paivayskooste = "{http://www.vn.fi/skeemat/asiakirjakooste/2010/04/27}PaivaysKooste"
    asema = "{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}AsemaTeksti"
    nimi = "{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}SukuNimi"

    tagDic = {"asiakirjatyyppi":asiakirjatyyppi, "tyyppikoodi":tyyppikoodi, "asiakirjanro":asiakirjanro, "vuosi":vuosi, "asiakirjanimi":asiakirjanimi, "viiteteksti":viiteteksti, 
    "saadostyyppi":saadostyyppi, "saadosnimi":saadosnimi, "kappaleKooste":kappaleKooste, "pykala":pykala, "pykalaTunnus":pykalaTunnus, "otsikko":otsikko, "momentti":momentti, "luku":luku, "katkoviiva":katkoviiva,
    "palstaviiva":palstaviiva, "paivayskooste":paivayskooste, "asema":asema, "nimi":nimi, "luku":luku, "lukuOtsikko":lukuOtsikko, "lukuTunnus":lukuTunnus, "johtolause":johtolause, "kohtaJohdanto":kohtaJohdanto,
    "momenttiKohta":momenttiKohta}

    return tagDic


#Returns all paragraphs in EVERY SINGLE XML-file within cwd and subfolders. 
def getAllParagraphs():
    allParagraphs = []
    paths = listAllFilePaths() 
    for path in paths:
        allParagraphs.append(getParagraphs(path))
    return allParagraphs

def countAllParagraphs():
    allParagraphs = listAllFilePaths() 
    for path in paths:
        allParagraphs.append(getParagraphs(path))
    return len(allParagraphs)

def getRoot(path):
    tree = ET.parse(path)
    root = tree.getroot()
    return root

def getNamespace(path):
    tree = ET.parse(path)
    root = tree.getroot()
    tag = root.tag
    namespace = re.findall("{.+}",tag)
    return namespace[0]

def getLawTags(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for element in root.iter():
        print(element.tag)

def getAllTagsAndTexts(path):
     tree = ET.parse(path)
     root = tree.getroot()
     for element in root.iter():
         print("%s - %s" % (element.tag, element.text))

#VahvistettavaLaki/SaadosOsa/Saados/Pykalisto/Pykala/MomenttiKooste
#{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKooste'
#MOMENTTI = SUBSECTION
def getParagraphs(path):
    paragraphs = []
    #namespace = getNamespace(path)
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in root.iter(tag = "{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}MomenttiKooste"):
        paragraphs.append(elem.text)
    return paragraphs

def getAsiakirjatyyppi(path):
    tyypit = []
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in tree.iter(tag = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}AsiakirjatyyppiNimi"):
        tyypit.append(elem.text)
    return tyypit

def getNimeketyyppi(path):
    tyypit = []
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in tree.iter(tag = "{http://www.vn.fi/skeemat/metatietoelementit/2010/04/27}NimekeTeksti"):
        tyypit.append(elem.text)
    return tyypit

def getAllekirjoittaja(path):
    allekirjoittajat = []
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in tree.iter("{http://www.vn.fi/skeemat/organisaatioelementit/2010/02/15}SukuNimi"):
        allekirjoittajat.append(elem.text)
    return allekirjoittajat 

#Returns a string!
def getAsiakirjaNro(path):
    print("Processing: " + str(path))
    asiakirjaNroStrLst = []
    tree = ET.parse(path)
    root = tree.getroot()
    try:
        for elem in tree.iter("{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}AsiakirjaNroTeksti"):
            try:
                asiakirjaNroStrLst.append(elem.text)
            except:
                asiakirjaNroStrLst.append(None)
        assert(len(asiakirjaNroStrLst)==1)
    except:
        return None
    return asiakirjaNroStrLst[0]

def getVuosi(path):
    vuosiLst = []
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in tree.iter("{http://www.vn.fi/skeemat/asiakirjaelementit/2010/04/27}ValtiopaivavuosiTeksti"):
        vuosiLst.append(elem.text)
    assert(len(vuosiLst)==1)
    return vuosiLst[0]

def getId(path):
    nro = getAsiakirjaNro(path)
    vuosi = getVuosi(path)
    try:
        id = nro+"/"+vuosi
    except:
        try:
            id = vuosi
        except:
            try:
                id = nro
            except:
                id = None
    return id

def getPykalaNrot(path):
    pykalaNroLst = []
    tree = ET.parse(path)
    root = tree.getroot()
    for elem in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}PykalaTunnusKooste"):
        pykalaNroLst.append(elem.text)
    return pykalaNroLst


#YEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEESSSSSSSSSSSSSS
def getPykalat(path):
    pykalat = []
    pykalaNroLst = getPykalaNrot(path)
    print(pykalaNroLst)
    tagDic = getTags()
    pykalaTag = tagDic.get("pykala")
    tree = ET.parse(path)
    root = tree.getroot()
    count = -1
    for pykala in tree.iter(pykalaTag):
        pykalaObject = Pykala()
        momentit = []
        pykalaTunnus = None
        otsikko = None
        luku = None
        momenttiNro = 1
        for pykalaTunnus in pykala.iter(tagDic.get("pykalaTunnus")):
            pykalaObject.pykalaTunnus = pykalaTunnus.text
        for otsikko in pykala.iter(tagDic.get("otsikko")):
            pykalaObject.otsikko = otsikko.text
        for luku in pykala.iter(tagDic.get("luku")):
            pykalaObject.luku = luku.text
        for momentti in pykala.iter(tagDic.get("momentti")):
            momenttiObject = Momentti(sija=momenttiNro, sisalto=momentti.text)
            momentit.append(momenttiObject)
            momenttiNro += 1
        try:
            pykalaObject.nro = pykalaNroLst.pop(0)
        except:
            pykalaObject.nro = 0
        pykalaObject.momentit = momentit
        pykalat.append(pykalaObject)
    return pykalat


def getLakiTyyppi(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for saadosnimeke in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimeke"):
        for saadostyyppi in saadosnimeke.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadostyyppiKooste"):
            tyyppi = saadostyyppi.text

    return tyyppi

def getLakiNimi(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for saadosnimeke in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimeke"):
        for nimi in saadosnimeke.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimekeKooste"):
            saadosnimi = nimi.text

    return saadosnimi

def getLakiKokoNimi(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for saadosnimeke in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimeke"):
        for saadostyyppi in saadosnimeke.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadostyyppiKooste"):
            tyyppi = saadostyyppi.text
        for nimi in saadosnimeke.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}SaadosNimekeKooste"):
            saadosnimi = nimi.text
    try:
        kokonimi = tyyppi + " " + saadosnimi
    except:
        kokonimi = "NIMETÖN"

    return kokonimi


def getPykalaAttributes(path):
    tree = ET.parse(path)
    root = tree.getroot()
    pykalaAttributes = []
    for pykala in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Pykala"):
        
        try:
            saannosTyyppi = parseAttribute(pykala.get("{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}pykalaLuokitusKoodi"))
            if (len(saannosTyyppi) == 0):
                saannosTyyppi = parseAttribute(pykala.get("{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus"))
        except:
            continue
        
        try:
            saannosSija = parseAttribute(pykala.get("{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus"))
            if (len(saannosSija) == 0):
                saannosSija = parseAttribute(pykala.get("{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}pykalaLuokitusKoodi"))
        except:
            continue

        try:
            pykalaAttributes.append((saannosSija, saannosTyyppi))
        except:
            continue

    return pykalaAttributes

def parseAttribute(attribute):

    parsed = attribute.replace("\xa0a","")
    parsed = parsed.replace("\xa0c","")
    parsed = parsed.replace("\u2009"," ")
    return parsed

def getPykalaNrot(path):

    tree = ET.parse(path)
    root = tree.getroot()
    pykalaNrot = [] 
    for pykala in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Pykala"):
        num = 0
        saannosSija = pykala.get("{http://www.vn.fi/skeemat/saadoselementit/2010/04/27}identifiointiTunnus")
        if (saannosSija == "Voimaantulo" or saannosSija == "VoimaantuloSaannos"):
            saannosSija = 999
        try:
            num = re.findall(r"[0-9]+", saannosSija)
        except:
            continue
        try:
            saannosSijaInt = int(num[0])
            pykalaNrot.append(saannosSijaInt)
        except:
            continue

    return pykalaNrot

def initUI():
    idList = []
    lawList = getLawList()
    print(str(len(lawList)) + " säädöstä ladattu")
    for law in lawList:
        idList.append(law.lawID)

#-----------------------------------------------------------------------------------------

def sortListByLength(e):
    return len(e)

def getLongestLawName():
    lawList = getLawList()
    nameList = []
    print("Odota...")
    for law in lawList:
        nameList.append(law.lawName)
        nameList.sort(key=sortListByLength)
    for name in nameList:
        print("\n")
        print("Length ")
        print(len(name))
        print("")
        print(name)

def printAllLawIDs():
    lawList = getLawList()
    idList = []
    print("Odota...")
    for law in lawList:
        idList.append(law.lawID)
    for id in idList:
        print(id)

def printPykalaTrees(path):
    tree = ET.parse(path)
    root = tree.getroot()
    for pykala in tree.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}Pykala"):
        for p in pykala.iter("{http://www.vn.fi/skeemat/saadoskooste/2010/04/27}KohdatMomentti"):
           for i in p:
               print(i)


def testRandom():
    polku = getRandomFilePath()
    print("Polku: " + polku)
    print("Asiakirjatyyppi: ")
    print(getAsiakirjatyyppi(polku))
    print("Pykälät: ")
    print(getPykalaNrot(polku))
    print("Nimeke: ")
    print(getNimeketyyppi(polku))
    print("Allekirjoittaja: ")
    print(getAllekirjoittaja(polku))
    print("Id: ")
    print(getId(polku))
    print("SISÄLTÖ: ")
    print(getPykalat(polku))
    testTree(polku)

def testAttributes():
    polku = getRandomFilePath()
    print("Attributes: ")
    print(getPykalaAttributes(polku))

def testTree(polku):
    tree = ET.parse(polku)
    root = tree.getroot()
    print("TREE:\n\n")
    for neighbor in root.iter():
        print(neighbor)
    print("\n")


path = getRandomFilePath()
law = createLaw(path)
law.printLaki()
print(getPykalaNrot(path))
print(getLawTags(path))
testTree(path)
print(printPykalaTrees(path))
print(getLawTags(path))
print(getId(path))


