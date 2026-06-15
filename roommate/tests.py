from django.test import TestCase
from roommate.models import RoomieUser, Listing, Interest, Message
from roommate.views import calculate_match_percentage, get_mock_distance
import datetime

class RoommateModelsTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user_seeker = RoomieUser.objects.create_user(
            username='test_seeker',
            phone='8888888888',
            phone_verified=True,
            age=22,
            gender='female',
            occupation='Student',
            languages=['English', 'Hindi'],
            seeker_profile={
                'food_preference': 'veg',
                'share_kitchen_non_veg': False,
                'smoking_ok': False,
                'drinking_ok': False,
                'partner_stays_over': 'no',
                'guests_policy': 'restricted',
                'noise_tolerance': 2,
                'cleanliness': 4,
                'cook_maid': 'any',
                'pets_ok': False,
                'parking_needed': False
            }
        )
        
        self.user_lister = RoomieUser.objects.create_user(
            username='test_lister',
            phone='7777777777',
            phone_verified=True,
            age=26,
            gender='male',
            occupation='Professional',
            languages=['English']
        )
        
        # Create test listing
        self.listing = Listing.objects.create(
            owner=self.user_lister,
            type='private_room',
            area='Koramangala',
            rent=15000,
            deposit=45000,
            monthly_expense_estimate=2000,
            available_from=datetime.date(2026, 7, 1),
            household_profile={
                'food_policy': 'veg',
                'share_kitchen_non_veg': False,
                'tenant_type': 'working_professionals',
                'smoking_allowed': False,
                'drinking_allowed': False,
                'partner_stays_over': 'no',
                'guests_policy': 'restricted',
                'noise_level': 2,
                'cleanliness_level': 4,
                'languages': ['English'],
                'cook_maid': 'none',
                'pets_allowed': False,
                'parking_available': False
            }
        )

    def test_model_string_representations(self):
        self.assertEqual(str(self.user_seeker), 'test_seeker')
        self.assertEqual(str(self.listing), 'Private Room in Koramangala (₹15000/mo)')

    def test_distance_calculator(self):
        # Same area distance
        dist_same = get_mock_distance('Koramangala', 'Koramangala')
        self.assertEqual(dist_same, 1.2)
        
        # Adjacent area distance
        dist_adj = get_mock_distance('Koramangala', 'HSR Layout')
        self.assertEqual(dist_adj, 3.5)

        # Far area distance
        dist_far = get_mock_distance('Koramangala', 'Whitefield')
        self.assertEqual(dist_far, 14.2)

    def test_match_percentage_calculation(self):
        # Perfect Match Check
        score_perfect = calculate_match_percentage(
            self.user_seeker.seeker_profile, 
            self.listing.household_profile
        )
        # All lifestyle rules line up perfectly
        self.assertEqual(score_perfect, 100)

        # Conflict Match Check (Lister allows smoking, seeker hates smoking)
        bad_profile = self.listing.household_profile.copy()
        bad_profile['smoking_allowed'] = True
        bad_profile['cleanliness_level'] = 1 # Seeker wants min 4, flat is 1 (messy)
        
        score_bad = calculate_match_percentage(
            self.user_seeker.seeker_profile,
            bad_profile
        )
        self.assertTrue(score_bad < 100)
        self.assertTrue(score_bad > 0)

    def test_interest_and_chat_creation(self):
        # Create interest
        interest = Interest.objects.create(
            from_user=self.user_seeker,
            target_type='listing',
            target_id=self.listing.id,
            status='interested'
        )
        self.assertEqual(interest.status, 'interested')
        
        # Create message
        conv_id = f"{self.user_seeker.id}_{self.user_lister.id}"
        msg = Message.objects.create(
            conversation_id=conv_id,
            sender=self.user_seeker,
            body="Hi! I am interested in your room."
        )
        self.assertEqual(msg.conversation_id, conv_id)
        self.assertEqual(msg.body, "Hi! I am interested in your room.")
