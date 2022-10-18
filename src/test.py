from peers import Peer
import unittest

class TestPeer(unittest.TestCase):
    def test_buy1(self):
        peer1 = Peer('1', 'seller', 'ns1', ['fish', 'boar', 'salt'], 2)
        peer1.buy()
        peer1.buy()
        assert peer1.buy() == False

    def test_buy2(self):
        peer1 = Peer('1', 'seller', 'ns1', ['fish', 'boar', 'salt'], 1)
        assert peer1.buy() == True

if __name__ == '__main__':
    unittest.main()