from django.shortcuts import render, redirect
from qrcode import *
from .models import MonumentTickets, TourDestination, UserPreference, UserRecommendation
from django.views.decorators.csrf import csrf_exempt
from datetime import date, datetime
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login
from .filters import OrderFilter,DetailFilter
from .graphs import get_chart
import pandas as pd
from django.http import JsonResponse
from django.utils import timezone
import random

def homepage(request):
    return redirect("react_app")


class MyReactView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        return {'context_variable': 'value'}



def Ticket_display(request):
    today=date.today()
    d3 = today.strftime("%Y-%m-%d")
    customers = MonumentTickets.objects.filter(date=d3,paid=True,cancelled=False)
    myfilter=OrderFilter(request.GET,queryset=customers)
    customers=myfilter.qs
    return render(request,'ticket.html',{"object_list":customers,"filter":myfilter,"date":today})

def display(request,monuments):
    
    customers = MonumentTickets.objects.filter(monument=monuments)
    myfilter=DetailFilter(request.GET,queryset=customers)
    customers=myfilter.qs
    customer = MonumentTickets.objects.filter(monument=monuments)
    if customer.count()!=0:
        df=customer.values()
        df=pd.DataFrame(df)
        a=df['verified'].value_counts()
        b=a.index.tolist()
        print(b)
        if True not in b:
            a=a.append(pd.Series({True:0},index=[1]))
        if False not in b:
            a=a.append(pd.Series({False:0},index=[0]))
        print (a)

        l=[a[True],a[False]]
        chart=get_chart(l)
        return render(request,'detail.html',{"object_list":customers,"filter":myfilter,"chart":chart,"Monument":monuments})
       

    else :
        return render(request,'detail.html',{"object_list":customers,"filter":myfilter})
        
    




@csrf_exempt
def cancel_booking(request):
    if request.method == 'POST':
        booking_id = request.POST.get('booking_id')
        try:
            booking = MonumentTickets.objects.get(id=booking_id, paid=True, cancelled=False)
            booking.cancelled = True
            booking.cancelled_at = timezone.now()
            booking.save()
            return JsonResponse({'success': True, 'message': 'Booking cancelled successfully'})
        except MonumentTickets.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Booking not found or already cancelled'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

# Dummy QR scanner functions to fix URL issues
def selectMonument(request):
    return redirect('ticket')

def ScanQR(request, monuments):
    return render(request, 'SCANNER.html', {'monument': monuments})

def Call_Scan(request, monuments):
    return render(request, 'SCANNER.html', {'monument': monuments})

def lcd_display(request):
    return render(request, 'counter.html')

# Tour Recommendation Views
def tour_recommendation_view(request):
    """View for tour recommendations based on user preferences"""
    # Handle form submission for user preferences
    if request.method == 'POST':
        # Get user preferences from form
        preferred_categories = request.POST.getlist('categories')
        preferred_regions = request.POST.getlist('regions')
        preferred_experience_types = request.POST.getlist('experience_types')
        budget_range = request.POST.get('budget', 'moderate')
        accessibility_preference = request.POST.get('accessibility', 'any')
        crowd_preference = request.POST.get('crowd', 'any')
        
        # Get filtered destinations based on preferences
        destinations = get_recommended_destinations(
            preferred_categories=preferred_categories,
            preferred_regions=preferred_regions,
            preferred_experience_types=preferred_experience_types,
            budget_range=budget_range,
            accessibility_preference=accessibility_preference,
            crowd_preference=crowd_preference
        )
        
        if not destinations:
            return render(request, 'tour_recommendation.html', {
                'error': 'No destinations match your preferences. Please try different criteria.',
                'show_form': True,
                'categories': TourDestination.CATEGORY_CHOICES,
                'regions': TourDestination.REGION_CHOICES,
                'experience_types': TourDestination.EXPERIENCE_TYPE_CHOICES,
            })
        
        # Select the best destination based on scoring
        selected_destination = destinations[0]
        
        # Get reviews for the selected destination
        reviews = selected_destination.reviews.all()[:5]
        
        # Create recommendation reason
        reason = generate_recommendation_reason(
            selected_destination,
            preferred_categories,
            preferred_regions,
            preferred_experience_types
        )
        
        context = {
            'destination': selected_destination,
            'reviews': reviews,
            'reason': reason,
            'preferences_used': True,
        }
        
        return render(request, 'tour_recommendation.html', context)
    
    # GET request - show preference form or random recommendation
    if request.GET.get('random') == 'true':
        # User wants a random recommendation
        destinations = TourDestination.objects.filter(is_active=True)
        if not destinations.exists():
            return render(request, 'tour_recommendation.html', {
                'error': 'No destinations available. Please populate the database first.'
            })
        
        selected_destination = random.choice(destinations)
        reviews = selected_destination.reviews.all()[:5]
        
        context = {
            'destination': selected_destination,
            'reviews': reviews,
            'reason': "Selected randomly for you to discover something new!",
        }
        
        return render(request, 'tour_recommendation.html', context)
    
    # Show preference form
    context = {
        'show_form': True,
        'categories': TourDestination._meta.get_field('category').choices,
        'regions': TourDestination._meta.get_field('region').choices,
        'experience_types': TourDestination._meta.get_field('experience_type').choices,
        'accessibility_levels': TourDestination._meta.get_field('accessibility').choices,
        'crowd_levels': TourDestination._meta.get_field('crowd_level').choices,
    }
    
    return render(request, 'tour_recommendation.html', context)

