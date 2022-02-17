from http import client
from flask import request
import requests

from Domain.Nodes import Nodes

class httpClient:

    def __init__(self) -> None:
        pass

    def areYouThere(self, target_i: int):
        selfId = Nodes().getSelfId()

        r = requests.get()

        print('test')

    def areYouNormal(self):
        print('test')

    def halt(self):
        print('test')

    def newCoordinator(self):
        print('test')

    def check(self):
        print('test')

    def election(self):
        print('test')

    def ready(self):
        print('test')

    def _getEndpoint(target_id) -> str:
        return f'http://node{target_id}-svc:5000'
        