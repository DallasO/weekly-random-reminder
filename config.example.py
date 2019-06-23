#
#           THIS IS THE CONFIG FILE
#

# MQTT
#
# If you would like to use MQTT as your push service, configure these options
#
# CONFIG.pushService.mqtt.clientUserName = 'mqttBroker'
# CONFIG.pushService.mqtt.clientPass     = '*********************'
# CONFIG.pushService.mqtt.clientTopics   = ["main/sendnotification/random1", "main/sendnotification/random2"]
# CONFIG.pushService.mqtt.clientPayload  = "ON"
# CONFIG.pushService.mqtt.clientIP       = "127.0.0.1"
# CONFIG.pushService.mqtt.clientPort     = 1883 # 1883 for TCP, 8883 for TLS

# Webhooks

# If you would like to use a webhook/API
# Data will be sent as json
#
# CONFIG.pushService.webhook.url  = "localhost/<token>" # Or example.com/<token>

# Reminders
CONFIG.reminders = {
    "yoga": {
        
    },
}
