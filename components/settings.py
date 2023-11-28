from PyQt5.QtWidgets import QDialog, QLineEdit, QLabel, QVBoxLayout, QPushButton, QComboBox
import json

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowTitle('设置')
        self.setFixedSize(400, 400)  # 设置窗口大小
        layout = QVBoxLayout(self)

        self.open_ai_label = QLabel("Open AI API Key")
        self.open_ai_input = QLineEdit(self)
        layout.addWidget(self.open_ai_label)
        layout.addWidget(self.open_ai_input)

        self.azure_sub_label = QLabel("Azure Subscription")
        self.azure_sub_input = QLineEdit(self)
        layout.addWidget(self.azure_sub_label)
        layout.addWidget(self.azure_sub_input)

        self.azure_reg_label = QLabel("Azure Region")
        self.azure_reg_input = QLineEdit(self)
        layout.addWidget(self.azure_reg_label)
        layout.addWidget(self.azure_reg_input)

        self.language_label = QLabel("使用语言")
        self.language_input = QComboBox(self)
        self.language_input.addItems(["中文", "英文", "日文"])  # 添加语言选择
        layout.addWidget(self.language_label)
        layout.addWidget(self.language_input)

        self.audio_label = QLabel("语音输出")
        self.audio_input = QComboBox(self)
        self.audio_input.addItems(['zh-CN-YunzeNeural', 'zh-CN-YunjieNeural'])  
        layout.addWidget(self.audio_label)
        layout.addWidget(self.audio_input)

        self.llm_label = QLabel("大语言模型")
        self.llm_input = QComboBox(self)
        self.llm_input.addItems(['gpt-3.5-turbo-0301', 'gpt-4','gpt-3.5-turbo-16k-0613','gpt-3.5-turbo','gpt-4-32k','gpt-4-32k-0613',])  
        layout.addWidget(self.llm_label)
        layout.addWidget(self.llm_input)

        self.save_button = QPushButton('确认', self)
        self.save_button.clicked.connect(self.save_settings)
        layout.addWidget(self.save_button)

        self.settings = {}  # 创建一个字典来存储设置

        # 读取 settings.json 文件并填入值
        try:
            with open('settings.json', 'r') as f:
                self.settings = json.load(f)
                self.open_ai_input.setText(self.settings.get('open_ai_key', ''))
                self.azure_sub_input.setText(self.settings.get('azure_sub', ''))
                self.azure_reg_input.setText(self.settings.get('azure_reg', ''))
                index = self.language_input.findText(self.settings.get('language', ''))
                if index != -1:
                    self.language_input.setCurrentIndex(index)
        except Exception as e:
            print(f'Error loading settings: {e}')

    def save_settings(self):
        settings = {
            'open_ai_key': self.open_ai_input.text(),
            'azure_sub': self.azure_sub_input.text(),
            'azure_reg': self.azure_reg_input.text(),
            'language': self.language_input.currentText()  # 获取当前选中的语言
        }
        with open('settings.json', 'w') as f:  # 将设置写入到 settings.json 文件中
            json.dump(settings, f)
        self.close()