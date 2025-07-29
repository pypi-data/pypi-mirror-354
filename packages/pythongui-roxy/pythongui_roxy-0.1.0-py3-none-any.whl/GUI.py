import sys
import urllib.request
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import uic
import os

from Matrix import pose_to_matrix, forward_kinematics,matrix_to_pose
from IK import *
from Params import DH, WeldingTorch, JointLimit
from dataset import fk_dataset
from ML import train_model, predict_random_ik, load_decoder_model


def resource_path(relative_path):
    base_path = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


form_first     = resource_path('window_1.ui')
form_second    = resource_path('window_2.ui')
form_third     = resource_path('window_3.ui')
form_forth     = resource_path('window_4.ui')
form_fifth     = resource_path('window_5.ui')
form_sixth     = resource_path('window_6.ui')
form_seven     = resource_path('window_7.ui')
form_eight     = resource_path('window_8.ui')
form_nine     = resource_path('window_9.ui')

form_firstwindow   = uic.loadUiType(form_first)[0]
form_secondwindow  = uic.loadUiType(form_second)[0]
form_thridwindow   = uic.loadUiType(form_third)[0]
form_forthwindow   = uic.loadUiType(form_forth)[0]
form_fifthwindow   = uic.loadUiType(form_fifth)[0]
form_sixthwindow   = uic.loadUiType(form_sixth)[0]
form_sevenwindow   = uic.loadUiType(form_seven)[0]
form_eightwindow   = uic.loadUiType(form_eight)[0]
form_ninewindow   = uic.loadUiType(form_nine)[0]

