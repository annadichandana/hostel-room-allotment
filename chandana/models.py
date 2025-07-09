from django.db import models
from datetime import date
from django.db import models
class student(models.Model):
    name = models.CharField(max_length=50)
    rollno = models.CharField(max_length=50)
    branch = models.CharField(max_length=50)
    admission_year = models.IntegerField()
    Email = models.EmailField(help_text="Enter Your Email address")
    phonenumber = models.CharField(max_length=15)
    password = models.CharField(max_length=100, blank=True, null=True)

    @property
    def current_year(self):
        today = date.today()
        delta = today.year - self.admission_year
        if today.month < 7:  
            delta -= 1
        return min(delta + 1, 4)  
    def __str__(self):
        return f"{self.name} ({self.rollno})"

class rooms(models.Model):
    roomno=models.CharField(max_length=10,unique=True)
    totalbeds=models.IntegerField()
    @property
    def occupied(self):
        return RoomAllocation.objects.filter(room=self).count()
    @property
    def remaining_beds(self):
        return self.totalbeds - self.occupied
    def __str__(self):
        return self.roomno


class RoomAllocation(models.Model):
    student = models.OneToOneField(student, on_delete=models.CASCADE)
    room = models.ForeignKey(rooms, on_delete=models.CASCADE)
    allocated_on = models.DateTimeField(auto_now_add=True)