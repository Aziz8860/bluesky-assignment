from flask import jsonify, make_response

def jsonapi_response(data, status=200):
    return make_response(
        jsonify({'data': data}),
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