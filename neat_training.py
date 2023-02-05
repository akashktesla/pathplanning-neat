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
    def __init__(self,_index,nn,model,pos):
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

    def input(self,key):
        #input for agent
        pass

    def update(self):
        if self.is_alive:
            
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
                self.is_alive = False
                print("collision detected")
            if mod(d3) < 0.55 :
                self.is_alive = False
                print("collision detected")
            if mod(d5) < 0.55 :
                self.is_alive = False
                print("collision detected")
            if mod(d7) < 0.55 :
                self.is_alive = False
                print("collision detected")

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

            if _max == 11:
                self.x += time.dt*speed*math.sin(angle1)
                self.z += time.dt*speed*math.cos(angle1)
            #back
            if _max == 12:
                self.x += time.dt*speed*math.sin(angle5)
                self.z += time.dt*speed*math.cos(angle5)
            #right
            if _max == 13:
                self.x += time.dt*speed*math.sin(angle3)
                self.z += time.dt*speed*math.cos(angle3)
            #left
            if _max == 14:
                self.x += time.dt*speed*math.sin(angle7)
                self.z += time.dt*speed*math.cos(angle7)

    def update_fitness(self):
        #updates fitness according to the parameters
        pass 

class drone(Entity):
    def __init__(self,model,position):
        super().__init__()
        self.model="cube"
        self.position = position
        self.texture = "white_cube"
    def input(self,key):
        global render_displacement
        disp = math.dist((0,0,0),(self.x,self.y,self.z))
        if key=="z":
            for i in render_displacement:
                destroy(i)
            render_displacement.append(Text(text = f"Displacement:{disp}",y = 0.5,x = -.85,z = -1))
        pass

    def update(self):
        global td
        global tof_const
        global tof
        tof = int(time.time()-tof_const)
        global render
        for i in render:
            destroy(i)
        render.append(Text(text = f"Total distance travelled: {td}",y = 0.40,x = -.85,z = -1))
        render.append(Text(text = f"Time of flight: {tof}",y = 0.45,x = -.85,z = -1))
        global speed
        #all 4 angles used to calculate all the 4 movements
        angle1 = (self.rotation.y)*math.pi/180
        angle2 = (self.rotation.y+90)*math.pi/180
        angle3 = (self.rotation.y+180)*math.pi/180
        angle4 = (self.rotation.y+270)*math.pi/180
        #movement script
        if held_keys["up arrow"] or held_keys["w"]:
            self.x += time.dt*speed*math.sin(angle1)
            self.z += time.dt*speed*math.cos(angle1)
            td += mod(time.dt*speed*math.sin(angle1)) + mod(time.dt*speed*math.cos(angle1))
        if held_keys["right arrow"] or held_keys["d"]:
            self.x += time.dt*speed*math.sin(angle2)
            self.z += time.dt*speed*math.cos(angle2)
            td += mod(time.dt*speed*math.sin(angle2)) + mod(time.dt*speed*math.cos(angle2))
        if held_keys["down arrow"] or held_keys["s"]:
            self.x += time.dt*speed*math.sin(angle3)
            self.z += time.dt*speed*math.cos(angle3)
            td += mod(time.dt*speed*math.sin(angle3)) + mod(time.dt*speed*math.cos(angle3))
        if held_keys["left arrow"] or held_keys["a"]:
            self.x += time.dt*speed*math.sin(angle4)
            self.z += time.dt*speed*math.cos(angle4)
            td += mod(time.dt*speed*math.sin(angle4)) + mod(time.dt*speed*math.cos(angle4))


class simobj(Entity):
    def __init__(self,model,position ):
        super().__init__()
        self.model=model
        self.position = position

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
    a = Enemy((0,0,20))
    a.scale_x = 10
    terrain.append(a)
    #border

    a = Enemy((0,0,100))
    a.scale_x = 40
    terrain.append(a)

    a = Enemy((20,0,50))
    a.scale_z = 100
    terrain.append(a)

    a = Enemy((-20,0,50))
    a.scale_z = 100
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
    nn = NeuralNetwork(
        [1,2,3,4,5,6,7,8,9,10],#input layer
        [11,12,13,14],#output layer
        [15],#hidden layer
        {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0},#node map
        [],#connection network
        2.5,#stepsize
        1,#next innovation number
        16,#next node number
        1,#min weight 
        100 #max weight
    )
    #end
    initial_population = mutation(nn)
    #training
    global population
    population = []
    for i,item in enumerate(initial_population):
        population.append(Agent(i,item,"cube",(0,0.5,0)))

def main():
    app = Ursina()
    global td
    td = 0
    global tof_const
    tof_const = time.time()
    global render_displacement
    render_displacement = []
    global vcamera
    window.exit_button.visible = False
    window.fps_counter.enabled = True
    window.title = "Simulation"
    vcamera = EditorCamera()
    global y
    global render 
    render = []
    Entity(model='plane', scale=1000, color=color.white, shader=lit_with_shadows_shader)
    global entities
    global aki
    global speed
    speed = 20
    entities = []
    global terrain
    terrain = []
    pivot = Entity(position = (0,10,0))
    cam = DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
    terrain_generation()
    neat_training()
    app.run()

main()
