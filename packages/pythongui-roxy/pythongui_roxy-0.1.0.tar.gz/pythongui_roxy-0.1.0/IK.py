import numpy as np
from scipy.spatial.transform import Rotation
from Matrix import transformation_matrix
from itertools import product

# 역기구학 솔버 
def IK(pose, T, dh_params, welding_torch, use_torch=False):
    # welding torch 유무 
    if use_torch:
            T06 = T @ np.linalg.inv(welding_torch())
    else:
        T06 = T
        
    # theta 1,2,3
    x, y, z, rx, ry, rz = pose
    d1, d4, d6 = dh_params[0][0], abs(dh_params[3][0]), abs(dh_params[5][0])
    r1, r2, r3 = dh_params[0][1], dh_params[1][1], dh_params[2][1]
    rx, ry, rz = np.radians([rx, ry, rz])
    R = Rotation.from_euler('xyz', [rx, ry, rz]).as_matrix()
    nx, ny, nz = R[:, 2]
    xpw = x - d6 * nx
    ypw = y - d6 * ny
    zpw = z - d6 * nz
    theta1 = np.arctan2(ypw, xpw)
    h1 = np.sqrt(xpw**2 + ypw**2) - r1
    h2 = zpw - d1
    h0 = np.sqrt(h1**2 + h2**2)
    h3 = np.sqrt(r3**2 + d4**2)
    beta1 = np.arctan2(h2, h1)
    beta2 = np.arccos((r2**2 + h0**2 - h3**2) / (2 * r2 * h0))
    theta2 = np.pi/2 - beta1 - beta2
    gamma1 = np.arccos((r2**2 + h3**2 - h0**2) / (2 * r2 * h3))
    gamma2 = np.arctan2(d4, r3)
    theta3 = np.pi - gamma1 - gamma2
    
    angles_rad = [theta1, theta2, theta3, beta1, beta2, gamma1, gamma2]
    angles_deg = np.degrees(angles_rad)
    theta1, theta2, theta3, beta1, beta2, gamma1, gamma2 = angles_deg
    
    for elbow in [1, -1]:
        if elbow == 1:
            theta2_mod = theta2
            theta3_mod_n = -theta3 - theta2
        else:
            theta2_mod = theta2 + 2 * beta2
            theta3_mod = -theta3 - 2 * gamma2
            theta3_mod_n = -theta3_mod - theta2_mod
            
        T01_i = transformation_matrix(theta1, dh_params[0][0], dh_params[0][1], dh_params[0][2])
        T12_i = transformation_matrix(theta2_mod - 90, dh_params[1][0], dh_params[1][1], dh_params[1][2])
        T23_i = transformation_matrix(-theta3_mod_n - theta2_mod, dh_params[2][0], dh_params[2][1], dh_params[2][2])
        T03_i = T01_i @ T12_i @ T23_i
        R03 = T03_i[:3, :3]
        R06 = T06[:3, :3]
        R36 = R03.T @ R06
        for wrist in [1, -1]:
            s5 = wrist * np.sqrt(1 - R36[2,2]**2)
            theta5 = np.arctan2(s5, -R36[2,2])
            theta4 = np.arctan2(R36[1,2]*wrist, R36[0,2]*wrist)
            theta6 = np.arctan2(R36[2,1]*wrist, R36[2,0]*wrist)

            base_sol = [theta1, theta2_mod, theta3_mod_n, 
                        np.degrees(theta4), np.degrees(theta5), np.degrees(theta6)]
    return base_sol

# joint limit 안에 드는 값 filtering
def apply_angle_wrapping(base_sol, joint_limits):
    valid_options = []
    for i, angle in enumerate(base_sol):
        low, high = joint_limits[i]
        wrapped = [angle + 360 * k for k in range(-2, 3)]
        filtered = [round(a, 4) for a in wrapped if low <= a <= high]
        valid_options.append(filtered)

    extended_sols = [list(combo) for combo in product(*valid_options)]
    raw_solutions = []
    raw_solutions.extend(extended_sols)
    
    return raw_solutions

# 오차 
def compute_error(T_desired, T_calc):
    pos_error = np.linalg.norm(T_desired[:3, 3] - T_calc[:3, 3])
    R_d = T_desired[:3, :3]
    R_c = T_calc[:3, :3]
    cos_angle = (np.trace(R_d.T @ R_c) - 1) / 2
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    rot_error = np.degrees(np.arccos(cos_angle))
    return pos_error, rot_error