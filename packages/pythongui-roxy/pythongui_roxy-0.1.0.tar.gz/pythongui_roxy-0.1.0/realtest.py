import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import torch
import torch.nn as nn
import torch.optim as optim
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
        
def load_data(csv_path):
    df = pd.read_csv(csv_path, encoding='cp949')

    X_pose = df[["x", "y", "z", "Rx", "Ry", "Rz"]].values
    X_angles = df[["theta1", "theta2", "theta3", "theta4", "theta5", "theta6"]].values

    X_all = np.hstack([X_pose, X_angles])
    Y = X_angles

    scaler_X = MinMaxScaler().fit(X_all)
    X_all_scaled = scaler_X.transform(X_all)

    scaler_Y = MinMaxScaler().fit(Y)
    Y_scaled = scaler_Y.transform(Y)

    X_train, X_test, Y_train, Y_test = train_test_split(X_all_scaled, Y_scaled,
                                                        test_size=0.1, random_state=0)

    return X_train, X_test, Y_train, Y_test, scaler_X, scaler_Y

class FFANN(nn.Module):
    def __init__(self, input_size=12, hidden_size=250, output_size=6):
        super(FFANN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.Tanh()
        self.fc2 = nn.Linear(hidden_size, output_size)

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        return self.fc2(out)


def train_model(X_train, Y_train, num_epochs=3000, lr=0.01):
    X_train = torch.tensor(X_train, dtype=torch.float32)
    Y_train = torch.tensor(Y_train, dtype=torch.float32)

    model = FFANN()
    criterion = nn.MSELoss()
    
    # 'Bayesian Regularization' 대안으로 L2 정규화 적용 (weight decay)
    optimizer = optim.Adam(model.parameters(), lr=lr, weight_decay=1e-3)

    for epoch in range(num_epochs):
        optimizer.zero_grad()
        outputs = model(X_train)
        loss = criterion(outputs, Y_train)
        loss.backward()
        optimizer.step()

        if epoch % 500 == 0:
            print(f"Epoch {epoch}, Loss: {loss.item():.6f}")

    return model

def predict_pose(model, scaler_X, scaler_Y):
    pose = np.array([[5,5,5,5,5,5]])  # (1, 6)

    dummy_angles = np.array([[5,5,5,5,5,5]])  # 예시 각도
    full_input = np.hstack([pose, dummy_angles])  # (1,12)

    scaled_input = scaler_X.transform(full_input)
    input_tensor = torch.tensor(scaled_input, dtype=torch.float32)

    with torch.no_grad():
        output = model(input_tensor)
        result = output.numpy()
        result_denorm = scaler_Y.inverse_transform(result)
    
    print("🔹 예측된 관절각도 (비정규화):")
    print(result_denorm[0])


csv_path = "Arcmate_fk_dataset.csv"  
X_train, X_test, Y_train, Y_test, scaler_X, scaler_Y = load_data(csv_path)
model = train_model(X_train, Y_train)
predict_pose(model, scaler_X, scaler_Y)
