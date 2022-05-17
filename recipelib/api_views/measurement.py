from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from recipelib.operations.measurements.measurement_actions import create_measurement, get_all_measurements, get_measurement_by_id
from recipelib.infrastructure.validation.request_validation import validate_request

@method_decorator(csrf_exempt, name='dispatch')
class MeasurementView(View):
    def get(self, req, measurement_id=None):
        if measurement_id is not None:
            return get_measurement_by_id(req, measurement_id)
        return get_all_measurements(req)

    def post(self, req):
        return validate_request(req, create_measurement)
