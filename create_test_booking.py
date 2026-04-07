#!/usr/bin/env python3
import os
import django
from datetime import date, datetime

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Backend.settings')
django.setup()

from qrscan.models import MonumentTickets

# Create a test booking
booking = MonumentTickets.objects.create(
    name="Test User",
    city="AGRA",
    monument="Taj Mahal",
    date=date.today(),
    email="test@example.com",
    phone="1234567890",
    count_adult=2,
    count_children=1,
    count_abroad=0,
    count_senior=1,
    price_adult=45,
    price_children=0,
    price_abroad=1050,
    price_senior=23,
    total_count=4,
    total_cost="113",
    paid=True,
    doc_type="Aadhar Card",
    personal_id_no="123456789012",
    cancelled=False
)

print(f"Test booking created with ID: {booking.id}")
print(f"Name: {booking.name}")
print(f"Monument: {booking.monument}")
print(f"Adults: {booking.count_adult}, Children: {booking.count_children}, Seniors: {booking.count_senior}")
print(f"Total Cost: {booking.total_cost}")
