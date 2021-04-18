import numpy as np


class Robot:
    def __init__(self):
        self.joints = [None, Joint(None), Joint(None)]

    def return_joint(self, i):
        return self.joints[i + 1]

    def append_joint(self):
        if self.len > 10:
            return 0
        self.joints.append(Joint(self.joints[-1]))
        return 1

    def insert_joint(self, i):
        if self.len > 10:
            return 0
        self.joints.insert(i+1, Joint(self.joints[i]))
        return 1

    def pop_joint(self):
        if self.len == 2:
            return 0
        self.joints.pop(-1)
        return 1

    def remove_joint(self, i):
        if self.len == 2:
            return 0
        self.joints.pop(i+1)
        return 1

    @property
    def len(self):
        return len(self.joints) - 1

    def update_joint(self, joint):
        joint.update(self.joints.index(joint)-1)

    def draw(self, gl):
        for joint in reversed(self.joints):
            joint.draw_self(gl)


class Joint:
    pos: np.ndarray
    rot: np.ndarray
    gl_pos: np.ndarray
    gl_rot: np.ndarray
    size = 0.5

    def __init__(self, parent):
        self.alpha, self.a, self.d, self.theta = 0.0, 0.0, 0.0, 0.0
        self.d_var, self.theta_var = False, False

        self.pos = np.zeros(shape=(3, 1), dtype=np.float32)
        self.rot = np.zeros(shape=(3, 3), dtype=np.float32)
        self.gl_pos = np.zeros(shape=(3, 1), dtype=np.float32)
        self.gl_rot = np.zeros(shape=(3, 3), dtype=np.float32)

        self.update(parent)

    def update(self, parent):
        delta_pos = self.generate_matrix[:3, 3]
        delta_rot = self.generate_matrix[:3, :3]

        if parent is None:
            self.pos = delta_pos
            self.rot = delta_rot
        else:
            base_pos = parent.pos
            base_rot = parent.rot
            self.pos = base_pos + delta_pos
            self.rot = base_rot @ delta_rot

        self.gl_pos = np.array([self.pos[2], self.pos[0], self.pos[1]])

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

    def draw_self(self, gl):
        pass
