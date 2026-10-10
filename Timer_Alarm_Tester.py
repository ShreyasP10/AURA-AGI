from TOOLS.TimeComponents_mod import extract_time_components_mod
from TOOLS.SYSTEM_SETTINGS import Alarms
from ENGINE.STT import DevsDoCode
from ENGINE.TTS import edge_tts

if __name__ == "__main__":
    listener = DevsDoCode.SpeechToTextListener(
        language="en-IN"
    )  # You can specify the desired language here
    alarm_manager = Alarms.AlarmManager(verbose=True)

    while True:
        speech = listener.listen()
        print("FINAL EXTRACTION: ", speech)
        # hour, minute, am_pm, date, alarm_timer = extract_time_components(speech)
        hour, minute, am_pm, date, alarm_timer = extract_time_components_mod(speech)
        print(
            f"Hour: {hour}, Minute: {minute}, AM/PM: {am_pm}, Date: {date}, Alarm/Timer: {alarm_timer}"
        )
        response = {"status": "error", "message": "Could not determine if you wanted an alarm or timer."}
        if alarm_timer == "alarm":
            response = alarm_manager.set_alarm(hour, minute, am_pm, date)
        elif alarm_timer == "timer":
            response = alarm_manager.set_timer(hour, minute)
        print(
            "Response Status: ",
            response["status"],
            "Response Message: ",
            response["message"],
        )
        edge_tts.speak(response["message"])
