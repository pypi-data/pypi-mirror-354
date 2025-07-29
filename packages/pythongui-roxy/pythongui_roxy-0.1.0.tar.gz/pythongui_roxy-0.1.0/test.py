
# import numpy as np
# import csv
# from scipy.spatial.transform import Rotation

# # D-H 파라미터: 각 관절의 [d, a, alpha]
# dh_params = [
#     [525, 150, -np.pi/2],  # Joint 1
#     [0, 790, 0],           # Joint 2
#     [0, 250, np.pi/2],     # Joint 3
#     [-835, 0, -np.pi/2],   # Joint 4
#     [0, 0, np.pi/2],       # Joint 5
#     [-100, 0, -np.pi]      # Joint 6
# ]

# def get_euler_angles_xyz(T):
# # =============================================================================
# #     4x4 변환 행렬 T를 입력받아 XYZ 오일러 각(Rx, Ry, Rz)을 구하는 함수
# #     반환 각도 단위는 도(degree)
# # =============================================================================

#     rotation_matrix = T[:3, :3]  # 상위 3x3 회전 행렬 추출
#     euler_angles = Rotation.from_matrix(rotation_matrix).as_euler('xyz', degrees=True)  # XYZ 기준 오일러 각 계산
#     return list(euler_angles)

# # 용접 토치에 대한 위치 및 자세 보정 변환 행렬 생성
# def welding_torch():
#     # y축으로 22도 회전
#     theta = np.deg2rad(22)
#     cos_t = np.cos(theta)
#     sin_t = np.sin(theta)
    
#     R_y = np.array([
#         [cos_t, 0, -sin_t, 0],
#         [0, 1, 0, 0],
#         [sin_t, 0, cos_t, 0],
#         [0, 0, 0, 1]
#     ])
    
#     # x축 방향으로 -51.352mm 이동
#     T_x = np.array([
#         [1, 0, 0, -51.352],
#         [0, 1, 0, 0],
#         [0, 0, 1, 0],
#         [0, 0, 0, 1]
#     ])
    
#     # z축 방향으로 501.314mm 이동
#     T_z = np.array([
#         [1, 0, 0, 0],
#         [0, 1, 0, 0],
#         [0, 0, 1, 501.314],
#         [0, 0, 0, 1]
#     ])
    
#     # 최종 변환 행렬 계산
#     T_welding_torch = T_z @ T_x @ R_y
#     return T_welding_torch

# # D-H 파라미터를 이용한 단일 변환 행렬 생성 함수
# def transformation_matrix(theta, d, a, alpha):
#     theta = np.radians(theta)  # 각도 단위 변환 (도 -> 라디안)

#     matrix = np.array([
#         [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
#         [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
#         [0, np.sin(alpha), np.cos(alpha), d],
#         [0, 0, 0, 1]
#     ])
    
#     return matrix

# # 용접 토치 보정 행렬 미리 계산
# T_welding_torch = welding_torch()

# # 각 관절별 작동 범위 (단위: 도)
# # Arc Mate 120ic 기준 (Visual Components 확인)
# joint_ranges_deg = [
#     (-185, 185),
#     (-100, 160),
#     (-185, 60),
#     (-200, 200),
#     (-180, 180),
#     (-450, 450)
# ]

# interval_deg = 30  # 샘플링 간격 (도 단위)

# # 결과 저장용 CSV 파일 생성
# output_file = open("Arcmate_fk_dataset.csv", "w", newline="")
# writer = csv.writer(output_file)
# writer.writerow(["x", "y", "z", "Rx", "Ry", "Rz"] + [f"관절{i+1}" for i in range(6)])

# # 재귀적으로 가능한 모든 조합에 대해 Forward Kinematics 계산 및 저장
# def generate_fk_dataset(joint_angles=[], level=0):
#     if level == 6:
#         관절1, 관절2, 관절3, 관절4, 관절5, 관절6 = joint_angles

