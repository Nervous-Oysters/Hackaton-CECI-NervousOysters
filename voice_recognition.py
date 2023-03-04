import speech_recognition as sr
from pynput import mouse, keyboard

keyboard_controller = keyboard.Controller()
mouse_controller = mouse.Controller()



def recognize_speech_from_mic(recognizer, microphone):
    """Transcribe speech from recorded from `microphone`.

    Returns a dictionary with three keys:
    "success": a boolean indicating whether or not the API request was
               successful
    "error":   `None` if no error occured, otherwise a string containing
               an error message if the API could not be reached or
               speech was unrecognizable
    "transcription": `None` if speech could not be transcribed,
               otherwise a string containing the transcribed text
    """
    if not isinstance(recognizer, sr.Recognizer): raise TypeError("`recognizer` must be `Recognizer` instance")
    if not isinstance(microphone, sr.Microphone): raise TypeError("`microphone` must be `Microphone` instance")

    with microphone as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5) # duration : shorter respond faster (recommend no less than 0.5)
        audio = recognizer.listen(source, timeout=2)
        print("done listening")

    # set up the response object
    response = {
        "success": True,
        "error": None,
        "transcription": None
    }
    try:
        response["transcription"] = recognizer.recognize_google(audio, language='en-US', show_all=True)
    except sr.RequestError:
        # API was unreachable or unresponsive
        response["success"] = False
        response["error"] = "API unavailable"
    except sr.UnknownValueError:
        # speech was unintelligible
        response["error"] = "Unable to recognize speech"
    print(response)
    return response

#recognize_speech_from_mic(recognizer, microphone)