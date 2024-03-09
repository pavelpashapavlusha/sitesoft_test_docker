from django.db import models


class Habr_Parser(models.Model):
    title = models.CharField(max_length=1000)
    url = models.CharField(max_length=1000)
    date = models.CharField(max_length=1000)
    name_author = models.CharField(max_length=1000)
    url_author = models.CharField(max_length=1000)

    def __str__(self):
        return self.title


class Habs(models.Model):
    hab = models.CharField(max_length=1000)
    title_article = models.CharField(max_length=1000, )

    def __str__(self):
        return self.hab
