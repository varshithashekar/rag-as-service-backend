def success_response(data):
    return {
        "status": "success",
        "data": data,
        "error": None
    }


def error_response(code, message):
    return {
        "status": "error",
        "data": None,
        "error": {
            "code": code,
            "message": message
        }
    }