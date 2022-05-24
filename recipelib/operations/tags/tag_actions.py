from django.http import JsonResponse

from recipelib.models import Tag
from recipelib.serializers import TagSerializer
from recipelib.utils import (
    already_exists_json_response,
    error_json_response,
    not_found_json_response,
)

schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "placeholder_url": {"type": "string"},
    },
    "required": ["name", "placeholder_url"],
}


def create_tag(req, data):
    try:
        tag = Tag.objects.filter(name=data.get("name"))
        if tag:
            return already_exists_json_response("tag", "name", tag[0].name)
        tag = Tag.objects.create(
            name=data.get("name"), placeholder_url=data.get("placeholder_url")
        )
        tag.save()
        return JsonResponse(TagSerializer(tag).data, safe=False, status=201)

    except Exception as err:
        print(err)
        return error_json_response(err)


create_tag.schema = schema


def get_all_tags(req):
    try:
        tags = Tag.objects.all()
        return JsonResponse(
            TagSerializer(tags, many=True).data,
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)


def get_tag(req, tag):
    try:
        return JsonResponse(TagSerializer(tag).data, safe=False, status=200)
    except Exception as err:
        print(err)
        return error_json_response(err)


def delete_tag(req, tag):
    try:
        tag.delete()
        return JsonResponse(
            {"message": "tag deleted successfully"},
            safe=False,
            status=200,
        )
    except Exception as err:
        print(err)
        return error_json_response(err)
