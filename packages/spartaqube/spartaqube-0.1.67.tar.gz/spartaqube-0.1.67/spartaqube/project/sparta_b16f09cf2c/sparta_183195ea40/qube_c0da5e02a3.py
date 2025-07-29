from django.shortcuts import render
import project.sparta_312a90fa32.sparta_6696c7e57c.qube_52d8b82b2d as qube_52d8b82b2d


def sparta_8a4daf76c5(request, exception=None):
    """
    View Homepage Welcome back
    """
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar['menuBar'] = -1
    userKeyDict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dictVar.update(userKeyDict)
    return render(request, 'dist/project/error/404.html', dictVar)


def sparta_0d94f66ce1(request, exception=None):
    """
    View Homepage Welcome back to SpartaQuant
    """
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar['menuBar'] = -1
    userKeyDict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dictVar.update(userKeyDict)
    return render(request, 'dist/project/error/500.html', dictVar)


def sparta_b110768232(request, exception=None):
    """
    View Homepage Welcome back
    """
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar['menuBar'] = -1
    userKeyDict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dictVar.update(userKeyDict)
    return render(request, 'dist/project/error/403.html', dictVar)


def sparta_18c0c0a649(request, exception=None):
    """
    View Homepage Welcome back
    """
    dictVar = qube_52d8b82b2d.sparta_5c1489406e(request)
    dictVar['menuBar'] = -1
    userKeyDict = qube_52d8b82b2d.sparta_35c7890672(request.user)
    dictVar.update(userKeyDict)
    return render(request, 'dist/project/error/400.html', dictVar)

#END OF QUBE
