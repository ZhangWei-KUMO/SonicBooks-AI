from PySide6.QtWidgets import (QMessageBox)

def show_version():
        version_info = QMessageBox()
        version_info.setWindowTitle("版本信息")
        version_info.setText("苏州云帧数浪信息科技有限公司版权所有 @2023-2024 版本号 1.0.0")
        version_info.exec_()