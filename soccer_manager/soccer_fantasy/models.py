from django.db import models

# Create your models here.
class UserRegistry(models.Model):

    user_name = models.CharField(max_length=100)
    user_email = models.EmailField(max_length=100)
    user_password = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=12)
    status = models.BooleanField(default=False)

class Teams(models.Model):
    team_name = models.CharField(max_length=100)
    team_country = models.CharField(max_length=100)
    team_value = models.IntegerField(default=0)
    team_budget = models.IntegerField(default=0)
    owned_by = models.ForeignKey(UserRegistry, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField()

class PlayersRegistry(models.Model):
    player_firstname = models.CharField(max_length=100)
    player_lastname = models.CharField(max_length=100)
    player_age = models.IntegerField(default=0)
    player_country = models.CharField(max_length=100)
    player_value = models.IntegerField(default=0)
    player_team = models.ForeignKey(Teams, on_delete=models.CASCADE)


