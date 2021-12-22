import RecordingData as rd1
import notify2



mood = 2


message = rd1.outputActions(mood)
notify2.init("Emotion Output")
notification = notify2.Notification(summary = "Mood Reader", message =  message)
notification.set_urgency(notify2.URGENCY_NORMAL)
notification.set_timeout(2000)
notification.show()