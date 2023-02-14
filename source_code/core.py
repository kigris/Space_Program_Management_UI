from datetime import *
import model

'''Funciones de inicio de sesión'''


def checkLogin(user, password):
    return model.checkLogin(user, password)


'''Funciones útiles'''


def check_Number(number, stringError, positive=True, floatNum=False):
    if not floatNum:
        try:
            number = int(number)
            if positive:
                if number <= 0:
                    raise Exception()
        except:
            return stringError
    else:
        try:
            number = float(number)
            if positive:
                if number <= 0:
                    raise Exception()
        except:
            return stringError


def populateDB():
    model.populate_db()


''' Funciones del sistema '''


def addDaysSystem(days):
    model.addDays(days)


def getDate():
    return model.getDate()


''' Funciones de cohetes'''


def addRocket(name, maxWeight):
    maxWeight = maxWeight.replace(',', '.')
    try:
        maxWeight = float(maxWeight)
    except Exception:
        return 0
    model.addRocket(name, float(maxWeight))
    return 1


def getCountAllRockets():
    return model.countAllRocket()


def getCountRockets(assigned):
    return model.countRockets(assigned)


def getAllRockets():
    return model.getAllRockets()


def getRockets(assigned):
    return model.getRockets(assigned)


def editRocket(id, name, weight):
    weight = weight.replace(',', '.')
    result = check_Number(
        weight, "El peso debe ser un número real positivo", floatNum=True)
    if result:
        return result
    if not model.editRocket(id, name, float(weight)):
        return "El cohete no puede ser editado porque hay un lanzamiento que lo está utilizando"


def getRocketById(id):
    return model.getRocketById(id)


def deleteRocket(id):
    if not model.deleteRocket(id):
        return "El cohete no puede ser borrado porque hay un lanzamiento que lo está utilizando"


''' Funciones de peticiones'''


def getPetitions(assigned, fail=False):
    return model.getPetitions(assigned)


def addPetition(descId, desc, weight, days):
    result = check_Number(
        weight, "El peso debe ser un número real positivo", floatNum=True)
    if result:
        return result
    result = check_Number(
        days, "Los días deben ser un número de días entero")
    if result:
        return result
    model.addPetition(descId, desc, float(weight), int(days))


def editPetition(petitionId, descId, desc, weight, days):
    try:
        weight = float(weight)
    except:
        return "El peso debe ser un número real positivo"
    try:
        days = int(days)
    except:
        return "Los días deben ser un número de días entero"
    model.editPetition(petitionId, descId, desc, weight, days)


def getCountPetitions(assigned):
    return model.countPetitions(assigned)


def deletePetition(id):
    model.deletePetition(id)


def getAllPetitions():
    return model.getAllPetitions()


def countHistoricPetitions(delivered):
    return model.countHistoricPetitions(delivered)


def getHistoricPetitions(delivered):
    return model.getHistoricPetitions(delivered)


def sendPetition(id):
    model.sendPetition(id)


def getPetitionsByLaunch(id):
    return model.getPetitionsByLaunch(id)


def getPetitionDeadline(id):
    return model.getPetitionDeadline(id)


def arrivePetition(id):
    model.arrivePetition(id)


def assignPetitionsFinalDate(id, finalDate):
    model.assignPetitionsFinalDate(id, finalDate)


''' Funciones de lanzamientos'''


def addLaunch(rocketId, descId, days, desc):
    try:
        days = int(days)
    except:
        return "Los días deben ser un número de días entero"
    model.addLaunch(rocketId, descId, days, desc)


def getLaunches(assigned=True, deployed=False):
    return model.getLaunches(assigned)


def getDeployedLaunches(deployed):
    return model.getDeployedLaunches(deployed)


def getCountLaunches(assigned=True):
    return model.countLaunches(assigned)


def getCountDeployedLaunches(deployed):
    return model.countDeployedLaunches(deployed)


def getLaunchCapacity(id):
    return model.getLaunchCapacity(id)


