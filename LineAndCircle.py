
import sys
import pygame
import math
from Vector import Vector


# данные окружности

Cx=300
Cy=300
Cr=100

cir=[Cx,Cy,Cr]

# данные прямой

Lx=340
Ly=370
L_an=20

line=[Cx,Cy,Cr]

def quart(angle):
	angle=angle%360
	Pos_X=-1 if 90<angle<=270 else 1
	Pos_Y=1 if 0<=angle<180 else -1
	return Pos_X,Pos_Y


def cross(cir,line):
	""" функция определяет точки пересечения прямой и окружности
	окружность задана в виде [x,y,r]
	прямая задана в виде [x,y,a], где "х"" и "у" кординаты точки на прямой
	"а" угол в градусах между прямой и горизонталью"""

	alpha=math.pi*line[2]/180

	# разница координат между точкой на прямой и ценром окружности
	A=line[0]-cir[0] 
	B=line[1]-cir[1]

	pos_X,pos_Y= quart(line[2])

	if (line[2]/90)%2 == 1:
		x=x1=A

		y=pos_Y*(cir[2]**2-x**2)**0.5
		y1=-y

	elif (line[2]/90)%2 == 0:
		y=y1=B
		x=pos_X*(cir[2]**2-y**2)**0.5
		x1=-x

	else:
		Cx=B-A*math.tan(alpha)
		Dax=Cx*math.sin(2*alpha)
		Dbx=(Cx**2-cir[2]**2)*((math.cos(alpha))**2)
		Dx=Dax**2-4*Dbx

		if Dx<0: return False #  прямая не пересекает окружность

		x=(-Dax+(Dx**0.5)*pos_X)/2
		x1=(-Dax-(Dx**0.5)*pos_X)/2

		Cy=A-B/math.tan(alpha)
		Day=Cy*math.sin(2*alpha)
		Dby=(Cy**2-cir[2]**2)*((math.sin(alpha))**2)
		Dy=Day**2-4*Dby

		if Dy<0: return False

		y=(-Day+(Dy**0.5)*pos_Y)/2
		y1=(-Day-(Dy**0.5)*pos_Y)/2


	x+=cir[0]
	y+=cir[1]

	x1+=cir[0]
	y1+=cir[1]

	return [x,y],[x1,y1]

# Графическое тестирование функции
def test(cir,line):
	RED=(240,10,0)
	BLUE=(10,10,240)
	GREEN=(20, 80, 30)
	IVORY=(220, 225, 205)
	WOOD=(100, 40, 00)
	L_WOOD=(170, 100, 20)

	pygame.init()

	width = 600
	height = 600

	screen = pygame.display.set_mode((width, height))

	pygame.display.set_caption('Line and Circle')
	
	# расчет точек линии линии
	angle=math.pi*line[2]/180
	xs=line[0]-math.cos(angle)*400
	ys=line[1]-math.sin(angle)*400

	xe=line[0]+math.cos(angle)*400
	ye=line[1]+math.sin(angle)*400

	screen.fill((GREEN))

	pygame.draw.circle(screen, IVORY, (int(cir[0]),int(cir[1])),int(cir[2]),2)
	pygame.draw.line(screen, (0,0,0), [cir[0],0], [cir[0],600], 1)
	pygame.draw.line(screen, (0,0,0), [0,cir[1]], [600,cir[1]], 1)


	pygame.draw.line(screen, L_WOOD, [xs,ys], [xe,ye], 2)
	pygame.draw.circle(screen, WOOD, (int(line[0]), int(line[1])),3)

	if cross(cir,line): 
	
		[x,y],[x1,y1]=cross(cir,line)
	
		pygame.draw.circle(screen, RED, (int(x), int(y)),6,2)
		pygame.draw.circle(screen, BLUE, (int(x1), int(y1)),6,2)
		

	else:	
		pygame.display.set_caption('No crossing points') 

	pygame.display.flip()


if __name__ == '__main__':
	circle=[300,300,200]
	line=[280,370,285]
	print (*line)
	test(circle,line)