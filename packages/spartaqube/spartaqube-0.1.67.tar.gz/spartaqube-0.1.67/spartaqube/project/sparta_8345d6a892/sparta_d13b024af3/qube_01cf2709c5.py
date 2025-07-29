from datetime import datetime, timedelta
import pytz
UTC = pytz.utc
from django.utils import timezone
from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from project.models import User, UserProfile, UserGroup, notificationShare, notificationGroup, notificationShare
from project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d import sparta_2fd496e13c


def sparta_894a12f004(json_data, user_obj):
    """
    Load notifications (shared, group added, alert trigger, software update)
    """
    date_three_days = datetime.now().astimezone(UTC) - timedelta(days=3)
    nb_notification_not_seen = 0
    notification_share_set = list(notificationShare.objects.filter(user=
        user_obj, is_delete=0, is_seen=False))
    notification_share_set += list(notificationShare.objects.filter(user=
        user_obj, is_delete=0, is_seen=True, date_seen__gt=date_three_days))
    res_notification_list = []
    fld_2_remove = ['id', 'user', 'user_group', 'is_delete', 'date_seen']
    for this_notification_obj in notification_share_set:
        this_notification_dict = sparta_2fd496e13c(model_to_dict(
            this_notification_obj))
        typeObject = int(this_notification_obj.typeObject)
        if not this_notification_obj.is_seen:
            nb_notification_not_seen += 1
        for this_fld in fld_2_remove:
            this_notification_dict.pop(this_fld, None)
        user_from_notification_obj = User.objects.get(id=
            this_notification_obj.user_from.id)
        user_from_name = (user_from_notification_obj.first_name + ' ' +
            user_from_notification_obj.last_name)
        date_created = this_notification_obj.date_created.astimezone(UTC)
        this_notification_dict['userFromName'] = user_from_name
        this_notification_dict['humanDate'] = sparta_56148bab1f(date_created)
        if typeObject == 0:
            pass
    notificationGroupSet = list(notificationGroup.objects.filter(user=
        user_obj, is_delete=0, is_seen=False))
    notificationGroupSet += list(notificationGroup.objects.filter(user=
        user_obj, is_delete=0, is_seen=True, date_seen__gt=date_three_days))
    for this_notification_obj in notificationGroupSet:
        if not this_notification_obj.is_seen:
            nb_notification_not_seen += 1
        this_notification_dict = sparta_2fd496e13c(model_to_dict(
            this_notification_obj))
        user_from_notification_obj = User.objects.get(id=
            this_notification_obj.user_from.id)
        user_from_name = (user_from_notification_obj.first_name + ' ' +
            user_from_notification_obj.last_name)
        date_created = this_notification_obj.dateCreated.astimezone(UTC)
        this_notification_dict['userFromName'] = user_from_name
        this_notification_dict['type_object'] = -2
        this_notification_dict['humanDate'] = sparta_56148bab1f(date_created)
        res_notification_list.append(this_notification_dict)
    res_notification_list = sorted(res_notification_list, key=lambda obj:
        obj['dateCreated'], reverse=True)
    return {'res': 1, 'resNotifications': res_notification_list,
        'nbNotificationNotSeen': nb_notification_not_seen}


def sparta_56148bab1f(dateCreated):
    time = datetime.now().astimezone(UTC)
    if dateCreated.day == time.day:
        if int(time.hour - dateCreated.hour) == 0:
            return 'A moment ago'
        elif int(time.hour - dateCreated.hour) == 1:
            return '1 hour ago'
        return str(time.hour - dateCreated.hour) + ' hours ago'
    elif dateCreated.month == time.month:
        if int(time.day - dateCreated.day) == 1:
            return 'Yesterday'
        return str(time.day - dateCreated.day) + ' days ago'
    elif dateCreated.year == time.year:
        if int(time.month - dateCreated.month) == 1:
            return 'Last month'
        return str(time.month - dateCreated.month) + ' months ago'
    return str(dateCreated)


def sparta_4ac7a585b9(json_data, user_obj):
    """
    Set seen notification
    """
    print('JUST BEFORE WARNING')
    date_now = datetime.now().astimezone(UTC)
    notification_share_set = notificationShare.objects.filter(user=user_obj,
        is_delete=0, is_seen=0)
    for this_notification_obj in notification_share_set:
        if this_notification_obj.dateSeen is not None:
            if abs(this_notification_obj.date_seen.day -
                this_notification_obj.date_created.day) > 2:
                this_notification_obj.is_delete = 1
        this_notification_obj.is_seen = 1
        this_notification_obj.date_seen = date_now
        this_notification_obj.save()
    notification_group_set = notificationGroup.objects.filter(user=user_obj,
        is_delete=0, is_seen=0)
    for this_notification_obj in notification_group_set:
        if this_notification_obj.date_seen is not None:
            if abs(this_notification_obj.date_seen.day -
                this_notification_obj.date_created.day) > 2:
                this_notification_obj.is_delete = 1
        this_notification_obj.is_seen = 1
        this_notification_obj.date_seen = date_now
        this_notification_obj.save()
    return {'res': 1}

#END OF QUBE
