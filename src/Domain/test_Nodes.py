from unittest import TestCase

from src.Domain.Nodes import Nodes


class TestNodes(TestCase):
    def setUp(self):
        self._uut = Nodes()

    def test_get_leader(self):
        self._uut.setLeader(1)
        leader = self._uut.getLeader()
        self.assertEqual(leader, 1)

    def test_get_leader_exception(self):
        #with self.assertRaises(Exception):
        #   leader = self._uut.getLeader()
        pass

    def test_generate_friends_nodes_list(self):
        self._uut.generateFriendsNodesList(me=1, totalNodes=3)
        friends = self._uut.getFriendsNodesList()
        self.assertListEqual(friends, list([2,3]))


    def test_get_self_id(self):
        pass

    def test_get_higher_priority_nodes_than_self(self):
        pass

    def test_get_halted_by(self):
        pass

    def test_set_halted_by(self):
        pass

    def test_is_state(self):
        pass

    def test_set_state(self):
        pass

    def test_set_task(self):
        pass
