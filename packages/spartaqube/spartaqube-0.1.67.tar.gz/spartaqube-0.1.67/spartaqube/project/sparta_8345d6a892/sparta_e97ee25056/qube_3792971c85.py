import json
import base64
import hashlib, re, uuid
import pandas as pd
from datetime import datetime, timedelta
from dateutil import parser
import pytz
UTC = pytz.utc
from django.db.models import Q
from django.conf import settings as conf_settings
from django.contrib.auth.models import User
from django.contrib.humanize.templatetags.humanize import naturalday
from django.forms.models import model_to_dict
from project.models import User, UserProfile, UserGroup, UserGroupUser, ShareRights, notificationShare
from project.sparta_8345d6a892.sparta_87f32c6e97 import qube_93b4ab09a2 as qube_93b4ab09a2
from project.sparta_8345d6a892.sparta_370971529b import qube_da282a9e29 as qube_da282a9e29


def sparta_3a4d831997(json_data, userObj):
    """
    Search Members or group of members in order to share dataQuantDB, functions etc..."""
    keySearchMember = json_data['query']
    keySearchMember = keySearchMember.lower()
    resSearch = []
    userProfilObjSet = UserProfile.objects.filter(Q(
        user__first_name__icontains=keySearchMember) | Q(
        user__last_name__icontains=keySearchMember)).all()[0:6]
    for thisUserProfilObj in userProfilObjSet:
        thisUserObj = thisUserProfilObj.user
        if userObj == thisUserObj:
            continue
        avatarObj = thisUserProfilObj.avatar
        image64 = '-1'
        if avatarObj is not None:
            image64 = thisUserProfilObj.avatarObj.image64
        resSearch.append({'name': thisUserObj.first_name + ' ' + str(
            thisUserObj.last_name), 'value': thisUserProfilObj.user_profile_id, 'image64': image64, 'type': 'user'})
    userGroupSet = UserGroup.objects.filter(name__icontains=keySearchMember,
        is_delete=False).all()[0:6]
    for thisUserGroup in userGroupSet:
        resSearch.append({'name': thisUserGroup.name, 'value':
            thisUserGroup.groupId, 'type': 'group'})
    res = {'res': 1, 'members': resSearch, 'nbRes': len(resSearch)}
    return res


def sparta_d5beec0a69(json_data, user_obj):
    """
    Load all dependencies that need to be shared as well (not implemented yet)
    """
    shareType = int(json_data['shareType'])
    if shareType == 0:
        portfolio_id = json_data['ptf_id']
        portfolio_set = Portfolio.objects.filter(ptf_id=portfolio_id,
            is_delete=False).all()
        if portfolio_set.count() == 1:
            portfolio_obj = portfolio_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                portfolio_shared_set = PortfolioShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, portfolio=
                    portfolio_obj) & ~Q(portfolio__user=user_obj) | Q(
                    is_delete=0, user=user_obj, portfolio=portfolio_obj))
            else:
                portfolio_shared_set = PortfolioShared.objects.filter(is_delete
                    =0, user=user_obj, portfolio=portfolio_obj)
            if portfolio_shared_set.count() > 0:
                portfolio_shared_obj = portfolio_shared_set[0]
                share_rights_obj = portfolio_shared_obj.ShareRights
                createDependenciesDict = []
                nbDependencies = len(createDependenciesDict)
                res_dict = {'res': 1, 'resDependenciesDict':
                    createDependenciesDict, 'nbDependencies':
                    nbDependencies, 'bWriteMe': share_rights_obj.has_write_rights, 'bReshareMe': share_rights_obj.has_reshare_rights, 'bAdminMe': share_rights_obj.is_admin}
                return res_dict
    elif shareType == 1:
        universe_id = json_data['universe_id']
        universe_set = Universe.objects.filter(universe_id=universe_id,
            is_delete=False).all()
        if universe_set.count() == 1:
            universe_obj = universe_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                universe_shared_set = UniverseShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, universe=
                    universe_obj) & ~Q(universe__user=user_obj) | Q(
                    is_delete=0, user=user_obj, universe=universe_obj))
            else:
                universe_shared_set = UniverseShared.objects.filter(is_delete
                    =0, user=user_obj, universe=universe_obj)
            if universe_shared_set.count() > 0:
                universe_shared_obj = universe_shared_set[0]
                share_rights_obj = universe_shared_obj.shareRights
                createDependenciesDict = []
                nbDependencies = len(createDependenciesDict)
                res_dict = {'res': 1, 'resDependenciesDict':
                    createDependenciesDict, 'nbDependencies':
                    nbDependencies, 'bWriteMe': share_rights_obj.has_write_rights, 'bReshareMe': share_rights_obj.has_reshare_rights, 'bAdminMe': share_rights_obj.is_admin}
                return res_dict
    return {'res': -1}


