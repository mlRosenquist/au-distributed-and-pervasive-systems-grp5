class Nodes(object):
    _instance = None
    _leader = -1

    def __new__(class_, *args, **kwargs):
        if not isinstance(class_._instance, class_):
            class_._instance = object.__new__(class_, *args, **kwargs)
        return class_._instance

    def getLeader(class_) -> int:
        if(class_._leader == -1):
            raise Exception('Leader is not initialized', f'Value set to default: {class_._leader}')

        return class_._leader

    def setLeader(class_, leader: int):
        class_._leader = leader


    
