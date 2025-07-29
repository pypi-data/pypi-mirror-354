import os
import json
import base64
import requests
import hashlib
from datetime import datetime, timedelta
from dateutil import parser
import pytz
UTC = pytz.utc
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import UserProfile, ticket, ticketMessage
from project.sparta_8688631f3d.sparta_c77f2d3c37 import qube_8f0cad92aa as qube_8f0cad92aa
from project.sparta_8688631f3d.sparta_07864420ce import qube_7bd77509b9 as qube_7bd77509b9
from project.sparta_8688631f3d.sparta_355a680bf7 import qube_1d2a59f054 as qube_1d2a59f054
from project.sparta_8688631f3d.sparta_a9eedb9d32.qube_60d1e416df import Email as Email
from project.sparta_ef90090f65.sparta_40861746d9.qube_380ad6266d import sparta_5543508842
ADMIN_EMAIL = conf_settings.ADMIN_EMAIL_TICKET
MAX_TICKETS = conf_settings.MAX_TICKETS


def sparta_75bf652e0b(json_data, user_obj):
    """
    Create help center case
    """
    captcha = json_data['captcha']
    title = json_data['titleCase']
    message = json_data['messageCase']
    typeCase = json_data['typeCase']
    yesterday = datetime.now() - timedelta(1)
    dateNow = datetime.now().astimezone(UTC)
    ticket_id = str(str(user_obj.email) + str(dateNow)).encode('utf-8')
    ticket_id = hashlib.md5(ticket_id).hexdigest()
    ticketSet = ticket.objects.filter(date_created__gte=yesterday, user=
        user_obj)
    nbTickets = len(ticketSet)
    if nbTickets <= MAX_TICKETS:
        json_data_post = {'captcha': captcha, 'title': title, 'message':
            message, 'typeCase': typeCase, 'ticket_id': ticket_id, 'email':
            user_obj.email, 'first_name': user_obj.first_name, 'last_name':
            user_obj.last_name}
        json_data_post['jsonData'] = json.dumps(json_data_post)
        proxies_dict = {'http': os.environ.get('http_proxy', None), 'https':
            os.environ.get('https_proxy', None)}
        response = requests.post(
            f'{conf_settings.SPARTAQUBE_WEBSITE}/help-center-new-case',
            data=json.dumps(json_data_post), proxies=proxies_dict)
        if response.status_code == 200:
            try:
                dateNow = datetime.now().astimezone(UTC)
                ticketObj = ticket.objects.create(ticket_id=ticket_id,
                    type_ticket=typeCase, title=title, date_created=dateNow,
                    user=user_obj)
                ticketMessage.objects.create(ticket=ticketObj, message=
                    message, user=user_obj, date_created=dateNow)
                user_profile_obj = UserProfile.objects.get(user=user_obj)
                user_profile_obj.has_open_tickets = True
                user_profile_obj.save()
            except Exception as e:
                return {'res': -1, 'errorMsg': str(e)}
        return {'res': 1, 'nbTickets': nbTickets}
    else:
        return {'res': -1, 'errorMsg':
            'You have reached the maximum tickets limit'}


def sparta_486e49d8dc(message, typeCase=0, companyName=None):
    """
    
    """
    typeCaseStr = 'BUG'
    if int(typeCase) == 0:
        typeCaseStr = 'GENERAL'
    admin_user_set = User.objects.filter(is_staff=True)
    if admin_user_set.count() > 0:
        admin_user_obj = admin_user_set[0]
        emailObj = Email(admin_user_obj.username, [conf_settings.CONTACT_US_EMAIL], 'New case opened', 'New case of type > ' +
            str(typeCaseStr))
        if companyName is not None:
            emailObj.addOneRow('Company', companyName)
            emailObj.addLineSeparator()
        emailObj.addOneRow('Message', message)
        emailObj.addLineSeparator()
        if int(typeCase) == 0:
            emailObj.addOneRow('Type', 'General question')
        else:
            emailObj.addOneRow('Type', 'Report Bug')
        emailObj.send()


def sparta_d38eec7139(json_data, user_obj):
    """
    Load my cases
    """
    has_user_closed = json_data['has_user_closed']
    if user_obj.is_staff:
        ticket_set = ticket.objects.filter(is_delete=0, has_user_closed=
            has_user_closed).order_by('status_ticket')
        arrRes = []
        if ticket_set.count() > 0:
            for this_ticket_obj in ticket_set:
                this_dict = sparta_5543508842(model_to_dict(
                    this_ticket_obj))
                del this_dict['user']
                this_dict['date_created'] = naturalday(parser.parse(str(
                    this_dict['date_created'])))
                arrRes.append(this_dict)
        return {'res': 1, 'arrRes': arrRes}
    else:
        ticket_set = ticket.objects.filter(user=user_obj, is_delete=0,
            has_user_closed=has_user_closed).order_by('-date_created')
        arrRes = []
        if ticket_set.count() > 0:
            for this_ticket_obj in ticket_set:
                this_dict = sparta_5543508842(model_to_dict(
                    this_ticket_obj))
                del this_dict['user']
                arrRes.append(this_dict)
        return {'res': 1, 'arrRes': arrRes}


