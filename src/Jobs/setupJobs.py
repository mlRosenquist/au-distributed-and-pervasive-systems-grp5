import asyncio
import random
import time

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from Domain.Nodes import Nodes
from Domain.httpClient import httpClient

nodes = Nodes()
client = httpClient()

def printScreen():
    print('Hello!')

# async def simulateNodeIsDown():
#     print('Setting State to down')
#     nodes.setState(nodes.states.down)
#     downTime = random.randint(5, 10)
#     print(f'Sleeping in {downTime} seconds')
#     await asyncio.sleep(downTime)
#     await client.election()

def simulateNodeIsDown():
    if (nodes.getSelfId() == len(nodes.getFriendsNodesList()) + 1):
        print('Simulating node is down')
        print('Setting State to down', flush=True)
        nodes.setState(nodes.states.down)
        downTime = random.randint(20, 30)
        print(f'Sleeping in {downTime} seconds', flush=True)

        time.sleep(downTime)
        client.electionSync()

def checkLeaderIsAlive():
    if( nodes.getCoordinator() != -1 and
        nodes.getSelfId() != nodes.getCoordinator()):
        
        print('Checking that the leader is alive')
        coordinatorIsThere = client.areYouThere(nodes.getCoordinator())
        if(not coordinatorIsThere):
            client.electionSync()

def setupEvents():
    downInterval = random.randint(10, 15)
    checkLeaderInterval = random.randint(5, 10)
    print(f'We simulating the node to be down every {downInterval} seconds', flush=True)
    print(f'Checking leader is alive every {downInterval} seconds', flush=True)

    backgroundScheduler = BackgroundScheduler()
    backgroundScheduler.add_job(func=simulateNodeIsDown, trigger="interval", seconds=downInterval, id='simulateNodeIsDown')
    backgroundScheduler.add_job(func=checkLeaderIsAlive, trigger="interval", seconds=checkLeaderInterval, id='checkLeaderIsAlive')
    backgroundScheduler.start()
