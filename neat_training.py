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
        self.scale_y = 2

    def input(self,key):
        pass

    def update(self):
        pass

class Agent(Entity):
    def __init__(self,_index,nn,model,pos,target):
        super().__init__()
        self.pop_index = _index
        self.model = model
        self.position = pos
        self.texture = "white_cube"
        self.nn = nn
        self.tof = 0
        self.distance = 0
        self.displacement = 0
        self.fitness = 0
        self.is_alive=True
        # target pos to neural network
        self.nn.node_map[13] = target[0]
        self.nn.node_map[14] = target[1]
        self.nn.node_map[15] = target[2]
    def input(self,key):
        #input for agent
        pass

    def update(self):
        # print(f"id: {self.pop_index}")
        # print(f"alive: {self.is_alive}")
        if self.is_alive:
            # position to neural network
            pos = self.position
            print(f"possss: {pos}")
            self.nn.node_map[10] = pos[0]
            self.nn.node_map[11] = pos[1]
            self.nn.node_map[12] = pos[2]


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

            dir1 = (sin(angle1),cos(angle1))
            dir2 = (sin(angle2),cos(angle2))
            dir3 = (sin(angle3),cos(angle3))
            dir4 = (sin(angle4),cos(angle4))
            dir5 = (sin(angle5),cos(angle5))
            dir6 = (sin(angle6),cos(angle6))
            dir7 = (sin(angle7),cos(angle7))
            dir8 = (sin(angle8),cos(angle8))

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
            d1 = min(raycast1.distance,max_dist)
            d2 = min(raycast2.distance,max_dist)
            d3 = min(raycast3.distance,max_dist)
            d4 = min(raycast4.distance,max_dist)
            d5 = min(raycast5.distance,max_dist)
            d6 = min(raycast6.distance,max_dist)
            d7 = min(raycast7.distance,max_dist)
            d8 = min(raycast8.distance,max_dist)
            print(d1,d2,d3,d4,d5,d6,d7,d8)

            if mod(d1) < 0.55 :
                print("collision detected")
                self.is_alive = False
            if mod(d3) < 0.55 :
                print("collision detected")
                self.is_alive = False
            if mod(d5) < 0.55 :
                print("collision detected")
                self.is_alive = False
            if mod(d7) < 0.55 :
                print("collision detected")
                self.is_alive = False

            #setting the distance as input layer
            self.nn.node_map["1"] = d1
            self.nn.node_map["2"] = d2
            self.nn.node_map["3"] = d3
            self.nn.node_map["4"] = d4
            self.nn.node_map["5"] = d5
            self.nn.node_map["6"] = d6
            self.nn.node_map["7"] = d7
            self.nn.node_map["8"] = d8
            calculate(self.nn)

            #get the output layer
            out = self.nn.output_layer
            _list = []
            for i in out:
                _list.append(self.nn.node_map[str(i)])
            _max = out[_list.index(max(_list))]
            #forward
            global speed

            if _max == 16:
                self.x += time.dt*speed*math.sin(angle1)
                self.z += time.dt*speed*math.cos(angle1)
            #back
            if _max == 17:
                self.x += time.dt*speed*math.sin(angle5)
                self.z += time.dt*speed*math.cos(angle5)
            #right
            if _max == 18:
                self.x += time.dt*speed*math.sin(angle3)
                self.z += time.dt*speed*math.cos(angle3)
            #left
            if _max == 19:
                self.x += time.dt*speed*math.sin(angle7)
                self.z += time.dt*speed*math.cos(angle7)

    def update_fitness(self):
        #updates fitness according to the parameters
        pass 

def input(key):
    if key=="d":
        terrain_degeneration()
    if key=="g":
        terrain_generation()
    if key=="p":
        population_degeneration()
    global y
    global aki

def update():
    # update for cmd
    pass
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
        terrain.append(Enemy((randint(-10,10),0,i)))

def terrain_degeneration():
    global terrain
    for i in terrain:
        destroy(i)

def population_degeneration():
    global population
    for i in population:
        destroy(i)

def neat_training():
    global generation_number
    #10,11,12 - player pos
    #13,14,15 - target pos
    nn = NeuralNetwork(
        [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],#input layer
        [16,17,18,19],#output layer
        [20],#hidden layer
        {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,
         "16":0,"17":0,"18":0,"19":0,"20":0},#node map
        [],#connection network
        2.5,#stepsize
        1,#next innovation number
        21,#next node number
        1,#min weight 
        100 #max weight
    )
    #end
    initial_population = mutation(nn)
    #training
    global population
    population = []
    for i,item in enumerate(initial_population):
        population.append(Agent(i,item,"cube",(0,0.5,0),(0,0,100)))

def main():
    app = Ursina()
    global vcamera
    global generation_number
    generation_number = 1
    window.exit_button.visible = False
    window.fps_counter.enabled = True
    window.title = "Simulation"
    vcamera = EditorCamera()
    Entity(model='plane', scale=1000, color=color.white, shader=lit_with_shadows_shader)
    global speed
    speed = 20
    global terrain
    terrain = []
    pivot = Entity(position = (0,10,0))
    cam = DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
    terrain_generation()
    neat_training()
    app.run()

main()
