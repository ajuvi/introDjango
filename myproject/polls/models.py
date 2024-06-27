import datetime
from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def total_votes(self):
        total = 0
        for choice in self.choice_set.all():
            total += choice.vote_set.count()
        return total

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    #votes = models.IntegerField(default=0)

    def count_votes(self): 
        return self.vote_set.all().count()

    def __str__(self):
        return self.choice_text

class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    data = models.DateTimeField(auto_now=True)
    ip = models.CharField(max_length=20)

    def __str__(self):
        return f'{id} - {self.question} -  {self.choice}'
