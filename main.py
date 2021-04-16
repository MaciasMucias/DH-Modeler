from CoordSys import Joint
import vpython as vp

if __name__ == '__main__':
    dh_table = [[0, 0, 5, 0],
                [0, 5, 0, 90]]
    joints = [Joint(None, [0, 0, 0, 0])]
    for dh in dh_table:
        joints.append(joints[-1].new_joint(dh))