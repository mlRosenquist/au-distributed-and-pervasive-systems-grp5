import threading, time, random, os, sys

import numpy as np
from numpy import array

class Nodes(object):
    _instance = None
    _leader = -1
    _mutex = threading.Lock()
    _nodesList = []

    _haltedBy = 0
    _states = {"down", "reorganizing", "normal", "election"}
    _currentState = "down"

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def getLeader(class_) -> int:
        if(class_._leader == -1):
            raise Exception('Leader is not initialized', f'Value set to default: {class_._leader}')

        return class_._leader

    def setLeader(class_, leader: int):
        class_._mutex.acquire()
        class_._leader = leader
        class_._mutex.release()

    def generateFriendsNodesList(class_) -> None:
        me = os.getenv('NODE_ID')
        totalNodes = os.getenv('NO_NODES')

        # If it runs in debug mode, assign none exiting enviourment variables:
        if __debug__:
            me = 1
            totalNodes = 7

        if(me == None):
            raise Exception('Local NODE_ID not set', f'Value set to default: {me}')
        if(totalNodes == None):
            raise Exception('Local NO_NODES not set', f'Value set to default: {me}')

        for node in range(totalNodes):
            if(node == me):
                continue
            class_._nodesList.append(node)

    def getFriendsNodesList(class_) -> array:
        if(class_._nodesList == []):
            raise Exception('Node list not yet set', f'Value set to default: {class_._nodesList}')
        return class_._nodesList

    def getSelfId() -> int:
        if __debug__:
            return 1
        self_id = os.getenv('NODE_ID')
        return int(self_id)

    def getHigherPriorityNodesThanSelf(class_) -> array:
        higher = [node for node in class_._nodesList if node > class_.getSelfId()]
        return higher

    def getHaltedBy(class_) -> int:
        return class_._haltedBy

    def setHaltedBy(class_, haltedBy: int):
        class_._haltedBy = haltedBy

    def isState(class_, stateToChack: str) -> bool:
        return stateToChack == class_._currentState

    def setState(class_, wantedState: str):
        class_._currentState = wantedState