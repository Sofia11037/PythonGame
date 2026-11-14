from items.item import Item

class Battery(Item):
    def __init__(self, x, y):
        super().__init__(x, y, 130, 100, 'images/items/battery.png', picked_up=False)
        self.name = 'battery'