#         # Forward Kinematics 계산 (관절각 보정 포함)
#         T01 = transformation_matrix(관절1, dh_params[0][0], dh_params[0][1], dh_params[0][2])
#         T12 = transformation_matrix(관절2 - 90, dh_params[1][0], dh_params[1][1], dh_params[1][2])
#         T23 = transformation_matrix(-관절3 - 관절2, dh_params[2][0], dh_params[2][1], dh_params[2][2])
#         T34 = transformation_matrix(관절4, dh_params[3][0], dh_params[3][1], dh_params[3][2])
#         T45 = transformation_matrix(-관절5, dh_params[4][0], dh_params[4][1], dh_params[4][2])
#         T56 = transformation_matrix(관절6, dh_params[5][0], dh_params[5][1], dh_params[5][2])

#         final_matrix = T01 @ T12 @ T23 @ T34 @ T45 @ T56 @ T_welding_torch

#         pos = final_matrix[:3, 3]  # 위치 (x, y, z)
#         rx, ry, rz = get_euler_angles_xyz(final_matrix)  # 오일러 각도 계산

#         # CSV 파일에 기록
#         writer.writerow([*pos, rx, ry, rz, 관절1, 관절2, 관절3, 관절4, 관절5, 관절6])
#         return

#     min_deg, max_deg = joint_ranges_deg[level]
#     for angle in range(min_deg, max_deg + 1, interval_deg):
#         generate_fk_dataset(joint_angles + [angle], level + 1)

# # 데이터셋 생성 실행
# generate_fk_dataset()
# output_file.close()



# ######################################################################################################




# import tensorflow as tf
# from tensorflow.keras import layers, models

# latent_dim = 4  # 잠재변수(latent variable) 차원 설정

# # AutoEncoder 모델 정의

# # Encoder: 자세 + 관절각 → 잠재공간(latent space)으로 압축
# def build_encoder():
#     input_ = layers.Input(shape=(12,))
#     processing = layers.Dense(256, activation='relu')(input_)
#     processing = layers.Dense(128, activation='relu')(processing)
#     post_processing = layers.Dense(latent_dim)(processing)
#     return models.Model(inputs=input_, outputs=post_processing, name="Encoder")

# # Decoder: 자세 + 잠재변수 → 관절각 예측
# def build_decoder():
#     input_ = layers.Input(shape=(6 + latent_dim,))  # 자세 6 + 잠재변수 4
#     processing = layers.Dense(128, activation='relu')(input_)
#     processing = layers.Dense(256, activation='relu')(processing)
#     out = layers.Dense(6)(processing)  # 출력: 관절각 6개
#     return models.Model(inputs=input_, outputs=out, name="Decoder")

# # 모델 생성
# encoder = build_encoder()
# decoder = build_decoder()

# # 전체 AutoEncoder 모델 구성
# input_all = tf.keras.Input(shape=(12,))  # 자세 + 관절각 (총 12개 입력)
# pose_input = input_all[:, :6]  # 앞 6개: 자세 (x, y, z, Rx, Ry, Rz)
# angle_input = input_all[:, 6:]  # 뒤 6개: 관절각

# post_processing = encoder(input_all)  # 잠재변수 추출
# decoder_input = tf.concat([pose_input, post_processing], axis=-1)  # 자세 + 잠재변수 결합
# reconstruncted_angles = decoder(decoder_input)  # 관절각 복원

# model = tf.keras.Model(inputs=input_all, outputs=reconstruncted_angles)
# model.compile(optimizer='adam', loss='mse')  # 손실함수: 평균제곱오차

# # 데이터 전처리 및 학습

# import numpy as np
# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import MinMaxScaler

# df = pd.read_csv('Arcmate_fk_dataset.csv', encoding='cp949')

# # 입력 특성 정의 (자세 + 관절각)
# X_pose = df[["x", "y", "z", "Rx", "Ry", "Rz"]].values
# X_angles = df[["罐1", "罐2", "罐3", "罐4", "罐5", "罐6"]].values

# X_all = np.hstack([X_pose, X_angles])  # 전체 입력 = 자세 + 관절각
# Y = X_angles  # 출력은 관절각

# # 정규화 (MinMaxScaler 사용)
# scaler_X = MinMaxScaler().fit(X_all)
# X_all_scaled = scaler_X.transform(X_all)

# scaler_Y = MinMaxScaler().fit(Y)
# Y_scaled = scaler_Y.transform(Y)

