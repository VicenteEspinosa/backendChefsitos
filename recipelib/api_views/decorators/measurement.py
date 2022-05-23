from functools import wraps

from recipelib.models import Measurement
from recipelib.utils import error_json_response, not_found_json_response


def find_measurement_by_id(view):
    @wraps(view)
    def wrapper(request, measurement_id, *args, **kwargs):
        try:
            measurement_array = Measurement.objects.filter(pk=measurement_id)
            if measurement_array:
                return view(request, measurement_array[0], *args, **kwargs)
            return not_found_json_response("measurement")
        except Exception as err:
            print(err)
            return error_json_response(err)

    return wrapper
