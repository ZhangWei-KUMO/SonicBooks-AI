import sys

from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget,
                               QSplitter, QTextEdit, QPushButton, QFileDialog, QMessageBox)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('TubeV AI电子书助手')
        self.setGeometry(300, 300, 500, 400)

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
        layout_left.addWidget(self.text_area)
        splitter.addWidget(widget_left)

        # Right Widget (Buttons)
        widget_right = QWidget()
        layout_right = QVBoxLayout(widget_right)
        self.select_book_button = QPushButton('选择电子书')
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
        layout_right.addWidget(self.generate_audio_button)
        layout_right.addWidget(self.play_button)
        layout_right.addWidget(self.prev_page_button)
        layout_right.addWidget(self.next_page_button)
        splitter.addWidget(widget_right)

        # Bottom Widget (Status Labels)
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

        # Connect buttons to their functions (assuming you have or will create these functions)
        # self.select_book_button.clicked.connect(self.select_book)
        # self.prev_page_button.clicked.connect(self.prev_page)
        # self.next_page_button.clicked.connect(self.next_page)
        # self.generate_audio_button.clicked.connect(self.generate_audio)
        # self.play_button.clicked.connect(self.play)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
