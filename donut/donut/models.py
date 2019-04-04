from django.db import models

class Donut_Group(models.Model):
    name = models.CharField(max_length=1000)
    frequency_in_days = models.IntegerField()
    csv_name = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.name
    

class ConnectedPair(models.Model):
    userid1 = models.IntegerField()
    userid2 = models.IntegerField()
    connected_group = models.ForeignKey(Donut_Group,
                                on_delete=models.CASCADE)
    def __str__(self):
        return str(self.userid1) + ", "+str(self.userid2)

