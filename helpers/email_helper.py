import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils.macros import GMAIL_APP_PASSWORD

def get_homework_mail_content(RECEIVER_MAIL, STUDENT_FIRST_NAME, STUDENT_LAST_NAME, HOMEWORK_CONTENT):
    SENDER_MAIL = "contact.edsquared@gmail.com"
    EMAIL_SUBJECT = "Homework Update"
    EMAIL_BODY = f"""
            <html>
            <head>
            <style>
            .email-container {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
            .logo {{
            display: block;
            margin: 0 auto;
            }}
            .content {{
            margin-top: 20px;
            }}
            .link_btn {{
            border: 1px solid white;
            border-radius: 10px;
            background-color: blue;
            color: white;
            }}
            </style>
            </head>
            <body>
            <div class="email-container">
            <img src="cid:logo_image" alt="Logo" class="logo" width="100" height="100"/>
            <div class="content">
            <p>Hello {STUDENT_FIRST_NAME} {STUDENT_LAST_NAME}!</p>
            <p>A new homework has been set: <strong>{HOMEWORK_CONTENT}</strong></p>
            <p>You can view and mark it as complete within the app, <a id='link_btn' href='https://apps.apple.com/it/app/edsquared/id6615075755?l=en-GB'>EdSquared</a></p>
            </div>
            </div>
            </body>
            </html>
            """

    return {"SENDER_MAIL":SENDER_MAIL, "RECEIVER_MAIL":RECEIVER_MAIL, "EMAIL_SUBJECT":EMAIL_SUBJECT, "EMAIL_BODY":EMAIL_BODY}

def get_grade_set_content(RECEIVER_MAIL, STUDENT_FIRST_NAME, STUDENT_LAST_NAME):
    SENDER_MAIL = "contact.edsquared@gmail.com"
    EMAIL_SUBJECT = "New Grade Added"
    EMAIL_BODY = f"""
            <html>
            <head>
            <style>
            .email-container {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
            .logo {{
            display: block;
            margin: 0 auto;
            }}
            .content {{
            margin-top: 20px;
            }}
            .link_btn {{
            border: 1px solid white;
            border-radius: 10px;
            background-color: blue;
            color: white;
            }}
            </style>
            </head>
            <body>
            <div class="email-container">
            <img src="cid:logo_image" alt="Logo" class="logo" width="100" height="100"/>
            <div class="content">
            <p>Hello {STUDENT_FIRST_NAME} {STUDENT_LAST_NAME}!</p>
            <p>Your tutor added new grade.</strong></p>
            <p>You can view the updates in the app, <a id='link_btn' href='https://apps.apple.com/it/app/edsquared/id6615075755?l=en-GB'>EdSquared</a></p>
            </div>
            </div>
            </body>
            </html>
            """

    return {"SENDER_MAIL":SENDER_MAIL, "RECEIVER_MAIL":RECEIVER_MAIL, "EMAIL_SUBJECT":EMAIL_SUBJECT, "EMAIL_BODY":EMAIL_BODY}

def get_verification_code_content(RECEIVER_MAIL, VERIFICATION_CODE):
    SENDER_MAIL = "contact.edsquared@gmail.com"
    EMAIL_SUBJECT = "RESET PASSWORD: Verfication Code"
    EMAIL_BODY = f"""
            <html>
            <head>
            <style>
            .email-container {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
            .logo {{
            display: block;
            margin: 0 auto;
            }}
            .content {{
            margin-top: 20px;
            }}
            .link_btn {{
            border: 1px solid white;
            border-radius: 10px;
            background-color: blue;
            color: white;
            }}
            </style>
            </head>
            <body>
            <div class="email-container">
            <img src="cid:logo_image" alt="Logo" class="logo" width="100" height="100"/>
            <div class="content">
            <p>Hi,</p>
            <p>We received your Forgot Password request.</p>
            <p><strong>For the email {RECEIVER_MAIL}, here is the temporary verification code for the account: {VERIFICATION_CODE}</strong></p>
            <p>If you didn't request the code, you can safely disregard this message.</p>
            <p>If you have any questions or need further assistance, please do not hesitate to contact our support team.</p>
            <p>Best regards,</p>
            <p><a id='link_btn' href='https://apps.apple.com/it/app/edsquared/id6615075755?l=en-GB'>EdSquared</a></p>
            </div>
            </div>
            </body>
            </html>
            """

    return {"SENDER_MAIL":SENDER_MAIL, "RECEIVER_MAIL":RECEIVER_MAIL, "EMAIL_SUBJECT":EMAIL_SUBJECT, "EMAIL_BODY":EMAIL_BODY}

