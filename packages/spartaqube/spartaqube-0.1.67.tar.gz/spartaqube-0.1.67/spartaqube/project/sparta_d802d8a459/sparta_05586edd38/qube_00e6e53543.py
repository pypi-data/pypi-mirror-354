import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_950a603163 import qube_2ab426de66 as qube_2ab426de66
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_36715732c5
def sparta_ec4f45cbd9(request):
    """ 
    Load dataframe statistics explorer
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_ec4f45cbd9(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_44673c0a1e(request):
    """ 
    Get dataframe infos
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_44673c0a1e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f2dff3a94d(request):
    """ 
    Compute statistics (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_f2dff3a94d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_0b1c3b3ec9(request):
    """ 
    Compute columns statistics (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_0b1c3b3ec9(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d2f38bd9ea(request):
    """ 
    Compute columns statistics for correlations only (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_d2f38bd9ea(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_2a282d6b34(request):
    """ 
    Relationship explorer (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_2a282d6b34(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_0eb6003515(request):
    """ 
    Time Series Analysis (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_0eb6003515(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_0eb6003515(request):
    """ 
    Time Series Analysis (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_0eb6003515(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1152c20491(request):
    """ 
    PCA (based on a passed dataframe)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_1152c20491(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_7128d2d512(request):
    """ 
    PCA install sklearn
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_7128d2d512(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_9e67c00bd3(request):
    """ 
    PCA run
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_9e67c00bd3(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_018aa714bf(request):
    """ 
    Run Clustering
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_018aa714bf(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_4c2cb5bb14(request):
    """ 
    Run Correlation Network
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_4c2cb5bb14(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6a5d637124(request):
    """ 
    Run TSNE
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_6a5d637124(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_7c8640cb86(request):
    """ 
    Run Polynomial Regression
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_7c8640cb86(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_35cc9e7361(request):
    """ 
    Run Quantile Regression
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_35cc9e7361(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1e352fb3b4(request):
    """ 
    Run Rolling Regression
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_1e352fb3b4(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c228568878(request):
    """ 
    Run Recursive Regression
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_c228568878(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_489b543342(request):
    """ 
    Run Decision Tree
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_489b543342(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c2bd1e1d38(request):
    """ 
    Run Decision Tree Grid Search CV
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_c2bd1e1d38(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_5355980d1d(request):
    """ 
    Run Random Forest
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_5355980d1d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_df765dc206(request):
    """ 
    Run Random Forest Grid Search
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_df765dc206(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1f3b558266(request):
    """ 
    Run Features Importance
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_1f3b558266(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_e75321f00e(request):
    """ 
    Run Mutual Information
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_e75321f00e(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_98dd624adb(request):
    """ 
    Run Time Series Analysis Model
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_98dd624adb(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_433cc52e60(request):
    """ 
    Test lib installed
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_433cc52e60(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_00446c7b03(request):
    """ 
    Install lib
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_00446c7b03(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_0c9f61a7d7(request):
    """ 
    Update dataframe
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_0c9f61a7d7(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_041c813eaa(request):
    """ 
    Save dataframe config (conditional formatting, filters, sorting etc...)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_041c813eaa(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_01439542b8(request):
    """ 
    Create df (put_df) from gui (widget mode)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_01439542b8(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_e1ece029cd(request):
    """ 
    Create dataframe from connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_e1ece029cd(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_796520b6db(request):
    """ 
    Create dataframe from GUI copy/paste
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_796520b6db(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_748bffb111(request):
    """ 
    Preview dataframe from GUI copy/paste
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_748bffb111(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_9df0bb5299(request):
    """ 
    Delete dataframe
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_2ab426de66.sparta_9235b6fd90(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
