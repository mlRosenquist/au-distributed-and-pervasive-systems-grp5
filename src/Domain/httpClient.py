from http import client
from flask import request
from numpy import array
import requests
import Nodes

class httpClient:

    def __init__(self) -> None:
        pass

    # Immediate procedures
    def startElection(self, target_i: int) -> bool:
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()

        data = {}
        data['sender_j'] = sender_j
        r = requests.get(targetEndpoint, json=data, timeout=10)
        
        if(r.status_code != 200):
            return False

        return True

    # Immediate procedures
    def newCoordinator(self, target_i) -> None:
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        r = requests.post(targetEndpoint, json=data, timeout=10)

        return r.status_code

    def takeover(self, target_i: int):
        targetEndpoint = self._getEndpoint(target_i)
        r = requests.post(targetEndpoint, timeout=10)

    def election(self):
        # Get nodes with higher ids for election process
        allNodes = Nodes().getFriendsNodesList()
        potentialLeaders = []

        # Check if any higher node ids are alive
        for nodeId in allNodes:
            electionStatusCode = self.startElection(nodeId)
            if electionStatusCode == 200:
                potentialLeaders.append(nodeId)

        if potentialLeaders:
            highestPriorityNode = max(potentialLeaders)
            self.takeover(highestPriorityNode)
        else:
            Nodes()._coordinator = Nodes().getSelfId()
            for nodeId in Nodes().getHigherPriorityNodesThanSelf():
                response_statusCode = self.newCoordinator(nodeId)
                if(response_statusCode == 500):
                    self.election()
                    return

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
            for nodeId in Nodes().generateFriendsNodesList():
                self.newCoordinator(nodeId)

    def _getEndpoint(target_id) -> str:
        return f'http://node{target_id}-svc:5000'

        