"""Send mails for auth."""

from fastapi_jwt_auth import AuthJWT
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema

from backend.auth.auth_tokens import create_access_token, create_restore_token
from backend.settings import settings_mail

if settings_mail.is_enough_settings():
    conf = ConnectionConfig(
        MAIL_USERNAME=settings_mail.mail_address,
        MAIL_PASSWORD=settings_mail.mail_pwd,
        MAIL_FROM=settings_mail.mail_address,
        MAIL_FROM_NAME=settings_mail.mail_user,
        MAIL_PORT=settings_mail.mail_port,
        MAIL_SERVER=settings_mail.mail_server,
        MAIL_TLS=True,
        MAIL_SSL=False,
        USE_CREDENTIALS=True,
    )


async def send_activate_account_mail(
    user_id: int, email: str, authorize: AuthJWT
) -> None:
    """Send message for account activation."""
    if not settings_mail.is_enough_settings():
        print("Cannot send mail because not enough settings")
        raise AttributeError("Error while send Email")

    token: str = create_access_token(authorize, user_id)
    message: MessageSchema = MessageSchema(
        subject="Verify your e-mail address",
        recipients=[f"{email}"],
        body=f"""
                <div style="align-content: center;background-color: beige;width: 100%;height: auto">
                    <div style="text-transform: capitalize;font-size: 16px;font-weight: 600">
                        Click the followed link to activate your account:
                    </div>
                    <div>http://0.0.0.0:3000/activate/?token={token}/</div>
                    <div>Your Matcha team</div>
                </div>
        """,
        subtype="html",
    )
    fm: FastMail = FastMail(config=conf)
    await fm.send_message(message)


async def send_password_restore_mail(email: str, authorize: AuthJWT) -> None:
    """Send mail to restore password."""
    if not settings_mail.is_enough_settings():
        print("Cannot send mail because not enough settings")
        raise AttributeError("Error while send Email")

    token = create_restore_token(authorize, email)
    message: MessageSchema = MessageSchema(
        subject="Restore your password",
        recipients=[f"{email}"],
        body=f"""
                <div style="align-content: center;background-color: beige;width: 100%;height: auto">
                    <div style="text-transform: capitalize;font-size: 16px;font-weight: 600">
                        Click the followed link to restore your password.
                        If you've newer asked for this, just ignore this message.
                    </div>
                     <div> http://0.0.0.0:3000/restore-password/?token={token}/ </div>
                    <div>Your Matcha team</div>
                </div>
        """,
        subtype="html",
    )
    fm: FastMail = FastMail(config=conf)
    await fm.send_message(message)
