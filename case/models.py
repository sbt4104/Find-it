from django.db import models
from account.models import UserProfile
# Create your models here.
Choices = (
    ('Under Investigation','Under Investigation'),
    ('Completed','Completed'),
    ('Cancelled', 'Cancelled'),
)
class case(models.Model):
    case_number = models.IntegerField(unique=True)
    case_info = models.TextField()
    deadline = models.DateField(null = True)
    investigation_head = models.ForeignKey(UserProfile, on_delete=models.CASCADE,related_name='case_inv_head')
    members = models.ManyToManyField(UserProfile, blank=True, related_name='case_members')
    status = models.CharField(choices=Choices, max_length=100, default='Under Investigation' )

    def __str__(self):
        return str(self.case_number)

Task_Status = (
    ('Ongoing', 'Ongoing'),
    ('Completed', 'Completed'),
    ('Cancelled', 'Cancelled'),
)
class Task(models.Model):
    case_number = models.IntegerField(unique=False)
    task_number = models.IntegerField(unique=False)
    task_info = models.TextField()
    deadline = models.DateField(null = True)
    investigation_head = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null =True,related_name='task_inv_head')
    task_member = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null =True,related_name='task_member')
    task_case = models.ForeignKey(case, on_delete=models.CASCADE,null=True)
    task_status = models.CharField(choices=Task_Status, max_length=100, default='Ongoing' )

    def __str__(self):
        return str(self.task_number)

"""
class Report(models.Model):
    report = models.TextField()
    report_user = models.ForeignKey(UserProfile,on_delete= models.CASCADE)
    report_case = models.ForeignKey(case, on_delete=models.CASCADE)
    report_task = models.ForeignKey(Task,on_delete=models.CASCADE,null=True)
"""

#NLP

# Create your models here.
class Document(models.Model):
    unq = models.IntegerField(unique=True)
    file1 = models.FileField(upload_to='documents/%Y/%m/%d')
    csvfile1 = models.FileField(upload_to='documents/%Y/%m/%d')
    audio1 = models.FileField(upload_to='documents/%Y/%m/%d')
    url1 = models.URLField(blank=True)
