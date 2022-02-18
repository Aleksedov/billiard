import sys
import pygame
import math
from Vector import Vector
from LineAndCircle import cross

FPS=50
pattern=80
GREEN=(20, 80, 30)
IVORY=(220, 225, 205)
WOOD=(100, 40, 00)
L_WOOD=(170, 100, 20)
GRAY=(pattern,pattern,pattern)
BLACK=(0,0,0)
BLUE=(0, 0, 250)
RED=(250, 0, 0)

pygame.init()

width = 1300
height = 740

sc = pygame.display.set_mode((width, height))
sc.fill(WOOD)

#screen = pygame.Surface((90, 80))

table_surf=pygame.image.load('C:\Python\Games\Billiards\Table3.jpg').convert()
table_rect=table_surf.get_rect()


pygame.display.set_caption('Sedov')
clock = pygame.time.Clock()

# проверка на столкновение

def count_cue_hit(cue,ball): # расчет вектора шара после удара
	vec=Vector(0,0)
	V_cue=Vector(20*cue.force*math.cos(cue.angle),20*cue.force*math.sin(cue.angle)) # расчет вектора удара кием
	[Xh,Yh]=cross([ball.x,ball.y,ball.r],
				[cue.x,cue.y,180*cue.angle/math.pi])[0] # расчет точки попадания кием в шар, выбор только точки входа
	delta_X=ball.x-Xh
	delta_Y=ball.y-Yh
	V_cue=V_cue.turn(delta_X,delta_Y)
	vec.hit(V_cue)
	vec=vec.retrn(-delta_X,-delta_Y)
	return vec

def draw_help_line(cue,ball):	
	Ball_after_hit_speed=count_cue_hit(cue,ball)
	pygame.draw.line(sc, GREEN,  [ball.x,ball.y], [ball.x+Ball_after_hit_speed.x,ball.y+Ball_after_hit_speed.y], 1)

class Balls():
	"""объект шары, сотоящий из множества шаров"""
	def __init__(self,cue,*args,help_hit=0):
		self.claster=list(args)
		self.cue=cue
		self.loose=[]
		self.help_hit=help_hit
		self.player=0
		self.hit=0
		self.stop=1
		
	def __getitem__(self,i):
		return self.claster[i]

	def __len__(self):
		return len(self.claster)

	def add_ball(self,Ball):
		"""добавлене новых шаров"""
		self.claster.append(Ball)
		self.claster[0].color=GRAY

	def loose_ball(self,Ball):
		self.hit=1
		self.claster.remove(Ball)
		self.loose.append(Ball)
		Ball.r//=2
		Ball.y=Ball.r+5 if Ball.player else height-Ball.r-5
		Ball.x=125+(Ball.r*2+1)*len(self.loose)

	def count_entr(self):
		self.entropia=Vector(0,0)
		for i in self.claster:
			self.entropia+=i.speed
		entr=self.entropia.length()
		return int(entr) if int(entr)!=0 else False

	def hit_point(self,Ball,point):
		"""точки для удара"""
		self.cue.wait=1 # Переводит кий в режим выбора угла и силы удара
		self.cue.x=point[0]
		self.cue.y=point[1]
		self.hit_ball=Ball

	def stop_ap(self):
		if not self.hit: # переход хода если нет забитых шаров
			self.player=(self.player+1)%2
		self.hit=0
		self.stop=0

	def check_mouth(self): #  выбор главного шара
		"""проверка действий мыши"""
		if self.count_entr(): return
		if self.stop:	self.stop_ap()
		if not self.cue.wait: # если шар еще не выбран
			if pygame.mouse.get_pressed()[0]:
				clock.tick(5)
				pos=pygame.mouse.get_pos()

				for i in self.claster: 
					m_dist=((i.x-pos[0])**2+(i.y-pos[1])**2)**0.5
					if m_dist<i.r:
						self.hit_point(i,pos)
						return 

		if self.cue.wait: # если шар уже выбран
			if pygame.mouse.get_pressed()[2]: # отмена выбора шара выбран
				self.cue.wait=0
				return
			if pygame.mouse.get_pressed()[0]: # удар 
				self.hit_ball.speed=count_cue_hit(self.cue,self.hit_ball)
				self.stop=1
				self.cue.wait=0
				return

	def choose_pos(self): #  не в бильярде
		"""проверка положение мыши клавиатуры"""
		res=pygame.mouse.get_pos()
		if not self.cue.wait: # перемещение по столу
			self.cue.x=res[0]
			self.cue.y=res[1]
			#pygame.display.set_caption('Позиция X=%s, Y=%s' % (res[0],res[1]))
			return

		try:
			self.cue.angle=math.atan((res[1]-self.cue.y)/(res[0]-self.cue.x))# выбор угла удара
			if res[0]<self.cue.x:
				self.cue.angle+=math.pi
		
		except: self.cue.angle=math.pi

	def balls_static(self):

		for ball in self.loose:
			ball.draw()

		for i in range(len(self.claster)):
			self.claster[i].draw_shadow()

		for i in range(len(self.claster)):
			self.claster[i].draw()
			

	def balls_run(self):
		for ball in self.loose:
			ball.draw()

		for ball in self.claster: 			# проверяет положение шаров
			ball.draw_shadow()
			ball.speed*=0.99 				# сопротивление воздуха
			if ball.loose>0:				# перемещает шар в забитые
				ball.player=self.player
				self.loose_ball(ball)


		for i in range(len(self.claster)):
		
			if len(self.claster)>1:
				for n in range(i+1,len(self.claster)):					
					self.claster[i].check_position(self.claster[n])

			self.claster[i].draw()
			self.claster[i].move()
		
	def run(self):
		"""запуск и отрисовка"""

		sc.blit(table_surf, table_rect)	
		if len(self.claster)==0:
			return
		if not self.count_entr():
			self.balls_static()
			#pygame.display.set_caption('Ожидаю удар. Сила удара= %s' % self.cue.force)

			self.cue.draw(self.player)

			if self.help_hit and self.cue.wait:
				# рисование подсказки для удара
				draw_help_line(self.cue,self.hit_ball)

		else:
			self.balls_run()
			pygame.display.set_caption('Шаров в игре - %s, Шаров забито - %s' % (len(self.claster),len(self.loose)))
			#pygame.display.set_caption('Энтропия = %s' % self.count_entr())


