class Camera:
    def __init__(self, X, Y, Z):
        self.min_x, self.max_x = X
        self.min_y, self.max_y = Y
        self.min_z, self.max_z = Z

        self.objects_in_world = []

    def draw(self):
        pass