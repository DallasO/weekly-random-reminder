from datetime import datetime
import random
import secrets
import paho.mqtt.client as mqtt # https://pypi.org/project/paho-mqtt/



# ++++++++++++++++++++++++++++++++++++++++++++
preferredDateFormat = "%Y-%m-%d %H:%M:%S"
today               = datetime.now()
dayOfMonth          = today.strftime("%d")
month               = today.strftime("%m")
year                = today.strftime("%Y")
minDayOfWeek        = 1 # Monday
maxDayOfWeek        = 5 # Friday
daysOfWeek          = maxDayOfWeek - minDayOfWeek + 1 # range of max - min
# ++++++++++++++++++++++++++++++++++++++++++++
# --------------------------------------------
# Set these variables to alter behavior
# --------------------------------------------
# Filename to save upcoming reminders
reminderFile = 'reminderFile'
# Filename to save history
reminderHistory = 'reminderHistory'
# Log filename
reminderLog = 'reminder.log'
# Maximum times to be reminded in a week
upperLimit = 2
# Minimum days between reminders
# minDaysBetween = int(daysOfWeek / upperLimit)
minDaysBetween = 1
# Earliest time to send reminder (24hr)
earliestHour = 17
# latest time to send reminder (24hr)
latestHour = 21
# ++++++++++++++++++++++++++++++++++++++++++++



# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    # print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe([(userdata[0], 0)])
    client.publish(userdata[0], userdata[1], 0, True)

# Called when a message has been received on a topic that the client subscribes to .
def on_message(client, userdata, msg):
    # print("Message received:", msg.topic+" "+str(msg.payload, 'utf-8'))
    if str(msg.topic) == str(userdata[0]) and str(msg.payload, 'utf-8') == str(userdata[1]):
        # print("Received correct message!")
        client.disconnect()

def send_notification():
    # print("Send Notification")
    # If multiple Topics, notify a random one
    if len(secrets.clientTopics) > 1:
        topicInd = random.randint(0, len(secrets.clientTopics) - 1)
    else:
        topicInd = secrets.clientTopics[0]
    try:
        client = mqtt.Client('weekly-random-reminder', False)
        client.username_pw_set(secrets.clientUserName, secrets.clientPass)
        client.user_data_set([secrets.clientTopics[topicInd], secrets.clientPayload])
        client.on_connect   = on_connect
        client.on_message   = on_message

        client.connect(secrets.clientIP, secrets.clientPort, 60)
        client.loop_forever()
    except ConnectionRefusedError as e:
        errors.append(str(today)+":\tConnection refused. Is the MQTT broker online?")



# BEGIN :: function to overwrite file
def writeToFile(filename = reminderFile, list = None, permissions = 'w+'):
    if list != None:
        try:
            with open(filename, permissions) as f:
                try:
                    for item in list:
                        f.write(item + "\n")
                except ValueError as e:
                    errors.append(str(today) + ":\tError ##:\tlist is not of type list.")
        except FileNotFoundError as e:
            errors.append(str(today) + ":\tError ##:\tFileNotFoundError. Does " + filename + " exist?")
# END :: function to overwrite file



reminders = []
errors = []



# BEGIN :: Read file and save stored dates
try:
    with open(reminderFile, 'r') as f:
        for line in f:
            reminders.append(datetime.strptime(line.strip(), preferredDateFormat))
except FileNotFoundError as e:
    errors.append(str(today) + ":\tError ##:\tFileNotFoundError. Assuming first run.")    # First time running or dates were reset
# END :: Read file and save stored dates



# BEGIN :: Check if the reminder should go off
if len(reminders):
    # Get first reminder
    currentReminder = reminders[0]
    oldReminders = []

    if today > currentReminder:
        # Trigger Notification
        # log any notification errors
        send_notification()
        # remove this from reminders
        currentReminder = str(reminders.pop(0))
        oldReminders.append(currentReminder)
        writeToFile(reminderHistory, oldReminders, "a+")

# END :: Check if the reminder should go off



# BEGIN :: Create new dates to save to file
if len(reminders) < upperLimit:
    while len(reminders) < upperLimit:
        randomDate = random.randint(minDaysBetween, 6)
        possibleDate = True

        if len(reminders) >= 0 and len(reminders) <= upperLimit:
            dates = [int(date.strftime("%w")) for date in reminders]
            for date in dates:
                if (
                    randomDate == date or
                    randomDate == date + 1 or
                    randomDate + 1 == date or
                    randomDate == date + 2 or
                    randomDate + 2 == date
                    ):
                    possibleDate = False

        if possibleDate == True:
            randomHour      = str(random.randint(earliestHour, latestHour))
            randomMinute    = str(random.randint(0, 59))
            saveDay         = str(int(dayOfMonth) + randomDate)
            saveTime        = datetime.strptime(
                    year + "-" + month + "-" + saveDay + " " + randomHour + ":" + randomMinute + ":00",
                    preferredDateFormat
                )
            reminders.append(saveTime)
    reminders = [str(reminder) for reminder in reminders]
    reminders.sort()
    writeToFile(reminderFile, reminders)
if len(errors):
    writeToFile(reminderLog, errors)
# END :: Create new dates to save to file