class Ball():
	"""шар с координатами [x,y], вектором скорости [vx,vy] и радиусом r=20"""
	def __init__(self,x,y,vx=0,vy=0,r=24,color=(220, 225, 205),loose=0,player=0):
		self.x=x
		self.y=y
		self.speed = Vector(vx,vy)
		self.r=r
		self.color=color
		self.loose=0
		self.player=player
	
	def move(self):

		if self.loose > 0: return
		
		self.x+=self.speed.x*2/FPS
		self.y+=self.speed.y*2/FPS

		
		if self.x-self.r <=85:
			if 125<self.y<height-125:
				self.x=self.r+85 #борьба с залипанием
				self.speed.x=-self.speed.x
			elif self.x-self.r <=85:
				self.loose=1
		if self.x+self.r>=width-85:
			if 125<self.y<height-125:
				self.x=width-85-self.r #борьба с залипанием
				self.speed.x=-self.speed.x
			elif self.x>=width-85:
				self.loose=1
		if self.y-self.r <=85:
			if 125<self.x<630 or 665<self.x<width-125:
				self.y=self.r+85 #борьба с залипанием
				self.speed.y=-self.speed.y
			elif self.y<=85:	
				self.loose=1
		if self.y+self.r>=height-85:
			if 125<self.x<630 or 665<self.x<width-125: 
				self.y=height-85-self.r #борьба с залипанием
				self.speed.y=-self.speed.y				
			elif self.y>=height-85:
				self.loose=1

	def check_position(self,other):

		dist=((self.x-other.x)**2+(self.y-other.y)**2)**0.5
		if dist<=self.r+other.r: # условие слокновения
			# корреляция положения
			delta=self.r+other.r-dist
			COS_d=(self.x-other.x)/dist
			SIN_d=(self.y-other.y)/dist
			self.x+=delta*COS_d
			self.y+=delta*SIN_d

			# изменеие векторов движения после удара
			delta_X=self.x-other.x
			delta_Y=self.y-other.y

			Vst=self.speed.turn(delta_X,delta_Y)
			Vot=other.speed.turn(delta_X,delta_Y)
			Vst.hit(Vot)

			self.speed=Vst.retrn(delta_X,delta_Y)
			other.speed=Vot.retrn(delta_X,delta_Y)

	def draw_shadow(self):

		shade_x=int(self.x-2*self.r*(self.x-85)/(width-170))
		for i in range(8):
			pygame.draw.ellipse(sc,(44-i*5,115-i*5,42-i*5),(int(shade_x+2*i*(self.x-85)/(width-170)), int(self.y-self.r+i*2),(self.r-i)*2,((self.r-i*2)*2)))

	def draw(self):

		if self.loose == 0:
			n=8

			pygame.draw.circle(sc, (self.color[0]-pattern, self.color[1]-pattern, self.color[2]-pattern), (int(self.x), int(self.y)),self.r)
			for i in range(1,n):
				rad=int((self.r)*((n**2-i**2)**0.5)/n)
				color=(self.color[0]-pattern + int(i*pattern/n), self.color[1]-pattern+int(i*pattern/n),self.color[2]-pattern+int(i*pattern/n))
				
				pygame.draw.circle(sc, color, (int(self.x+2*i*((self.x-85)/(width-170)-0.5)), int(self.y)),rad)
			return

		if self.player:
			pygame.draw.circle(sc, (self.color[0]-pattern, self.color[1]-pattern, self.color[2]), (int(self.x), int(self.y)),self.r)
		else:
			pygame.draw.circle(sc, (self.color[0], self.color[1]-pattern, self.color[2]-pattern), (int(self.x), int(self.y)),self.r)


