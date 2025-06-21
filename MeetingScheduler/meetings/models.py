from django.db import models

# 🔹 Clients Table
class clients(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    code = models.CharField(max_length=6)

    def __str__(self):
        return self.name
    

class Owner(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name    


# 🔹 Meetings Table
class Meeting(models.Model):
    client = models.ForeignKey(clients, on_delete=models.CASCADE)
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, null=True)  # ← ensure this exists
    reg_no = models.CharField(max_length=100)
    meeting_type = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField() 

