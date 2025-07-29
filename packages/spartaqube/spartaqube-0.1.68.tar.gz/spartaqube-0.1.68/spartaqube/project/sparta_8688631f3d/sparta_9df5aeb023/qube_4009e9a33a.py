import os
import re
import uuid
import json
from datetime import datetime
from nbconvert.filters import strip_ansi
from project.sparta_8688631f3d.sparta_07864420ce import qube_7bd77509b9 as qube_7bd77509b9
from project.sparta_8688631f3d.sparta_c77f2d3c37.qube_8f0cad92aa import sparta_226d9606de, sparta_244cea0b2a
from project.logger_config import logger


def sparta_b7ccd41588(file_path):
    return os.path.isfile(file_path)


def sparta_6dff9487e0():
    return qube_7bd77509b9.sparta_408fe47d60(json.dumps({'date': str(datetime.now())})
        )


def sparta_7241b74ceb() ->dict:
    """
    Return empty metadata dict
    """
    metadata_dict = {'kernelspec': {'display_name': 'Python 3 (ipykernel)',
        'language': 'python', 'name': 'python3'}, 'language_info': {
        'codemirror_mode': {'name': 'ipython', 'version': 3},
        'file_extension': '.py', 'mimetype': 'text/x-python', 'name':
        'python', 'nbconvert_exporter': 'python', 'pygments_lexer':
        'ipython3'}, 'sqMetadata': sparta_6dff9487e0()}
    return metadata_dict


def sparta_f9d3724527() ->dict:
    return {'cell_type': 'code', 'source': [''], 'metadata': {},
        'execution_count': None, 'outputs': []}


def sparta_1d626ee264() ->list:
    return [sparta_f9d3724527()]


def sparta_142124822c() ->dict:
    """
    Create empty ipynb dict
    """
    return {'nbformat': 4, 'nbformat_minor': 0, 'metadata':
        sparta_7241b74ceb(), 'cells': []}


def sparta_4a275ac0ae(first_cell_code='') ->dict:
    """
    Return an empty ipynb dict
    """
    empty_notebook = sparta_142124822c()
    ini_cell_dict = sparta_f9d3724527()
    ini_cell_dict['source'] = [first_cell_code]
    empty_notebook['cells'] = [ini_cell_dict]
    return empty_notebook


def sparta_f85b909c28(full_path):
    """
    Get the ipynb notebook file (or create an empty)
    """
    if sparta_b7ccd41588(full_path):
        return sparta_dcec6aed93(full_path)
    else:
        return sparta_4a275ac0ae()


def sparta_dcec6aed93(full_path):
    """
    Get the ipynb notebook file
    """
    return sparta_e6b53d7bf5(full_path)


def sparta_1597019bcc() ->dict:
    """
    
    """
    ipynb_dict = sparta_142124822c()
    sq_metadata_dict = json.loads(qube_7bd77509b9.sparta_e87241929f(ipynb_dict[
        'metadata']['sqMetadata']))
    ipynb_dict['metadata']['sqMetadata'] = sq_metadata_dict
    return ipynb_dict


def sparta_e6b53d7bf5(full_path) ->dict:
    """
    
    """
    with open(full_path) as f:
        file_content = f.read()
    if len(file_content) == 0:
        ipynb_dict = sparta_142124822c()
    else:
        ipynb_dict = json.loads(file_content)
    ipynb_dict = sparta_fb8080c3bc(ipynb_dict)
    return ipynb_dict


def sparta_fb8080c3bc(ipynb_dict) ->dict:
    """
    
    """
    ipynb_keys = list(ipynb_dict.keys())
    if 'cells' in ipynb_keys:
        ipynb_cells = ipynb_dict['cells']
        for this_cell in ipynb_cells:
            if 'metadata' in list(this_cell.keys()):
                if 'sqMetadata' in this_cell['metadata']:
                    this_cell['metadata']['sqMetadata'
                        ] = qube_7bd77509b9.sparta_e87241929f(this_cell[
                        'metadata']['sqMetadata'])
    try:
        ipynb_dict['metadata']['sqMetadata'] = json.loads(qube_7bd77509b9.sparta_e87241929f(ipynb_dict['metadata']['sqMetadata']))
    except:
        ipynb_dict['metadata']['sqMetadata'] = json.loads(qube_7bd77509b9.sparta_e87241929f(sparta_6dff9487e0()))
    return ipynb_dict


