import os
import requests
import logging

from domain.service.sms_service import SMSService
from infrastructure.open_tracing import open_tracing
from infrastructure.open_tracing.open_tracing_handler import trace_service


class SMSServiceImpl(SMSService):
    @trace_service("SMS (send)", open_tracing)
    def send(self, target_number: str, message: str):
        send_url = 'https://apis.aligo.in/send/'

        sms_data = {
            'key': os.getenv("SMS_KEY"),
            'userid': os.getenv("SMS_USER_ID"),
            'sender': os.getenv("SMS_SENDER"),
            'receiver': target_number,
            'msg': message,
            'msg_type': 'SMS',
            'testmode_yn': 'N'
        }

        send_response = requests.post(send_url, data=sms_data)
        logging.info(send_response.json())