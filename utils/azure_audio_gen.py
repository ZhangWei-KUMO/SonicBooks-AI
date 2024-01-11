import os
import azurelocal.cognitiveservices.speech as speechsdk
import json
import sys
from PySide6.QtWidgets import QMessageBox
from PySide6.QtCore import QObject, Signal, Slot

# Get the current working directory
cwd = os.getcwd()

if getattr(sys, 'frozen', False):
            # 如果程序被打包了，则使用这个路径
            application_path = sys._MEIPASS
else:
         # 如果程序没有被打包，则使用当前文件的路径
            application_path = os.path.dirname(os.path.abspath(__file__))

settings_path = os.path.join(application_path, 'settings.json')


def load_settings():
    try:
        with open(settings_path, 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}
    return settings
settings = load_settings()

subscription = settings.get('azure_sub','a')
region = settings.get('azure_reg', 'japanwest')

speech_config = speechsdk.SpeechConfig(subscription,region)

speech_sdk_path = os.path.join(cwd, "azurelocal/cognitiveservices/speech")
dylib_path = os.path.join(cwd, "azurelocal/cognitiveservices/speech/libMicrosoft.CognitiveServices.Speech.core.dylib")

speech_config.set_property_by_name("speechsdk.imports.path", speech_sdk_path)
speech_config.set_property_by_name("speechsdk.imports.dylib_path", dylib_path)


# 定义一个包含信号的类
class Signaller(QObject):
    error_signal = Signal(str)  # 定义一个传递字符串的信号

# 创建槽函数，用于在主线程中显示消息框
@Slot(str)
def show_error_message(error_message):
    QMessageBox.critical(None, "Error", error_message)


signaller = Signaller()
signaller.error_signal.connect(show_error_message)

def azure_audio_gen(text,voice,title,chapter):
    """performs speech synthesis to a mp3 file"""
    speech_config.speech_synthesis_voice_name=voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = os.path.join(desktop, str(title) + "-" + str(chapter) + ".mp3")
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("文本合成 [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("错误信息: {}".format(cancellation_details.error_details))
                signaller.error_signal.emit("请在设置中检查您的密钥和区域API KEY填写是否正确")

