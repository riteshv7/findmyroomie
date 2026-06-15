import os
from django.core.management.base import BaseCommand
from roommate.models import RoomieUser, Listing
from django.utils import timezone
import datetime

class Command(BaseCommand):
    help = 'Seeds the database with users and Bangalore roommate listings'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding database...')

        # 1. Create Superuser if not exists
        if not RoomieUser.objects.filter(username='admin').exists():
            admin_user = RoomieUser.objects.create_superuser(
                username='admin',
                email='admin@findmyroomie.in',
                password='password123',
                phone='9999999999',
                phone_verified=True,
                email_verified=True,
                age=28,
                gender='male',
                occupation='Administrator',
                languages=['English', 'Hindi', 'Kannada'],
                roles=['seeker', 'lister'],
                seeker_profile={
                    "food_preference": "any",
                    "share_kitchen_non_veg": True,
                    "preferred_types": ["working_professionals", "bachelors"],
                    "smoking_ok": True,
                    "drinking_ok": True,
                    "partner_stays_over": "restricted",
                    "guests_policy": "restricted",
                    "noise_tolerance": 3,
                    "cleanliness": 3,
                    "languages": ["English", "Hindi"],
                    "cook_maid": "any",
                    "pets_ok": True,
                    "parking_needed": True,
                    "rent_min": 5000,
                    "rent_max": 30000,
                    "deposit_max": 100000,
                    "setup_cost_max": 20000,
                    "monthly_expense_max": 10000,
                    "preferred_areas": ["Koramangala", "HSR Layout"],
                    "distance_max_km": 5,
                }
            )
            self.stdout.write(self.style.SUCCESS('Superuser "admin" (password123) created successfully!'))
        else:
            self.stdout.write('Superuser already exists.')

        # 2. Create Seed Users (Listers)
        users_data = [
            {
                'username': 'aravind',
                'name': 'Aravind K.',
                'age': 26,
                'gender': 'male',
                'occupation': 'Software Engineer',
                'phone': '9876543210',
                'languages': ['English', 'Tamil', 'Kannada'],
            },
            {
                'username': 'priya',
                'name': 'Priya Sharma',
                'age': 24,
                'gender': 'female',
                'occupation': 'Product Designer',
                'phone': '8765432109',
                'languages': ['English', 'Hindi'],
            },
            {
                'username': 'karthik',
                'name': 'Karthik N.',
                'age': 28,
                'gender': 'male',
                'occupation': 'Data Analyst',
                'phone': '7654321098',
                'languages': ['English', 'Telugu', 'Kannada'],
            },
            {
                'username': 'sneha',
                'name': 'Sneha Patel',
                'age': 25,
                'gender': 'female',
                'occupation': 'Marketing Manager',
                'phone': '6543210987',
                'languages': ['English', 'Gujarati', 'Hindi'],
            }
        ]

        users = {}
        for ud in users_data:
            user, created = RoomieUser.objects.get_or_create(
                username=ud['username'],
                defaults={
                    'first_name': ud['name'].split()[0],
                    'last_name': ud['name'].split()[1] if len(ud['name'].split()) > 1 else '',
                    'email': f"{ud['username']}@example.com",
                    'phone': ud['phone'],
                    'phone_verified': True,
                    'age': ud['age'],
                    'gender': ud['gender'],
                    'occupation': ud['occupation'],
                    'languages': ud['languages'],
                    'roles': ['lister'],
                }
            )
            if created:
                user.set_password('password123')
                user.save()
                self.stdout.write(f"User {ud['username']} created.")
            users[ud['username']] = user

        # 3. Create Seed Listings (9 realistic Bangalore room listings)
        listings_data = [
            {
                'owner': 'aravind',
                'type': 'private_room',
                'area': 'Koramangala',
                'lat': 12.9352,
                'lng': 77.6246,
                'nearest_metro': 'Trinity Metro Station (3.2 km)',
                'rent': 18000,
                'deposit': 50000,
                'setup_cost': 5000,
                'monthly_expense_estimate': 3000,
                'available_from': datetime.date(2026, 7, 1),
                'status': 'available',
                'photos': ['/static/images/room1.png'],
                'house_rules': 'No loud noise after 11 PM. Clean up kitchen after cooking. Keep common areas neat.',
                'household_profile': {
                    'food_policy': 'non-veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'bachelors',
                    'smoking_allowed': True,
                    'drinking_allowed': True,
                    'partner_stays_over': 'restricted',
                    'guests_policy': 'restricted',
                    'noise_level': 3,
                    'cleanliness_level': 4,
                    'languages': ['English', 'Tamil'],
                    'cook_maid': 'present',
                    'pets_allowed': False,
                    'parking_available': False
                }
            },
            {
                'owner': 'priya',
                'type': '1bhk',
                'area': 'HSR Layout',
                'lat': 12.9121,
                'lng': 77.6446,
                'nearest_metro': 'Silk Board Bus Station (1.5 km)',
                'rent': 22000,
                'deposit': 60000,
                'setup_cost': 12000,
                'monthly_expense_estimate': 4000,
                'available_from': datetime.date(2026, 6, 20),
                'status': 'available',
                'photos': ['/static/images/room3.png'],
                'house_rules': 'Vegetarian cooking preferred. Partner stays over occasionally. Pet owners welcome!',
                'household_profile': {
                    'food_policy': 'veg',
                    'share_kitchen_non_veg': False,
                    'tenant_type': 'working_professionals',
                    'smoking_allowed': False,
                    'drinking_allowed': False,
                    'partner_stays_over': 'restricted',
                    'guests_policy': 'yes',
                    'noise_level': 1,
                    'cleanliness_level': 5,
                    'languages': ['English', 'Hindi'],
                    'cook_maid': 'none',
                    'pets_allowed': True,
                    'parking_available': True
                }
            },
            {
                'owner': 'karthik',
                'type': 'shared_room',
                'area': 'Indiranagar',
                'lat': 12.9719,
                'lng': 77.6412,
                'nearest_metro': 'Indiranagar Metro Station (0.5 km)',
                'rent': 12000,
                'deposit': 30000,
                'setup_cost': 3000,
                'monthly_expense_estimate': 2500,
                'available_from': datetime.date(2026, 7, 5),
                'status': 'available',
                'photos': ['/static/images/room2.png'],
                'house_rules': 'Weekend parties allowed. Guests allowed to stay over. Respect roommate workspace/privacy.',
                'household_profile': {
                    'food_policy': 'eggetarian',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'students',
                    'smoking_allowed': False,
                    'drinking_allowed': True,
                    'partner_stays_over': 'yes',
                    'guests_policy': 'yes',
                    'noise_level': 4,
                    'cleanliness_level': 3,
                    'languages': ['English', 'Kannada', 'Telugu'],
                    'cook_maid': 'wanted',
                    'pets_allowed': False,
                    'parking_available': True
                }
            },
            {
                'owner': 'sneha',
                'type': 'pg_bed',
                'area': 'BTM Layout',
                'lat': 12.9166,
                'lng': 77.6101,
                'nearest_metro': 'Rashtreeya Vidyalaya Road Metro (2.0 km)',
                'rent': 9000,
                'deposit': 15000,
                'setup_cost': 1000,
                'monthly_expense_estimate': 1500,
                'available_from': datetime.date(2026, 6, 18),
                'status': 'available',
                'photos': ['/static/images/room2.png'],
                'house_rules': 'Curfew time 10:30 PM. No outside guests allowed in the room. Quiet hours after 10 PM.',
                'household_profile': {
                    'food_policy': 'veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'students',
                    'smoking_allowed': False,
                    'drinking_allowed': False,
                    'partner_stays_over': 'no',
                    'guests_policy': 'no',
                    'noise_level': 2,
                    'cleanliness_level': 4,
                    'languages': ['English', 'Hindi'],
                    'cook_maid': 'present',
                    'pets_allowed': False,
                    'parking_available': False
                }
            },
            {
                'owner': 'aravind',
                'type': '1rk',
                'area': 'Bellandur',
                'lat': 12.9260,
                'lng': 77.6762,
                'nearest_metro': 'Whitefield Metro Station (8.0 km)',
                'rent': 15000,
                'deposit': 40000,
                'setup_cost': 4000,
                'monthly_expense_estimate': 3000,
                'available_from': datetime.date(2026, 7, 1),
                'status': 'available',
                'photos': ['/static/images/room1.png'],
                'house_rules': 'Ideal for young tech professionals. Safe and quiet environment. Gated community.',
                'household_profile': {
                    'food_policy': 'non-veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'working_professionals',
                    'smoking_allowed': False,
                    'drinking_allowed': True,
                    'partner_stays_over': 'yes',
                    'guests_policy': 'yes',
                    'noise_level': 3,
                    'cleanliness_level': 3,
                    'languages': ['English'],
                    'cook_maid': 'present',
                    'pets_allowed': True,
                    'parking_available': True
                }
            },
            {
                'owner': 'karthik',
                'type': 'private_room',
                'area': 'Marathahalli',
                'lat': 12.9562,
                'lng': 77.6974,
                'nearest_metro': 'Indiranagar Metro (6.0 km)',
                'rent': 14000,
                'deposit': 40000,
                'setup_cost': 2000,
                'monthly_expense_estimate': 2800,
                'available_from': datetime.date(2026, 7, 10),
                'status': 'available',
                'photos': ['/static/images/room1.png'],
                'house_rules': 'Smoking allowed in balcony. Maid visits daily. Maintenance is shared.',
                'household_profile': {
                    'food_policy': 'non-veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'working_professionals',
                    'smoking_allowed': True,
                    'drinking_allowed': True,
                    'partner_stays_over': 'restricted',
                    'guests_policy': 'yes',
                    'noise_level': 3,
                    'cleanliness_level': 3,
                    'languages': ['English', 'Telugu'],
                    'cook_maid': 'none',
                    'pets_allowed': False,
                    'parking_available': False
                }
            },
            {
                'owner': 'sneha',
                'type': '1bhk',
                'area': 'Whitefield',
                'lat': 12.9698,
                'lng': 77.7499,
                'nearest_metro': 'Whitefield Hope Farm Metro (0.8 km)',
                'rent': 25000,
                'deposit': 75000,
                'setup_cost': 15000,
                'monthly_expense_estimate': 5000,
                'available_from': datetime.date(2026, 7, 1),
                'status': 'available',
                'photos': ['/static/images/room3.png'],
                'house_rules': 'Premium high-rise society. 24/7 security, gym, pool access. Respect society guidelines.',
                'household_profile': {
                    'food_policy': 'veg',
                    'share_kitchen_non_veg': False,
                    'tenant_type': 'working_professionals',
                    'smoking_allowed': False,
                    'drinking_allowed': False,
                    'partner_stays_over': 'no',
                    'guests_policy': 'restricted',
                    'noise_level': 2,
                    'cleanliness_level': 5,
                    'languages': ['English', 'Hindi'],
                    'cook_maid': 'present',
                    'pets_allowed': False,
                    'parking_available': True
                }
            },
            {
                'owner': 'priya',
                'type': 'pg_bed',
                'area': 'Electronic City',
                'lat': 12.8452,
                'lng': 77.6602,
                'nearest_metro': 'Electronic City Metro (0.4 km)',
                'rent': 8000,
                'deposit': 20000,
                'setup_cost': 500,
                'monthly_expense_estimate': 1000,
                'available_from': datetime.date(2026, 6, 25),
                'status': 'available',
                'photos': ['/static/images/room2.png'],
                'house_rules': 'Strict cleanliness standards. Shared washing machine and kitchen.',
                'household_profile': {
                    'food_policy': 'non-veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'students',
                    'smoking_allowed': False,
                    'drinking_allowed': False,
                    'partner_stays_over': 'no',
                    'guests_policy': 'no',
                    'noise_level': 2,
                    'cleanliness_level': 4,
                    'languages': ['English', 'Kannada'],
                    'cook_maid': 'present',
                    'pets_allowed': False,
                    'parking_available': False
                }
            },
            {
                'owner': 'aravind',
                'type': 'shared_room',
                'area': 'Koramangala',
                'lat': 12.9352,
                'lng': 77.6246,
                'nearest_metro': 'Trinity Metro Station (3.5 km)',
                'rent': 11000,
                'deposit': 30000,
                'setup_cost': 2500,
                'monthly_expense_estimate': 2000,
                'available_from': datetime.date(2026, 7, 1),
                'status': 'available',
                'photos': ['/static/images/room2.png'],
                'house_rules': 'Fun flatmates, regular movie nights. Common kitchen and hall. Maid comes daily.',
                'household_profile': {
                    'food_policy': 'non-veg',
                    'share_kitchen_non_veg': True,
                    'tenant_type': 'bachelors',
                    'smoking_allowed': True,
                    'drinking_allowed': True,
                    'partner_stays_over': 'yes',
                    'guests_policy': 'yes',
                    'noise_level': 4,
                    'cleanliness_level': 3,
                    'languages': ['English', 'Tamil'],
                    'cook_maid': 'wanted',
                    'pets_allowed': False,
                    'parking_available': True
                }
            }
        ]

        # Clear existing listings to avoid duplicates when running seed command multiple times
        Listing.objects.all().delete()

        for ld in listings_data:
            owner_user = users[ld['owner']]
            listing = Listing.objects.create(
                owner=owner_user,
                type=ld['type'],
                area=ld['area'],
                lat=ld['lat'],
                lng=ld['lng'],
                nearest_metro=ld['nearest_metro'],
                rent=ld['rent'],
                deposit=ld['deposit'],
                setup_cost=ld['setup_cost'],
                monthly_expense_estimate=ld['monthly_expense_estimate'],
                available_from=ld['available_from'],
                status=ld['status'],
                photos=ld['photos'],
                house_rules=ld['house_rules'],
                household_profile=ld['household_profile']
            )
            self.stdout.write(f"Seeded listing: {listing}")

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))
