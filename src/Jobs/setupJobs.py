from apscheduler.schedulers.background import BackgroundScheduler # automated repair


def printScreen():
    print('Hello!')

def setupEvents():
    scheduler = BackgroundScheduler()
    
    # Setup jobs here
    scheduler.add_job(func=printScreen, trigger="interval", seconds=10, id='printer')

    #Start scheduler
    scheduler.start()
