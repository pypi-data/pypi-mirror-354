from enum import Enum
class AA(Enum):
    a1 ='a1'
    b1='b1'

a =AA('a1')
print(a)
class AType:
    e0=1
    e1=2

a = getattr(AType,'e0')


print(a)
class MyExcept(Exception):
    def __init__(self,code,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.code =code


try:
    raise MyExcept(code=1)
except Exception as e:
    print(str(e))

