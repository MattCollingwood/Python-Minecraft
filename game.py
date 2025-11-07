from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController

app = Ursina()

# load all assets
textures = {
    1: load_texture("Assets/Textures/Grass.png"),
    2: load_texture("Assets/Textures/Dirt.png"),
    3: load_texture("Assets/Textures/Brick.png"),
    4: load_texture("Assets/Textures/Wood.png"),
    5: load_texture("Assets/Textures/Stone.png")
}

sky_bg = load_texture("Assets/Texture/Sky.png")
build_sound = Audio("Assets/SFX/Build_Sound.wav", loop=False, autoplay=False)



block_pick = 1

class Block(Button):
    def __init__(self, position=(0,0,0), texture=textures[1], breakable=True):
        super().__init__( #used to initialize the starting images in the game
            parent=scene,
            position=position,
            model="Assets/Models/Block.obj", # references the block model
            origin_y=0.5, # indicates where we are supposed to start
            texture=texture,
            color = Color(random.uniform(0.9, 1), random.uniform(0.9, 1), random.uniform(0.9, 1), 1),
            highlight_color=color.light_gray, #shows up when we are looking at the block
            scale=0.5
        )
        self.breakable = breakable

    def input(self, key):
        if self.hovered:
            if key == "left mouse down":
                build_sound.play()
                new_block = Block(position=self.position + mouse.normal, texture=textures[block_pick])
            elif key == "right mouse down" and self.breakable: # the and statement prevents digging through bedrock
                build_sound.play()
                destroy(self) #destroys the block that we are looking at.





class Sky(Entity): #builds the sky background
    def __init__(self):
        super().__init__(
            parent=scene,
            model="sphere",
            texture=sky_bg,
            scale=150,
            double_sided=True
        )


class Tree(Entity): #build a tree
    def __init__(self, position=(0,0,0)):
        super().__init__(
            parent=scene,
            position=position,
            model="Assets/Models/Lowpoly_tree_sample.obj",
            scale = (0.65,0.65,0.65),
            collider="mesh"
        )

def generate_trees(num_trees=3, terrain_size=20):
    for _ in range(num_trees):
        x = random.randint(0, terrain_size-1)
        y = 3
        z = random.randint(0, terrain_size-1)
        Tree(position=(x,y,z))

def generate_terrain():
    height = 5
    for z in range(25): # creates the game world based on the parameters used in this for loop
        for x in range(25):

            for y in range(height):
                if y == height - 1:
                    Block(position=(x,y,z), texture=textures[1])
                elif y >= height - 3:
                    Block(position=(x,y,z), texture=textures[2])
                else:
                    Block(position=(x,y,z), texture=textures[5])

            Block(position=(x,-1,z), texture=textures[5], breakable=False)




# update/input
def update():
    global block_pick 
    for i in range(1,6):
        if held_keys[str(i)]: #allows user to use the numbers on the keyboard to change the block placed
            block_pick = i
            break
    if held_keys["escape"]: #allows for program to shut down if esc is held down
        application.quit()

    if player.y <= -5:
        player.position = (10,10,10) #resets the player if they fall off the land




player = FirstPersonController(position=(10, 10, 10))
player.cursor.visible = False
sky = Sky()
generate_trees()
generate_terrain()

if __name__ == "__main__":
    app.run()