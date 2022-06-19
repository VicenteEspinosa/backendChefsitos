from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    description = models.TextField(max_length=500, blank=True)
    picture_url = models.CharField(max_length=300)
    following = models.ManyToManyField(
        "self", symmetrical=False, related_name="followers", blank=True
    )


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


# @receiver(post_save, sender=User)
# def update_user_profile(_, instance, user_id, updated, **kwargs):
#     if updated:
#         user = User.objects.get(pk=user_id)
#         instance.profile.save()
