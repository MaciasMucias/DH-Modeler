import glm


class mat4:
    def __init__(self, mat=glm.identity(glm.mat4)):
        self.mat = mat

    def rotate(self, angle, axis):
        x, y, z = axis
        self.mat = glm.rotate(self.mat, glm.radians(angle), glm.vec3(x, y, z))

    def translate(self, x, y, z):
        self.mat = glm.translate(self.mat, glm.vec3(x, y, z))


class ViewMat(mat4):
    def translate(self, x, y, z):
        """
        Translate the view matrix
        Because we are moving the "camera" we will move everything else in the opposite direction
        :param x: Translation amount in X axis
        :param y: Translation amount in Y axis
        :param z: Translation amount in Z axis
        :return:
        """
        super(ViewMat, self).translate(-x, -y, -z)
