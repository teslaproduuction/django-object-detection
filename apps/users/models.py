from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from PIL import Image


class Organization(models.TextChoices):
    A = 'A', _("A")
    B = 'B', _("B")


class Gender(models.TextChoices):
    MALE = 'M', _("Male")
    FEMALE = 'F', _("Female")
    OTHER = 'O', _("Other")
    PREFER_NOT_TO_SAY = 'P', _("Prefer not to say")


class CustomUser(AbstractUser):
    orig_name = models.CharField(
        choices=Organization.choices, max_length=2)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        null=True,
        blank=True,
        verbose_name=_("Gender")
    )


class Profile(models.Model):
    user = models.OneToOneField("users.CustomUser", on_delete=models.CASCADE)
    image = models.ImageField(default='default.png', upload_to='profile_pics')

    def __str__(self):
        return f'{self.user} Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            output_size = (300, 300)
            img.thumbnail(output_size)
            img.save(self.image.path)