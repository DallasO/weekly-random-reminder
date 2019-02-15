#Python imports
import datetime, random, math



# Custom pip imports
import paho.mqtt.client as mqtt # https://pypi.org/project/paho-mqtt/



# Application imports
import secrets



# ++++++++++++++++++++++++++++++++++++++++++++
preferredDateFormat = "%Y-%m-%d %H:%M:%S"
today               = datetime.datetime.replace(datetime.datetime.now(), microsecond=0)
year                = int(today.strftime("%Y"))
month               = int(today.strftime("%m"))
dayOfMonth          = int(today.strftime("%d"))
minDayOfWeek        = 1 # Monday
maxDayOfWeek        = 5 # Friday
anyDay              = maxDayOfWeek + minDayOfWeek == 0
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
minDaysBetween = 2
# Limit times to send reminder (24hr)
earliestHour = 17
latestHour = 22
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
        topicInd = 0
    try:
        client = mqtt.Client('weekly-random-reminder', False)
        client.username_pw_set(secrets.clientUserName, secrets.clientPass)
        client.user_data_set([secrets.clientTopics[topicInd], secrets.clientPayload])
        client.on_connect = on_connect
        client.on_message = on_message

        client.connect(secrets.clientIP, secrets.clientPort)
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
                    errors.append(str(today) + ":\tError ##0:\tlist is not of type list.")
        except FileNotFoundError as e:
            errors.append(str(today) + ":\tError ##1:\tFileNotFoundError. Does " + filename + " exist?")
    else:
        errors.append(str(today) + ":\tError ##1:\tValueError. Tried to write nothing to file")
# END :: function to overwrite file



reminders = []
errors = []



# BEGIN :: Read file and save stored dates
try:
    with open(reminderFile, 'r') as f:
        for line in [l.strip() for l in f]:
            try:
                reminders.append(datetime.datetime.strptime(line, preferredDateFormat))
            except ValueError as e:
                # Catch invalid dates
                dateFileError = str(today) + ":\tError ##2:\tValueError. "
                if len(line) > 0:
                    errors.append("%sInvalid date in %s - %s" % (dateFileError, reminderFile, line))
                else:
                    errors.append("%sInvalid date in %s." % (dateFileError, reminderFile))
except FileNotFoundError as e:
    errors.append(str(today) + ":\tError ##3:\tFileNotFoundError. Assuming first run.")
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
    infinityGauntlet = 0
    while len(reminders) < upperLimit:
        infinityGauntlet += 1
        randomDate = random.randint(minDaysBetween, max(minDaysBetween, math.ceil(7 / upperLimit)))
        possibleDate = True

        dates = [datetime.datetime.replace(reminder, hour=0, minute=0, second=0) for reminder in reminders] or []
        dates.append(datetime.datetime(year, month, dayOfMonth))

        testDay = max(dates) + datetime.timedelta(days=randomDate) # New Date at midnight
        testDayOfWeek = int(testDay.strftime("%w"))

        if not anyDay and (testDayOfWeek < minDayOfWeek or testDayOfWeek > maxDayOfWeek):
            possibleDate = False

        if infinityGauntlet > 3:
            possibleDate = True
            errors.append(str(today) + ":\tError ##4:\tGauntletError. Blocked a run to infinity.")

        if possibleDate == True:
            randomHour   = random.randint(earliestHour, latestHour)
            randomMinute = random.randint(0, 59)
            saveDay      = testDay + datetime.timedelta(hours=randomHour, minutes=randomMinute)
            reminders.append(saveDay)

    reminders = [str(reminder) for reminder in reminders]
    reminders.sort()
    writeToFile(reminderFile, reminders)

if len(errors):
    writeToFile(reminderLog, errors)
# END :: Create new dates to save to file
