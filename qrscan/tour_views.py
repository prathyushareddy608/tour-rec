from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .tour_models import TourDestination, UserPreference, UserRecommendation
import random


@login_required
def tour_recommendation_view(request):
    # Fetch user preferences if they exist
    user_prefs, created = UserPreference.objects.get_or_create(user=request.user)

    # Filter destinations based on user preferences
    destinations = TourDestination.objects.filter(is_active=True)

    # Apply filtering logic
    if user_prefs:
        if user_prefs.preferred_categories:
            destinations = destinations.filter(category__in=user_prefs.preferred_categories)
        if user_prefs.preferred_regions:
            destinations = destinations.filter(region__in=user_prefs.preferred_regions)
        if user_prefs.preferred_experience_types:
            destinations = destinations.filter(experience_type__in=user_prefs.preferred_experience_types)
        destinations = destinations.filter(crowd_level__lte=user_prefs.crowd_preference)
        destinations = destinations.filter(accessibility__lte=user_prefs.accessibility_preference)

    # Randomly select a place
    selected_destination = random.choice(destinations)

    # Create or update user recommendation
    UserRecommendation.objects.update_or_create(
        user=request.user,
        destination=selected_destination,
        defaults={
            'recommendation_score': random.uniform(0.7, 1.0),
            'reason': f"Recommended based on your preferences for {selected_destination.category} and {selected_destination.experience_type} experiences."
        }
    )

    # Fetch reviews for the selected destination
    reviews = selected_destination.reviews.all()

    return render(request, 'tour_recommendation.html', {
        'destination': selected_destination,
        'reviews': reviews,
    })


@login_required
def destination_overview(request, pk):
    # Fetch destination details
    destination = get_object_or_404(TourDestination, pk=pk)
    reviews = destination.reviews.all()

    return render(request, 'destination_overview.html', {
        'destination': destination,
        'reviews': reviews,
    })
