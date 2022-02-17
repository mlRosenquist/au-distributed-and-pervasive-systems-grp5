from http import client
from flask import request
from numpy import array
import requests

from Domain.Nodes import Nodes

class httpClient:

    def __init__(self) -> None:
        pass

    # Immediate procedures
    def areYouThere(self, target_i: int) -> bool:
        targetEndpoint = self._getEndpoint(target_i)

        r = requests.get(targetEndpoint, timeout=10)
        
        if(r.status_code != 200):
            return False

        return True
    
    # Immediate procedures
    def areYouNormal(self, target_i):
        targetEndpoint = self._getEndpoint(target_i)

        r = requests.get(targetEndpoint, timeout=10)
        
        if(r.status_code != 200):
            return False

        return True

    # Immediate procedures
    def halt(self, target_i) -> None:
        targetEndpoint = self._getEndpoint(target_i)

        data = {}
        data['sender_j'] = Nodes().getSelfId()
        r = requests.post(targetEndpoint, data=data, timeout=10)

    # Immediate procedures
    def newCoordinator(self, target_i) -> None:
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        r = requests.post(targetEndpoint, data=data, timeout=10)

    # Immediate procedures
    def ready(self, target_i):
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        data['work_x'] = "Work"
        r = requests.post(targetEndpoint, data=data, timeout=10)

    def election(self):
        # Get nodes with higher ids for election process
        higherNodes_j = Nodes().getHigherPriorityNodesThanSelf()

        # Check if any higher node ids are alive
        for nodeId in range(higherNodes_j):
            areYouThere = self.areYouThere(nodeId)
            if(areYouThere):
                return

        # We are highest priority node alive
        # Halting all lower priority nodes
        self.stop()
        Nodes().setState(Nodes().states.election)
        Nodes()._haltedBy = Nodes().getSelfId()
        # Set
        
        


    def check(self):
        print('test')

    def stop(self) -> None:
        wantedTask = Nodes().tasks.stopped
        Nodes().setTask(wantedTask)

    def _getEndpoint(target_id) -> str:
        return f'http://node{target_id}-svc:5000'

        