def sparta_3c044d5c30(json_data, user_obj):
    """
    
    """
    shared_set = []
    arrRes = []
    shareType = int(json_data['shareType'])
    if shareType == 0:
        portfolio_id = json_data['ptf_id']
        portfolio_set = Portfolio.objects.filter(ptf_id=portfolio_id,
            is_delete=False).all()
        if portfolio_set.count() == 1:
            portfolio_obj = portfolio_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                portfolio_shared_set = PortfolioShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, portfolio=
                    portfolio_obj) & ~Q(portfolio__user=user_obj) | Q(
                    is_delete=0, user=user_obj, portfolio=portfolio_obj))
            else:
                portfolio_shared_set = PortfolioShared.objects.filter(is_delete
                    =0, user=user_obj, portfolio=portfolio_obj)
            if portfolio_shared_set.count() > 0:
                portfolio_shared_obj = portfolio_shared_set[0]
                if portfolio_shared_obj.ShareRights.is_admin:
                    shared_set = PortfolioShared.objects.filter(is_delete=
                        False, portfolio=portfolio_obj)
    elif shareType == 1:
        universe_id = json_data['universe_id']
        universe_set = Universe.objects.filter(universe_id=universe_id,
            is_delete=False).all()
        if universe_set.count() == 1:
            universe_obj = universe_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                universe_shared_set = UniverseShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, universe=
                    universe_obj) & ~Q(universe__user=user_obj) | Q(
                    is_delete=0, user=user_obj, universe=universe_obj))
            else:
                universe_shared_set = UniverseShared.objects.filter(is_delete
                    =0, user=user_obj, universe=universe_obj)
            if universe_shared_set.count() > 0:
                universe_shared_obj = universe_shared_set[0]
                if universe_shared_obj.ShareRights.is_admin:
                    shared_set = UniverseShared.objects.filter(is_delete=
                        False, universe=universe_obj)
    for this_shared_obj in shared_set:
        b_admin = False
        if this_shared_obj.userGroup is not None:
            group_access_type = 1
            name = this_shared_obj.userGroup.name
        else:
            group_access_type = 0
            name = (this_shared_obj.user.first_name + ' ' + this_shared_obj.user.last_name)
            b_admin = this_shared_obj.shareRights.is_admin
        if not b_admin:
            resTmpDict = {'groupAccessType': group_access_type, 'name':
                name, 'bWrite': int(this_shared_obj.ShareRights.has_write_rights), 'bReshare': int(this_shared_obj.ShareRights.has_reshare_rights), 'idShared': this_shared_obj.id
                }
            arrRes.append(resTmpDict)
    res = {'res': 1, 'arrRes': arrRes}
    return res


