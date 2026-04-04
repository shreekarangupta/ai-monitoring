import smtplib
from email.message import EmailMessage
import os
import time

# 🔒 YOUR FIXED EMAIL (OWNER)
EMAIL = "laddusharma123321@gmail.com"
PASSWORD = "movolzxnljsxmchk"


def send_email(image_path, to_email):
    try:
        if not to_email:
            print("⚠️ No user email provided")
            return

        msg = EmailMessage()
        msg['Subject'] = '🚨 AI CCTV Alert: Motion Detected!'
        msg['From'] = EMAIL
        msg['To'] = to_email  # ✅ dynamic user email

        # 🧠 Smart message
        msg.set_content(f"""
🚨 Alert from AI CCTV System

Motion / Object Detected!

📅 Time: {time.strftime('%Y-%m-%d %H:%M:%S')}

Check attached image for details.

-- AI Monitoring System
""")

        # 📸 attach image
        with open(image_path, 'rb') as f:
            msg.add_attachment(
                f.read(),
                maintype='image',
                subtype='jpeg',
                filename=os.path.basename(image_path)
            )

        # 📧 send email
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(EMAIL, PASSWORD)
            smtp.send_message(msg)

        print(f"✅ Email sent to {to_email}")

    except Exception as e:
        print("❌ Email Error:", e)