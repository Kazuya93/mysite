from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    num = models.IntegerField()

class FT_Q(models.Model):
    eid = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    vendor_can_see = models.BooleanField()
    is_finalized = models.BooleanField()

class FT_A(models.Model):
    qid = models.ForeignKey(FT_Q, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    Answer = models.CharField(max_length=200)

class MC_Q(models.Model):
    eid = models.ForeignKey(Event, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)
    vendor_can_see = models.BooleanField()
    is_finalized = models.BooleanField()

class MC_Choice(models.Model):
    qid = models.ForeignKey(MC_Q, on_delete=models.CASCADE)
    choice = models.CharField(max_length=200)

class MC_A(models.Model):
    eid = models.ForeignKey(MC_Q, on_delete=models.CASCADE)
    answer = models.ForeignKey(MC_Choice, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)

class access(models.Model):
    eid = models.ForeignKey(Event, on_delete=models.CASCADE)
    username = models.CharField(max_length=200)
    role = models.CharField(max_length=100)