from http import client
from flask import request
from numpy import array
import requests
from Domain.Nodes import *

class httpClient:

    def __init__(self) -> None:
        pass

    # Immediate procedures
    async def startElection(self, target_i: int) -> bool:
        targetEndpoint = self.getEndpoint(target_i)
        sender_j = Nodes().getSelfId()

        data = {}
        data['sender_j'] = sender_j
        r = requests.get(f'{targetEndpoint}/startElection', json=data, timeout=10)
        
        return r.status_code

    # Immediate procedures
    def newCoordinator(self, target_i: int) -> None:
        targetEndpoint = self.getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        r = requests.post(f'{targetEndpoint}/newCoordinator', json=data, timeout=10)

        return r.status_code

    def takeover(self, target_i: int):
        targetEndpoint = self.getEndpoint(target_i)
        r = requests.post(f'{targetEndpoint}/takeover', timeout=10)

    async def election(self):
        Nodes().raiseElectionFlag()
        # Get nodes with higher ids for election process
        allNodes = Nodes().getFriendsNodesList()
        potentialLeaders = []

        # Check if any higher node ids are alive
        for nodeId in allNodes:
            electionStatusCode = await self.startElection(nodeId)
            if electionStatusCode == 200:
                potentialLeaders.append(nodeId)

        if potentialLeaders:
            highestPriorityNode = max(potentialLeaders)
            self.takeover(highestPriorityNode)
        else:
            Nodes()._coordinator = Nodes().getSelfId()
            for nodeId in Nodes().generateFriendsNodesList():
                self.newCoordinator(nodeId)
            Nodes().lowerElectionFlag()

    def checkHigherOrBecomeCoordinator(self):
        potentialLeaders = []

        for nodeId in Nodes().getHigherPriorityNodesThanSelf():
            checkStatus = self.startElection(nodeId)
            if checkStatus == 200:
                potentialLeaders.append(nodeId)

        if potentialLeaders:
            highestPriorityNode = max(potentialLeaders)
            self.takeover(highestPriorityNode)
        else:
            for nodeId in Nodes().getFriendsNodesList():
                self.newCoordinator(nodeId)

    def getEndpoint(self, target_id: int) -> str:
        return f'http://node{target_id}-svc:5000'

        