# # 학습용/테스트용 분할
# X_train, X_test, Y_train, Y_test = train_test_split(X_all_scaled, Y_scaled, 
#                                                     test_size=0.1, random_state=0)

# # 모델 학습
# model.fit(X_train, Y_train, validation_data=(X_test, Y_test), epochs=50, batch_size=1024)

# # 학습된 decoder 저장
# decoder.save("ik_decoder.h5")

# # decoder 모델 불러오기
# from tensorflow.keras.models import load_model
# decoder = load_model("ik_decoder.h5")

# # 역기구학 추정 함수 (자세를 기준으로 다양한 관절각 후보 생성)
# def predict_random_ik(pose, num_variations=10):
#     results = []
#     pose = np.array(pose).reshape(1, -1)  # (1, 6) 형상으로 변환

#     # pose 데이터도 학습 시 사용한 정규화 방식에 맞춰 스케일 조정
#     pose_min = scaler_X.data_min_[:6]
#     pose_max = scaler_X.data_max_[:6]
#     pose_scaled = (pose - pose_min) / (pose_max - pose_min)

#     for _ in range(num_variations):
#         z = np.random.normal(0, 1, size=(1, latent_dim))  # 잠재변수 무작위 샘플링
#         input_decoder = np.hstack([pose_scaled, z])  # 자세 + 잠재변수
#         pred_scaled = decoder.predict(input_decoder, verbose=0)
#         pred_real = scaler_Y.inverse_transform(pred_scaled)  # 정규화 해제하여 실제 관절각으로 변환
#         results.append(pred_real[0])
    
#     return results













import numpy as np
from scipy.spatial.transform import Rotation
from itertools import product

# DH 파라미터 (세타를 제외한 값, 알파는 이미 라디안)
dh_params = [
    [450, 150, -np.pi/2],
    [0, 600, 0],
    [0, 200, np.pi/2],
    [-860, 0, -np.pi/2],
    [0, 0, np.pi/2],
    [-100, 0, np.pi]
]

# 조인트 제한 (degree)
joint_limits = [
    (-170, 170),
    (-130, 130),
    (-229, 229),
    (-200, 200),
    (-180, 180),
    (-450, 450)
]

def transformation_matrix(theta, d, a, alpha):
    theta = np.radians(theta)
    matrix = np.array([
        [np.cos(theta), -np.sin(theta)*np.cos(alpha), np.sin(theta)*np.sin(alpha), a*np.cos(theta)],
        [np.sin(theta), np.cos(theta)*np.cos(alpha), -np.cos(theta)*np.sin(alpha), a*np.sin(theta)],
        [0, np.sin(alpha), np.cos(alpha), d],
        [0, 0, 0, 1]
    ])
    return matrix

def welding_torch():
    theta = np.deg2rad(22)
    cos_t = np.cos(theta)
    sin_t = np.sin(theta)
    R_y = np.array([
        [cos_t, 0, -sin_t, 0],
        [0, 1, 0, 0],
        [sin_t, 0, cos_t, 0],
        [0, 0, 0, 1]
    ])
    T_x = np.array([
        [1, 0, 0, -51.352],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])
    T_z = np.array([
        [1, 0, 0, 0],
        [0, 1, 0, 0],
        [0, 0, 1, 501.314],
        [0, 0, 0, 1]
    ])
    return T_z @ T_x @ R_y

def get_euler_angles_xyz(final_matrix):
    rotation_matrix = final_matrix[:3, :3]
    euler_angles = Rotation.from_matrix(rotation_matrix).as_euler('xyz', degrees=True)
    return list(euler_angles)

def calculate_theta123_xyz(xp, yp, zp, rx_deg, ry_deg, rz_deg, d1, d4, d6, r1, r2, r3):
    rx, ry, rz = np.radians([rx_deg, ry_deg, rz_deg])
    R = Rotation.from_euler('xyz', [rx, ry, rz]).as_matrix()
    nx, ny, nz = R[:, 2]
    xpw = xp - d6 * nx
    ypw = yp - d6 * ny
    zpw = zp - d6 * nz
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
    return np.degrees(theta1), np.degrees(theta2), np.degrees(theta3), np.degrees(beta1), np.degrees(beta2), np.degrees(gamma1), np.degrees(gamma2)

