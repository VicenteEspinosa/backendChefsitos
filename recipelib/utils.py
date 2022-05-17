from django.http import JsonResponse

def already_exists_json_response(model_name="model", key_name="key", value="value"):
    return JsonResponse(
        {
            "internalCode": "entity-not-processable",
            "path": "name",
            "message": f"Database record of {model_name} with {key_name} '{value}' already exists",
        },
        safe=False,
        status=422,
    )

def error_json_response(error):
    return JsonResponse(
        {
            "internalCode": "internal-error",
            "message": "An error has ocurred",
            "error_content": str(error)
        },
        safe=False,
        status=500,
    )

def not_an_admin_json_response():
    return JsonResponse(
        {
            "message": f"This action is only for administrators",
        },
        safe=False,
        status=403,
    )

def not_found_json_response(object_name="item"):
    return JsonResponse(
        {
            "message": f"{object_name} not found",
        },
        safe=False,
        status=404,
    )

def not_logged_in_json_response():
    return JsonResponse(
        {
            "message": f"Please sign in to access this endpoint",
        },
        safe=False,
        status=401,
    )