# #######################################################
class window_1(QDialog, form_firstwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        
        self.quit_btn.clicked.connect(self.quitButton)

    def quitButton(self):
        quit()
        
    def btn_1_to_2(self):
        self.hide()
        self.second = window_2()
        self.second.exec()
        self.show()

# #######################################################
class window_2(QDialog, form_secondwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.loadImageFromFile() 
        self.loadImageFromFile2()
        
    def loadImageFromFile(self) :
        self.qPixmapFileVar = QPixmap()
        self.qPixmapFileVar.load("fanuc.jpg")
        self.qPixmapFileVar = self.qPixmapFileVar.scaledToWidth(150)
        self.pic_label.setPixmap(self.qPixmapFileVar)
        
    def loadImageFromFile2(self) :
        self.qPixmapFileVar2 = QPixmap()
        self.qPixmapFileVar2.load("fanuc100.jpg")
        self.qPixmapFileVar2 = self.qPixmapFileVar2.scaledToWidth(160)
        self.pic_label_2.setPixmap(self.qPixmapFileVar2)
        
    def btn_2_to_3(self):
        self.hide()
        self.second = window_3()
        self.second.exec()
        self.show()
        
    def btn_2_to_6(self):

        dh_params = [
    [525, 150, -90],
    [0, 790, 0],
    [0, 250, 90],
    [-835, 0, -90],
    [0, 0, 90],
    [-100, 0, 90]
]
        
        welding_torch_list = [22, -51.352, 501.314]  
        
        joint_limit = [
            [-170, 170],
            [-130, 130],
            [-229, 229],
            [-200, 200],
            [-180, 180],
            [-450, 450]
        ]
        
        self.hide()
        self.second = window_6(dh_params, welding_torch_list, joint_limit)  
        self.second.exec()
        self.show()
    def btn_2_to_6_1(self):

        dh_params = [
    [450, 150, -90],
    [0, 600, 0],
    [0, 200, 90],
    [-860, 0, -90],
    [0, 0, 90],
    [-100, 0, 180]
]
        
        welding_torch_list = [22, -51.352, 501.314]  
        
        joint_limit = [
            [-170, 170],
            [-125, 125],
            [-223.5, 223.5],
            [-190, 190],
            [-190, 190],
            [-360, 360]
        ]
        
        self.hide()
        self.second = window_6(dh_params, welding_torch_list, joint_limit)  
        self.second.exec()
        self.show()

# #######################################################
class window_3(QDialog, form_thridwindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.save_btn.clicked.connect(self.getTableData)

    def btn_3_to_4(self):
        dh_params = self.getTableData()
        self.hide()
        self.second = window_4(dh_params)
        self.second.exec()
        self.show()

    def showValue(self):
        data = list(range(1, 25))
        rows, cols = 6, 4
        index = 0

        for i in range(rows):
            for j in range(cols):
                value = data[index]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
                index += 1

    def getTableData(self):
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        data_matrix = []

        for i in range(rows):
            row_data = []
            for j in range(cols):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    try:
                        value = float(item.text())
                    except ValueError:
                        value = item.text()
                else:
                    value = ""
                row_data.append(value)
            data_matrix.append(row_data)
            
        dh_params = [row[1:] for row in data_matrix]
        print("DH Params:", dh_params)
        return dh_params

# #######################################################
class window_4(QDialog, form_forthwindow):
    def __init__(self,dh_params):
        super(window_4, self).__init__()
        self.initUi()
        self.show()
        self.dh_params = dh_params
        
    def initUi(self):
        self.setupUi(self)
        self.save_btn.clicked.connect(self.getTorchData)
        
    def getTorchData(self):
        val1 = self.lineEdit_1.text()
        val2 = self.lineEdit_2.text()
        val3 = self.lineEdit_3.text()

        # 값이 숫자면 float으로 변환 (선택사항)
        try:
            val1 = float(val1)
        except ValueError:
            pass

        try:
            val2 = float(val2)
        except ValueError:
            pass

        try:
            val3 = float(val3)
        except ValueError:
            pass

        welding_torch_list = [val1, val2, val3]
        print("용접 토치 파라미터:", welding_torch_list)
        return welding_torch_list

    def btn_4_to_5(self):
        welding_torch_list = self.getTorchData()
        self.hide()
        self.second = window_5(self.dh_params, welding_torch_list)
        self.second.exec()
        self.show()

# #######################################################
class window_5(QDialog, form_fifthwindow):
    def __init__(self,dh_params, welding_torch_list):
        super(window_5, self).__init__()
        self.initUi()
        self.show()
        self.dh_params=dh_params
        self.welding_torch_list=welding_torch_list

    def initUi(self):
        self.setupUi(self)
        self.save_btn.clicked.connect(self.getJointData)

    def btn_5_to_6(self):
        joint_limit=self.getJointData()
        self.hide()
        self.second = window_6(self.dh_params, self.welding_torch_list, joint_limit)
        self.second.exec()
        self.show()

    def showValue(self):
        data = list(range(1, 25))
        rows, cols = 6, 2
        index = 0

        for i in range(rows):
            for j in range(cols):
                value = data[index]
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(value)))
                index += 1

    def getJointData(self):
        rows = self.tableWidget.rowCount()
        cols = self.tableWidget.columnCount()
        joint_limit = []

        for i in range(rows):
            row_data = []
            for j in range(cols):
                item = self.tableWidget.item(i, j)
                if item is not None:
                    try:
                        value = float(item.text())
                    except ValueError:
                        value = item.text()
                else:
                    value = ""
                row_data.append(value)
            joint_limit.append(row_data)

        print(joint_limit)
        return joint_limit

# #######################################################
class window_6(QDialog, form_sixthwindow):
    def __init__(self,dh_params,welding_torch_list, joint_limit):
        super().__init__()
        self.setupUi(self)
        self.dh_params=dh_params
        self.welding_torch_list=welding_torch_list
        self.joint_limit=joint_limit
        
    def btn_6_to_7(self):
        self.hide()
        self.second = window_7(self.dh_params, self.welding_torch_list, self.joint_limit)
        self.second.exec()
        self.show()

# #######################################################
class window_7(QDialog, form_sevenwindow):
    def __init__(self,dh_params,welding_torch_list, joint_limit):
        super().__init__()
        self.setupUi(self)
        self.dh_params=dh_params
        self.welding_torch_list=welding_torch_list
        self.joint_limit=joint_limit


    def initUi(self):
        self.setupUi(self)
        self.next_btn.clicked.connect(self.getPositionData)
        
    def getPositionData(self):
        val1 = self.lineEdit_1.text()
        val2 = self.lineEdit_2.text()
        val3 = self.lineEdit_3.text()
        val4 = self.lineEdit_4.text()
        val5 = self.lineEdit_5.text()
        val6 = self.lineEdit_6.text()

        # 값이 숫자면 float으로 변환 (선택사항)
        try:
            val1 = float(val1)
        except ValueError:
            pass

        try:
            val2 = float(val2)
        except ValueError:
            pass

        try:
            val3 = float(val3)
        except ValueError:
            pass
        
        try:
            val4 = float(val4)
        except ValueError:
            pass
        
        try:
            val5 = float(val5)
        except ValueError:
            pass
        
        try:
            val6 = float(val6)
        except ValueError:
            pass

        pose = [val1, val2, val3, val4, val5, val6]
        print("위치:", pose)
        
        return pose
    
    def btn_7_to_8(self):
        pose=self.getPositionData()
        self.hide()
        self.second = window_8(self.dh_params, self.welding_torch_list, self.joint_limit, pose)
        self.second.exec()
        self.show()
        
# #######################################################
class window_8(QDialog, form_eightwindow):
    def __init__(self,dh_params,welding_torch_list, joint_limit,pose):
        super().__init__()
        self.setupUi(self)
        self.dh_params=dh_params
        self.welding_torch_list=welding_torch_list
        self.joint_limit=joint_limit
        self.pose=pose
        # self.start_btn.clicked.connect(self.run_inverse_kinematics)
        self.finish_btn.clicked.connect(self.run_inverse_kinematics)
        
        print(" window_3에서 받은 DH 파라미터:", self.dh_params)
        print(" window_4에서 받은 용접 토치 파라미터:", self.welding_torch_list)
        print(" window_5에서 받은 조인트 리밋:", self.joint_limit)
        print(" window_7에서 받은 Position:", self.pose)
        
    def run_inverse_kinematics(self):
        T = pose_to_matrix(self.pose)
        welding_torch = WeldingTorch(*self.welding_torch_list)
        ik_solution = IK(self.pose, T, self.dh_params, welding_torch, use_torch=False)
        ik_multi_solutions = apply_angle_wrapping(ik_solution, self.joint_limit)
        dh_params = [[a, b, np.deg2rad(c)] for a, b, c in self.dh_params]

        result_text = ""
        for i, sol in enumerate(ik_multi_solutions):
            T_sol = forward_kinematics(sol, dh_params, self.welding_torch_list, use_torch=False)
            pose_result = matrix_to_pose(T_sol)
            pos = pose_result[:3]
            rot = pose_result[3:]
            result_text += f"# Solution {i+1}\n"
            result_text += f"Theta: {[round(t, 2) for t in sol]}\n"

        #  콘솔 출력
        print(result_text)
        return result_text
        
    def btn_8_to_9(self):
        result_text=self.run_inverse_kinematics()
        self.hide()
        self.second = window_9(result_text)
        self.second.exec()
        self.show()

# #######################################################

class window_9(QDialog, form_ninewindow):
    def __init__(self, result_text):
        super().__init__()
        self.setupUi(self)
        self.result_text=result_text
        
        print(" window_8에서 받은 result_text:", self.result_text)
        
        self.resultTextEdit.setText(self.result_text)
        self.finish_btn.clicked.connect(self.quitButton)

    def quitButton(self):
        quit()
        

# #######################################################

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     myWindow = window_1()
#     myWindow.show()
#     app.exec_()

def main():
    app = QApplication(sys.argv)
    myWindow = window_1()
    myWindow.show()
    app.exec_()


if __name__ == '__main__':
    main()
