#importing stuff
try:
    from ursina import *
    from ursina.raycaster import raycast
    import time
    import json
    from ursina.shaders import lit_with_shadows_shader
    from math import sin,cos
    from neat import *

except Exception as e:
    print(f"error: {e}")

def mod(x):
    if x<0:
        return -x
    return x

class drone(Entity):
    def __init__(self,model,position,texture):
        super().__init__()
        self.model="cube"
        self.position = position
        self.texture = texture
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
        # print(tof)
        # print(f'td: {td}')
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
    # print(key)
    global y
    global aki

def update():
    # update for cmd
    global vcamera
    # global aki
    #ant colony algorithm goes here
    # vcamera.position = aki.position
    rot = vcamera.rotation_y
    aki.rotation_y = rot
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

    raycast1 = raycast(aki.position,dir1)
    raycast2 = raycast(aki.position,dir2)
    raycast3 = raycast(aki.position,dir3)
    raycast4 = raycast(aki.position,dir4)
    raycast5 = raycast(aki.position,dir5)
    raycast6 = raycast(aki.position,dir6)
    raycast7 = raycast(aki.position,dir7)
    raycast8 = raycast(aki.position,dir8)

    d1 = raycast1.distance
    d2 = raycast2.distance
    d3 = raycast3.distance
    d4 = raycast4.distance
    d5 = raycast5.distance
    d6 = raycast6.distance
    d7 = raycast7.distance
    d8 = raycast8.distance
    #would later used as a input neural layer network
    # print(f'raycast 1 {raycast1.distance}')
    # print(f'raycast 2 {raycast2.distance}')
    # print(f'raycast 3 {raycast3.distance}')
    # print(f'raycast 4 {raycast4.distance}')
    # print(f'raycast 5 {raycast5.distance}')
    # print(f'raycast 6 {raycast6.distance}')
    # print(f'raycast 7 {raycast7.distance}')
    # print(f'raycast 8 {raycast8.distance}')


def main():
    # app = Ursina()
    # global td
    # td = 0
    # global tof_const
    # tof_const = time.time()
    # global render_displacement
    # render_displacement = []
    # global vcamera
    # # window.fullscreen = True
    # window.exit_button.visible = False
    # window.fps_counter.enabled = False
    # window.title = "Simulation"
    # vcamera = EditorCamera()
    # global y
    # global render 
    # render = []
    # Entity(model='plane', scale=100, color=color.white, shader=lit_with_shadows_shader)
    # global entities
    # global aki
    # global speed
    # speed = 20
    # entities = []
    # aki = drone(model = "cube",position = (0,0.5,0),texture = "white_cube" )
    # wall_left = Entity(model='cube', collider='box', scale_y=3, origin_y=-.5, color=color.azure, x=-4)
    # pivot = Entity(position = (0,10,0))
    # cam = DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))

    #1-8 raycast , 9,10 - input values
    #Neural network stuff
    #initial neural network
    nn = NeuralNetwork(
        [1,2,3,4,5,6,7,8,9,10],
        [11,12,13,14],
        {"1":2.3,"2":3.7,"3":3.3,"4":4.1,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,},
        [],
        2.5,
        1,
        15,
        1,
        100
    )
    #end
    nl = mutation(nn)
    print(f"nerual list {nl}")
    # app.run()


main()
