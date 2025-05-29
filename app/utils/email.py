from aiosmtplib import SMTP
from email.message import EmailMessage
from app.core.config import settings
from app.models.user import User


async def send_email_async(to: str, subject: str, body: str):
    msg = EmailMessage()
    msg["From"] = f"{settings.SENDER_NAME} <{settings.SENDER_EMAIL}>"
    msg["To"] = to
    msg["Subject"] = subject
    msg.set_content(body)

    smtp = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=True
    )
    await smtp.connect()
    #await smtp.starttls()
    await smtp.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
    await smtp.send_message(msg)
    await smtp.quit()


def send_verification_email(email: str, token: str):
    verify_url = f"http://localhost:8000/auth/verify-email?token={token}"
    print(f"[EMAIL] To: {email}\nVerify your account: {verify_url}")


async def send_password_reset_email(email, token: str):
    reset_link = f"http://localhost:8000/auth/reset-password?token={token}"
    subject = "Reset your password"
    body = f"""
    Hi {email},

    You requested to reset your password. Click the link below:

    {reset_link}

    If you didn't request this, you can ignore this message.
    """

    await send_email_async(
        to=email,
        subject=subject,
        body=body
    )

#def send_password_reset_email(email: str, token: str):
    # reset_url = f"http://localhost:8000/auth/reset-password?token={token}"
    # print(f"[EMAIL] To: {email}\nReset your password: {reset_url}")