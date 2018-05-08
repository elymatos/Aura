from flask import jsonify
FAIL = "fail"
ERROR = "error"
SUCCESS = "success"


def build_response(status, content=None):
    if status == SUCCESS:
        return jsonify(
            status=status, data=content or {}
        )
    else:
        if content is None:
            raise ValueError("Failed, but someone didnt say why.")
        return jsonify(
            status=status, message=content
        )



