from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=255, blank=False, null=False, unique=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return str(self.name)


class VanityUrl(models.Model):

    RESPONSE_CODES = {
        '301': '301 Moved Permanently',
        '302': '302 Found',
        '307': '307 Temporary Redirect',
        '308': '308 Permanent Redirect',
    }

    id = models.AutoField(primary_key=True)
    vanity_url = models.CharField(max_length=255,
                                  blank=False, null=False, unique=True,
                                  verbose_name='Redirect from')
    target = models.CharField(max_length=512, default='',
                              blank=False, null=False)
    code = models.CharField(max_length=8, default='301',
                            blank=False, null=False,
                            choices=RESPONSE_CODES)

    category = models.ForeignKey(Category, null=True, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'Vanity URL'
