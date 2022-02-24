from http import client
from flask import request
from numpy import array
import requests

from Domain.Nodes import Nodes

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

    def election(self):
        # Get nodes with higher ids for election process
        allNodes = Nodes().getFriendsNodesList()
        potentialLeaders = []

        # Check if any higher node ids are alive
        for nodeId in allNodes:
            startElection = self.startElection(nodeId)
            if startElection:
                potentialLeaders.append(nodeId)

        if potentialLeaders:
            #become leader...
            #for nodeId in Nodes().:
            #    response_statusCode = self.newCoordinator(nodeId)
            #    if(response_statusCode == 500):
            #        self.election()
            #        return

    def timeout(self):
        currentState = Nodes()._currentState

        if(currentState == Nodes()._currentState.normal or currentState == Nodes()._currentState.reorganizing):
            coordinater = Nodes().getCoordinator()
            check = self.areYouThere(coordinater)

            if(check == False):
                self.election()
        else:
            self.election()

    def stop(self) -> None:
        wantedTask = Nodes().tasks.stopped
        Nodes().setTask(wantedTask)

    def _getEndpoint(target_id) -> str:
        return f'http://node{target_id}-svc:5000'

        