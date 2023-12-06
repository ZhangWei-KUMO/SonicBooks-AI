from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog,QLabel,QGridLayout,QSplitter,QTextEdit,QMenuBar,QMenu,QAction,QMessageBox,QMainWindow
from utils.azure_audio_gen import azure_audio_gen
from utils.azure_tts import azure_tts
import epubs
from PyQt5.QtCore import Qt
import threading
import sys
from components.settings import SettingsDialog
class MyApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.title = ''
        self.lang = 'zh-CN-YunzeNeural'
        self.text = []
        self.current_index = 0
        self.current_page = 0  # 当前页数
        
    def closeEvent(self, event):
        print("应用程序已关闭")  # 打印程序关闭消息
        super().closeEvent(event)

    def initUI(self):
        self.setWindowTitle('TubeV AI电子书助手')
        # Create menu bar
        menubar = QMenuBar(self)
        menubar.setFixedWidth(500) 
        
        # Create 'Settings' menu
        settings = QAction('设置', self)
        settings.triggered.connect(self.open_settings)
        
        # Create 'Version' menu
        version = QAction('版本号', self)
        version.triggered.connect(self.show_version)

        # Add actions to menu bar
        fileMenu = menubar.addMenu('菜单')
        fileMenu.addAction(settings)
        fileMenu.addAction(version)
        grid = QGridLayout()
        self.setLayout(grid)
        widget_left = QWidget()
        widget_right = QWidget()
        widget_bottom = QWidget() 
        widget_left.setStyleSheet("background-color: white;")
        widget_bottom.setMaximumHeight(80)
        # 将这两个标签添加到底部布局中
        # 在widget_bottom上创建一个布局
        layout_bottom = QVBoxLayout(widget_bottom)

        # 创建path_label和title_label
       
        self.page_label = QLabel("") 
        self.path_label = QLabel(" ")
        self.title_label = QLabel(" ")
        layout_bottom.addWidget(self.title_label)
        layout_bottom.addWidget(self.path_label)
        layout_bottom.addWidget(self.page_label) 
        splitter = QSplitter(self)
        splitter.setStyleSheet("QSplitter::handle {background-color: transparent; margin:0px; padding:0px;}")
        splitter.addWidget(widget_left)
        splitter.addWidget(widget_right)
        self.setGeometry(300, 300, 500, 400)
        splitter.setSizes([80, 20])

        layout_right = QVBoxLayout(widget_right)
        select_book = QPushButton('选择电子书', self)
        prev_page_button = QPushButton('上一页', self, enabled=False)
        next_page_button = QPushButton('下一页', self,  enabled=False)
        generateAudio = QPushButton('生成音频', self, enabled=False)
        play = QPushButton('播放', self, enabled=False)
        
        layout_right.addWidget(select_book)
        layout_right.addWidget(generateAudio)
        layout_right.addWidget(play)
        layout_right.addWidget(prev_page_button)
        layout_right.addWidget(next_page_button)

        select_book.clicked.connect(self.select_file)
        prev_page_button.clicked.connect(self.prev_page)
        next_page_button.clicked.connect(self.next_page)
        play.clicked.connect(self.play)
        generateAudio.clicked.connect(self.generateAudioFile)

        self.text_area = QTextEdit(widget_left)
        self.text_area.setStyleSheet("border: 0;")  # 添加这行代码
        self.text_area.setReadOnly(True)  # 设置为只读
        self.text_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 隐藏垂直滚动条
        layout_left = QVBoxLayout(widget_left)
        layout_left.addWidget(self.text_area)

        grid.addWidget(splitter, 0, 0)
         # 将底部的widget添加到垂直布局中
        grid.addWidget(widget_bottom) 
        self.prev_page_button = prev_page_button
        self.next_page_button = next_page_button
        self.generateAudio = generateAudio
        self.play = play
    
        self.show()

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
            self.generateAudio.setEnabled(True)
            self.play.setEnabled(True)
          

        else:
            pass  # 用户选择取消后，不做任何操作

    def open_settings(self):
        self.settings_dialog = SettingsDialog(self)
        self.settings_dialog.show()

    def show_version(self):
        version_info = QMessageBox()
        version_info.setWindowTitle("版本信息")
        version_info.setText("苏州云帧数浪信息科技有限公司版权所有 @2023-2024 版本号 1.0.0")
        version_info.exec_()

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
    # 翻页
    def prev_page(self):
        if self.current_page > 0:
            self.display_page(self.current_page - 1)

    def next_page(self):
        if self.current_page < len(self.text) :
            self.display_page(self.current_page + 1)

    def play(self):
        self.generateAudio.setEnabled(False)
        self.play.setText("语音播放中...")
        thread = threading.Thread(target=self.azure_tts_thread)
        thread.start()

    def on_finished(self):
        pass
    
    def generateAudioFile(self):
        self.generateAudio.setEnabled(False)
        self.generateAudio.setText("正在生成音频...")
        thread = threading.Thread(target=self.azure_audio_gen_thread)
        thread.start()

    def azure_audio_gen_thread(self):
        azure_audio_gen(self.text[self.current_page],self.lang,self.title,self.current_page)
        self.generateAudio.setText("生成音频")
        self.generateAudio.setEnabled(True) 

    def azure_tts_thread(self):
        azure_tts(self.text[self.current_page][:100],self.lang)
        self.play.setText("播放")
        self.generateAudio.setEnabled(True)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())



