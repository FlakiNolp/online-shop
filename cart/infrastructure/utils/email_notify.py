import aiosmtplib
from email.mime.text import MIMEText


class EmailNotify:
    def __init__(self, smtp_server: str, email: str, password: str, smtp_port: int = 587):
        self.smtp_server: str = smtp_server
        self.smtp_port: int = smtp_port
        self.sender: str = email
        self.password: str = password
        self._async_server = aiosmtplib.SMTP(hostname=self.smtp_server, port=self.smtp_port)

    async def send_mail(self, recipient, text):
        try:
            async with self._async_server:
                await self._async_server.login(self.sender, self.password)
                msg = MIMEText(text)
                msg['Subject'] = 'Регистрация нового аккаунта'
                await self._async_server.sendmail(self.sender, recipient, msg.as_string())
        except Exception as e:
            return e
