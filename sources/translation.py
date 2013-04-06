# -*- coding: utf-8 -*-
"""
@var GDictTranslation: dictionnaire contenant les traductions.
@type GDictTranslation: dict
@var GLng: langue courante.
@type GLng: str
""" 
GDictTranslation = {}
GLng = ''

def loadTranslation(aFile):
    """
    Charge les traductions contenues dans un fichier.
    Le chargement d'un fichier de traductions remplace les traductions déjà chargées.
    @param aFile: Nom du fichier à chargé
    @type aFile: str
    """

    try:
        lFile = open(aFile)
    except:
        print 'Error: "' + str(aFile) + '" not found.'
        return

    lNLine = 0
    lFile = lFile.read()
    lFile = lFile.split('\n')
    lFile = [l for l in lFile if len(l)>0]

    for lLine in lFile:
        lNLine += 1
        if lLine[0] != '#':
            lLine = lLine.split(';')

            if len(lLine) < 3:
                print 'Warning - loadTranslation: translation : line ' + str(lNLine) + ' wrong numbers of arguments (' + str(len(lLine)) + ' given, minimun 3 expected)'
                print '\tline ignored'
            else:

                if len(lLine) > 3:
                    print 'Warning - loadTranslation : translation : line ' + str(lNLine) + ' wrong numbers of arguments (' + str(len(lLine)) + ' given, minimun 3 expected)'

                lCode = lLine[0]
                lLng = lLine[1]
                lText = lLine[2]


                for lTxt in lText.split('#')[1:]:
                    try:
                        lN = int(lTxt[0])
                        if lN == 0:
                            print 'Warning - loadTranslation: ' + lLng + '-' + lCode + ': a text variable must be a number from 1 to 9'
                    except:
                        print 'Warning -loadTranslation: ' + lLng + '-' + lCode + ': a text variable must be a number from 1 to 9'


                global GDictTranslation

                if lLng not in GDictTranslation:
                    GDictTranslation[lLng] = {}

                GDictTranslation[lLng][lCode] = lText

def checkTranslation():
    """
    Vérifie l'état des traductions et affiche un compte rendu dans la console.
    """

    print '\nTranslation:'

    lOk = True
    for lLng in GDictTranslation:
        print '\t' + lLng + ': ' + str(len(GDictTranslation[lLng]))


    lErrors = 0

    lSErrors = ''
    lListCode = []

    for lDict in GDictTranslation.values():
        for lCode in lDict:
            if lCode not in lListCode:
                lListCode.append(lCode)


    for lCode in lListCode:
        lSLng = ''
        for lLng in GDictTranslation:
            if lCode not in GDictTranslation[lLng].keys():
                if lSLng != '':
                    lSLng += ','
                lSLng += ' ' + lLng

        if lSLng != '':
            if lSErrors != '':
                lSErrors += '\n'
            lSErrors += '\t' + lCode + ' not found for:' + lSLng

    if lSErrors == '':
        print '\n 0 Error found\n'
    else:
        print '\n ' + str(len(lSErrors.split('\n'))) + ' Errors found:'
        print lSErrors + '\n'

def setLanguage(aNewLng):
    """
    Change la langue courante.
    Si la langue n'existe pas dans le fichier, un message apparaitra dans la console.
    @param aNewLng: code de la langue
    @type aNewLng: str
    """

    global GLng
    GLng = aNewLng
    if aNewLng not in GDictTranslation:
        print 'Warning: setLanguage - ' + aNewLng + ' language unknow'

def getTranslation(aCode,*aArgs):
    """
    Donne la traduction liée au code donné et à la langue courante.
    @param aCode: code de la traduction
    @type aCode: str
    @param aArgs: liste des arguments éventuelle du message
    @type aArgs: list
    @return: texte de la traduction
    @rtype: str
    """

    if GLng == '':
        print 'Warning: getTranslation - language requested'
        return aCode
    elif GLng not in GDictTranslation:
        print 'Warning: getTranslation -' + GLng + ' language unknow'
        return aCode
    elif aCode not in GDictTranslation[GLng]:
        print 'Warning: getTranslation -' + aCode + ' code unknow'
        return aCode
    else:
        lText = GDictTranslation[GLng][aCode]

        if '#' in lText:

            lText = lText.split('#')

            if len(aArgs) < len(lText) -1:
                print 'Warning: getTranslation -' + GLng + '-' + aCode + ': not enought arguments (' + str(len(aArgs)) + ' given, ' + str(len(lText) -1) + ' expected)'
            elif len(aArgs) > len(lText) -1:
                print 'Warning: getTranslation -' + GLng + '-' + aCode + ': too much arguments (' + str(len(aArgs)) + ' given, ' + str(len(lText) -1) + ' expected)'

            lTextTmp = ''
            for lIndex in range(len(lText)-1):
                lTxt=lText[lIndex]
                if lIndex != 0:
                    lTxt = lTxt[1:]
                try:
                    lArg = int(lText[lIndex+1][0])
                    if lArg > 0 and lArg <= len(aArgs):
                        lArg = aArgs[lArg-1]
                    else:
                        print 'Warning: getTranslation -' + GLng + '-' + aCode + ': a text variable must be a number from 1 to 9'
                        lArg = lText[lIndex+1]
                except:
                    print 'Warning: getTranslation -' + GLng + '-' + aCode + ': a text variable must be a number from 1 to 9'
                    lArg = lText[lIndex+1]
                lTextTmp += lTxt + str(lArg)

            lText = lTextTmp + lText[-1][1:]

        return lText

def currentLanguage():
    """
    Renvoie la langue courante
    @return: code de la langue
    @rtype: str
    """
    return GLng

def getLanguages():
    """
    Renvoie une liste des langues disponibles dans le fichier de tradcutions chargés.
    @return: liste des langues disponibles
    @rtype: list
    """
    return GDictTranslation.keys()

def isLanguage(aLng):
    """
    Si la langue donné existe dans le fichier chargé, renvoie True, sinon renvoie False.
    @param aLng: code de la langue à tester.
    @type aLng: str
    @return: true: si la langue existe, sinon false
    @rtype: bool

    """
    if aLng in GDictTranslation:
        return True
    return False