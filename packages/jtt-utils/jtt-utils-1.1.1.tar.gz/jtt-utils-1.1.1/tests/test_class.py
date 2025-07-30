class A:
    def __init__(self,start):
        self.value = start
        self.make_method()
    def getX(self):
        return self.value ** 2

    def get_c(self,name):
        assert name == 'cc'
        return '%s %d' % (name,self.getX())
    def setX(self,value):
        self.value = value
    X = property(getX,setX)  #

    def make_method(self):
        bb ='bb'
        def make_func(name):
            def _method(self):

                return self.get_c(name)

            return _method

        setattr(self.__class__,'b',property(make_func(bb)))

a =A(5)
print(a.X)
print(a.b)
