# Azure 语音合成服务 Python可用方法

1. get_voices_async(locale)  异步获取可用的语音。
2. speak_ssml_async 以阻塞（同步）模式对 ssml 执行综合。
3. speak_text 以阻塞（同步）模式对纯文本执行合成。
4. speak_text_async 以非阻塞（同步）模式对纯文本执行合成。
5. start_speaking_ssml 以阻塞（同步）模式开始 ssml 综合。
6. start_speaking_ssml_async 以非阻塞（异步）模式开始 ssml 综合。
7. start_speaking_text 以阻塞（同步）模式开始纯文本合成。
8. start_speaking_text_async 以非阻塞（异步）模式开始对纯文本进行合成。
9. stop_speaking 同步终止正在进行的综合操作。该方法将停止播放并清除PullAudioOutputStream中未读的数据。
10. stop_speaking_async 异步终止正在进行的综合操作。该方法将停止播放并清除PullAudioOutputStream中未读的数据。

参考文献：
1. [Microsoft SpeechSynthesizer Class](https://learn.microsoft.com/en-us/python/api/azure-cognitiveservices-speech/azure.cognitiveservices.speech.speechsynthesizer?view=azure-python)