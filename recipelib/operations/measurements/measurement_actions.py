from django.http import JsonResponse
from recipelib.models import Measurement, measurement
from recipelib.serializers import MeasurementSerializer

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
            return JsonResponse(
                {
                    "internalCode": "entity-not-processable",
                    "path": "name",
                    "message": f"Measurement with name '{measurement.name}' already exists",
                },
                safe=False,
                status=422,
            )
        measurement = Measurement.objects.create(
            name=data.get("name")
        )
        measurement.save()
        return JsonResponse(MeasurementSerializer(measurement).data, safe=False, status=201)

    except Exception as err:
        print(err)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": "An error has ocurred",
            },
            safe=False,
            status=500,
        )

create_measurement.schema = schema

def get_all_measurements(req):
    try:
        measurements = Measurement.objects.all()
        return JsonResponse(MeasurementSerializer(measurements, many=True).data, safe=False, status=200)
    except Exception as err:
        print(err)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": "An error has ocurred",
            },
            safe=False,
            status=500,
        )
    
def get_measurement_by_id(req, measurement_id):
    try:
        measurement = Measurement.objects.filter(pk=measurement_id)
        if measurement:
            return JsonResponse(MeasurementSerializer(measurement[0]).data, safe=False, status=200)
        return JsonResponse(
                {
                    "message": "measurement not found",
                },
                safe=False,
                status=404,
            )
    except Exception as err:
        print(err)
        return JsonResponse(
            {
                "internalCode": "internal-error",
                "message": "An error has ocurred",
            },
            safe=False,
            status=500,
        )