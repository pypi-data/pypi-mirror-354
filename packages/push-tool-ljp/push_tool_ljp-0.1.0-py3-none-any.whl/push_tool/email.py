import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional, Union, Dict
from pathlib import Path

class EmailSender:
    """邮件发送工具"""
    
    def __init__(
        self,
        smtp_server: str,
        smtp_port: int,
        username: str,
        password: str,
        use_tls: bool = True
    ):
        """
        初始化邮件发送器
        
        Args:
            smtp_server: SMTP服务器地址
            smtp_port: SMTP服务器端口
            username: 发件人用户名
            password: 发件人密码
            use_tls: 是否使用TLS加密
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
        
    def send_email(
        self,
        subject: str,
        content: str,
        to_addrs: Union[str, List[str]],
        from_addr: Optional[str] = None,
        cc_addrs: Optional[Union[str, List[str]]] = None,
        bcc_addrs: Optional[Union[str, List[str]]] = None,
        html: bool = False,
        attachments: Optional[List[Union[str, Path]]] = None,
        headers: Optional[Dict[str, str]] = None
    ) -> bool:
        """
        发送邮件
        
        Args:
            subject: 邮件主题
            content: 邮件内容
            to_addrs: 收件人地址(单个或多个)
            from_addr: 发件人地址(默认使用username)
            cc_addrs: 抄送地址(单个或多个)
            bcc_addrs: 密送地址(单个或多个)
            html: 是否使用HTML格式
            attachments: 附件路径列表
            headers: 自定义邮件头

        Returns:
            是否发送成功
        """
        # 创建邮件消息
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = from_addr or self.username

        # 处理收件人列表
        if isinstance(to_addrs, str):
            to_addrs = [to_addrs]
        msg['To'] = ', '.join(to_addrs)

        # 处理抄送和密送
        if cc_addrs:
            if isinstance(cc_addrs, str):
                cc_addrs = [cc_addrs]
            msg['Cc'] = ', '.join(cc_addrs)
            to_addrs.extend(cc_addrs)

        if bcc_addrs:
            if isinstance(bcc_addrs, str):
                bcc_addrs = [bcc_addrs]
            to_addrs.extend(bcc_addrs)

        # 添加自定义头
        if headers:
            for key, value in headers.items():
                msg[key] = value

        # 添加邮件正文
        content_type = 'html' if html else 'plain'
        msg.attach(MIMEText(content, content_type, 'utf-8'))

        # 添加附件
        if attachments:
            for attachment in attachments:
                self._add_attachment(msg, attachment)

        # 发送邮件
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to send email: {str(e)}")

    def _add_attachment(self, msg: MIMEMultipart, file_path: Union[str, Path]) -> None:
        """添加附件到邮件"""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Attachment not found: {file_path}")

        with open(path, 'rb') as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())

        encoders.encode_base64(part)
        part.add_header(
            'Content-Disposition',
            f'attachment; filename="{path.name}"'
        )
        msg.attach(part)
