import time
import azure.cognitiveservices.speech as speechsdk
import json

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
audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)

def debounce(seconds):
    def decorator(func):
        last_called = [0]
        def wrapper(*args, **kwargs):
            elapsed_time = time.time() - last_called[0]
            if elapsed_time > seconds:
                last_called[0] = time.time()
                return func(*args, **kwargs)
            else:
                print(f"{func.__name__} 在 {seconds} 秒内不能被再次调用。")
        return wrapper
    return decorator

@debounce(10)
def azure_tts(text,voice):
    # The language of the voice that speaks.
    speech_config.speech_synthesis_voice_name=voice
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
    speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()
 
    if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("文本合成 [{}]".format(text))
    elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = speech_synthesis_result.cancellation_details
        print("文本合成: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("错误信息: {}".format(cancellation_details.error_details))
                print("你是否正确设置了Azure的API KEY?")