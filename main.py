import sys
import epubs
import threading

from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget,QMenuBar,
                               QSplitter, QTextEdit, QPushButton, QFileDialog, QMessageBox)
from PySide6.QtCore import Qt
from PySide6.QtGui import QAction

from components.settings import SettingsDialog
from components.version import show_version

from utils.azure_audio_gen import azure_audio_gen

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TubeV AI音频助手')
        self.setGeometry(300, 300, 800, 800)
        self.lang = 'zh-CN-YunzeNeural'

         # Create menu bar
        menubar = QMenuBar(self)
        menubar.setFixedWidth(500) 
        
        # Create 'Settings' menu
        settings = QAction('设置', self)
        settings.triggered.connect(self.open_settings)
        
        # Create 'Version' menu
        version = QAction('版本号', self)
        version.triggered.connect(show_version)

        # Add actions to menu bar
        fileMenu = menubar.addMenu('菜单')
        fileMenu.addAction(settings)
        fileMenu.addAction(version)

        # Central Widget and Layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Splitter for Left and Right Widgets
        splitter = QSplitter()
        main_layout.addWidget(splitter)

        # Left Widget (Text Display)
        widget_left = QWidget()
        layout_left = QVBoxLayout(widget_left)
        self.text_area = QTextEdit()
        self.text_area.setReadOnly(True)
              # Left Widget (Text Display)
        layout_left.setContentsMargins(0, 0, 0, 0)  # 设置布局的外边距为0

        self.text_area = QTextEdit()
        self.text_area.setStyleSheet("border: 0; font-size: 16px;")  # 设置字体大小和移除边框
        self.text_area.setReadOnly(True)  # 设置为只读
        self.text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        self.text_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏水平滚动条
        self.text_area.setText("请上传您的电子书或文本")  # 填充文本，你需要确保这里的字符串足够长，以填满视图

        layout_left.addWidget(self.text_area)
        splitter.addWidget(widget_left)
        
        # Right Widget (Buttons)
        widget_right = QWidget()
        layout_right = QVBoxLayout(widget_right)
        self.select_book_button = QPushButton('选择电子书')
        self.select_txt_button = QPushButton('选择文本')
        self.prev_page_button = QPushButton('上一页')
        self.next_page_button = QPushButton('下一页')
        self.generate_audio_button = QPushButton('生成音频')
        self.play_button = QPushButton('播放')

        # Initially, disable buttons that require an ebook to be loaded
        self.prev_page_button.setEnabled(False)
        self.next_page_button.setEnabled(False)
        self.generate_audio_button.setEnabled(False)
        self.play_button.setEnabled(False)

        layout_right.addWidget(self.select_book_button)
        layout_right.addWidget(self.select_txt_button)
        layout_right.addWidget(self.generate_audio_button)
        layout_right.addWidget(self.play_button)
        layout_right.addWidget(self.prev_page_button)
        layout_right.addWidget(self.next_page_button)
        splitter.addWidget(widget_right)

        # 底部组件 (Status Labels)
        widget_bottom = QWidget()
        widget_bottom.setMaximumHeight(80)
        layout_bottom = QVBoxLayout(widget_bottom)
        self.title_label = QLabel()
        self.path_label = QLabel()
        self.page_label = QLabel()
        layout_bottom.addWidget(self.title_label)
        layout_bottom.addWidget(self.path_label)
        layout_bottom.addWidget(self.page_label)
        main_layout.addWidget(widget_bottom)

        # Set the splitter sizes to a reasonable ratio
        splitter.setSizes([350, 150])

        # 事件绑定
        self.select_book_button.clicked.connect(self.select_file)
        self.prev_page_button.clicked.connect(self.prev_page)
        self.next_page_button.clicked.connect(self.next_page)
        self.generate_audio_button.clicked.connect(self.generateAudioFile)

 
        
    def select_file(self):
            options = QFileDialog.Options()
            options |= QFileDialog.ReadOnly
            file_name, _ = QFileDialog.getOpenFileName(self, '选择电子书', '',
                                           '电子书文件 (*.epub)', options=options)
            if file_name:  # 检查文件名是否为空
                self.text=[]
                self.text_area.clear()
                markdown = epubs.to_text(file_name)
                self.title = markdown[0][0].replace("#", "")
                author = markdown[0][1].replace("#", "")
                self.file_path = file_name
                self.title_label.setText("《"+self.title+"》" + " 作者: " + author)
                self.path_label.setText("文件路径: " + self.file_path)
                for item in markdown:
                    pureText = ' '.join(item).replace("#", "")
                    if(len(pureText)>1000):
                        self.text.append(pureText)
                        self.text_area.append(pureText) 
                self.display_page(0)  
            # 生成视频按钮和播放按钮可用
                self.generate_audio_button.setEnabled(True)
            else:
                pass  # 用户选择取消后，不做任何操作
            
            # 生成音频函数
    def generateAudioFile(self):
                self.generate_audio_button.setEnabled(False)
                self.generate_audio_button.setText("正在生成音频...")
                thread = threading.Thread(target=self.azure_audio_gen_thread)
                thread.start()
        
            # 生成音频线程
    def azure_audio_gen_thread(self):
            azure_audio_gen(self.text[self.current_page],self.lang,self.title,self.current_page)
            self.generate_audio_button.setText("生成音频")
            self.generate_audio_button.setEnabled(True) 
    
    def prev_page(self):
        if self.current_page > 0:
            self.display_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < len(self.text) :
            self.display_page(self.current_page + 1)
    
     # 展示页面
    def display_page(self, page):
        start_index = page
        end_index = start_index +1
        # 清除页面内容
        self.text_area.clear()
        for line in self.text[start_index:end_index]:
            # 添加当前
            self.text_area.append(line)
        self.current_page = page
        # 对页面按钮进行更新
        self.update_page_buttons()
        self.page_label.setText(f"第 {self.current_page + 1} 页")
        self.text_area.verticalScrollBar().setValue(0) 

    def update_page_buttons(self):
        self.prev_page_button.setEnabled(self.current_page > 0)
        self.next_page_button.setEnabled(self.current_page < len(self.text))

    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