def get_tutor_code_mail_content(RECEIVER_MAIL, ADMIN_CODE):
    SENDER_MAIL = "contact.edsquared@gmail.com"
    EMAIL_SUBJECT = "Tutor Registration Code"
    EMAIL_BODY = f"""
            <html>
            <head>
            <style>
            .email-container {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
            .logo {{
            display: block;
            margin: 0 auto;
            }}
            .content {{
            margin-top: 20px;
            }}
            .link_btn {{
            border: 1px solid white;
            border-radius: 10px;
            background-color: blue;
            color: white;
            }}
            </style>
            </head>
            <body>
            <div class="email-container">
            <img src="cid:logo_image" alt="Logo" class="logo" width="100" height="100"/>
            <div class="content">
            <p>Hello {RECEIVER_MAIL},</p>
            <p>Thank you for registering as an admin on EdSquared. Below is your unique verification code:</p>
            <p><strong>{ADMIN_CODE}</strong></p>
            <p>Please use this code to verify your email and activate your admin account. Once verified, you can share this code with your students. When your students use this code while creating their accounts, they will be linked to your admin account, allowing you to monitor their grades and progress.</p>
            <p>Keep this code safe and do not share it with anyone other than your students.</p>
            <p>To learn more about the app and how to use it, please refer to this <a id='link_btn' href='https://github.com/Cas-07/EdSquared_documentation/blob/main/support.md'>support</a> page.
            <p>If you have any questions or need further assistance, please do not hesitate to contact our support team by replying to this email.</p>
            <p>Best regards,</p>
            <p><a id='link_btn' href='https://apps.apple.com/it/app/edsquared/id6615075755?l=en-GB'>EdSquared</a></p>
            </div>
            </div>
            </body>
            </html>
            """

    return {"SENDER_MAIL":SENDER_MAIL, "RECEIVER_MAIL":RECEIVER_MAIL, "EMAIL_SUBJECT":EMAIL_SUBJECT, "EMAIL_BODY":EMAIL_BODY}

def get_student_registration_update_mail(RECEIVER_MAIL, S_FIRST_NAME, S_LAST_NAME, S_EMAIL):
    SENDER_MAIL = "contact.edsquared@gmail.com"
    EMAIL_SUBJECT = "Someone Registered using your tutor code"
    EMAIL_BODY = f"""
            <html>
            <head>
            <style>
            .email-container {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            }}
            .logo {{
            display: block;
            margin: 0 auto;
            }}
            .content {{
            margin-top: 20px;
            }}
            .link_btn {{
            border: 1px solid white;
            border-radius: 10px;
            background-color: blue;
            color: white;
            }}
            </style>
            </head>
            <body>
            <div class="email-container">
            <img src="cid:logo_image" alt="Logo" class="logo" width="100" height="100"/>
            <div class="content">
            <p>Hello {RECEIVER_MAIL},</p>
            <p>{S_FIRST_NAME} {S_LAST_NAME} has registered using your Tutor Code.</p>
            <p><strong>Student's email: {S_EMAIL}</strong></p>
            <p>If you have any questions or need further assistance, please do not hesitate to contact our support team.</p>
            <p>Best regards,</p>
            <p><a id='link_btn' href='https://apps.apple.com/it/app/edsquared/id6615075755?l=en-GB'>EdSquared</a></p>
            </div>
            </div>
            </body>
            </html>
            """

    return {"SENDER_MAIL":SENDER_MAIL, "RECEIVER_MAIL":RECEIVER_MAIL, "EMAIL_SUBJECT":EMAIL_SUBJECT, "EMAIL_BODY":EMAIL_BODY}

def send_mail(SENDER_MAIL, RECEIVER_MAIL, EMAIL_SUBJECT, EMAIL_BODY):
    """Sends an email from the contact.edsquared@gmail.com to the receiver's email address.
    The email is sent through the Gmail SMTP server, this function relies on external libraries
    for handling email formatting and SMTP communication.

    Args:
        SENDER_MAIL (str): contact.edsquared@gmail.com
        RECEIVER_MAIL (str): The recipient's email address.
        EMAIL_SUBJECT (str): The subject line of the email.
        EMAIL_BODY (str): The HTML body content of the email.

    Returns:
        bool: Returns True if the email was sent successfully, False otherwise.

    Raises:
        smtplib.SMTPAuthenticationError: If the SMTP server authentication fails.
        Exception: If there is a general failure in sending the email."""
    try:
        msg = MIMEMultipart()
        msg['Subject'] = EMAIL_SUBJECT
        msg['From'] = SENDER_MAIL
        msg['To'] = RECEIVER_MAIL
        msg.attach(MIMEText(EMAIL_BODY, 'html'))
        with open('utils/graphics/logo.png', 'rb') as img:
            mime_image = MIMEImage(img.read())
            mime_image.add_header('Content-ID', '<logo_image>')
            mime_image.add_header('Content-Disposition', 'inline', filename='logo.png')
            msg.attach(mime_image)

        # SMTP server configuration MIME
        smtp_server = "smtp.gmail.com"
        smtp_port = 587
        email = SENDER_MAIL
        password = GMAIL_APP_PASSWORD

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(email, password)
            server.sendmail(email, [RECEIVER_MAIL], msg.as_string())
            print("Email sent successfully.")
            return True

    except smtplib.SMTPAuthenticationError as e:
        print(f"Failed to authenticate: {e}")
        return False
    except Exception as e:
        print(f"Failed to send email: {e}")
        return False