def sparta_e73732e169(json_data, user_obj):
    """
    Load messages
    """
    ticket_id = json_data['ticket_id']
    if user_obj.is_staff:
        ticket_set = ticket.objects.filter(ticket_id=ticket_id, is_delete=0)
    else:
        ticket_set = ticket.objects.filter(user=user_obj, ticket_id=
            ticket_id, is_delete=0)
    arr_msg = []
    if ticket_set.count() > 0:
        ticket_obj = ticket_set[0]
        if not user_obj.is_staff:
            ticket_obj.b_show_user_notification = False
            ticket_obj.save()
        ticket_msg_set = ticketMessage.objects.filter(ticket=ticket_obj)
        if ticket_msg_set.count() > 0:
            prev_user = ticket_msg_set[0].user
            tmp_arr = []
            for idx, this_msg_obj in enumerate(ticket_msg_set):
                current_user = this_msg_obj.user
                this_dict = sparta_5543508842(model_to_dict(
                    this_msg_obj))
                this_dict['date_created'] = naturalday(parser.parse(str(
                    this_dict['date_created'])))
                if user_obj == current_user:
                    this_dict['me'] = 1
                else:
                    this_dict['me'] = 0
                if current_user == prev_user:
                    tmp_arr.append(this_dict)
                    if idx == len(ticket_msg_set) - 1:
                        arr_msg.append(tmp_arr)
                else:
                    arr_msg.append(tmp_arr)
                    tmp_arr = [this_dict]
                    if idx == len(ticket_msg_set) - 1:
                        arr_msg.append(tmp_arr)
                prev_user = current_user
    return {'res': 1, 'arrMsg': arr_msg}


def sparta_16002f861b(json_data, user_obj):
    """
        Send new message in the chat
    """
    ticket_id = json_data['ticket_id']
    message = json_data['message']
    if user_obj.is_staff:
        ticketSet = ticket.objects.filter(ticket_id=ticket_id)
    else:
        ticketSet = ticket.objects.filter(user=user_obj, ticket_id=ticket_id)
    if ticketSet.count() > 0:
        ticketObj = ticketSet[0]
        dateNow = datetime.now().astimezone(UTC)
        ticketMessage.objects.create(ticket=ticketObj, message=message,
            user=user_obj, date_created=dateNow)
        if ticketObj.b_send_email and not user_obj.is_staff:
            ticketObj.b_send_email = False
            ticketObj.save()
            sparta_486e49d8dc(message, ticketObj.type_ticket, None)
        if user_obj.is_staff:
            ticketObj.status_ticket = 2
            ticketObj.b_send_email = True
            ticketObj.has_user_closed = False
            ticketObj.b_show_user_notification = True
            ticketObj.save()
            user_profile_obj = UserProfile.objects.get(user=ticketObj.user)
            user_profile_obj.has_open_tickets = True
            user_profile_obj.save()
        else:
            ticketObj.status_ticket = 1
            ticketObj.has_user_closed = False
            ticketObj.b_send_email = False
            ticketObj.b_show_user_notification = False
            ticketObj.save()
        return {'res': 1}
    return {'res': -1, 'errorMsg': 'An unexpected error occurred'}


def sparta_63830f5ca3(json_data, user_obj):
    """
        Close case
    """
    ticket_id = json_data['ticket_id']
    if user_obj.is_staff:
        ticketSet = ticket.objects.filter(ticket_id=ticket_id)
    else:
        ticketSet = ticket.objects.filter(user=user_obj, ticket_id=ticket_id)
    if ticketSet.count() > 0:
        ticketObj = ticketSet[0]
        ticketObj.has_user_closed = True
        ticketObj.save()
    return {'res': 1}


def sparta_2b94dd7864(json_data):
    """
        Remove flag notification. The user saw the message (so no notification so show anymore to the user)
    """
    userId = json_data['userId']
    ticket_id = json_data['ticket_id']
    ticketSet = ticket.objects.filter(user_id=userId, ticket_id=ticket_id)
    if ticketSet.count() > 0:
        ticketObj = ticketSet[0]
        ticketObj.b_show_user_notification = False
        ticketObj.save()
    return {'res': 1}


def sparta_7c45ca35f6(user_obj):
    """
    Load number of notification ticket
    """
    ticketSet = ticket.objects.filter(user=user_obj,
        b_show_user_notification=True, has_user_closed=False)
    return {'res': 1, 'nbNotifications': ticketSet.count()}

#END OF QUBE
