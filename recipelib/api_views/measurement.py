from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.measurement import (
    find_measurement_by_id,
)
from recipelib.api_views.decorators.user import admin_check
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.measurements.measurement_actions import (
    create_measurement,
    delete_measurement_by_id,
    get_all_measurements,
    get_measurement_by_id,
)


@method_decorator(csrf_exempt, name="dispatch")
class MeasurementView(View):
    @method_decorator(find_measurement_by_id)
    def get(self, req, measurement=None):
        if measurement is not None:
            return get_measurement_by_id(req, measurement)
        return get_all_measurements(req)

    @method_decorator(admin_check)
    def post(self, req):
        return validate_request(req, create_measurement)

    @method_decorator(admin_check)
    @method_decorator(find_measurement_by_id)
    def delete(self, req, measurement):
        return delete_measurement_by_id(req, measurement)
