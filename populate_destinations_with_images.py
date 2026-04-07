#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from qrscan.models import TourDestination, DestinationReview
from django.contrib.auth.models import User

def populate_destinations():
    """Populate the database with sample Indian destinations with real images"""
    
    destinations_data = [
        {
            'name': 'Taj Mahal',
            'city': 'Agra',
            'state': 'Uttar Pradesh',
            'region': 'north',
            'description': 'An ivory-white marble mausoleum on the banks of river Yamuna, built by Mughal emperor Shah Jahan in memory of his wife Mumtaz Mahal.',
            'historical_significance': 'Built between 1631-1648, the Taj Mahal is considered the finest example of Mughal architecture, combining Indian, Persian, and Islamic influences.',
            'best_time_to_visit': 'October to March',
            'entry_fee': 50.00,
            'opening_hours': '6:00 AM - 6:30 PM (Closed on Fridays)',
            'category': 'historical',
            'architectural_style': 'Indo-Islamic Architecture',
            'unesco_heritage': True,
            'experience_type': 'heritage',
            'accessibility': 'easy',
            'duration_recommended': '2-3 hours',
            'crowd_level': 'high',
            'latitude': 27.1751,
            'longitude': 78.0421,
            'image_url': 'https://images.unsplash.com/photo-1564507592333-c60657eea523?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'virtual_tour_url': 'https://taj.tajmahal.gov.in/virtual-tour/',
            'average_rating': 4.8,
            'total_reviews': 15420,
        },
        {
            'name': 'Red Fort',
            'city': 'Delhi',
            'state': 'Delhi',
            'region': 'north',
            'description': 'A historic fortified palace that served as the main residence of the Mughal emperors for nearly 200 years.',
            'historical_significance': 'Built in 1648, it was the political and ceremonial center of Mughal rule. It\'s where India\'s independence was declared in 1947.',
            'best_time_to_visit': 'October to March',
            'entry_fee': 35.00,
            'opening_hours': '9:30 AM - 4:30 PM (Closed on Mondays)',
            'category': 'historical',
            'architectural_style': 'Mughal Architecture',
            'unesco_heritage': True,
            'experience_type': 'heritage',
            'accessibility': 'easy',
            'duration_recommended': '2-3 hours',
            'crowd_level': 'high',
            'latitude': 28.6562,
            'longitude': 77.2410,
            'image_url': 'https://images.unsplash.com/photo-1587474260584-136574528ed5?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.3,
            'total_reviews': 8930,
        },
        {
            'name': 'Hawa Mahal',
            'city': 'Jaipur',
            'state': 'Rajasthan',
            'region': 'north',
            'description': 'The Palace of Winds, a stunning pink sandstone palace with intricate lattice work and 953 small windows.',
            'historical_significance': 'Built in 1799 by Maharaja Sawai Pratap Singh, designed to allow royal ladies to observe street festivals while remaining unseen.',
            'best_time_to_visit': 'October to March',
            'entry_fee': 50.00,
            'opening_hours': '9:00 AM - 4:30 PM',
            'category': 'palace',
            'architectural_style': 'Rajputana Architecture',
            'unesco_heritage': False,
            'experience_type': 'heritage',
            'accessibility': 'easy',
            'duration_recommended': '1-2 hours',
            'crowd_level': 'high',
            'latitude': 26.9239,
            'longitude': 75.8267,
            'image_url': 'https://images.unsplash.com/photo-1599661046827-dacde6976549?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.5,
            'total_reviews': 6750,
        },
        {
            'name': 'Gateway of India',
            'city': 'Mumbai',
            'state': 'Maharashtra', 
            'region': 'west',
            'description': 'An arch-monument built to commemorate the landing of King George V and Queen Mary at Apollo Bunder in 1911.',
            'historical_significance': 'Built in 1924, it served as the ceremonial entrance to India for Viceroys and new Governors. The last British troops departed from here in 1948.',
            'best_time_to_visit': 'November to February',
            'entry_fee': 0.00,
            'opening_hours': '24 hours (illuminated until midnight)',
            'category': 'historical',
            'architectural_style': 'Indo-Saracenic Architecture',
            'unesco_heritage': False,
            'experience_type': 'heritage',
            'accessibility': 'easy',
            'duration_recommended': '1 hour',
            'crowd_level': 'high',
            'latitude': 18.9220,
            'longitude': 72.8347,
            'image_url': 'https://images.unsplash.com/photo-1570168007204-dfb528c6958f?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.2,
            'total_reviews': 12340,
        },
        {
            'name': 'Mysore Palace',
            'city': 'Mysore',
            'state': 'Karnataka',
            'region': 'south',
            'description': 'A magnificent royal palace known for its grandeur and architectural beauty, former seat of the Wodeyar dynasty.',
            'historical_significance': 'Built in 1912, it\'s one of the largest palaces in India and showcases Indo-Saracenic architecture with intricate carvings and paintings.',
            'best_time_to_visit': 'October to March',
            'entry_fee': 70.00,
            'opening_hours': '10:00 AM - 5:30 PM',
            'category': 'palace',
            'architectural_style': 'Indo-Saracenic Architecture',
            'unesco_heritage': False,
            'experience_type': 'heritage',
            'accessibility': 'easy',
            'duration_recommended': '2-3 hours',
            'crowd_level': 'moderate',
            'latitude': 12.3051,
            'longitude': 76.6551,
            'image_url': 'https://images.unsplash.com/photo-1582510003544-4d00b7f74220?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.6,
            'total_reviews': 5680,
        },
        {
            'name': 'Hampi',
            'city': 'Hampi',
            'state': 'Karnataka',
            'region': 'south',
            'description': 'Ruins of the ancient city of Vijayanagara, featuring magnificent temples, palaces, and monuments spread across a rocky landscape.',
            'historical_significance': 'Capital of the Vijayanagara Empire (14th-16th century), it was one of the richest cities of its time with over 500,000 inhabitants.',
            'best_time_to_visit': 'October to February',
            'entry_fee': 40.00,
            'opening_hours': '6:00 AM - 6:00 PM',
            'category': 'historical',
            'architectural_style': 'Vijayanagara Architecture',
            'unesco_heritage': True,
            'experience_type': 'heritage',
            'accessibility': 'moderate',
            'duration_recommended': 'Full day',
            'crowd_level': 'moderate',
            'latitude': 15.3350,
            'longitude': 76.4600,
            'image_url': 'https://images.unsplash.com/photo-1582650625119-3a31f8fa2699?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.7,
            'total_reviews': 4320,
        },
        # Additional destinations for variety
        {
            'name': 'Goa Beaches',
            'city': 'Panaji',
            'state': 'Goa',
            'region': 'west',
            'description': 'Pristine beaches with golden sand, swaying palm trees, and vibrant beach culture offering the perfect tropical getaway.',
            'historical_significance': 'Former Portuguese colony with unique Indo-Portuguese culture reflected in architecture, cuisine, and traditions.',
            'best_time_to_visit': 'November to February',
            'entry_fee': 0.00,
            'opening_hours': '24 hours',
            'category': 'beach',
            'architectural_style': 'Portuguese Colonial',
            'unesco_heritage': False,
            'experience_type': 'relaxation',
            'accessibility': 'easy',
            'duration_recommended': '2-3 days',
            'crowd_level': 'high',
            'latitude': 15.2993,
            'longitude': 74.1240,
            'image_url': 'https://images.unsplash.com/photo-1512343879784-a960bf40e7f2?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.4,
            'total_reviews': 18750,
        },
        {
            'name': 'Varanasi Ghats',
            'city': 'Varanasi',
            'state': 'Uttar Pradesh',
            'region': 'north',
            'description': 'One of the oldest continuously inhabited cities in the world, famous for its sacred ghats along the Ganges River.',
            'historical_significance': 'Known as Kashi, it has been a center of learning and spirituality for over 3000 years, attracting pilgrims and scholars.',
            'best_time_to_visit': 'October to March',
            'entry_fee': 0.00,
            'opening_hours': '24 hours (best viewed at sunrise/sunset)',
            'category': 'religious',
            'architectural_style': 'Ancient Indian',
            'unesco_heritage': False,
            'experience_type': 'spiritual',
            'accessibility': 'moderate',
            'duration_recommended': '2-3 days',
            'crowd_level': 'high',
            'latitude': 25.3176,
            'longitude': 82.9739,
            'image_url': 'https://images.unsplash.com/photo-1561361513-2d000a50f0dc?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.3,
            'total_reviews': 9840,
        },
        {
            'name': 'Kerala Backwaters',
            'city': 'Alleppey',
            'state': 'Kerala',
            'region': 'south',
            'description': 'A network of interconnected canals, rivers, lakes and inlets forming a labyrinthine waterway system.',
            'historical_significance': 'Traditional transportation and trade route system dating back centuries, showcasing Kerala\'s unique ecosystem and culture.',
            'best_time_to_visit': 'September to March',
            'entry_fee': 500.00,
            'opening_hours': 'Houseboat tours available 24/7',
            'category': 'natural',
            'architectural_style': 'Traditional Kerala',
            'unesco_heritage': False,
            'experience_type': 'nature',
            'accessibility': 'easy',
            'duration_recommended': '1-2 days',
            'crowd_level': 'moderate',
            'latitude': 9.4981,
            'longitude': 76.3388,
            'image_url': 'https://images.unsplash.com/photo-1602216056096-3b40cc0c9944?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.5,
            'total_reviews': 7890,
        },
        {
            'name': 'Ladakh Monasteries',
            'city': 'Leh',
            'state': 'Ladakh',
            'region': 'north',
            'description': 'Ancient Buddhist monasteries perched on mountain cliffs, offering spiritual insights and breathtaking Himalayan views.',
            'historical_significance': 'Centers of Tibetan Buddhism dating back to 11th century, preserving ancient manuscripts, art, and spiritual traditions.',
            'best_time_to_visit': 'May to September',
            'entry_fee': 30.00,
            'opening_hours': '6:00 AM - 6:00 PM',
            'category': 'religious',
            'architectural_style': 'Tibetan Buddhist',
            'unesco_heritage': False,
            'experience_type': 'spiritual',
            'accessibility': 'difficult',
            'duration_recommended': '3-4 days',
            'crowd_level': 'low',
            'latitude': 34.1526,
            'longitude': 77.5770,
            'image_url': 'https://images.unsplash.com/photo-1506905925346-21bda4d32df4?ixlib=rb-4.0.3&auto=format&fit=crop&w=1000&q=80',
            'average_rating': 4.8,
            'total_reviews': 3210,
        }
    ]
    
    # Create destinations
    created_count = 0
    for dest_data in destinations_data:
        destination, created = TourDestination.objects.get_or_create(
            name=dest_data['name'],
            city=dest_data['city'],
            state=dest_data['state'],
            defaults=dest_data
        )
        if created:
            created_count += 1
            print(f"Created: {destination.name}")
            
            # Add sample reviews for each destination
            add_sample_reviews(destination)
        else:
            print(f"Already exists: {destination.name}")
    
    print(f"\nPopulation complete! Created {created_count} new destinations.")
    print(f"Total destinations in database: {TourDestination.objects.count()}")

def add_sample_reviews(destination):
    """Add sample reviews for a destination"""
    sample_reviews = [
        {
            'reviewer_name': 'Rajesh Kumar',
            'rating': 5,
            'review_text': 'Absolutely breathtaking! A must-visit destination that exceeded all expectations. The architecture and history are mesmerizing.',
        },
        {
            'reviewer_name': 'Priya Sharma',
            'rating': 4,
            'review_text': 'Beautiful place with rich cultural heritage. Well maintained and informative guides available. Highly recommended!',
        },
        {
            'reviewer_name': 'David Johnson',
            'rating': 5,
            'review_text': 'Incredible experience! The beauty and craftsmanship are beyond words. Perfect for history enthusiasts and photographers.',
        },
        {
            'reviewer_name': 'Anita Patel',
            'rating': 4,
            'review_text': 'Wonderful destination with great historical significance. The best time to visit is early morning to avoid crowds.',
        }
    ]
    
    for review_data in sample_reviews[:2]:  # Add 2 reviews per destination
        DestinationReview.objects.create(
            destination=destination,
            **review_data
        )

if __name__ == '__main__':
    print("Populating destinations with images and comprehensive data...")
    populate_destinations()
