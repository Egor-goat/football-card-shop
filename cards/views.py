from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import PlayerCard, UserCard, UserProfile, TeamCard, Pack
import random
from django.contrib import messages


@login_required
def card_shop(request):
    cards = PlayerCard.objects.all()
    packs = Pack.objects.all()
    profile = get_object_or_404(UserProfile, user=request.user)

    return render(
        request,
        "cards/shop.html",
        {
            "cards": cards,
            "packs": packs,
            'profile': profile,
        }
    )


@login_required
def buy_card(request, card_id):
    card = get_object_or_404(PlayerCard, id=card_id)
    profile = get_object_or_404(UserProfile, user=request.user)

    if profile.coins < card.price:
        return redirect("card_shop")
    
    profile.coins -= card.price
    profile.save()

    user_card, created = UserCard.objects.get_or_create(
        user=request.user,
        card=card,
        defaults={
            "quantity": 1
        }
    )

    if not created:
        user_card.quantity += 1
        user_card.save()
    return redirect("card_shop")


@login_required
def my_cards(request):
    user_cards = UserCard.objects.filter(user=request.user)
    profile = UserProfile.objects.get(user=request.user)

    total_income = 0

    return render(
        request,
        "cards/my_cards.html",
        {
            "user_cards": user_cards,
            "profile": profile,
            "total_income": total_income,
        }
    )


@login_required
def collect_income(request):

    profile = UserProfile.objects.get(
        user=request.user
    )

    user_cards = UserCard.objects.filter(
        user=request.user
    )

    total_income = 0

    for user_card in user_cards:
        total_income += (
            user_card.card.income
            *
            user_card.quantity
        )

    profile.coins += total_income

    profile.save()

    return redirect(
        "my_cards"
    )

@login_required
def add_to_team(request, card_id):
    card = get_object_or_404(PlayerCard, id=card_id)

    team_size = TeamCard.objects.filter(
        user=request.user
    ).count()
    if team_size >= 11:
        messages.error(
            request,
            "Your team is full! You can only have 11 players."
        )

        return redirect("my_cards")

    TeamCard.objects.get_or_create(
        user=request.user,
        card=card
    )

    return redirect("my_cards")

@login_required
def open_pack(request, pack_id):
    profile = get_object_or_404(UserProfile, user=request.user,)

    pack = get_object_or_404(
        Pack,
        id=pack_id,
    )

    if profile.coins < pack.price:
        messages.error(request, "Not enough coins to open a pack.")
        return redirect("card_shop")
    
    all_cards = list(PlayerCard.objects.all())

    if not all_cards:
        messages.error(request, "No cards available.")
        return redirect("card_shop")

    bronze_cards = list(PlayerCard.objects.filter(rarity='bronze'))
    silver_cards = list(PlayerCard.objects.filter(rarity='silver'))
    gold_cards = list(PlayerCard.objects.filter(rarity='gold'))
    legendary_cards = list(PlayerCard.objects.filter(rarity='legendary'))

    rarity_roll = random.randint(1, 100)

    bronze_limit = pack.bronze_chance

    silver_limit = (
        bronze_limit + pack.silver_chance
    )

    gold_limit = (
        silver_limit + pack.gold_chance
    )

    if rarity_roll <= bronze_limit and bronze_cards:
        random_card = random.choice(bronze_cards)

    elif rarity_roll <= silver_limit and silver_cards:
        random_card = random.choice(silver_cards)

    elif rarity_roll <= gold_limit and gold_cards:
        random_card = random.choice(gold_cards)

    elif legendary_cards:
        random_card = random.choice(legendary_cards)

    else:
        random_card = random.choice(all_cards)

    profile.coins -= pack.price
    profile.save()

    user_card, created = UserCard.objects.get_or_create(
        user=request.user,
        card=random_card,
        defaults={
            "quantity": 1,
            },
    )

    if not created:
        user_card.quantity += 1
        user_card.save()


    return render(
        request,
        "cards/pack_result.html",
        {
            "card": random_card,
            "pack": pack,
        }
        )


@login_required
def my_team(request):
    team_cards = TeamCard.objects.filter(
        user=request.user
    )

    total_rating = 0
    total_income = 0

    for team_card in team_cards:
        total_rating += team_card.card.overall
        total_income += team_card.card.income

    if team_cards:
        team_rating = total_rating // len(team_cards)
    else:
        team_rating = 0

    return render(
        request,
        "cards/my_team.html",
        {
            "team_cards": team_cards,
            "team_rating": team_rating,
            "total_income": total_income,
        }
    )

@login_required
def remove_from_team(request, team_card_id):
    team_card = get_object_or_404(
        TeamCard,
        id=team_card_id,
        user=request.user
    )

    team_card.delete()
    return redirect('my_team')