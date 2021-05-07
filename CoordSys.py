import numpy as np
from glm import mat4


class Robot:
    def __init__(self):
        self.joints = None

    def initialise(self):
        self.joints = [None, Joint(None), Joint(None)]

    def return_joint(self, i):
        return self.joints[i + 2]

    def append_joint(self):
        if self.len > 10:
            return 0
        self.joints.append(Joint(self.joints[-1]))
        return 1

    def insert_joint(self, i):
        if self.len > 10:
            return 0
        self.joints.insert(i + 1, Joint(self.joints[i]))
        return 1

    def pop_joint(self):
        if self.len == 2:
            return 0
        self.joints.pop(-1)
        return 1

    def remove_joint(self, i):
        if self.len == 2:
            return 0
        self.joints.pop(i + 1)
        return 1

    @property
    def len(self):
        return len(self.joints) - 1

    def update_joint(self, joint_num):
        for i in range(joint_num+2, len(self.joints)):
            self.joints[i].update(self.joints[i-1])

    def draw(self, proj, view):
        for joint in reversed(self.joints[1:]):
            joint.draw(proj, view)


class Joint:
    pos: np.ndarray
    rot: np.ndarray
    size = 0.5

    def __init__(self, parent):
        from Objects3D import coord_3d
        self.coord_3d = coord_3d.copy()

        self.alpha, self.a, self.d, self.theta = 0.0, 0.0, 0.0, 0.0
        self.d_var, self.theta_var = False, False

        self.mat = np.eye(4)

        self.update(parent)

    def update(self, parent):
        if parent is None:
            self.mat = np.eye(4)
        else:
            self.mat = parent.mat @ self.generate_matrix

        self.coord_3d.apply_mat(mat4(self.mat.T.tolist()))

    @property
    def generate_matrix(self) -> np.ndarray:
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

    def draw(self, proj, view):
        self.coord_3d.draw(proj, view)
