import os
import azurelocal.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import json

# Get the current working directory
cwd = os.getcwd()


def load_settings():
    try:
        with open('settings.json', 'r') as f:
            settings = json.load(f)
    except FileNotFoundError:
        settings = {}
    return settings
settings = load_settings()
subscription = settings.get('subscription', 'a')
region = settings.get('region', 'japanwest')

speech_config = speechsdk.SpeechConfig(subscription,region)

speech_sdk_path = os.path.join(cwd, "azurelocal/cognitiveservices/speech")
dylib_path = os.path.join(cwd, "azurelocal/cognitiveservices/speech/libMicrosoft.CognitiveServices.Speech.core.dylib")

speech_config.set_property_by_name("speechsdk.imports.path", speech_sdk_path)
speech_config.set_property_by_name("speechsdk.imports.dylib_path", dylib_path)
def azure_audio_gen(text,voice,title,chapter):
    print(voice,"生成MP3文件中...",text)
    """performs speech synthesis to a mp3 file"""
    speech_config.speech_synthesis_voice_name=voice
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
    desktop = os.path.join(os.path.expanduser("~"), "Desktop")
    file_name = os.path.join(desktop, str(title) + "-" + str(chapter) + ".mp3")
    file_config = speechsdk.audio.AudioOutputConfig(filename=file_name)
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=file_config)
    print("Enter some text that you want to synthesize, Ctrl-Z to exit")
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("文本合成 [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("文本合成: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("错误信息: {}".format(cancellation_details.error_details))
