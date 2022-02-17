from apscheduler.schedulers.background import BackgroundScheduler # automated repair


def printScreen():
    print('Hello!')

def checkIfLeaderAlive():
    print('Check leader')

def setupEvents():
    scheduler = BackgroundScheduler()
    
    # Setup jobs here
    scheduler.add_job(func=printScreen, trigger="interval", seconds=10, id='printerScreen')
    scheduler.add_job(func=checkIfLeaderAlive, trigger="interval", seconds=10, id='checkIfLeaderAlive')

    #Start scheduler
    scheduler.start()
