from items.item import Item

class Camera(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 65, 50, 'images/items/camera.png', picked_up=False)
        self.camera_on = False
        self.name = 'camera'