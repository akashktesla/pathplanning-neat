#importing stuff
try:
    from ursina import *
    import time
    import json
    from ursina.shaders import lit_with_shadows_shader

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
        print(tof)
        print(f'td: {td}')
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
    #ant colony algorithm goes here
    # vcamera.position = aki.position
    aki.rotation_y = vcamera.rotation_y

def main():
    app = Ursina()
    global td
    td = 0
    global tof_const
    tof_const = time.time()
    global render_displacement
    render_displacement = []
    global vcamera
    # window.fullscreen = True
    window.exit_button.visible = False
    window.fps_counter.enabled = False
    window.title = "Simulation"
    vcamera = EditorCamera()
    global y
    global render 
    render = []
    Entity(model='plane', scale=100, color=color.white, shader=lit_with_shadows_shader)
    global entities
    global aki
    global speed
    speed = 20
    entities = []
    aki = drone(model = "cube",position = (0,0.5,0),texture = "white_cube" )
    pivot = Entity(position = (0,10,0))
    cam = DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
    app.run()

main()
