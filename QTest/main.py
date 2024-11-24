import sys
import os
import paramiko
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QPushButton, QDialog
from PyQt5.QtGui import QIcon
from ui import Ui_Dialog
import subprocess

# 第二级： 按键动作
def on_button_clicked():
    log_text_edit = ui.textBrowser
    try:
        subprocess.Popen("D:/ToolsSpace/Tftpd32/tftpd32.exe", shell=True)
        # os.system("D:/ToolsSpace/Tftpd32/tftpd32.exe")
        log_ok = "tftpd32.exe 打开成功"
        log_text_edit.append(log_ok)
    except FileNotFoundError:
        log_error = ("tftpd32.exe文件未找到。请检查文件路径。")
        log_text_edit.append(log_error)

def on_pushButton_clicked():
    log_message = "按钮被点击了！"
    log_text_edit = ui.textBrowser     # 获取文本框对象

    log_text_edit.append(log_message)

def transfer_file():
    file_to_transfer = "akalin_256x256.ico"
    destination_ip = "192.168.174.128"
    destination_directory = "/home/xiaohong/TestSpace"
    username = "xiaohong"
    password = "350582hong"
    log_text_edit = ui.textBrowser

    try:
        ssh = paramiko.SSHClient() # 创建SSH客户端对象
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())  # 自动添加主机密钥（这可能会有安全风险，在生产环境中应该谨慎处理）
        ssh.connect(destination_ip, username=username, password=password) # 连接到服务器
        scp = ssh.open_sftp() # 创建SCP客户端对象

        scp.put(file_to_transfer, f"{destination_directory}/{file_to_transfer}") # 传输文件
        log_info = (f"将文件 {file_to_transfer} 传输到 {destination_ip}:{destination_directory}...\n")
        scp.close() # 关闭连接

        # 在目标环境上执行date指令
        stdin, stdout, stderr = ssh.exec_command("date")
        # 获取date指令的返回值（标准输出）
        date_output = stdout.read().decode('utf-8')
        log_info += (f"{date_output}\n")

        ssh.close()
    except paramiko.AuthenticationFailed:
        log_info = ("认证失败。请检查用户名和密码。")
    except paramiko.SSHException as e:
        log_info = (f"SSH连接出错: {e}")
    except FileNotFoundError:
        log_info = ("文件未找到。请检查文件路径。")

    log_text_edit.append(log_info)
# 第一级： 控制所有按键
def buttonAction(ui):
    pushButton = ui.pushButton                          # 获取界面中的按钮对象
    #pushButton.clicked.connect(on_pushButton_clicked)   # 连接按钮的点击信号到主程序中定义的槽函数
    pushButton.clicked.connect(on_button_clicked)
    transfer_button = ui.pushButton_2
    transfer_button.clicked.connect(transfer_file)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    mainWindow = QDialog()  # 创建主窗口对象，这里以QMainWindow为例，也可以是QDialog等其他窗口类型，根据你的设计来定
    ui = Ui_Dialog()        # 创建由转换后的ui模块生成的界面设置对象
    ui.setupUi(mainWindow)  # 使用ui对象设置主窗口的界面
    mainWindow.setWindowIcon(QIcon("akalin_256x256.ico"))
    mainWindow.setMinimumSize(300, 200)

    buttonAction(ui)

    mainWindow.show()       # 显示主窗口
    sys.exit(app.exec_())