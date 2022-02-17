import threading, time, random, os, sys

class Nodes(object):
    _instance = None
    _leader = -1
    _mutex = threading.Lock()
    _nodesList = []

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

    def generateNodesList(class_) -> None:
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


    
