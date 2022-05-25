from json import loads

from django.http import JsonResponse
from jsonschema import validate


def validate_request(req, response_function, *args, **kargs):
    try:
        if len(req.body) == 0:
            return JsonResponse(
                {
                    "internalCode": "entity-not-processable",
                    "path": "body",
                    "message": "There is no body",
                },
                safe=False,
                status=422,
            )
        data = loads(req.body.decode("utf-8"))
        validate(data, response_function.schema)
        return response_function(req, data, *args, **kargs)
    except Exception as err:
        res = {"internalCode": "validation-error", "message": err.message}
        if len(err.path) == 0:
            res["path"] = err.message.split(" ")[0].replace("'", "")
        else:
            res["path"] = err.path[0]
        return JsonResponse(res, safe=False, status=400)
