from django.db import models
from django.utils import timezone
class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title
    def first_line(self):
            line_list = self.text.split('\n')
            return line_list[0]
    def link2map(self):
            line_list = self.text.split('\n')
            return "https://www.google.com/maps/embed/v1/search?key=AIzaSyCo5C_ndWSOe_gZGlxNWkL5Cc-GR01fUS0&zoom=16&q="+line_list[0]
