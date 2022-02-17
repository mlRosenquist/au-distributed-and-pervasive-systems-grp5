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

        r = requests.get(targetEndpoint)
        
        if(r.status_code != 200):
            return False

        return True
    
    # Immediate procedures
    def areYouNormal(self, target_i):
        targetEndpoint = self._getEndpoint(target_i)

        r = requests.get(targetEndpoint)
        
        if(r.status_code != 200):
            return False

        return True

    # Immediate procedures
    def halt(self, target_i) -> None:
        targetEndpoint = self._getEndpoint(target_i)

        data = {}
        data['sender_j'] = Nodes().getSelfId()
        r = requests.post(targetEndpoint, data=data)

    # Immediate procedures
    def newCoordinator(self, target_i) -> None:
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        r = requests.post(targetEndpoint, data=data)

    # Immediate procedures
    def ready(self, target_i):
        targetEndpoint = self._getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        data['work_x'] = "Work"
        r = requests.post(targetEndpoint, data=data)

    def election(self):
        # Get nodes with higher ids for election process
        higherNodes_j = Nodes().getHigherPriorityNodesThanSelf()

        # Check if any higher node ids are alive
        for node in range(higherNodes_j):
            

    def check(self):
        print('test')

    def _getEndpoint(target_id) -> str:
        return f'http://node{target_id}-svc:5000'

        