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

    def test_lookup1(self):
        peer1 = Peer('1', 'seller', 'ns1', ['fish', 'boar', 'salt'], 1)
        peer1.lookup('1', 'fish', 1, ['2', '3'])

        pass
    
    def test_lookup2(self):
        peer1 = Peer('1', 'seller', 'ns1', ['fish', 'boar', 'salt'], 1)
        peer1.lookup('1', 'fish', 0, ['2', '3'])
        pass

        
if __name__ == '__main__':
    unittest.main()