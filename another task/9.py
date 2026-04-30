class Vector():
    def __init__(self,x,y):
        self.__x = x
        self.__y = y 
    def print(self):
        print(f"{self.__x};{self.__y}")
    def __add__(self, other):
        return Vector(self.__x + other.__x, self.__y + other.__y)
    def __sub__(self, other):
        return Vector(self.__x - other.__x, self.__y - other.__y)

v1 = Vector(2,4)
v2 = Vector(4,8)
v3 = v1 + v2
v3.print()
v4 = v1 - v2
v4.print()