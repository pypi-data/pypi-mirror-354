from datetime import datetime
import hashlib
import os, sys
import django


def sparta_8542592f4e():
    """
    
    """
    currentPath = os.path.dirname(os.path.abspath(__file__)).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(currentPath).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(oneLevelUpPath).replace('\\', '/')
    oneLevelUpPath = os.path.dirname(oneLevelUpPath).replace('\\', '/')
    sys.path.append(oneLevelUpPath)
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'spartaqube_app.settings')
    os.environ['DJANGO_ALLOW_ASYNC_UNSAFE'] = 'true'
    django.setup()


def sparta_8e13e2e466():
    """
        Create admin user
    """
    from django.contrib.auth.models import User
    from project.models import UserProfile
    if not User.objects.filter(username='admin').exists():
        email = 'admin@spartaqube.com'
        userObj = User.objects.create_user('admin', first_name='admin',
            last_name='admin', email=email, password='admin')
        userObj.is_superuser = True
        userObj.is_staff = True
        userObj.save()
        userProfile = UserProfile(user=userObj)
        idKeyTmp = str(userObj.id) + '_' + str(userObj.email)
        idKeyTmp = idKeyTmp.encode('utf-8')
        idKeyTmp1 = hashlib.md5(idKeyTmp).hexdigest() + str(datetime.now())
        idKeyTmp1 = idKeyTmp1.encode('utf-8')
        userProfile.userId = hashlib.sha256(idKeyTmp1).hexdigest()
        userProfile.email = email
        userProfile.save()


if __name__ == '__main__':
    sparta_8542592f4e()
    sparta_8e13e2e466()

#END OF QUBE
