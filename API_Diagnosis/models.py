from django.contrib import admin
from django.db import models
from API_Source.models import User
from cloudinary.models import CloudinaryField


GENDER_ = (("Male", "Male"), ("Female", "Female"))
ANATOM_SITE_GENERAL = (
    ("abdoben", "abdoben"), ("back", "back"), ("chest", "chest")
    , ("ear", "ear"), ("face", "face"), ("foot", "foot")
    , ("hand", "hand"), ("head/neck", "head/neck"), ("torsor", "torsor")
    , ("palms/soles", "palms/soles"), ("upper extremity", "upper extremity")
    , ("lower extremity", "lower extremity")
)


def upload_path(instance, filename):
    return '/'.join(['covers', str(instance.anatom_site_general_challenge), filename])


class DiagnosisRecord(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="DRecord_of_author")
    create_at = models.DateTimeField(auto_now_add=True)
    # image_record = models.ImageField(blank=True, null=True, upload_to=upload_path)
    image_record = CloudinaryField('image')
    gender = models.CharField(
        max_length=20,
        choices=GENDER_,
        default='1',
        blank=False
    )
    anatom_site_general_challenge = models.CharField(
        max_length=256,
        choices=ANATOM_SITE_GENERAL,
        default='unknown',
        blank=False
    )
    age_approx = models.IntegerField(blank=False)
    predict = models.IntegerField(blank=True, null=True, default=0)

    def save(self, *args, **kwargs):
        super(DiagnosisRecord, self).save(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


admin.site.register(DiagnosisRecord)