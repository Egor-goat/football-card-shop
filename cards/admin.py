from django.contrib import admin
from .models import PlayerCard, UserCard, UserProfile, TeamCard, Pack

@admin.register(PlayerCard)
class PlayerCardAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        'overall',
        'position',
        'rarity',
        'pace',
        'shooting',
        'passing',
        'dribbling',
        'defending',
        'physical',
        'playstyles',
        'playstyle_plus',
        'price',
    )


@admin.register(UserCard)
class UserCardAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        'card',
        'quantity',
    )

@admin.register(TeamCard)
class TeamCardAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "card",
    )

@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        'price',
        'bronze_chance',
        'silver_chance',
        'gold_chance',
        'legendary_chance',
    )