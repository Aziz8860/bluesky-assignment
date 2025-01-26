from flask import jsonify, make_response

def jsonapi_response(data, message="Data found", error=None, meta=None, status=200):
    """Format a successful JSON:API response."""
    response = {
        'data': data,
        'message': message,
        'error': error
    }
    if meta:
        response['meta'] = meta
    return make_response(
        jsonify(response),
        status,
        {'Content-Type': 'application/vnd.api+json'}
    )

def jsonapi_error(message, error, status=400):
    """Format an error JSON:API response."""
    return make_response(
        jsonify({
            'data': [],
            'message': message,
            'error': error
        }),
        status,
        {'Content-Type': 'application/vnd.api+json'}
    )