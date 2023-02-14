import sqlite3
from database import *
from datetime import datetime, timedelta

# Se comprueba los requisitos de la base de datos
check_database()

''' Funciones de la base de datos '''


def connectDb():
    con = sqlite3.connect(DATA_PATH + DB_FILENAME + '.db')
    cur = con.cursor()
    return cur


def saveChanges(cur):
    cur.connection.commit()
    cur.connection.close()


''' Funciones de usuario '''


def checkLogin(user, password):
    cursor = connectDb()
    if(cursor.execute(f"select count(*) from users where user = '{user}' and password = '{password}'").fetchone()[0] == 0):
        return False
    else:
        return True


''' Funciones de sistema '''


def getDate():
    cur = connectDb()
    return cur.execute("select value from configuration where description = 'systemDate'").fetchone()[0]


def addDays(days):
    cur = connectDb()
    date = cur.execute(
        "select value from configuration where description = 'systemDate'").fetchone()[0]
    date = datetime.strptime(date, "%Y-%m-%d")
    add = timedelta(days=days)
    newDate = date + add
    cur.execute(
        f"update configuration set value = date('{newDate}') where description = 'systemDate'")
    saveChanges(cur)


''' Funciones de cohetes '''


def addRocket(name, maxWeight):
    cursor = connectDb()
    cursor.execute(
        f"insert into rockets (name,maxWeight) values ('{name}',{maxWeight})")
    saveChanges(cursor)


def getAllRockets():
    cursor = connectDb()
    return cursor.execute("select * from rockets").fetchall()


def getRockets(assigned=False):
    cur = connectDb()
    if (assigned):
        return cur.execute("select * from rockets where id in (select rocketId from launches)").fetchall()
    return cur.execute("select * from rockets where id not in (select rocketId from launches)").fetchall()


def getRocketById(id):
    cur = connectDb()
    return cur.execute(f"select * from rockets where id = {id}").fetchone()


def countAllRocket():
    cur = connectDb()
    return cur.execute("select count(*) from rockets").fetchone()[0]


def countRockets(assigned=False):
    cur = connectDb()
    if (assigned):
        return cur.execute("select count() from rockets where id in (select rocketId from launches)").fetchone()[0]
    return cur.execute("select count() from rockets where id not in (select rocketId from launches)").fetchone()[0]


def deleteRocket(idRocket):
    cur = connectDb()
    if(rocketHaveLaunches(idRocket)):
        return False
    cur.execute(f"delete from rockets where id = {idRocket}")
    saveChanges(cur)
    return True


def editRocket(rocketId, name, maxWeight):
    cur = connectDb()
    if rocketHaveLaunches(rocketId):
        return False
    cur.execute(
        f"update rockets set name = '{name}', maxWeight = {maxWeight} where id = {rocketId}")
    saveChanges(cur)
    return True


def rocketHaveLaunches(idRocket):
    cur = connectDb()
    count = cur.execute(
        f"select count(*) from rockets join launches on launches.rocketId = rockets.id where rockets.id={idRocket}").fetchone()[0]
    if (count > 0):
        return True
    else:
        return False


def assignRocket(idLaunch, idRocket):
    cur = connectDb()
    cur.execute(
        f"update launches set  rocketid={idRocket} where id = {idLaunch}")
    saveChanges(cur)


''' Funciones de lanzamientos '''


def addLaunch(rocketId, descId, days, desc):
    cursor = connectDb()
    date = getDate()
    cursor.execute(
        f"insert into launches (rocketId, desc_id, days, description, status, startDate) values ({rocketId},'{descId}',{days},'{desc}',1,date('{date}'))")
    saveChanges(cursor)


def getLaunches(assigned=False):
    cursor = connectDb()
    if(assigned):
        return cursor.execute("select * from launches where launches.status=5").fetchall()
    return cursor.execute("select * from launches where launches.status=1").fetchall()


def getDeployedLaunches(deployed=True):
    cursor = connectDb()
    if deployed:
        return cursor.execute("select * from launches where launches.status=2").fetchall()
    return cursor.execute("select * from launches where (launches.status is null or launches.status!=2 and finalDate is null)").fetchall()


def countLaunches(deployed):
    cur = connectDb()
    if(deployed):
        return cur.execute("select count(*) from launches where launches.status=5").fetchone()[0]
    return cur.execute("select count(*) from launches where launches.status=1").fetchone()[0]