def get_recommended_destinations(preferred_categories=None, preferred_regions=None, 
                               preferred_experience_types=None, budget_range='moderate',
                               accessibility_preference='any', crowd_preference='any'):
    """Get destinations based on user preferences with scoring"""
    destinations = TourDestination.objects.filter(is_active=True)
    
    # Apply budget filter
    if budget_range == 'budget':
        destinations = destinations.filter(entry_fee__lte=500)
    elif budget_range == 'moderate':
        destinations = destinations.filter(entry_fee__lte=2000)
    # Premium has no upper limit
    
    # Apply accessibility filter
    if accessibility_preference == 'easy':
        destinations = destinations.filter(accessibility='easy')
    
    # Apply crowd preference filter
    if crowd_preference == 'low':
        destinations = destinations.filter(crowd_level='low')
    
    # Score destinations based on preferences
    scored_destinations = []
    for dest in destinations:
        score = 0
        
        # Category preference scoring
        if preferred_categories and dest.category in preferred_categories:
            score += 3
        
        # Region preference scoring
        if preferred_regions and dest.region in preferred_regions:
            score += 2
        
        # Experience type scoring
        if preferred_experience_types and dest.experience_type in preferred_experience_types:
            score += 3
        
        # UNESCO heritage bonus
        if dest.unesco_heritage:
            score += 1
        
        # Rating bonus
        score += float(dest.average_rating) / 5 * 2  # Convert 5-star to 2-point scale
        
        scored_destinations.append((dest, score))
    
    # Sort by score (highest first) and return destinations
    scored_destinations.sort(key=lambda x: x[1], reverse=True)
    return [dest[0] for dest in scored_destinations]

def generate_recommendation_reason(destination, categories, regions, experience_types):
    """Generate a personalized reason for the recommendation"""
    reasons = []
    
    if categories and destination.category in categories:
        reasons.append(f"matches your interest in {destination.get_category_display().lower()}")
    
    if regions and destination.region in regions:
        reasons.append(f"is located in your preferred {destination.get_region_display()}")
    
    if experience_types and destination.experience_type in experience_types:
        reasons.append(f"offers the {destination.get_experience_type_display().lower()} experience you're looking for")
    
    if destination.unesco_heritage:
        reasons.append("is a UNESCO World Heritage site")
    
    if destination.average_rating >= 4.5:
        reasons.append(f"has excellent reviews ({destination.average_rating}/5 stars)")
    
    if not reasons:
        return "This destination offers a unique experience worth exploring!"
    
    return f"Recommended because it {', '.join(reasons)}."

# New view for preference-based recommendations
def set_preferences_view(request):
    """View to set and save user preferences"""
    if request.method == 'POST':
        # Redirect to recommendation with preferences
        return redirect('tour_recommendation')
    
    context = {
        'categories': TourDestination._meta.get_field('category').choices,
        'regions': TourDestination._meta.get_field('region').choices,
        'experience_types': TourDestination._meta.get_field('experience_type').choices,
    }
    
    return render(request, 'set_preferences.html', context)

def book_destination_view(request, pk):
    """View to show booking form for a specific destination"""
    try:
        destination = TourDestination.objects.get(pk=pk, is_active=True)
    except TourDestination.DoesNotExist:
        return render(request, '404.html', {'message': 'Destination not found'})
    
    from datetime import date
    today = date.today().strftime('%Y-%m-%d')
    
    context = {
        'destination': destination,
        'today': today,
    }
    
    return render(request, 'book_destination.html', context)

def destination_overview(request, pk):
    """View for detailed destination overview"""
    try:
        destination = TourDestination.objects.get(pk=pk, is_active=True)
    except TourDestination.DoesNotExist:
        return render(request, '404.html', {'message': 'Destination not found'})
    
    # Get reviews for this destination
    reviews = destination.reviews.all()
    
    context = {
        'destination': destination,
        'reviews': reviews,
    }
    
    return render(request, 'destination_overview.html', context)

def all_destinations(request):
    """View to display all destinations"""
    destinations = TourDestination.objects.filter(is_active=True).order_by('name')
    
    # Filter by state if provided
    state_filter = request.GET.get('state')
    if state_filter:
        destinations = destinations.filter(state__icontains=state_filter)
    
    # Filter by category if provided
    category_filter = request.GET.get('category')
    if category_filter:
        destinations = destinations.filter(category=category_filter)
    
    # Get unique states and categories for filter dropdowns
    states = TourDestination.objects.filter(is_active=True).values_list('state', flat=True).distinct().order_by('state')
    categories = TourDestination.objects.filter(is_active=True).values_list('category', flat=True).distinct()
    
    context = {
        'destinations': destinations,
        'states': states,
        'categories': categories,
        'selected_state': state_filter,
        'selected_category': category_filter,
    }
    
    return render(request, 'all_destinations.html', context)
