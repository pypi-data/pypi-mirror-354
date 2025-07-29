import numpy as np
import csv
from Matrix import forward_kinematics,matrix_to_pose

def fk_dataset(joint_limits, dh_params, welding_torch, filename="Arcmate_fk_dataset.csv", interval_deg=30):

    # 결과 저장용 CSV 파일 생성
    with open(filename, "w", newline="") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["x", "y", "z", "Rx", "Ry", "Rz"] + [f"theta{i+1}" for i in range(6)])

        def DataSet(joint_angles=[], level=0):
            if level == 6:
                thetas = joint_angles
                T = forward_kinematics(thetas, dh_params, welding_torch, use_torch=True)
                pose=matrix_to_pose(T)
                writer.writerow([*pose] + thetas)
                return

            min_deg, max_deg = joint_limits[level]
            for angle in range(min_deg, max_deg + 1, interval_deg):
                DataSet(joint_angles + [angle], level + 1)

        DataSet()