class cue:
	""" кий """
	def __init__(self,x,y,lenght,angle=math.pi,r=5,color=L_WOOD,force=21,wait=0):
		self.x=x
		self.y=y
		self.wait=wait # 0 = выбирает точку, 1 = прицеливается
		self.lenght=lenght
		self.angle=angle
		self.force=force
		self.r=r
		self.color=color
		
	def draw(self,player=0):
		COS=math.cos(self.angle)
		SIN=math.sin(self.angle)
		xs=self.x+self.force*COS
		ys=self.y+self.force*SIN
		lenght_x=COS*self.lenght
		lenght_y=SIN*self.lenght
		xe=xs+lenght_x
		ye=ys+lenght_y
		
		# handle
		aim=BLUE if player else RED
		pygame.draw.circle(sc, BLACK,(int(xs),int(ys)),4)
		pygame.draw.line(sc, self.color, [xs,ys], [xe,ye], self.r)
		xs1=xe-lenght_x/3
		ys1=ye-lenght_y/3
		pygame.draw.line(sc, (80, 20, 00), [xs1,ys1], [xe,ye], self.r*2)
		pygame.draw.line(sc, (100, 40, 00), [xs1,ys1], [xe,ye], self.r*2-3)

		# остальная часть
		xe=xs1
		ye=ys1
		l_x=(lenght_x*2/3)/self.r
		l_y=(lenght_y*2/3)/self.r
		for i in range(self.r):
			xs1=xe-l_x
			ys1=ye-l_y
			pygame.draw.line(sc, (200+i*10, 130+i*10, 50+i*10), [xs1,ys1], [xe,ye], self.r*2-i)
			xe=xs1
			ye=ys1

		aim_col=WOOD if self.wait else aim 
		pygame.draw.circle(sc, aim_col, (int(self.x), int(self.y)),3)


C=cue((width//2),(height*2//3)+40,600)

B=Balls(C,help_hit=1)

# создание первого стека

B.add_ball(Ball((width//3),(height//2)))

D=2*B[0].r
h=D*(3**0.5)/2

for i in range(5):
	y=int(height//2-D*i/2)
	
	x=int((width//3)+300+h*i)
	
	for n in range(i+1):
		B.add_ball(Ball(x,y))
		y+=D


while True:
		
	clock.tick(FPS)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()
	
	
		if event.type == pygame.MOUSEBUTTONDOWN:
			if event.button == 4:
				B.cue.force+=1
				if B.cue.force>60:
					B.cue.force=60
			if event.button == 5:
				B.cue.force-=1
				if B.cue.force<1:
					B.cue.force=1

	B.check_mouth()
	B.choose_pos()
	B.run()

	#sc.blit(screen, (600,00))
	pygame.display.update()	
	