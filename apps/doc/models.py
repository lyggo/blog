from django.db import models

class Doc(models.Model):
    file_path = models.URLField()
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    is_delete = models.BooleanField(default=False)
    author = models.ForeignKey('authPro.User', on_delete=models.CASCADE, blank=True)

