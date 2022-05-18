from django.http import JsonResponse

from recipelib.models import Measurement
from recipelib.serializers import MeasurementSerializer
from recipelib.utils import (
    already_exists_json_response,
    error_json_response,
    not_found_json_response,
)

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
    },
    "required": ["name"],
}


def create_measurement(req, data):
    try:
        measurement = Measurement.objects.filter(name=data.get("name"))
        if measurement:
            return already_exists_json_response(
                "measurement", "name", measurement[0].name
            )
        measurement = Measurement.objects.create(name=data.get("name"))
        measurement.save()
        return JsonResponse(
            MeasurementSerializer(measurement).data, safe=False, status=201
        )

    except Exception as err:
        print(err)
        return error_json_response(err)


create_measurement.schema = schema


def get_all_measurements(req):
    try:
        measurements = Measurement.objects.all()
        return JsonResponse(
            MeasurementSerializer(measurements, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def get_measurement(req, measurement):
    try:
        return JsonResponse(
            MeasurementSerializer(measurement).data, safe=False, status=200
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def delete_measurement(req, measurement):
    try:
        measurement.delete()
        return JsonResponse(
            {"message": "measurement deleted successfully"},
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)
