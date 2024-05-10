from django.db import models


class User(models.Model):
    user_id = models.CharField(max_length=63, primary_key=True)
    firstname = models.CharField(max_length=255, null=True, blank=True)
    lastname = models.CharField(max_length=255, null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True)

    objects = models.Manager()

    def __str__(self):
        return self.firstname


class Text(models.Model):
    user_id = models.CharField(max_length=265, null=True, blank=True)
    text = models.CharField(max_length=511, null=True, blank=True)
    date = models.CharField(max_length=511, null=True, blank=True)

    # audio = models.FileField(null=True, blank=True)
    # picture = models.ImageField(null=True, blank=True, upload_to="images")
    # file = models.FileField(null=True, blank=True)

    objects = models.Manager()

    # class Meta:
    #     unique_together = ("user_id", "text", "date")

    # def __str__(self):
    #     return self.text


class TelegramFile(models.Model):
    file_id = models.CharField(max_length=255)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)

    file = models.FileField(null=True, blank=True)


