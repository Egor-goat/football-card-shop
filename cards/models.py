from django.contrib.auth.models import User
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE
    )

    coins = models.IntegerField(default=200)

    def __str__(self):
        return f"{self.user.username} - {self.coins} coins"

class PlayerCard(models.Model):
    RARITY_CHOICES = [
        ('bronze', "Bronze"),
        ("silver", "Silver"),
        ("gold", "Gold"),
        ("legendary", 'Legendary'),
    ]
    POSITION_CHOICES = [
        ("GK", "Goalkeeper"),
        ("DEF", "Defender"),
        ("MID", "Midfielder"),
        ("ATT", "Attacker"),
    ]

    position = models.CharField(
        max_length=3,
        choices=POSITION_CHOICES,
        default="ATT"
    )
    
    
    name = models.CharField(max_length=100)

    overall = models.IntegerField()

    pace = models.IntegerField()
    shooting = models.IntegerField()
    passing = models.IntegerField()
    dribbling = models.IntegerField()
    defending = models.IntegerField()
    physical = models.IntegerField()
    playstyles = models.IntegerField()
    playstyle_plus = models.IntegerField()
    price = models.IntegerField()
    income = models.IntegerField(default=10)

    rarity = models.CharField(
        max_length=20,
        choices=RARITY_CHOICES,
        default="bronze"
    )

    def __str__(self):
        return self.name

    image = models.ImageField(
        upload_to='cards/',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.name
    

class TeamCard(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    card = models.ForeignKey(
        PlayerCard,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.user.username} team - {self.card.name}"

    
class UserCard(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    card = models.ForeignKey(
        PlayerCard,
        on_delete=models.CASCADE
    )

    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.card.name}"

class Pack(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()

    bronze_chance = models.IntegerField(default=60)
    silver_chance = models.IntegerField(default=25)
    gold_chance = models.IntegerField(default=12)
    legendary_chance = models.IntegerField(default=3)

    def __str__(self):
        return f"{self.name} - {self.price} coins"
