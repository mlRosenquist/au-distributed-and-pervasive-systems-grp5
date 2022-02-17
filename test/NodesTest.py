from lib2to3.pytree import Node
import unittest
import sys
sys.path.append(".")

from numpy import array
from src.Domain.Nodes import Nodes

class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self._uut = Nodes()
    
    # setLeader & getLeader
    def leader_is_updated(self):
        self._uut.setLeader(1)
        leader = self._uut.getLeader()
        self.assertEqual(leader, 1)

    def leader_is_not_set_throwsException(self):
        with self.assertRaises(Exception):
            leader = self._uut.getLeader()

    # generateFriendsNodeList
    def friends_Node_List_isGenerated_Correctly(self):
      self._uut.generateFriendsNodesList(1, 3)
      friends = self._uut.getFriendsNodesList()
      array.


if __name__ == '__main__':
    unittest.main()