def sparta_1dbf0a0a23(full_path):
    """
    Load non mapped external ipynb file (into SpartaQube code editor)
    """
    ipynb_dict = dict()
    with open(full_path) as f:
        ipynb_dict = f.read()
    if len(ipynb_dict) == 0:
        ipynb_dict = sparta_1597019bcc()
        ipynb_dict['metadata']['sqMetadata'] = json.dumps(ipynb_dict[
            'metadata']['sqMetadata'])
    else:
        ipynb_dict = json.loads(ipynb_dict)
        if 'metadata' in list(ipynb_dict.keys()):
            if 'sqMetadata' in list(ipynb_dict['metadata'].keys()):
                ipynb_dict = sparta_fb8080c3bc(ipynb_dict)
                ipynb_dict['metadata']['sqMetadata'] = json.dumps(ipynb_dict
                    ['metadata']['sqMetadata'])
    ipynb_dict['fullPath'] = full_path
    return ipynb_dict


def save_ipnyb_from_notebook_cells(notebook_cells_arr, full_path,
    dashboard_id='-1'):
    """
    Save an ipynb resource
    """
    ipynb_cells_new = []
    for this_cell_dict in notebook_cells_arr:
        this_cell_dict['bIsComputing'] = False
        b_delete = this_cell_dict['bDelete']
        cell_type = this_cell_dict['cellType']
        code = this_cell_dict['code']
        position_index = this_cell_dict['positionIndex']
        this_cell_dict['source'] = [code]
        ipynb_output_list = this_cell_dict.get('ipynbOutput', [])
        ipynb_error_list = this_cell_dict.get('ipynbError', [])
        logger.debug('ipynb_output_list')
        logger.debug(ipynb_output_list)
        logger.debug(type(ipynb_output_list))
        logger.debug('ipynb_error_list')
        logger.debug(ipynb_error_list)
        logger.debug(type(ipynb_error_list))
        logger.debug('this_cell_dict')
        logger.debug(this_cell_dict)
        if int(b_delete) == 0:
            if cell_type == 0:
                cell_type_str = 'code'
            elif cell_type == 1:
                cell_type_str = 'markdown'
            elif cell_type == 2:
                cell_type_str = 'markdown'
            elif cell_type == 3:
                cell_type_str = 'raw'
            save_cell_dict = {'metadata': {'sqMetadata': qube_7bd77509b9.sparta_408fe47d60(json.dumps(this_cell_dict))}, 'id': uuid.uuid4().hex[:8], 'cell_type': cell_type_str, 'source': [code],
                'execution_count': None, 'tmp_idx': position_index,
                'outputs': []}
            if len(ipynb_output_list) > 0:
                outputs_store = []
                for elem_dict in ipynb_output_list:
                    tmp_dict = {}
                    tmp_dict[elem_dict['type']] = [elem_dict['output']]
                    outputs_store.append({'data': tmp_dict, 'output_type':
                        'execute_result'})
                save_cell_dict['outputs'] = outputs_store
            elif len(ipynb_error_list) > 0:
                save_cell_dict['outputs'] = ipynb_error_list
                try:
                    tb_errors = []
                    ipython_input_pat = re.compile(
                        '<ipython-input-\\d+-[0-9a-f]+>')
                    for elem_dict in ipynb_error_list:
                        elem_dict['output_type'] = 'error'
                        tb_errors += [re.sub(ipython_input_pat,
                            '<IPY-INPUT>', strip_ansi(line)) for line in
                            elem_dict['traceback']]
                    if len(tb_errors) > 0:
                        save_cell_dict['tbErrors'] = '\n'.join(tb_errors)
                except Exception as e:
                    logger.debug(
                        'Except prepare error output traceback with msg:')
                    logger.debug(e)
            else:
                save_cell_dict['outputs'] = []
            ipynb_cells_new.append(save_cell_dict)
    ipynb_cells_new = sorted(ipynb_cells_new, key=lambda d: d['tmp_idx'])
    [thisObj.pop('tmp_idx', None) for thisObj in ipynb_cells_new]
    ipynb_existing_dict = sparta_f85b909c28(full_path)
    sq_metadata_dict = ipynb_existing_dict['metadata']['sqMetadata']
    sq_metadata_dict['identifier'] = {'dashboardId': dashboard_id}
    ipynb_existing_dict['metadata']['sqMetadata'] = qube_7bd77509b9.sparta_408fe47d60(
        json.dumps(sq_metadata_dict))
    ipynb_existing_dict['cells'] = ipynb_cells_new
    with open(full_path, 'w') as file:
        json.dump(ipynb_existing_dict, file, indent=4)
    return {'res': 1}


def sparta_1b0c5846fa(full_path) ->list:
    """
    This function returns a list of the notebookArrCells from the ipynb raw file
    """
    full_path = sparta_226d9606de(full_path)
    ipynb_dict = dict()
    with open(full_path) as f:
        ipynb_json = f.read()
        ipynb_dict = json.loads(ipynb_json)
    cells = ipynb_dict['cells']
    notebook_cells_list = []
    for cell_dict in cells:
        notebook_cells_list.append({'code': cell_dict['source'][0]})
    logger.debug('notebook_cells_list')
    logger.debug(notebook_cells_list)
    return notebook_cells_list

#END OF QUBE
