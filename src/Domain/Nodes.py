import enum
import threading, time, random, os, sys

import numpy as np
from numpy import array

class Nodes(object):
    _instance = None
    _mutex = threading.Lock()

    # is S(i)c
    _coordinator = -1
    # all nodes but i
    _nodesList = []
    # is S(i)h
    _haltedBy = -1
    # is S(i)Up
    _haltedUpNodes = []

    class states(enum.Enum):
        down = "down"
        reorganizing = "reorganizing"
        normal = "normal"
        election = "election"

    class tasks(enum.Enum):
        working = "working"
        stopped = "stopped"
    # is S(i)s
    _currentState = states.normal
    # is S(i)x
    _currentTask = tasks.working

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def getCoordinator(class_) -> int:
        if(class_._coordinator == -1):
            raise Exception('Leader is not initialized', f'Value set to default: {class_._coordinator}')

        return class_._coordinator

    def setCoordinator(class_, coordinator: int):
        print(f'Node: {class_.getSelfId()}: coordinator changed from Node ID: {class_.getCoordinator()} to Node ID: {coordinator}')
        class_._coordinator = coordinator
        class_._mutex.release()

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

    def getSelfId(class_) -> int:
        self_id = os.getenv('NODE_ID')
        return int(self_id)

    def getHigherPriorityNodesThanSelf(class_) -> array:
        higher = [node for node in class_._nodesList if node > class_.getSelfId()]
        return higher

    def getHaltedBy(class_) -> int:
        return class_._haltedBy

    def setHaltedBy(class_, haltedBy: int):
        class_._haltedBy = haltedBy

    def isState(class_, stateToChack: states) -> bool:
        return stateToChack == class_._currentState

    def setState(class_, wantedState: states):
        print(f'Node: {class_.getSelfId()}: state changed from: {class_.getState()} to: {wantedState}')
        class_._currentState = wantedState


    def getState(class_):
        return class_._currentState

    #def isTask(class_, stateToChack: tasks) -> bool:
    #    return stateToChack == class_._currentTask

    def setTask(class_, wantedTask: tasks):
        class_._currentTask = wantedTask

    def getLowerPriorityNodesThanSelf(class_) -> array:
        lowerPriority = [node for node in class_._nodesList if node < class_.getSelfId()]
        return lowerPriority;