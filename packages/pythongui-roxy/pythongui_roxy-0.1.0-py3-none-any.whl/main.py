from Matrix import pose_to_matrix, forward_kinematics,matrix_to_pose
from IK import *
from Params import DH, WeldingTorch, JointLimit
from dataset import fk_dataset
from ML import train_model, predict_random_ik, load_decoder_model


# print("XYZ 위치와 오일러각(XYZ, 단위: deg)을 입력하세요:")
# x = float(input("x (mm): "))
# y = float(input("y (mm): "))
# z = float(input("z (mm): "))
# rx = float(input("roll (rx, deg): "))
# ry = float(input("pitch (ry, deg): "))
# rz = float(input("yaw (rz, deg): "))

x,y,z,rx, ry, rz=5,5,5,5,5,5
pose=[x, y, z, rx, ry, rz]
T = pose_to_matrix(pose)
dh_params=DH()
welding_torch=WeldingTorch(22, -51.352, 501.314)
joint_limits=JointLimit()

ik_solution=IK(pose, T, dh_params, welding_torch, use_torch=False)
ik_multi_solutions=apply_angle_wrapping(ik_solution, joint_limits)

for i, sol in enumerate(ik_multi_solutions):
      T_sol = forward_kinematics(sol, dh_params, welding_torch, use_torch=False)
      pose=matrix_to_pose(T_sol)
      pos = pose[:3]
      rot = pose[4:]
      print(f"# Solution {i+1}")
      print(f"Theta: {[round(t, 2) for t in sol]}")
      print(f"  → 위치: {[round(p, 2) for p in pos]}")
      print(f"  → 오일러각(XYZ): {[round(r, 2) for r in rot]}\n")
      
      
#########################################################################################################

# fk_dataset(joint_limits, dh_params, welding_torch)

# model, encoder, decoder, scaler_X, scaler_Y = build_and_train_model()

# predict_random_ik = load_decoder_and_predictor(scaler_X, scaler_Y)

# pose = [500, 100, 1200, 0, 90, 0]

# results = predict_random_ik(pose, num_variations=5)

# # 출력
# for i, angles in enumerate(results):
#     print(f"후보 {i+1}: {angles}")


# # 학습 및 decoder 저장
# decoder, scaler_X, scaler_Y = train_model(csv_path="Arcmate_fk_dataset.csv")

# # 저장된 decoder 불러오기
# decoder_loaded = load_decoder_model("ik_decoder.h5")

# # 역기구학 추정
# pose = [5, 5, 5, 5, 5, 5]
# results = predict_random_ik(pose, decoder_loaded, scaler_X, scaler_Y, num_variations=10)

# for i, res in enumerate(results):
#     print(f"후보 {i+1}: {res}")

