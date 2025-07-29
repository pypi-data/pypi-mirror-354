import numpy as np

def DH():
    dh_params = [
    [525, 150, -np.pi/2],
    [0, 790, 0],
    [0, 250, np.pi/2],
    [-835, 0, -np.pi/2],
    [0, 0, np.pi/2],
    [-100, 0, np.pi]
]
    return dh_params

def JointLimit():
    joint_limits = [
    (-170, 170),
    (-130, 130),
    (-229, 229),
    (-200, 200),
    (-180, 180),
    (-450, 450)
]
    return joint_limits

def WeldingTorch(x,y,z):
    theta = np.deg2rad(x)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    R_y = np.array([
        [cos_t, 0, -sin_t, 0],
        [0, 1, 0, 0],
        [sin_t, 0, cos_t, 0],
        [0, 0, 0, 1]
    ])
    T_x = np.array([
        [1, 0, 0, y],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    T_z = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, z],
        [0, 0, 0, 1]
    ])
    return T_z @ T_x @ R_y

# def welding_torch():
#     theta = np.deg2rad(22)
#     cos_t = np.cos(theta)
#     sin_t = np.sin(theta)
#     R_y = np.array([
#         [cos_t, 0, -sin_t, 0],
#         [0, 1, 0, 0],
#         [sin_t, 0, cos_t, 0],
#         [0, 0, 0, 1]
#     ])
#     T_x = np.array([
#         [1, 0, 0, -51.352],
#         [0, 1, 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, 1]
#     ])
#     T_z = np.array([
#         [1, 0, 0, 0],
#         [0, 1, 0, 0],
#         [0, 0, 1, 501.314],
#         [0, 0, 0, 1]
#     ])
#     return T_z @ T_x @ R_y
