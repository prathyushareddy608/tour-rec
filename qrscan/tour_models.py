from django.db import models
from django.contrib.auth.models import User

class TourDestination(models.Model):
    """Model for storing Indian tourist destinations"""
    
    # Basic Information
    name = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    region = models.CharField(max_length=50, choices=[
        ('north', 'North India'),
        ('south', 'South India'),
        ('east', 'East India'),
        ('west', 'West India'),
        ('northeast', 'Northeast India'),
        ('central', 'Central India'),
    ])
    
    # Description and Details
    description = models.TextField()
    historical_significance = models.TextField()
    best_time_to_visit = models.CharField(max_length=100)
    entry_fee = models.DecimalField(max_digits=8, decimal_places=2)
    opening_hours = models.CharField(max_length=100)
    
    # Attributes for recommendation
    category = models.CharField(max_length=50, choices=[
        ('historical', 'Historical Monument'),
        ('religious', 'Religious Site'),
        ('natural', 'Natural Wonder'),
        ('museum', 'Museum'),
        ('palace', 'Palace/Fort'),
        ('temple', 'Temple'),
        ('beach', 'Beach'),
        ('hill_station', 'Hill Station'),
        ('wildlife', 'Wildlife Sanctuary'),
        ('cultural', 'Cultural Site'),
    ])
    
    architectural_style = models.CharField(max_length=100, blank=True)
    unesco_heritage = models.BooleanField(default=False)
    
    # Experience attributes
    experience_type = models.CharField(max_length=50, choices=[
        ('adventure', 'Adventure'),
        ('cultural', 'Cultural'),
        ('spiritual', 'Spiritual'),
        ('nature', 'Nature'),
        ('heritage', 'Heritage'),
        ('photography', 'Photography'),
        ('relaxation', 'Relaxation'),
    ])
    
    # Practical information
    accessibility = models.CharField(max_length=50, choices=[
        ('easy', 'Easy Access'),
        ('moderate', 'Moderate Access'),
        ('difficult', 'Difficult Access'),
    ])
    
    duration_recommended = models.CharField(max_length=50)  # e.g., "2-3 hours", "Full day"
    crowd_level = models.CharField(max_length=20, choices=[
        ('low', 'Low'),
        ('moderate', 'Moderate'),
        ('high', 'High'),
    ])
    
    # Location coordinates
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
    # Media
    image_url = models.URLField(blank=True)
    virtual_tour_url = models.URLField(blank=True)
    
    # Ratings and reviews
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    total_reviews = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['category']),
            models.Index(fields=['state']),
            models.Index(fields=['region']),
            models.Index(fields=['unesco_heritage']),
        ]
    
    def __str__(self):
        return f"{self.name}, {self.city}, {self.state}"

class UserPreference(models.Model):
    """Model for storing user preferences for tour recommendations"""
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)  # For anonymous users
    
    # Preference attributes
    preferred_categories = models.JSONField(default=list)  # List of category preferences
    preferred_regions = models.JSONField(default=list)    # List of region preferences
    preferred_experience_types = models.JSONField(default=list)  # List of experience types
    
    budget_range = models.CharField(max_length=20, choices=[
        ('budget', 'Budget (₹0-500)'),
        ('moderate', 'Moderate (₹500-2000)'),
        ('premium', 'Premium (₹2000+)'),
    ], default='moderate')
    
    accessibility_preference = models.CharField(max_length=20, choices=[
        ('easy', 'Easy Access Only'),
        ('any', 'Any Accessibility'),
    ], default='any')
    
    crowd_preference = models.CharField(max_length=20, choices=[
        ('low', 'Avoid Crowds'),
        ('any', 'Any Crowd Level'),
    ], default='any')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Preferences for {self.user.username}"
        return f"Anonymous preferences (Session: {self.session_key})"

class UserRecommendation(models.Model):
    """Model for storing user-specific recommendations"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    destination = models.ForeignKey(TourDestination, on_delete=models.CASCADE)
    
    recommendation_score = models.DecimalField(max_digits=5, decimal_places=3)
    reason = models.TextField()  # Explanation for why this was recommended
    
    viewed = models.BooleanField(default=False)
    bookmarked = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-recommendation_score', '-created_at']
        unique_together = ['session_key', 'destination']
    
    def __str__(self):
        user_info = self.user.username if self.user else f"Session: {self.session_key}"
        return f"Recommendation for {user_info}: {self.destination.name}"

class DestinationReview(models.Model):
    """Model for user reviews of destinations"""
    
    destination = models.ForeignKey(TourDestination, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    reviewer_name = models.CharField(max_length=100)  # For anonymous reviews
    
    rating = models.IntegerField(choices=[(i, i) for i in range(1, 6)])  # 1-5 stars
    review_text = models.TextField()
    visit_date = models.DateField(null=True, blank=True)
    
    helpful_votes = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    is_verified = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Review by {self.reviewer_name} for {self.destination.name} - {self.rating} stars"
