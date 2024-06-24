"""
    This file is to define functions or pieces of code to be used once or multiple times,
    within the program, allowing other files focus on logic intended 
    whilst using pieces of code necessary for the program from here.
"""


def get_serializer_key_error(errors_dict: dict):
    '''
    from serializer.error, we get the very first error from the error dictionary and return
    '''
    try:
        key = list(errors_dict)[0]
        error = errors_dict.get(key)
        return f'`{key}` -> {error[0]}'
    except Exception:
        return ''
    

def response_data(message, status_code):

    """ 
    Returns a structured response body.
    """

    data = {
        "message": message,
        "status-code": status_code
    }

    return data