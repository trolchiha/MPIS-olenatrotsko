from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Project(models.Model):
    class WorkType(models.TextChoices):
        SOCIAL = 'соціальна'
        MEDICAL = 'медична'
        HUMANITARIAN = 'гуманітарна'
        EDUCATIONAL = 'освітня'
        CULTURAL = 'культурна'
        SPORT = 'спортивна'
        SCIENTIFIC = 'наукова'
        OTHER = 'інша'

    name = models.CharField(max_length=100)
    description = models.TextField()
    coordinator = models.ForeignKey(User, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    work_type = models.CharField(
        max_length=11,
        choices=WorkType.choices,
        default=WorkType.OTHER,
    )

    def __str__(self):
        return self.name

class Application(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)
    application_text = models.TextField(null=True, blank=True)
    application_date = models.DateField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.project.name + " - " + self.applicant.first_name + " " + self.applicant.last_name
    
class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return self.name
    
class Volunteer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True)
    phone_number = models.CharField(max_length=20)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.user.first_name + " " + self.volunteer.last_name

class ProjectVolunteer(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    volunteer = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.project.name + " - " + self.volunteer.first_name + " " + self.volunteer.last_name
