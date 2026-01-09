import paho.mqtt.client as mqtt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP Email config
EMAIL_FROM = ""
EMAIL_TO = ""
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 465
EMAIL_PASSWORD = ""

def send_email(alert_type, value, recommendation, color="#FF0000"):
    """
    alert_type : titre de l'alerte (Water / Flood / Fire)
    value : valeur détectée
    recommendation : texte recommandation
    color : couleur du titre
    """
    # Création email HTML avec style CSS
    msg = MIMEMultipart("alternative")
    msg['Subject'] = f"ALERT: {alert_type}"
    msg['From'] = EMAIL_FROM
    msg['To'] = EMAIL_TO

    html = f"""
    <html>
      <head>
        <style>
          body {{
            font-family: Arial, sans-serif;
            background-color: #f4f4f4;
            color: #333;
          }}
          .container {{
            background-color: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
            width: 500px;
            margin: auto;
          }}
          h2 {{
            color: {color};
            text-align: center;
          }}
          p {{
            font-size: 16px;
          }}
          .value {{
            font-weight: bold;
          }}
          .recommendation {{
            margin-top: 15px;
            padding: 10px;
            background-color: #ffefef;
            border-left: 5px solid {color};
            border-radius: 4px;
          }}
        </style>
      </head>
      <body>
        <div class="container">
          <h2>{alert_type}</h2>
          <p>Valeur détectée: <span class="value">{value}</span></p>
          <div class="recommendation">
            <b>Recommandation:</b> {recommendation}
          </div>
        </div>
      </body>
    </html>
    """
    part = MIMEText(html, "html")
    msg.attach(part)

    with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
        server.login(EMAIL_FROM, EMAIL_PASSWORD)
        server.sendmail(EMAIL_FROM, EMAIL_TO, msg.as_string())

# Callback MQTT
def on_message(client, userdata, msg):
    topic = msg.topic
    try:
        value = float(msg.payload.decode())
    except:
        value = msg.payload.decode()

    if topic == "sensors/waterlevel" and value > 80:
        send_email(
            "Water Level Alert", 
            f"{value} cm", 
            "Evacuate the area and check water barriers.",
            color="#1E90FF"  # bleu
        )
    elif topic == "sensors/floodlevel" and value > 40:
        send_email(
            "Flood Level Alert", 
            f"{value} cm", 
            "Activate flood protection systems and inform authorities.",
            color="#FF4500"  # orange
        )
    elif topic == "sensors/fire" and value == 1:
        send_email(
            "Fire Alert", 
            "Detected!", 
            "Call fire services immediately and evacuate.",
            color="#FF0000"  # rouge
        )

# MQTT setup
client = mqtt.Client()
client.connect("localhost", 1883, 60)
client.subscribe("sensors/waterlevel")
client.subscribe("sensors/floodlevel")
client.subscribe("sensors/fire")
client.on_message = on_message

print("Alert sender running...")
client.loop_forever()
