#importing stuff
try:
    from ursina import *
    from time import sleep
    from ursina.raycaster import raycast
    import time
    import json
    from ursina.shaders import lit_with_shadows_shader
    from math import sin,cos
    from neat import *
    from random import *

except Exception as e:
    print(f"error: {e}")

def mod(x):
    if x<0:
        return -x
    return x

class Enemy(Entity):
    def __init__(self,position):
        super().__init__()
        self.model = "cube"
        self.collider = 'box' 
        self.color = color.red
        self.position = position
        self.scale_y = 1

    def input(self,key):
        pass

    def update(self):
        pass

class Agent(Entity):
    def __init__(self,model,pos):
        super().__init__()
        self.model = model
        self.position = pos
        self.texture = "white_cube"
        self.decision = "up"

    def input(self,key):
        rot = self.rotation_y
        self.rotation_y = rot
        angle1 = (rot)*math.pi/180
        angle2 = (rot+45)*math.pi/180
        angle3 = (rot+90)*math.pi/180
        angle4 = (rot+135)*math.pi/180
        angle5 = (rot+180)*math.pi/180
        angle6 = (rot+225)*math.pi/180
        angle7 = (rot+270)*math.pi/180
        angle8 = (rot+315)*math.pi/180
        #input for agent
        if key=="w":
            self.decision="up"
        if key=="a":
            self.decision="left"
        if key=="s":
            self.decision="down"
        if key=="d":
            self.decision = "right"

    def update(self):
            rot = self.rotation_y
            self.rotation_y = rot
            angle1 = (rot)*math.pi/180
            angle2 = (rot+45)*math.pi/180
            angle3 = (rot+90)*math.pi/180
            angle4 = (rot+135)*math.pi/180
            angle5 = (rot+180)*math.pi/180
            angle6 = (rot+225)*math.pi/180
            angle7 = (rot+270)*math.pi/180
            angle8 = (rot+315)*math.pi/180

            dir1 = (0,0,1) 
            dir2 = (1,0,1) 
            dir3 = (1,0,0)
            dir4 = (1,0,-1)
            dir5 = (0,0,-1)
            dir6 = (-1,0,-1)
            dir7 = (-1,0,0)
            dir8 = (-1,0,1)

            print(f"dir1,dir3{dir1},{dir3}")
            raycast1 = raycast(self.position,dir1)
            raycast2 = raycast(self.position,dir2)
            raycast3 = raycast(self.position,dir3)
            raycast4 = raycast(self.position,dir4)
            raycast5 = raycast(self.position,dir5)
            raycast6 = raycast(self.position,dir6)
            raycast7 = raycast(self.position,dir7)
            raycast8 = raycast(self.position,dir8)
            #remove this after adding boundaries
            max_dist = 100
            print(raycast1.distance)
            d1 = min(raycast1.distance, max_dist)
            d2 = min(raycast2.distance, max_dist)
            d3 = min(raycast3.distance, max_dist)
            d4 = min(raycast4.distance, max_dist)
            d5 = min(raycast5.distance, max_dist)
            d6 = min(raycast6.distance, max_dist)
            d7 = min(raycast7.distance, max_dist)
            d8 = min(raycast8.distance, max_dist)
            print(d1,d2,d3,d4,d5,d6,d7,d8)

            if mod(d1) < 1 or mod(d3) < 1 or mod(d5) < 1 or mod(d7) < 1:
                print("collision detected")
            if mod(d3)< 2 or mod(d1)< 2 or mod(d2) <2:
                self.decision = "stop"

            #move forward
            if self.decision=="up":
                x_dist = time.dt*speed*math.sin(angle1)
                z_dist = time.dt*speed*math.cos(angle1)
                self.x += x_dist
                self.z += z_dist
                # self.distance += mod(x_dist) + mod(z_dist)
            if self.decision=="left":
                x_dist = time.dt*speed*math.sin(angle7)
                z_dist = time.dt*speed*math.cos(angle7)
                self.x += x_dist
                self.z += z_dist
            if self.decision=="down":
                x_dist = time.dt*speed*math.sin(angle5)
                z_dist = time.dt*speed*math.cos(angle5)
                self.x += x_dist
                self.z += z_dist
            if self.decision=="right":
                x_dist = time.dt*speed*math.sin(angle3)
                z_dist = time.dt*speed*math.cos(angle3)
                self.x += x_dist
                self.z += z_dist

    def update_fitness(self,fitness):
        self.fitness = fitness

def terrain_generation():
    global terrain

    a = Enemy((0,0,100))
    a.scale_x = 40
    terrain.append(a)

    a = Enemy((0,0,-20))
    a.scale_x = 40
    terrain.append(a)

    a = Enemy((20,0,40))
    a.scale_z = 120
    terrain.append(a)

    a = Enemy((-20,0,40))
    a.scale_z = 120
    terrain.append(a)

    for i in range(-10,100):
        terrain.append(Enemy((randint(-20,20),0,i)))
        terrain.append(Enemy((randint(-20,20),0,i)))

def testing():
    global agent
    agent.append(Agent("cube",(0,0.5,0)))


def main():
    app = Ursina()
    global vcamera
    global generation_number
    window.exit_button.visible = False
    window.fps_counter.enabled = True
    window.title = "Simulation"
    vcamera = EditorCamera()
    Entity(model='plane', scale=1000, color=color.white, shader=lit_with_shadows_shader)
    global speed
    speed = 1
    global terrain
    terrain = []
    global agent
    agent = []
    pivot = Entity(position = (0,10,0))
    cam = DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
    terrain_generation()
    testing()
    app.run()

main()