def sparta_f4807c62c5(json_data, user_obj):
    """
    
    """
    dateNow = datetime.now().astimezone(UTC)
    userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
    userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
    member2ShareArr = json_data['member2ShareArr']
    share_type = int(json_data['shareType'])

    def createShareRightsObj(shareRightsObj):
        """
        Create shareRights object
        Need to check my current write as I want to share or reshare this object and i cannot give more elevated rights
        than mine
        """
        bWritePrivilege = json_data['bWritePrivilege']
        bResharePrivilege = json_data['bResharePrivilege']
        if shareRightsObj is not None:
            bWritePrivilegeMe = shareRightsObj.has_write_rights
            bReshareMe = shareRightsObj.has_reshare_rights
            if not bWritePrivilegeMe:
                bWritePrivilege = False
            if not bReshareMe:
                bResharePrivilege = False
        shareRightsInstance = ShareRights.objects.create(is_admin=False,
            has_write_rights=bWritePrivilege, has_reshare_rights=
            bResharePrivilege, last_update=dateNow)
        return shareRightsInstance

    def sendNotificationShared(thisMember, share_type, userOrUserGroup, obj):

        def sendUserNotification(this_user):
            """
                This functions sends the notifications to a specific user
            """
            notification_share_obj = notificationShare.objects.create(
                type_object=share_type, user=this_user, user_from=user_obj,
                date_created=dateNow)
            if share_type == 0:
                notification_share_obj.portfolio = obj
            elif share_type == 1:
                notification_share_obj.universe = obj
            notification_share_obj.save()
        if thisMember['type'] == 'user':
            sendUserNotification(userOrUserGroup)
        else:
            userGroupUserSet = UserGroupUser.objects.filter(is_delete=False,
                userGroup=userOrUserGroup)
            if userGroupUserSet.count() > 0:
                for thisUserGroupUserObj in userGroupUserSet:
                    thisUser = thisUserGroupUserObj.user
                    if not thisUser == user_obj:
                        sendUserNotification(thisUser)
    if share_type == 0:
        portfolio_id = json_data['ptf_id']
        portfolio_set = Portfolio.objects.filter(ptf_id=portfolio_id,
            is_delete=False).all()
        if portfolio_set.count() == 1:
            portfolio_obj = portfolio_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                portfolio_shared_set = PortfolioShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, portfolio=
                    portfolio_obj) & ~Q(portfolio__user=user_obj) | Q(
                    is_delete=0, user=user_obj, portfolio=portfolio_obj))
            else:
                portfolio_shared_set = PortfolioShared.objects.filter(is_delete
                    =0, user=user_obj, portfolio=portfolio_obj)
            if portfolio_shared_set.count() > 0:
                portfolio_shared_obj = portfolio_shared_set[0]
                share_rights_obj = portfolio_shared_obj.ShareRights
                if not share_rights_obj.has_reshare_rights:
                    return {'res': -1, 'errorMsg':
                        'Your are not allowed to share this object'}
                for thisMember in member2ShareArr:
                    if thisMember['type'] == 'user':
                        thisUserProfileObj = UserProfile.objects.get(
                            user_profile_id=thisMember['member'])
                        testExistingSharedSet = PortfolioShared.objects.filter(
                            user=thisUserProfileObj.user, portfolio=
                            portfolio_obj)
                        if testExistingSharedSet.count() == 0:
                            PortfolioShared.objects.create(portfolio=
                                portfolio_obj, user=thisUserProfileObj.user,
                                dateCreated=dateNow, shareRights=
                                createShareRightsObj(share_rights_obj))
                            sendNotificationShared(thisMember, share_type,
                                thisUserProfileObj.user, portfolio_obj)
                        else:
                            testExistingSharedObj = testExistingSharedSet[0]
                            if testExistingSharedObj.is_delete:
                                testExistingSharedObj.is_delete = False
                                testExistingSharedObj.ShareRights = (
                                    createShareRightsObj(share_rights_obj))
                                testExistingSharedObj.save()
                                sendNotificationShared(thisMember,
                                    share_type, thisUserProfileObj.user,
                                    portfolio_obj)
                    else:
                        thisUserGroupObj = UserGroup.objects.get(groupId=
                            thisMember['member'])
                        testExistingSharedSet = PortfolioShared.objects.filter(
                            user_group=thisUserGroupObj, portfolio=
                            portfolio_obj)
                        if testExistingSharedSet.count() == 0:
                            PortfolioShared.objects.create(portfolio=
                                portfolio_obj, userGroup=thisUserGroupObj,
                                dateCreated=dateNow, shareRights=
                                createShareRightsObj(share_rights_obj))
                            sendNotificationShared(thisMember, share_type,
                                thisUserGroupObj, portfolio_obj)
    elif share_type == 1:
        universe_id = json_data['universe_id']
        universe_set = Universe.objects.filter(universe_id=universe_id,
            is_delete=False).all()
        if universe_set.count() == 1:
            universe_obj = universe_set[0]
            userGroupUserSet = qube_93b4ab09a2.sparta_b0ee4cd292(user_obj)
            userGroups = [thisObj.userGroup for thisObj in userGroupUserSet]
            if len(userGroups) > 0:
                universe_shared_set = UniverseShared.objects.filter(Q(
                    is_delete=0, userGroup__in=userGroups, universe=
                    universe_obj) & ~Q(universe__user=user_obj) | Q(
                    is_delete=0, user=user_obj, universe=universe_obj))
            else:
                universe_shared_set = UniverseShared.objects.filter(is_delete
                    =0, user=user_obj, universe=universe_obj)
            if universe_shared_set.count() > 0:
                universe_shared_obj = universe_shared_set[0]
                share_rights_obj = universe_shared_obj.ShareRights
                if not share_rights_obj.has_reshare_rights:
                    return {'res': -1, 'errorMsg':
                        'Your are not allowed to share this object'}
                for thisMember in member2ShareArr:
                    if thisMember['type'] == 'user':
                        thisUserProfileObj = UserProfile.objects.get(
                            user_profile_id=thisMember['member'])
                        testExistingSharedSet = UniverseShared.objects.filter(
                            user=thisUserProfileObj.user, universe=universe_obj
                            )
                        if testExistingSharedSet.count() == 0:
                            UniverseShared.objects.create(universe=
                                universe_obj, user=thisUserProfileObj.user,
                                dateCreated=dateNow, shareRights=
                                createShareRightsObj(share_rights_obj))
                            sendNotificationShared(thisMember, share_type,
                                thisUserProfileObj.user, universe_obj)
                        else:
                            testExistingSharedObj = testExistingSharedSet[0]
                            if testExistingSharedObj.is_delete:
                                testExistingSharedObj.is_delete = False
                                testExistingSharedObj.ShareRights = (
                                    createShareRightsObj(share_rights_obj))
                                testExistingSharedObj.save()
                                sendNotificationShared(thisMember,
                                    share_type, thisUserProfileObj.user,
                                    universe_obj)
                    else:
                        thisUserGroupObj = UserGroup.objects.get(groupId=
                            thisMember['member'])
                        testExistingSharedSet = PortfolioShared.objects.filter(
                            user_group=thisUserGroupObj, universe=universe_obj)
                        if testExistingSharedSet.count() == 0:
                            UniverseShared.objects.create(universe=
                                universe_obj, userGroup=thisUserGroupObj,
                                dateCreated=dateNow, shareRights=
                                createShareRightsObj(share_rights_obj))
                            sendNotificationShared(thisMember, share_type,
                                thisUserGroupObj, universe_obj)
    return {'res': 1}


