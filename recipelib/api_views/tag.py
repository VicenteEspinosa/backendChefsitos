from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from recipelib.api_views.decorators.tag import find_tag_by_id
from recipelib.api_views.decorators.user import admin_check
from recipelib.infrastructure.validation.request_validation import (
    validate_request,
)
from recipelib.operations.tags.tag_actions import (
    create_tag,
    delete_tag,
    get_all_tags,
    get_tag,
)


@method_decorator(csrf_exempt, name="dispatch")
class TagView(View):
    def get(self, req, tag_id=None):
        if tag_id is not None:
            return self.get_specific(req, tag_id)
        return get_all_tags(req)

    @method_decorator(find_tag_by_id)
    def get_specific(self, req, tag):
        return get_tag(req, tag)

    @method_decorator(admin_check)
    def post(self, req):
        return validate_request(req, create_tag)

    @method_decorator(admin_check)
    @method_decorator(find_tag_by_id)
    def delete(self, req, tag):
        return delete_tag(req, tag)
