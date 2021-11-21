import numpy as np
from glm import mat4


class Robot:
    def __init__(self):
        self.joints = None

    def initialise(self):
        """
        Initialise joints
        self.joints is structured such that object at index i-1 is the parent of the object at i
        :return:
        """
        self.joints = [None, Joint(None), Joint(None)]

    def return_joint(self, i):
        """
        Return specified joint
        :param i: Number of the joint to be returned
        :return: Specified joint

        """
        return self.joints[i + 2]

    def append_joint(self):
        """
        Add an extra joint at the end up to 10
        :return: Success value
        """
        if self.len > 10:
            return 0
        self.joints.append(Joint(self.joints[-1]))
        return 1

    def insert_joint(self, i):
        """
        Inserts a new joint before the one specified up to 10
        :param i: Number the new joint will have
        :return: Success value
        """
        if self.len > 10:
            return 0
        self.joints.insert(i + 1, Joint(self.joints[i]))
        return 1

    def pop_joint(self):
        """
        Remove a joint from the and down to 2
        :return: Success value
        """
        if self.len == 2:
            return 0
        self.joints.pop(-1)
        return 1

    def remove_joint(self, i):
        """
        Remove a specified joint
        :param i: Number of the joint to be removed
        :return: Success value
        """
        if self.len == 2:
            return 0
        self.joints.pop(i + 1)
        return 1

    @property
    def len(self):
        return len(self.joints) - 1

    def update_joint(self, joint_num):
        """
        Update position of a joint, and all his children
        :param joint_num: Number of the joint to be updated
        :return:
        """
        for i in range(joint_num+2, len(self.joints)):
            self.joints[i].update(self.joints[i-1])

    def draw(self, proj, view):
        """
        Draw all the joints
        :param proj: projection matrix
        :param view: view matrix
        :return:
        """
        for joint in reversed(self.joints[1:]):
            joint.draw(proj, view)


class Joint:
    def __init__(self, parent):
        from Objects3D import coord_3d
        self.coord_3d = coord_3d.copy()

        self.alpha, self.a, self.d, self.theta = 0.0, 0.0, 0.0, 0.0
        self.d_var, self.theta_var = False, False  # Not used yet

        self.mat = np.eye(4)

        # place it in the world on initialisation
        self.update(parent)

    def update(self, parent):
        """
        Update joints positions relative to it's parent
        :param parent: Joint parent
        :return:
        """
        # if this is the parent joint then this joint is in the origin so no translation nor rotation
        if parent is None:
            self.mat = np.eye(4)
        else:
            # if it has a parent then calculate this joints global position matrix
            self.mat = parent.mat @ self.generate_matrix

        # apply the matrix
        self.coord_3d.apply_mat(mat4(self.mat.T.tolist()))

    @property
    def generate_matrix(self) -> np.ndarray:
        """
        Create and return homogeneous matrix
        """
        s_t = self.sin(self.theta)
        c_t = self.cos(self.theta)
        s_a = self.sin(self.alpha)
        c_a = self.cos(self.alpha)
        return np.array([[c_t, -s_t * c_a, s_t * s_a, self.a * c_t],
                         [s_t, c_t * c_a, -c_t * s_a, self.a * s_t],
                         [0, s_a, c_a, self.d],
                         [0, 0, 0, 1]])

    # Sin i cos that return whole numbers for popular angles
    @staticmethod
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