def countDeployedLaunches(deployed=True):
    cur = connectDb()
    if deployed:
        return cur.execute("select count(*) from launches where launches.status=2").fetchone()[0]
    return cur.execute("select count(*) from launches where (launches.status is null or launches.status!=2 and finalDate is null)").fetchone()[0]


def countHistoricLaunches(delivered=False):
    cur = connectDb()
    if delivered:
        return cur.execute("select count(*) from launches where launches.status=3").fetchone()[0]
    return cur.execute("select count(*) from launches where launches.status=4").fetchone()[0]


def launchChangeState(launchId, newState):
    cur = connectDb()
    cur.execute(
        f"update launches set status={newState} where launchId={launchId}")
    saveChanges(cur)


def getLaunchByPetition(petitionId):
    cur = connectDb()
    return cur.execute(f"select * from launches join petitions on petitions.launchId = launches.id where petitions.launchId = {petitionId}").fetchone()


def assignLaunch(id):
    cur = connectDb()
    cur.execute(f"update launches set status=5 where id = {id}")
    saveChanges(cur)


def deleteLaunch(idLaunch):
    cur = connectDb()
    cur.execute(f"delete from launches where id = {idLaunch}").fetchone()
    saveChanges(cur)


def editLaunch(launchId, rocketId, descId, days, desc):
    cur = connectDb()
    cur.execute(
        f"update launches set  rocketId={rocketId},desc_id='{descId}', days = {days}, description = '{desc}' where id = {launchId}")
    saveChanges(cur)


def getLaunchesByDays(deployed=False):
    cursor = connectDb()
    if not deployed:
        return cursor.execute("select * from launches where (launches.status=1 or launches.status=5) order by days asc").fetchall()
    return cursor.execute("select * from launches order by days asc").fetchall()


def getLaunchesToDeploy():
    cursor = connectDb()
    return cursor.execute("select * from launches where finalDate is null").fetchall()


def getAllLaunches():
    cursor = connectDb()
    return cursor.execute("select * from launches").fetchall()


def deployLaunch(idLaunch):
    cur = connectDb()
    cur.execute(f"update launches set status=2 where id = {idLaunch}")
    saveChanges(cur)


def arriveLaunch(idLaunch):
    cur = connectDb()
    cur.execute(f"update launches set status=3 where id = {idLaunch}")
    saveChanges(cur)


def failLaunch(idLaunch):
    cur = connectDb()
    cur.execute(f"update launches set status=4 where id = {idLaunch}")
    saveChanges(cur)


def getLaunchDays(idLaunch):
    cur = connectDb()
    return cur.execute(f"select days from launches where id = {idLaunch}").fetchone()[0]


def getLaunchById(id):
    cur = connectDb()
    return cur.execute(f"select * from launches where id = {id}").fetchone()


def assignLaunchFinalDate(idLaunch, finalDate):
    cur = connectDb()
    cur.execute(
        f"update launches set finalDate=date('{finalDate}') where id = {idLaunch}")
    saveChanges(cur)


def getHistoricLaunches(delivered=True):
    cursor = connectDb()
    if delivered:
        return cursor.execute("select * from launches where status=3").fetchall()
    return cursor.execute("select * from launches where status=4").fetchall()


def getLaunchCapacity(id):
    cur = connectDb()
    rocketCapacity = cur.execute(
        f"select rockets.maxWeight from launches join rockets on rockets.id = launches.rocketId where launches.id = {id}").fetchone()[0]
    rocketLoad = cur.execute(
        f"select sum(weight) from launches join petitions on launches.id = petitions.launchId where launches.id = {id}").fetchone()[0]
    if not rocketLoad:
        rocketLoad = 0
    return rocketCapacity - rocketLoad


def getLaunchLoad(id):
    cur = connectDb()
    rocketLoad = cur.execute(
        f"select sum(weight) from launches join petitions on launches.id = petitions.launchId where launches.id = {id}").fetchone()[0]
    if not rocketLoad:
        rocketLoad = 0
    return rocketLoad


def getLaunchDeadline(id):
    cur = connectDb()
    infoFetch = cur.execute(
        f"select startDate, days from launches where id = {id}").fetchone()
    date = datetime.strptime(infoFetch[0], "%Y-%m-%d")
    days = timedelta(days=infoFetch[1])
    return date + days


''' Funciones de peticiones '''


def assignPetitionsFinalDate(idPetition, finalDate):
    cur = connectDb()
    cur.execute(
        f"update petitions set  finalDate=date('{finalDate}') where id = {idPetition}")
    saveChanges(cur)


