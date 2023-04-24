from sssyntax import utility as U
def test_prependGen():   
    h = (x for x in range(1,3))
    h = U.prependGen(0,h)
    assert ([*h]==[0,1,2])