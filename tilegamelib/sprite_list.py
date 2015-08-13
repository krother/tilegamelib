

class SpriteList(list):
    """
    Class for displaying a set of movable objects.
    """
    def draw(self):
        for sprite in self:
            sprite.draw()

    def is_moving(self):
        for sprite in self:
            if sprite.is_moving():
                return True

    def update(self):
        for sprite in self:
            sprite.move()
