import importlib
import re
import smtplib
from email import encoders
from email.message import EmailMessage
from email.mime.base import MIMEBase

import requests
from django.conf import settings
from django.core.files import File
from django.utils.translation import gettext_lazy as _

from zs_utils.email_notification import models
from zs_utils.exceptions import CustomException


class EmailServiceException(CustomException):
    pass


class SMTPSender:
    @classmethod
    def send_email(
        cls,
        receivers: list,
        sender: str,
        subject: str,
        message: str,
        files: dict = None,
        message_format: str = "plaintext",
        custom_config: dict = None,
        **kwargs,
    ):
        if not custom_config:
            custom_config = {}
        host = custom_config.get("host", settings.SMTP_HOST)
        port = custom_config.get("port", settings.SMTP_PORT)
        user = custom_config.get("user", settings.SMTP_LOGIN)
        password = custom_config.get("password", settings.SMTP_PASSWORD)

        smtp = smtplib.SMTP(host=host, port=port)
        smtp.connect(host=host, port=port)
        smtp.login(user=user, password=password)
        email_message = EmailMessage()
        email_message["From"] = f"{sender} <{user}>"
        email_message["To"] = receivers
        email_message["Subject"] = subject
        email_message.set_content(message, message_format)

        if files:
            for name, value in files.items():
                part = MIMEBase("application", "octet-stream")
                part.set_payload(value)
                encoders.encode_base64(part)
                part.add_header('content-disposition', 'attachment', filename=name)
                email_message.add_attachment(part)

        try:
            result = smtp.send_message(email_message)
        except smtplib.SMTPException as e:
            raise EmailServiceException(str(e))
        return result

    @classmethod
    def send_html_email(cls, **kwargs):
        return cls.send_email(message_format="html", **kwargs)


class SMTPBZClient:
    BASE_URL = "https://api.smtp.bz/v1"
    HEADERS = {"Authorization": settings.SMTP_API_TOKEN, "accept": "application/json"}

    @classmethod
    def get_last_message_id(cls, mail_from="", mail_to=""):
        url = f"{cls.BASE_URL}/log/message?limit=1"
        if mail_from:
            url += f"&from={mail_from}"
        if mail_to:
            url += f"&to={mail_to}"

        response = requests.get(url, headers=cls.HEADERS)
        if response.status_code != 200:
            raise EmailServiceException(
                _("Ошибка API SMTP.BZ: {status_code} - {text}").format(
                    status_code=response.status_code, text=response.text
                )
            )

        data = response.json().get("data") or [{}]
        message_id = data[0].get("messageid")
        return message_id

    @classmethod
    def get_message_status_code(cls, message_id="", mail_from="", mail_to="") -> dict:
        if not message_id:
            message_id = cls.get_last_message_id(mail_from=mail_from, mail_to=mail_to)
            if not message_id:
                return {"status_code": 404, "detail": _("Отправленных сообщений не найдено")}

        url = f"{cls.BASE_URL}/log/message/{message_id}"

        response = requests.get(url, headers=cls.HEADERS)
        if response.status_code != 200:
            raise EmailServiceException(
                _("Ошибка при получении лога {message_id}: {status_code}").format(
                    message_id=message_id, status_code=response.status_code
                )
            )

        detail = response.json().get("response") or ""
        status_code = detail[:3]
        date = response.json().get("date") or ""
        return {"status_code": status_code, "detail": detail, "date": date}


