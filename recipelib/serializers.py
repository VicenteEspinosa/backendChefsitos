from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from recipelib.models import Profile, User
from recipelib.models.measurement import Measurement


class UserSerializer(ModelSerializer):
    picture_url = serializers.SerializerMethodField("get_picture_url")
    description = serializers.SerializerMethodField("get_description")

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "description",
            "picture_url",
        )

    def get_picture_url(self, obj):
        return ProfileSerializer(obj.profile).data.get("picture_url")

    def get_description(self, obj):
        return ProfileSerializer(obj.profile).data.get("description")


class ProfileSerializer(ModelSerializer):
    class Meta:
        model = Profile
        fields = ("description", "picture_url")


class MeasurementSerializer(ModelSerializer):
    class Meta:
        model = Measurement
        fields = (
            "id",
            "name",
        )