def forward_kinematics(thetas, use_torch=False):
    T = np.eye(4)
    for i in range(6):
        theta = thetas[i]
        d, a, alpha = dh_params[i]
        if i == 1:
            theta -= 90
        elif i == 2:
            theta = -thetas[2] - thetas[1]
        elif i == 4:
            theta = -theta
        T = T @ transformation_matrix(theta, d, a, alpha)
    if use_torch:
        T = T @ welding_torch()
    return T

def compute_error(T_desired, T_calc):
    pos_error = np.linalg.norm(T_desired[:3, 3] - T_calc[:3, 3])
    R_d = T_desired[:3, :3]
    R_c = T_calc[:3, :3]
    cos_angle = (np.trace(R_d.T @ R_c) - 1) / 2
    cos_angle = np.clip(cos_angle, -1.0, 1.0)
    rot_error = np.degrees(np.arccos(cos_angle))
    return pos_error, rot_error


def apply_angle_wrapping(base_sol):
    # 각 조인트에 대해 wrapping 후보 중 joint limit 안에 드는 값만 선택
    valid_options = []
    for i, angle in enumerate(base_sol):
        low, high = joint_limits[i]
        wrapped = [angle + 360 * k for k in range(-2, 3)]
        filtered = [round(a, 4) for a in wrapped if low <= a <= high]
        valid_options.append(filtered)

    # 필터링된 옵션으로부터 가능한 조합 생성
    candidates = [list(combo) for combo in product(*valid_options)]
    return candidates

def solve_inverse_kinematics(T_tool, use_torch=False):
    if use_torch:
        T06 = T_tool @ np.linalg.inv(welding_torch())
    else:
        T06 = T_tool

    xp, yp, zp = T06[0, 3], T06[1, 3], T06[2, 3]
    rx, ry, rz = get_euler_angles_xyz(T06)
    d1, d4, d6 = dh_params[0][0], abs(dh_params[3][0]), abs(dh_params[5][0])
    r1, r2, r3 = dh_params[0][1], dh_params[1][1], dh_params[2][1]
    theta1, theta2, theta3, beta1, beta2, gamma1, gamma2 = calculate_theta123_xyz(xp, yp, zp, rx, ry, rz, d1, d4, d6, r1, r2, r3)
    raw_solutions = []
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

            extended_sols = apply_angle_wrapping(base_sol)
            raw_solutions.extend(extended_sols)

    return raw_solutions

def pose_to_transform(x, y, z, rx, ry, rz):
    """
    위치(x, y, z) 및 오일러각(rx, ry, rz in degrees)를 받아 4x4 변환행렬 반환
    """
    # 위치 벡터
    pos = np.array([x, y, z])

    # 회전행렬 (XYZ 순서 오일러각 → 3x3 회전행렬)
    rot = Rotation.from_euler('xyz', [rx, ry, rz], degrees=True).as_matrix()

    # 4x4 변환행렬 구성
    T = np.eye(4)
    T[:3, :3] = rot
    T[:3, 3] = pos

    return T


print("XYZ 위치와 오일러각(XYZ, 단위: deg)을 입력하세요:")
x = float(input("x (mm): "))
y = float(input("y (mm): "))
z = float(input("z (mm): "))
rx = float(input("roll (rx, deg): "))
ry = float(input("pitch (ry, deg): "))
rz = float(input("yaw (rz, deg): "))

T_tool = pose_to_transform(x, y, z, rx, ry, rz)

solutions = solve_inverse_kinematics(T_tool, use_torch=True)

print("\n✅ 다중해 역기구학 결과:")
for i, sol in enumerate(solutions):
      T_sol = forward_kinematics(sol, use_torch=True)
      pos = T_sol[:3, 3]
      rot = get_euler_angles_xyz(T_sol)
      print(f"# Solution {i+1}")
      print(f"Theta: {[round(t, 2) for t in sol]}")
      print(f"  → 위치: {[round(p, 2) for p in pos]}")
      print(f"  → 오일러각(XYZ): {[round(r, 2) for r in rot]}\n")
