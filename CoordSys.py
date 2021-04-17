import numpy as np


class Joint:
    def __init__(self, parent):
        self.parent = parent
        self.child = None
        self.pos = None
        self.rot = None
        self.alpha, self.a, self.d, self.theta = 0, 0, 0, 0
        self.d_var, self.theta_var = False, False
        self.update()
        #pos = vector(self.pos[1], self.pos[2], self.pos[0])  # Zamiana układu prawoskrętnego z obliczeń,
        #rot = [vector(self.rot[1, 0], self.rot[2, 0], self.rot[0, 0]),  # do lewoskrętnego do wyświetlania
        #       vector(self.rot[1, 1], self.rot[2, 1], self.rot[0, 1]),
        #       vector(self.rot[1, 2], self.rot[2, 2], self.rot[0, 2])]
        #self.cords = CoordinatesSystem(pos, rot, self.number)

    def return_joint(self, i):
        if self.number != i:
            return self.child.return_joint(i)
        return self

    def append_joint(self):
        if self.child is not None:
            self.child.append_joint()
        else:
            self.child = Joint(self)

    def insert_joint(self, i):
        if i != 0:
            self.child.insert_joint(i-1)
        else:
            tmp = Joint(self)
            if self.child is not None:
                self.child.parent = tmp
                tmp.child = self.child
            self.child = tmp

    def pop_joint(self):
        if self.child is None:
            return 0
        elif self.child.child is not None:
            return self.child.pop_joint()
        else:
            self.child.parent = None
            self.child = None
            return 1

    def remove_joint(self, i):
        if self.child is None:
            if self.parent is None:
                return 0
            self.parent.child = None
            self.parent = None
            return 1
        elif i != 0:
            return self.child.remove_joint(i - 1)
        else:
            if self.child is not None:
                self.child.parent = self.parent
            self.parent.child = self.child
            self.child = self.parent = None
            return 1

    @property
    def len(self):
        if self.child is not None:
            return self.child.len
        return self.number

    @property
    def number(self):
        if self.parent is not None:
            return self.parent.number + 1
        return 0

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
