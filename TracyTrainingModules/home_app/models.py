from django.db import models

# Create your models here.
class Custom_User(models.Model):
    access_code = models.CharField(max_length=25)
    user_type = models.CharField(max_length=5,choices=(('Student','stu'),('Supervisor','sup')),default='stu')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    sections = models.CharField(max_length=100)

    def __str__(self):
        return '{}, {}'.format(self.first_name,self.last_name)

class Content(models.Model):
    section_num = models.IntegerField()
    module_num = models.IntegerField()
    yt_link = models.TextField(max_length=None)
    content = models.TextField(max_length=None)

    def __str__(self):
        return 'Section:{} | Module:{} '.format(self.section_num,self.module_num)