def getLaunchLoad(id):
    return model.getLaunchLoad(id)


def editLaunch(launchId, rocketId, descId, days, desc):
    try:
        days = int(days)
    except:
        return "Los días deben ser un número de días entero"
    model.editLaunch(launchId, rocketId, descId, days, desc)


def deleteLaunch(id):
    model.deleteLaunch(id)


def deployLaunch(id):
    model.deployLaunch(id)


def getLaunchById(id):
    return model.getLaunchById(id)


def countHistoricLaunches(delivered):
    return model.countHistoricLaunches(delivered)


def getHistoricLaunches(delivered):
    return model.getHistoricLaunches(delivered)


def assignLaunchFinalDate(id, finalDate):
    model.assignLaunchFinalDate(id, finalDate)


def failLaunch(id):
    model.failLaunch(id)


def getLaunchDeadline(id):
    return model.getLaunchDeadline(id)


def arriveLaunch(id):
    model.arriveLaunch(id)


''' Funciones de acciones '''


def assign():
    petitions = model.getPetitionsByDays()
    launches = model.getLaunchesByDays()

    petitions_assigned = list()
    petitions_failed = list()
    for petition in petitions:
        assigned = False
        launchText = None
        for launch in launches:
            if model.petitionFitOnLaunch(petition[0], launch[0]):
                if model.petitionInTime(petition[0], launch[0]):
                    launchText = launch[2]
                    model.assignPetition(petition[0], launch[0])
                    assigned = True
                    break
        if assigned:
            petitions_assigned.append([petition[1], launchText])
            model.assignLaunch(launch[0])
        else:
            model.failPetition(petition[0])
            petitions_failed.append(petition[1])
    return petitions_assigned, petitions_failed


def forwardDays(days):
    addDaysSystem(days)
    currentDate = getDate()
    launches_out = list()
    launches = model.getLaunchesToDeploy()
    for launch in launches:
        deployLaunch(launch[0])

    for launch in launches:
        launchDeadline = getLaunchDeadline(launch[0])
        result = launchDeadline - datetime.strptime(getDate(), "%Y-%m-%d")
        petitionsDelivered = list()
        petitionsInTransit = list()
        if result.days <= 0:
            petitions = getPetitionsByLaunch(launch[0])
            if petitions:
                for petition in petitions:
                    arrivePetition(petition[0])
                    assignPetitionsFinalDate(
                        petition[0], launchDeadline.strftime("%Y-%m-%d"))
                    petitionsDelivered.append(petition[1])
            if not petitionsDelivered:
                failLaunch(launch[0])
                assignLaunchFinalDate(
                    launch[0], launchDeadline.strftime("%Y-%m-%d"))
                launches_out.append(
                    [1, launch[2], str(launchDeadline.strftime("%Y-%m-%d")), False])
            else:
                arriveLaunch(launch[0])
                assignLaunchFinalDate(
                    launch[0], launchDeadline.strftime("%Y-%m-%d"))
                launches_out.append(
                    [1, launch[2], str(launchDeadline.strftime("%Y-%m-%d")), petitionsDelivered])
        else:
            petitions = getPetitionsByLaunch(launch[0])
            if petitions:
                for petition in petitions:
                    sendPetition(petition[0])
                    petitionsInTransit.append(petition[1])
            launches_out.append(
                [0, launch[2], currentDate, petitionsInTransit])

    petitions = getPetitions(assigned=False)
    for petition in petitions:
        petitionDeadline = getPetitionDeadline(petition[0])
        result = petitionDeadline - datetime.strptime(currentDate, "%Y-%m-%d")
        if result.days <= 0:
            model.failPetition(petition[0])
            assignPetitionsFinalDate(
                petition[0], petitionDeadline.strftime("%Y-%m-%d"))
            launches_out.append(
                [2, petition[1], petitionDeadline.strftime("%Y-%m-%d")])
    return launches_out
