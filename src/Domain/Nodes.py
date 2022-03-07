import enum
import threading, time, random, os, sys

import numpy as np
from numpy import array

class Nodes(object):
    _instance = None
    _mutex = threading.Lock()
    amountMessages = 0
    # is S(i)c
    _coordinator = -1
    # election flag
    _electionFlag = False
    # down flag
    _down = False
    # all nodes but i
    _nodesList = []

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def getCoordinator(class_) -> int:
        return class_._coordinator

    def setCoordinator(class_, coordinator: int):
        print(f'Node: {class_.getSelfId()}: coordinator changed from Node ID: {class_.getCoordinator()} to Node ID: {coordinator}')
        class_._coordinator = coordinator

    def generateFriendsNodesList(class_, me, totalNodes) -> None:
        if(me == None):
            raise Exception('Local NODE_ID not set', f'Value set to default: {me}')
        if(totalNodes == None):
            raise Exception('Local NO_NODES not set', f'Value set to default: {me}')

        for node in range(totalNodes):
            node = node + 1
            if(node == me):
                continue
            print(f'My nodeId: {me} - Added nodeId to nodelist: {node}')
            class_._nodesList.append(node)

    def getFriendsNodesList(class_) -> array:
        if(class_._nodesList == []):
            raise Exception('Node list not yet set', f'Value set to default: {class_._nodesList}')
        return class_._nodesList

    def getHigherPriorityNodesThanSelf(class_) -> array:
        higher = [node for node in class_._nodesList if node > class_.getSelfId()]
        return higher

    def getSelfId(class_) -> int:
        self_id = os.getenv('NODE_ID')
        return int(self_id)

    def raiseElectionFlag(class_):
        class_._electionFlag = True

    def lowerElectionFlag(class_):
        class_._electionFlag = False

    def isElecting(class_) -> bool:
        return class_._electionFlag