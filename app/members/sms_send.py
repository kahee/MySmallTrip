from django.conf import settings
from sdk.api.message import Message
from sdk.exceptions import CoolsmsException


def send_message(phonenum, message):
    api_key = settings.COOLSMS_API_KEY
    api_secret = settings.COOLSMS_API_SECRET

    params = dict()
    params['type'] = 'sms'
    params['to'] = phonenum
    params['from'] = '01044321237'
    params['text'] = message
    cool = Message(api_key, api_secret)

    try:
        response = cool.send(params)
        print("Success Count : %s" % response['success_count'])
        print("Error Count : %s" % response['error_count'])
        print("Group ID : %s" % response['group_id'])

        if "error_list" in response:
            print("Error List : %s" % response['error_list'])
            return phonenum

    except CoolsmsException as e:
        print("Error Code : %s" % e.code)
        print("Error Message : %s" % e.msg)
