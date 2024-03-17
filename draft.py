from unittest.mock import patch
from unittest.mock import MagicMock


class ClassName1:
    pass


class ClassName2:
    pass


@patch('module.ClassName2')
@patch('module.ClassName1')
def test_class(MockClass1, MockClass2):
    ClassName1()
    ClassName2()
    assert MockClass1 is ClassName1
    assert MockClass2 is ClassName2
    assert MockClass1.called
    assert MockClass2.called


#########################################################


class ProductionClass:

    def method(self):
        return None


thing = ProductionClass()
x = thing.method = MagicMock(return_value=3)
y = thing.method(1, 2, 3, key='value')

q = thing.method.assert_called_with(1, 2, 3, key='value')

print(x)
print(y)
print(q)


