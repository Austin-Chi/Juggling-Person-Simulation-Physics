from curses.textpad import rectangle
from numpy import arccos
from numpy import arcsin
from vpython import*
g=9.8
r=0.3
d=0.6
is_thrown=False
once=False
v_hand=0
v=5
theta=arcsin(d*g/(v*v))/2
print(f"theta = {theta}")
v_right=vec(v*cos(pi/2+theta), v*sin(pi/2+theta), 0)
print(f"x = {v_right.x}"+f" y = {v_right.y}")
v_left=vec(v*cos(pi/2-theta), v*sin(pi/2-theta), 0)
span=0
t=0
dt= 0.001
N=7
m=0.2
cycle=0
stage=0
scene = canvas(width=600, height=800, background=color.white, align ='left')
##arm_right_pos=vec(d/2, 0, 0)
##arm_left_pos=vec(-d/2, 0, 0)
##scene2 = canvas(width = 300, height = 300, align = 'left', background = vec(0.5, 0.5, 0))
oscillation = graph(width = 400, align = 'right')
funct1 = gcurve(graph = oscillation, color=color.blue, width=4)
head=sphere(radius=d/3, pos=vec(0, 0.6+d/3, -d/3), color=color.red)
body = box(length=d, height=1.0, width=0.01, color=color.red)
uarm_r=cylinder(radius= 0.05, pos=vec(d/2, -0.05, 0),axis=vec(0, 0.6, 0), color=color.blue )
uarm_l=cylinder(radius= 0.05, pos=vec(-d/2, -0.05, 0),axis=vec(0, 0.6, 0), color=color.blue )
arm_right = cylinder(radius = 0.05 , pos = vec(d/2,0,0), axis = vec(-r, 0, 0), color = color.blue)
arm_left = cylinder(radius = 0.05 , pos = vec(-d/2,0,0), axis = vec(-r, 0, 0), color = color.blue)
hand_right = sphere(radius = 0.01, pos = arm_right.pos+arm_right.axis, color = color.red)
hand_left = sphere(radius = 0.01, pos = arm_left.pos+arm_left.axis, color = color.blue)
hand_right_v=vec(0, 0, 0)
hand_left_v=vec(0, 0, 0)
hand_a=0
balls=[]
balls_is_thown=[]
balls_by_right=[]
balls_v=[]
balls_a=[]
right_can_acc=False
left_can_acc=False
pos_odd=hand_right.pos
pos_even = hand_left.pos

        
fake_v=v*sin(pi/2+theta)
t=fake_v/g
        
v_hand=2*r*((N-1)/2)/t
        
hand_a=2*v*sin(pi/2+theta)*((N-1)/2)/t
arm_left.axis=vec(-r, 0, 0)
arm_right.axis=vec(-r,0,0)
for i in range (N):
    tpos = hand_right.pos
    by_right=True
    if i%2==1:
        tpos= hand_left.pos
        by_right=False
    ball = sphere(pos = tpos, radius = 0.03, color= color.green)
    balls.append(ball)
    is_thorwn=False
    balls_is_thown.append(is_thorwn)
    balls_by_right.append(by_right)
    if by_right==True:
        balls_v.append(v_right)
    elif by_right==False:
        balls_v.append(v_left)





while(True):
    rate(1000)
    cycle+=1
    span+=dt
    if arm_right.axis.x>=r:
        hand_right_v.x=-v_hand
    if arm_right.axis.x<=-r:
        hand_right_v.x=v_hand
    if arm_left.axis.x>=r:
        hand_left_v.x=-v_hand
    if arm_left.axis.x<=-r:
        hand_left_v.x=v_hand
    
    for i in range(N):
        if balls_is_thown[i]==True:
            balls_v[i]+=vec(0, -g, 0)*dt
            balls[i].pos+=balls_v[i]*dt
            if balls_by_right[i]==True:
                if mag(balls[i].pos-hand_left.pos)<=hand_left.radius+balls[i].radius:
                    balls[i].pos=hand_left.pos
                    hand_left_v.y=balls_v[i].y
                    balls_v[i]=v_left
                    left_can_acc=True
                    balls_is_thown[i]=False
                    balls_by_right[i]=False
            elif balls_by_right[i]==False:
                if mag(balls[i].pos-hand_right.pos)<=hand_right.radius+balls[i].radius:
                    balls[i].pos=hand_right.pos
                    hand_right_v.y=balls_v[i].y
                    balls_v[i]=v_right
                    right_can_acc=True
                    balls_is_thown[i]=False
                    balls_by_right[i]=True
    for i in range(N):
        if balls_is_thown[i]==False:
            if balls_by_right[i]==True:
                balls[i].pos=hand_right.pos
                if balls[i].pos.x<=arm_right.pos.x-r:
                    balls_is_thown[i]=True
                    break
            elif balls_by_right[i]==False:
                balls[i].pos=hand_left.pos
                if balls[i].pos.x>=arm_left.pos.x+r:
                    balls_is_thown[i]=True

    if hand_right_v.x<=0 and right_can_acc==True:
        hand_right_v.y+=hand_a*dt
    arm_right.axis+=hand_right_v*dt
    if hand_left_v.x>=0 and left_can_acc==True:
        hand_left_v.y+=hand_a*dt
    arm_left.axis+=hand_left_v*dt
    if hand_left_v.x<0:
        #hand_left_v.y=0
        arm_left.axis.y=0
    if hand_right_v.x>0:
        #hand_right_v.y=0
        arm_right.axis.y=0
    if arm_right.axis.y>0:
        #hand_right_v.y=0
        arm_right.axis.y=0
    if arm_left.axis.y>0:
        #hand_left_v.y=0
        arm_left.axis.y=0
    hand_right.pos=arm_right.pos+arm_right.axis
    hand_left.pos=arm_left.pos+arm_left.axis
    funct1.plot(pos=(span, balls[0].pos.x))


    