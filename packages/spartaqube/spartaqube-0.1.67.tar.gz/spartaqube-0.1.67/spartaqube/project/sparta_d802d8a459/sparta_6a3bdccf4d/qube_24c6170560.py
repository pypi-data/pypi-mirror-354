import json
import base64
from django.http import HttpResponse, Http404
from django.views.decorators.csrf import csrf_exempt
from project.sparta_8345d6a892.sparta_26ea98fb42 import qube_b61b0eabde as qube_b61b0eabde
from project.sparta_8345d6a892.sparta_5ba00adfe7.qube_abe0696d41 import sparta_f83f234832, sparta_36715732c5


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_44cf59c3f0(request):
    """
    Load db connectors
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_44cf59c3f0(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d87c1f97f5(request):
    """
    Store date last open connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_d87c1f97f5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_6f6ecf58c9(request):
    """
    Get list of available engines
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_6f6ecf58c9()
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_7ce317ed2b(request):
    """
    Test connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_7ce317ed2b(json_data)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_77d1631c64(request):
    """
    Preview connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_77d1631c64(json_data)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d871473883(request):
    """
    Get list of available engines
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_d871473883(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_978c08f48a(request):
    """
    Delete connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_978c08f48a(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c7ad1dd0e4(request):
    """
    Pip install connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_c7ad1dd0e4(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_c04664d9de(request):
    """
    Update connector
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_c04664d9de(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_b790a8e18b(request):
    """
    Load tables explorer
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_b790a8e18b(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_30651cf3a3(request):
    """
    Load spartaqube data store explorer (Available dataframes list)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_30651cf3a3(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_c8e00abfa8(request):
    """
    Load spartaqube data store explorer preview
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_c8e00abfa8(json_data
        , request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_81932ddbf4(request):
    """
    Load spartaqube data store explorer preview (for specific dispo date)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.load_spartaqube_data_store_preview_explorer_dispo(
        json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_76d5372734(request):
    """
    Load table columns
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_76d5372734(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_423d3e6af7(request):
    """
    Load data preview explorer
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_423d3e6af7(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_e5cc09b078(request):
    """
    Load data preview explorer statistics
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_e5cc09b078(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1edb6b5f56(request):
    """
    Compute infos and statistics from data source data explorer
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_1edb6b5f56(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f3723d6abc(request):
    """
    Load wss stream structure (from the connector table preview)
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_f3723d6abc(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_8b38b36fbb(request):
    """
    Backend to prepare or load component's output
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_8b38b36fbb(json_data, request.user)
    b_pickle = False
    if b_pickle:
        import os
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'tutoJson',
            f"{json_data['model']}_tuto.json"), 'w') as file:
            json.dump(res, file)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_a73e9d99db(request):
    """
    Get tuto (save as json) in order to to recompute heavily the df-relationships, df-tsa
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    print("json_data['model'] >>> " + str(json_data['model']))
    try:
        import os
        current_path = os.path.dirname(__file__)
        with open(os.path.join(current_path, 'tutoJson',
            f"{json_data['model']}_tuto.json"), 'r') as f:
            res = json.load(f)
    except:
        res = {'res': -1, 'errorMsg': 'Tutorial not available'}
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_65c2061a4d(request):
    """
    Compute statistics modal
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_65c2061a4d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_3ca44cf0ba(request):
    """
    Groupby input data
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_3ca44cf0ba(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_2b881f82a4(request):
    """
    Save plot
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_2b881f82a4(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_73f7d5eb5b(request):
    """
    Update plot
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_73f7d5eb5b(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f1b1c871c4(request):
    """
    # TODO TO IMPLEMENT
    Load data preview explorer statistics
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_f1b1c871c4(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_45a6ac7b8d(request):
    """
    Load plots library
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_45a6ac7b8d(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_36715732c5
def sparta_df4344ecda(request):
    """
    Open plot
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_df4344ecda(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_d939df94fd(request):
    """
    Open plot log
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_d939df94fd(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_601967adb3(request):
    """
    Delete plot
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_601967adb3(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_1fa5156f98(request):
    """
    Update plot config
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_1fa5156f98(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_14000e12c7(request):
    """
    Load plots library widgets
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_14000e12c7(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_e8212eebf7(request):
    """
    Update widget
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_e8212eebf7(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_522bebb076(request):
    """
    Get widget title
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_522bebb076(json_data,
        request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_f20459a0d5(request):
    """
    Unexpose widget
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_f20459a0d5(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)


@csrf_exempt
@sparta_f83f234832
@sparta_36715732c5
def sparta_11d129b200(request):
    """
    Use a widget with other inputs data sent from the Jupyter notebook
    """
    json_data_ = json.loads(request.body)
    json_data = json.loads(json_data_['jsonData'])
    res = qube_b61b0eabde.sparta_11d129b200(json_data, request.user)
    resJson = json.dumps(res)
    return HttpResponse(resJson)

#END OF QUBE
