def sparta_5eb561e104(s):
    """
    Converts a string to a boolean value.:param s: The input string to convert (e.g., 'true', 'false', 'yes', 'no', '1', '0')
    :return: Boolean value True or False
    :raises: ValueError if the string cannot be converted
    """
    if isinstance(s, str):
        s = s.strip().lower()
        if s in ['true', '1', 'yes', 'y']:
            return True
        elif s in ['false', '0', 'no', 'n']:
            return False
    raise ValueError(f"Cannot convert '{s}' to a boolean.")


def sparta_eca660fb82(assign_dict) ->dict:
    """
        Code to be executed when a GUI component is triggered and kernel variables must be assigned with GUI component's values
        assign_dict = {
            'guiType': '',
            'variable': '',
            'value': '',
            'variableState': '',
        }
    """
    gui_type = assign_dict['guiType']
    data_assign_value = assign_dict['value']
    if gui_type == 'boolean':
        if not isinstance(data_assign_value, bool):
            data_assign_value = sparta_5eb561e104(data_assign_value)
    assign_state_variable = f"""import json
{assign_dict['variableState']} = json.loads({assign_dict['interactiveVarDict']})"""
    assign_code = f"{assign_dict['variable']} = {data_assign_value}"
    return {'assign_code': assign_code, 'assign_state_variable':
        assign_state_variable}

#END OF QUBE