class EmailService(SMTPSender, SMTPBZClient):
    """
    Сервис для отправки писем по шаблону через Unisender
    """

    # ------------------------------ Генерация полного HTML шаблона ------------------------------
    @classmethod
    def get_template_file(cls, template_name: str):
        """
        Получение файла с частями шаблона
        """
        template_package = getattr(settings, "EMAIL_TEMPLATE_PACKAGE")
        if not template_package:
            raise EmailServiceException(_("Не указан базовый пакет шаблонов в настройках"))

        full_template_module = f"{template_package}.{template_name}"

        try:
            template_module = importlib.import_module(full_template_module)
        except ModuleNotFoundError:
            raise EmailServiceException(_("Шаблон {template_name} не найден").format(template_name=template_name))

        return template_module

    @classmethod
    def get_template_languages(cls, template_name: str) -> list:
        """
        Получение всех языков шаблона
        """
        template_file = cls.get_template_file(template_name=template_name)
        languages = list()
        for part in dir(template_file):
            if "body" in part:
                languages.append(part.split("_")[-1])
        return languages

    @classmethod
    def validate_template_params(cls, html_template: str, template_params: dict):
        """
        Валидация параметров шаблона
        """
        params = re.findall(pattern=r"{(.*?)}", string=html_template)
        required_params = [template_param.replace("{", "") for template_param in params]

        errors = dict()
        required_params = list(set(required_params))
        for required_param in required_params:
            if required_param not in template_params:
                errors[f"template_params.{required_param}"] = _("Обязательное поле.")
        if errors:
            raise EmailServiceException(message_dict=errors)

    @classmethod
    def get_template_data(cls, template_name: str, language: str, template_params: dict) -> dict:
        """
        Получение данных шаблона
        """
        # Базовая информация: файл шаблона с частями и url со статикой
        template_file = cls.get_template_file(template_name=template_name)
        static_url = getattr(settings, "EMAIL_STATIC_FOLDER_URL", "https://storage.yandexcloud.net/zs-static/email/")
        if not hasattr(template_file, f"body_{language}"):
            raise EmailServiceException(
                message_dict={
                    "language": _("Для данного шаблона не определён язык '{language}'").format(language=language)
                }
            )

        # Костыль для шаблона zonesmart.order
        if "items" in template_params:
            items = ""
            item_template = getattr(template_file, f"items_{language}", getattr(template_file, "items", None))
            for item in template_params["items"]:
                items += item_template.format(**item)
            template_params["items"] = items

        # Переносим части шаблона в словарь
        title = getattr(template_file, f"title_{language}")
        template_data = {
            "title": title,
            "subject": getattr(template_file, f"subject_{language}", title).format(**template_params),
            "body": getattr(template_file, f"body_{language}"),
            "cheers": getattr(template_file, f"cheers_{language}", ""),
            "footer": getattr(template_file, f"footer_{language}", ""),
            "logo": template_file.base.logo,
            "email_icon": getattr(template_file, "icon", ""),
            "static_url": static_url,
        }

        # Составление полного шаблона из частей
        base_template = template_file.base.base_template
        template_data["html"] = base_template.format(**template_data)
        cls.validate_template_params(html_template=template_data["html"], template_params=template_params)
        template_data["html"] = template_data["html"].format(**template_params)
        return template_data

    @classmethod
    def create_email_notification(
        cls,
        sender: str,
        receivers: list,
        template_name: str,
        language: str = "ru",
        is_urgent: bool = False,
        params: dict = None,
        files: list = None,
    ) -> models.EmailNotification:
        """
        Создание объекта email уведомления
        """
        email_notification = models.EmailNotification.objects.create(
            sender=sender,
            receivers=receivers,
            language=language,
            template_name=template_name,
            template_params=params,
            is_urgent=is_urgent,
        )
        if files:
            for file in files:
                models.EmailNotificationFile.objects.create(
                    email_notification=email_notification, name=file.name, file=File(file)
                )
        return email_notification

    # ------------------------------ Отправка email письма ------------------------------

    @classmethod
    def send_email_notification(cls, email_notification: models.EmailNotification, force: bool = False, **kwargs):
        """
        Отправка email-уведомления по объекту email_notification
        """
        if email_notification.is_sent and not force:
            raise EmailServiceException(_("Уведомление уже было отправлено."))

        files = dict()
        for file in email_notification.files.all():
            files[file.name] = file.file.read()

        try:
            results = cls.send_template_email(
                sender=email_notification.sender,
                receivers=email_notification.receivers,
                template_name=email_notification.template_name,
                language=email_notification.language,
                params=email_notification.template_params,
                files=files,
                **kwargs,
            )
        except EmailServiceException:
            email_notification.delete()
            raise

        email_notification.is_sent = True
        email_notification.save(update_fields=["is_sent"])
        return results

    @classmethod
    def send_template_email(
        cls,
        template_name: str,
        language: str,
        sender: str,
        receivers: list,
        params: dict,
        files: dict = None,
        **kwargs,
    ):
        """
        Отправка email-уведомления по шаблону
        """
        language = language if language == "ru" else "en"
        template_data = cls.get_template_data(template_name=template_name, language=language, template_params=params)
        return cls.send_html_email(
            sender=sender,
            receivers=receivers,
            subject=template_data["subject"],
            message=template_data["html"],
            files=files,
            **kwargs,
        )
