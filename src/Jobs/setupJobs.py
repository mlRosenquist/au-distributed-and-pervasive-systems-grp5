from apscheduler.schedulers.background import BackgroundScheduler # automated repair


def printScreen():
    print('Hello!')

def checkIfMasterAlive():
    print('Check master')

def setupEvents():
    scheduler = BackgroundScheduler()
    
    # Setup jobs here
    scheduler.add_job(func=printScreen, trigger="interval", seconds=10, id='printerScreen')
    scheduler.add_job(func=checkIfMasterAlive, trigger="interval", seconds=10, id='checkIfMasterAlive')

    #Start scheduler
    scheduler.start()