def addPetition(descId, desc, weight, days):
    cursor = connectDb()
    date = getDate()
    cursor.execute(
        f"INSERT INTO petitions (desc_id, description, weight, days, startDate) VALUES ('{descId}', '{desc}', {weight}, {days}, date('{date}'))")
    saveChanges(cursor)


def getAllPetitions():
    cursor = connectDb()
    return cursor.execute("select * from petitions").fetchall()


def getPetitions(assigned=False, fail=False):
    cursor = connectDb()
    if fail:
        return cursor.execute("select * from petitions where status=4").fetchall()
    if not assigned:
        return cursor.execute("select * from petitions where launchid is null and finalDate is null").fetchall()
    return cursor.execute("select * from petitions where launchid is NOT null and finalDate is null").fetchall()


def getHistoricPetitions(delivered=True):
    cursor = connectDb()
    if delivered:
        return cursor.execute("select * from petitions where status = 3").fetchall()
    return cursor.execute("select * from petitions where status = 4 and finalDate is NOT null").fetchall()


def countPetitions(assigned=False):
    cur = connectDb()
    if not assigned:
        return cur.execute("select count(*) from petitions where launchid is null and finalDate is null").fetchone()[0]
    return cur.execute("select count(*) from petitions where launchid is not null and finalDate is null").fetchone()[0]


def countHistoricPetitions(delivered=True):
    cur = connectDb()
    if delivered:
        return cur.execute("select count(*) from petitions where status = 3").fetchone()[0]
    return cur.execute("select count(*) from petitions where status = 4 and finalDate is not null").fetchone()[0]


def getPetitionsByLaunch(idLaunch):
    cur = connectDb()
    return cur.execute(f"select * from petitions where launchId = {idLaunch}").fetchall()


def deletePetition(idPetition):
    cur = connectDb()
    cur.execute(f"delete from petitions where id = {idPetition}")
    saveChanges(cur)


def editPetition(petitionId, descId, desc, weight, days):
    cur = connectDb()
    cur.execute(
        f"update petitions set desc_id = '{descId}', description = '{desc}', weight = {weight}, days = {days} where id = {petitionId}")
    saveChanges(cur)


def getPetitionsByDays(assigned=False):
    cursor = connectDb()
    if not assigned:
        return cursor.execute("select * from petitions where (launchId is null and finalDate is null) order by days asc").fetchall()
    return cursor.execute("select * from petitions order by days asc").fetchall()


def sendPetition(idPetition):
    cur = connectDb()
    cur.execute(f"update petitions set  status=2  where id = {idPetition}")
    saveChanges(cur)


def arrivePetition(idPetition):
    cur = connectDb()
    cur.execute(f"update petitions set status=3  where id = {idPetition}")
    saveChanges(cur)


def failPetition(idPetition):
    cur = connectDb()
    cur.execute(f"update petitions set status=4  where id = {idPetition}")
    saveChanges(cur)


def getPetitionDays(idPetition):
    cur = connectDb()
    return cur.execute(f"select days from petitions where id = {idPetition}").fetchone()[0]


def assignPetition(idPetition, idLaunch):
    cur = connectDb()
    cur.execute(
        f"update petitions set launchid={idLaunch} where id = {idPetition}")
    saveChanges(cur)


def getPetitionDeadline(id):
    cur = connectDb()
    infoFetch = cur.execute(
        f"select startDate, days from petitions where id = {id}").fetchone()
    date = datetime.strptime(infoFetch[0], "%Y-%m-%d")
    days = timedelta(days=infoFetch[1])
    return date + days


''' Funciones de acciones '''


def petitionFitOnLaunch(idPetition, idLaunch):
    cur = connectDb()
    petitionWeight = cur.execute(
        f"select weight from petitions where id = {idPetition}").fetchone()[0]
    rocketCapacity = cur.execute(
        f"select rockets.maxWeight from launches join rockets on rockets.id = launches.rocketId where launches.id = {idLaunch}").fetchone()[0]
    rocketLoad = cur.execute(
        f"select sum(weight) from launches join petitions on launches.id = petitions.launchId where launches.id = {idLaunch}").fetchone()[0]
    if not rocketLoad:
        rocketLoad = 0
    return petitionWeight <= (rocketCapacity-rocketLoad)


def petitionInTime(idPetition, idLaunch):
    cur = connectDb()
    petitionDays = cur.execute(
        f"select days from petitions where id = {idPetition}").fetchone()[0]
    launchDays = cur.execute(
        f"select days from launches where launches.id = {idLaunch}").fetchone()[0]
    return petitionDays >= launchDays
