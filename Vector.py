
class Vector():
	def __init__(self,x,y,m=1):
		self.x=x
		self.y=y
		self.m=m
	def __add__(self,other):
		return Vector(self.x+other.x,self.y+other.y,self.m)

	def __radd__(self,other):
		return Vector(self.x+other,self.y+other,self.m)

	def __mul__(self,other):
		return Vector(self.x*other,self.y*other,self.m)

	def __rmul__(self,other):
		return Vector(other*self.x,other*self.y,self.m)

	def __str__(self):
		return '[%s,%s,%s]' % (round(self.x, 2), round(self.y, 2),round(self.m, 2))
	def __eq__(self,other):
		if self.__class__ == other.__class__ and self.x == other.x and self.y == other.y:
			return True
		return False
	def __ne__(self,other):
		if self.__class__ != other.__class__ and self.x != other.x and self.y != other.y:
			return True
		return False


	def hit(self,other):
		V1,V2=self.x,other.x
		self.x=((self.m-other.m)*V1+2*other.m*V2)/(self.m+other.m)
		other.x=((other.m-self.m)*V2+2*self.m*V1)/(self.m+other.m)

	def wall_hit(self):
		self.x=-self.x
		

	def length(self):
		return (self.x**2+self.y**2)**0.5

	def pulse(self):
		return Vector(self.x*self.m,self.y*self.m)

	def turn(self,delta_X,delta_Y): 
		""" поворот системы координат при неизменном направлении вектора delta_X, delta_Y- разницы координат """
		hypot=(delta_X**2+delta_Y**2)**0.5
		COS=delta_X/hypot
		SIN=delta_Y/hypot
		VX=self.x*COS+self.y*SIN
		VY=self.y*COS-self.x*SIN
		return Vector(VX,VY,self.m)

	def single_turn(self,delta_X,delta_Y):
		""" поворот вектора в направлении x,y, где delta_X,delta_Y - разницы координат """
		hypot=(delta_X**2+delta_Y**2)**0.5
		COS=1 if hypot==0 else delta_X/hypot
		SIN=0 if hypot==0 else delta_Y/hypot
		VX=self.length()*COS
		VY=self.length()*SIN
		return Vector(VX,VY,self.m)


	def retrn(self,delta_X,delta_Y):
		return self.turn(delta_X,-delta_Y)



def test():

	V1=Vector(-3,4)

	V2=Vector(4,1)
	V3=Vector(20,3)

	V1st=V1.single_turn(5,6)
	print('Длинна вектора V1 %s = %s' % (V1,V1.length()))
	print('Длинна вектора V1st %s = %s' % (V1st,V1st.length()))
	print('V*7=',V1*7)
	print('7*v=',7*V1)
	print('Длинна вектора V2 %s = %s' % (V2,V2.length()))
	V1t=V1.turn(8,6)
	print('V1 turn',V1t,V1t.length())
	V2t=V2.turn(8,6)
	print('V2 turn',V2t,V2t.length())
	V1r=V1t.retrn(1,1)
	print('V1 return',V1r,V1r.length())
	V2r=V2t.retrn(8,6)
	print('V2 return',V2r,V2r.length())
	print('++++++++++++++++')
	V1t.hit(V2t)
	print('V1t hit V2t',V1t,V2t,V1t.length(),V2t.length())
	V1r=V1t.retrn(8,6)
	print('V1 return',V1r,V1r.length())
	V2r=V2t.retrn(8,6)
	print('V2 return',V2r,V2r.length())
	print('======================================+')
	V1=Vector(-3,4,5)
	V2=Vector(4,1,3)
	V3=Vector(20,3)


	print('Длинна вектора %s = %s' % (V1,V1.length()))
	print('Вектор импульса %s = %s' % (V1, V1.pulse()))
	print('Значение импульса %s = %s' % (V1, V1.pulse().length()))
	print('Значение импульса %s = %s' % (V1, V1.length()*V1.m))
	print('Длинна вектора %s = %s' % (V2,V2.length()))
	V1t=V1.turn(8-0,6-0)
	print('V1 turn',V1t,V1t.length())
	V2t=V2.turn(8,6)
	print('V2 turn',V2t,V2t.length())
	V1r=V1t.retrn(8,6)
	print('V1 return',V1r,V1r.length())
	V2r=V2t.retrn(8,6)
	print('V2 return',V2r,V2r.length())
	print('++++++++++++++++')
	V1t.hit(V2t)
	print('V1t hit V2t',V1t,V2t,V1t.length(),V2t.length())
	V1r=V1t.retrn(8,6)
	print('V1 return',V1r,V1r.length())
	V2r=V2t.retrn(8,6)
	print('V2 return',V2r,V2r.length())



if __name__ == '__main__':
	test()