def sparta_0c7ca8e326(json_data, user_obj):
    """
    
    """
    shareType = int(json_data['shareType'])
    idSharedObj = json_data['idSharedObj']
    rightsVal = bool(json_data['rightsVal'])
    typePrivilege = int(json_data['typePrivilege'])
    sharedSet = None
    if shareType == 0:
        portfolio_id = json_data['ptf_id']
        portfolio_set = Portfolio.objects.filter(ptf_id=portfolio_id,
            is_delete=False)
        if portfolio_set.count() > 0:
            portfolio_obj = portfolio_set[0]
            sharedSet = PortfolioShared.objects.filter(is_delete=0,
                portfolio=portfolio_obj, id=idSharedObj)
    elif shareType == 1:
        universe_id = json_data['universe_id']
        universe_set = Universe.objects.filter(universe_id=universe_id,
            is_delete=False)
        if universe_set.count() > 0:
            universe_obj = universe_set[0]
            sharedSet = UniverseShared.objects.filter(is_delete=0, universe
                =universe_obj, id=idSharedObj)
    if sharedSet is not None:
        if sharedSet.count() > 0:
            thisSharedObj = sharedSet[0]
            thisSharedRightsObj = thisSharedObj.ShareRights
            if typePrivilege == 0:
                thisSharedRightsObj.has_write_rights = rightsVal
            elif typePrivilege == 1:
                thisSharedRightsObj.has_reshare_rights = rightsVal
            thisSharedRightsObj.save()
    res = {'res': 1}
    return res

#END OF QUBE
