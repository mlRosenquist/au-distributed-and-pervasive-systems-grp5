from http import client
from flask import request
from numpy import array
import requests

from Domain.Nodes import Nodes

class httpClient:

    # Immediate procedures
    def areYouThere(self, target_i: int) -> bool:
        targetEndpoint = self.getEndpoint(target_i)

        r = requests.get(f'{targetEndpoint}/areYouThere', timeout=10)
        print(f'Received status code: {r.status_code}')        
        if(r.status_code != 200):
            return False

        return True

    def startElection(self, target_i: int) -> bool:
        targetEndpoint = self.getEndpoint(target_i)

        r = requests.get(f'{targetEndpoint}/election', timeout=10)
        print(f'Received status code: {r.status_code}')
    
    # Immediate procedures
    def areYouNormal(self, target_i) -> int:
        targetEndpoint = self.getEndpoint(target_i)

        r = requests.get(f'{targetEndpoint}/areYouNormal', timeout=10)

        return r.status_code

    # Immediate procedures
    def halt(self, target_i) -> int:
        targetEndpoint = self.getEndpoint(target_i)

        data = {}
        data['sender_j'] = Nodes().getSelfId()
        r = requests.post(f'{targetEndpoint}/halt', json=data, timeout=10)

        return r.status_code

    # Immediate procedures
    def newCoordinator(self, target_i) -> None:
        targetEndpoint = self.getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        r = requests.post(f'{targetEndpoint}/newCoordinator', json=data, timeout=10)

        return r.status_code

    # Immediate procedures
    def ready(self, target_i) -> int:
        targetEndpoint = self.getEndpoint(target_i)
        sender_j = Nodes().getSelfId()
        
        data = {}
        data['sender_j'] = sender_j
        data['work_x'] = "working"
        r = requests.post(f'{targetEndpoint}/ready', json=data, timeout=10)

        return r.status_code

    async def election(self):       
        if(Nodes().isState(Nodes().states.election)):
            return

        # Get nodes with higher ids for election process
        higherNodes_j = Nodes().getHigherPriorityNodesThanSelf()

        higherNodeReponseOk = False
        haltedBy = None
        # Check if any higher node ids are alive
        for nodeId in higherNodes_j:
            print(f'Contaction node: {nodeId}')
            areYouThere = self.areYouThere(nodeId)
            
            if(areYouThere):
                self.startElection(nodeId)
                higherNodeReponseOk = True
                haltedBy = nodeId

        if(higherNodeReponseOk):
            # Should be halted when we get response from higher node 
            #Nodes().setState(Nodes().states.election)
            #Nodes().setHaltedBy(haltedBy)
            return
            

        print('No contact, Initialize i am the leader')
        # We are highest priority node alive
        # Halting all lower priority nodes
        self.stop()
        Nodes().setState(Nodes().states.election)
        Nodes()._haltedBy = Nodes().getSelfId()
        # Set
        lowerPriority = Nodes().getLowerPriorityNodesThanSelf()
        Nodes()._haltedUpNodes = []

        for nodeId in lowerPriority:
            response_statusCode = self.halt(nodeId)
            if(response_statusCode == 200):
                Nodes()._haltedUpNodes.append(nodeId)

        Nodes().setCoordinator(Nodes().getSelfId())

        newState = Nodes().states.reorganizing
        Nodes().setState(newState)

        for nodeId in Nodes()._haltedUpNodes:
            response_statusCode = self.newCoordinator(nodeId)
            if(response_statusCode == 500):
                await self.election()
                return

        for nodeId in Nodes()._haltedUpNodes:
            response_statusCode = self.ready(nodeId)
            if(response_statusCode == 500):
                await self.election()
                return
        
        newState = Nodes().states.normal
        Nodes().setState(newState)

    def electionSync(self):
        print(Nodes().getState())
        print(Nodes().isState(Nodes().states.election))
        if(Nodes().isState(Nodes().states.election)):
            return
        # Get nodes with higher ids for election process
        higherNodes_j = Nodes().getHigherPriorityNodesThanSelf()

        higherNodeReponseOk = False
        # Check if any higher node ids are alive
        for nodeId in higherNodes_j:
            print(f'Contaction node: {nodeId}')
            areYouThere = self.areYouThere(nodeId)
            if (areYouThere):
                self.startElection(nodeId)
                higherNodeReponseOk = True

        if (higherNodeReponseOk):
            return

        print('No contact, Initialize i am the leader')
        # We are highest priority node alive
        # Halting all lower priority nodes
        self.stop()
        Nodes().setState(Nodes().states.election)
        Nodes()._haltedBy = Nodes().getSelfId()
        # Set
        lowerPriority = Nodes().getLowerPriorityNodesThanSelf()
        Nodes()._haltedUpNodes = []

        for nodeId in lowerPriority:
            response_statusCode = self.halt(nodeId)
            if (response_statusCode == 200):
                Nodes()._haltedUpNodes.append(nodeId)

        Nodes().setCoordinator(Nodes().getSelfId())

        newState = Nodes().states.reorganizing
        Nodes().setState(newState)

        for nodeId in Nodes()._haltedUpNodes:
            response_statusCode = self.newCoordinator(nodeId)
            if (response_statusCode == 500):
                self.election()
                return

        for nodeId in Nodes()._haltedUpNodes:
            response_statusCode = self.ready(nodeId)
            if (response_statusCode == 500):
                self.election()
                return

        newState = Nodes().states.normal
        Nodes().setState(newState)


    def check(self):
        currentState = Nodes()._currentState
        coordinationLeader = Nodes().getCoordinator()

        if(currentState == Nodes().states.normal and coordinationLeader == Nodes().getSelfId()):
            allNodesButOurself = Nodes().getFriendsNodesList()
            for node in allNodesButOurself:
                response_statusCode = self.areYouNormal(node)
                if(response_statusCode == 500):
                    continue
                if(response_statusCode != 200):
                    self.election()
                    return
                    


    def recovery(self):
        Nodes()._haltedBy = -1
        self.election()

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

    def getEndpoint(self, target_id: int) -> str:
        return f'http://node{target_id}-svc:5000'

        