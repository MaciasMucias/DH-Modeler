import numpy as np

class Joint:
    def __init__(self, parent, dh_parameters=(0, 0, 0, 0), number=0):
        self.parent = parent
        self.child = None
        self.pos = None
        self.rot = None
        self.number = number
        self.alpha, self.a, self.d, self.theta = dh_parameters
        self.update()
        #pos = vector(self.pos[1], self.pos[2], self.pos[0])  # Zamiana układu prawoskrętnego z obliczeń,
        #rot = [vector(self.rot[1, 0], self.rot[2, 0], self.rot[0, 0]),  # do lewoskrętnego do wyświetlania
        #       vector(self.rot[1, 1], self.rot[2, 1], self.rot[0, 1]),
        #       vector(self.rot[1, 2], self.rot[2, 2], self.rot[0, 2])]
        #self.cords = CoordinatesSystem(pos, rot, self.number)

    def new_joint(self, dh_parameters=(0, 0, 0, 0)):
        if self.child is not None:
            self.child.new_joint(dh_parameters)
        else:
            self.child = Joint(self, dh_parameters, self.number + 1)
        return self.child

    @property
    def len(self):
        if self.child is not None:
            return self.child.len
        return self.number

    def update(self):
        delta_pos = self.generate_matrix[:3, 3]
        delta_rot = self.generate_matrix[:3, :3]

        if self.parent is None:
            self.pos = delta_pos
            self.rot = delta_rot
        else:
            base_pos = self.parent.pos
            base_rot = self.parent.rot
            self.pos = base_pos + delta_pos
            self.rot = base_rot @ delta_rot

    @property
    def generate_matrix(self):
        s_t = self.sin(self.theta)
        c_t = self.cos(self.theta)
        s_a = self.sin(self.alpha)
        c_a = self.cos(self.alpha)
        return np.array([[c_t, -s_t * c_a, s_t * s_a, self.a * c_t],
                         [s_t, c_t * c_a, -c_t * s_a, self.a * s_t],
                         [0, s_a, c_a, self.d],
                         [0, 0, 0, 1]])  # Macierz transformacji jednorodnej

    @staticmethod  # Sin i cos zwracający wartości całkowite dla popularnych kątów
    def sin(x):
        if x in [0, 180]:
            return 0
        if x == 90:
            return 1
        if x == 270:
            return -1
        return np.sin(np.deg2rad(x))

    @staticmethod
    def cos(x):
        if x == 0:
            return 1
        if x in [90, 270]:
            return 0
        if x == 180:
            return -1
        return np.cos(np.deg2rad(x))


class CoordinatesSystem:
    def __init__(self, pos, rot, number):
        self.pos = pos
        self.rot = rot
        #self.point = vp.sphere(pos=self.pos, radius=0.1)
        self.axis = []
        self.labels = []
        text = [f'X_{number}', f'Y_{number}', f'Z_{number}']
        #for i in range(3):
        #    self.axis.append(vp.cylinder(pos=self.pos, axis=self.rot[i], color=colors[i], radius=0.02))
        #    self.labels.append(vp.label(pos=self.pos + self.rot[i], text=text[i], box=False))
