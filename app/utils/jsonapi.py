from flask import jsonify, make_response

def jsonapi_response(data, meta=None, status=200):
    response = {
        'data': data
    }
    if meta:
        response['meta'] = meta
    return make_response(
        jsonify(response),
        status,
        {'Content-Type': 'application/vnd.api+json'}
    )

def jsonapi_error(status, title, detail):
    return {
        'errors': [{
            'status': str(status),
            'title': title,
            'detail': detail
        }]
    }