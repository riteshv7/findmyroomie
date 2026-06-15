import random
import os
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.db.models import Q
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import RoomieUser, Listing, Interest, Message
from .forms import LoginForm, OTPForm, UserProfileForm, ListingForm, SeekerPreferenceForm
import datetime

def login_view(request):
    if request.user.is_authenticated:
        return redirect('search')
        
    otp_sent = request.session.get('otp_sent', False)
    phone = request.session.get('auth_phone', None)
    
    if request.method == 'POST':
        if not otp_sent:
            # Step 1: Phone submission
            form = LoginForm(request.POST)
            if form.is_valid():
                phone = form.cleaned_data['phone']
                request.session['auth_phone'] = phone
                # Generate mock OTP
                mock_otp = "123456" # Simple dev OTP
                request.session['mock_otp'] = mock_otp
                request.session['otp_sent'] = True
                
                messages.info(request, f"Simulated SMS sent to {phone}! Use OTP: {mock_otp}")
                return redirect('login')
        else:
            # Step 2: OTP verification
            form = OTPForm(request.POST)
            if form.is_valid():
                otp = form.cleaned_data['otp']
                mock_otp = request.session.get('mock_otp')
                phone = request.session.get('auth_phone')
                
                if otp == mock_otp:
                    # Clear session keys
                    request.session['otp_sent'] = False
                    request.session['mock_otp'] = None
                    request.session['auth_phone'] = None
                    
                    # Get or create user
                    username = f"phone_{phone}"
                    user, created = RoomieUser.objects.get_or_create(
                        phone=phone,
                        defaults={
                            'username': username,
                            'phone_verified': True,
                            'is_active': True
                        }
                    )
                    
                    # Force login
                    login(request, user)
                    
                    if created or not user.roles:
                        messages.success(request, "Welcome! Please choose your role to get started.")
                        return redirect('role_select')
                    else:
                        messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                        return redirect('search')
                else:
                    form.add_error('otp', 'Incorrect OTP code. Please try again.')
    else:
        if not otp_sent:
            form = LoginForm()
        else:
            form = OTPForm()
            
    return render(request, 'roommate/login.html', {
        'form': form,
        'otp_sent': otp_sent,
        'phone': phone
    })

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully.")
    return redirect('login')

@login_required
def role_select_view(request):
    if request.method == 'POST':
        selected_roles = request.POST.getlist('roles')
        if not selected_roles:
            messages.error(request, "Please select at least one role.")
            return redirect('role_select')
            
        request.user.roles = selected_roles
        request.user.save()
        
        if 'seeker' in selected_roles:
            return redirect('profile_setup')
        else:
            return redirect('create_listing')
            
    return render(request, 'roommate/role_select.html', {
        'roles': request.user.roles
    })

@login_required
def profile_setup_view(request):
    user = request.user
    
    # Prefill data helper
    initial_seeker = user.seeker_profile or {
        "food_preference": "any",
        "share_kitchen_non_veg": True,
        "preferred_types": ["bachelors", "working_professionals"],
        "smoking_ok": False,
        "drinking_ok": False,
        "partner_stays_over": "restricted",
        "guests_policy": "restricted",
        "noise_tolerance": "3",
        "cleanliness": "3",
        "languages": ["English"],
        "cook_maid": "any",
        "pets_ok": False,
        "parking_needed": False,
        "rent_min": 0,
        "rent_max": 40000,
        "deposit_max": 100000,
        "setup_cost_max": 20000,
        "monthly_expense_max": 5000,
        "preferred_areas": ["Koramangala"],
        "distance_max_km": 5
    }

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, instance=user)
        pref_form = SeekerPreferenceForm(request.POST)
        
        if user_form.is_valid() and pref_form.is_valid():
            # Save user details
            u = user_form.save(commit=False)
            u.languages = user_form.cleaned_data['languages']
            
            # Save preference profile
            seeker_data = {}
            for field in pref_form.fields:
                seeker_data[field] = pref_form.cleaned_data[field]
                
            u.seeker_profile = seeker_data
            if 'seeker' not in u.roles:
                u.roles.append('seeker')
            u.save()
            
            messages.success(request, "Your profile has been saved successfully!")
            return redirect('search')
    else:
        user_form = UserProfileForm(instance=user, initial={'languages': user.languages})
        pref_form = SeekerPreferenceForm(initial=initial_seeker)
        
    return render(request, 'roommate/profile_setup.html', {
        'user_form': user_form,
        'pref_form': pref_form
    })

@login_required
def create_listing_view(request):
    if request.method == 'POST':
        form = ListingForm(request.POST, request.FILES)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            
            # Handle actual image upload or fallback placeholder
            if request.FILES.get('image'):
                img_file = request.FILES['image']
                fs = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'photos'), base_url='/media/photos/')
                filename = fs.save(img_file.name, img_file)
                uploaded_file_url = fs.url(filename)
                listing.photos = [uploaded_file_url]
            else:
                listing.photos = [form.cleaned_data.get('photo_choice') or '/static/images/room1.png']
            
            # Group household profile fields
            listing.household_profile = {
                'food_policy': form.cleaned_data['food_policy'],
                'share_kitchen_non_veg': form.cleaned_data['share_kitchen_non_veg'],
                'tenant_type': form.cleaned_data['tenant_type'],
                'smoking_allowed': form.cleaned_data['smoking_allowed'],
                'drinking_allowed': form.cleaned_data['drinking_allowed'],
                'partner_stays_over': form.cleaned_data['partner_stays_over'],
                'guests_policy': form.cleaned_data['guests_policy'],
                'noise_level': int(form.cleaned_data['noise_level']),
                'cleanliness_level': int(form.cleaned_data['cleanliness_level']),
                'languages': form.cleaned_data['languages'],
                'cook_maid': form.cleaned_data['cook_maid'],
                'pets_allowed': form.cleaned_data['pets_allowed'],
                'parking_available': form.cleaned_data['parking_available']
            }
            
            # Set default mock coordinates based on selected area
            mock_coords = {
                'Koramangala': (12.9352, 77.6246),
                'HSR Layout': (12.9121, 77.6446),
                'Indiranagar': (12.9719, 77.6412),
                'BTM Layout': (12.9166, 77.6101),
                'Bellandur': (12.9260, 77.6762),
                'Marathahalli': (12.9562, 77.6974),
                'Whitefield': (12.9698, 77.7499),
                'Electronic City': (12.8452, 77.6602),
                'Other': (12.9716, 77.5946)
            }
            area = form.cleaned_data['area']
            listing.lat, listing.lng = mock_coords.get(area, (12.9716, 77.5946))
            
            listing.save()
            
            # Add role lister if not exists
            if 'lister' not in request.user.roles:
                request.user.roles.append('lister')
                request.user.save()
                
            messages.success(request, f"Listing created successfully in {listing.area}!")
            return redirect('search')
    else:
        form = ListingForm()
        
    return render(request, 'roommate/create_listing.html', {
        'form': form
    })

def get_mock_distance(area1, area2):
    if area1 == area2:
        return 1.2
    
    # Simple adjacency dictionary
    adjacent = {
        'Koramangala': ['HSR Layout', 'BTM Layout', 'Indiranagar', 'Bellandur'],
        'HSR Layout': ['Koramangala', 'BTM Layout', 'Bellandur'],
        'BTM Layout': ['Koramangala', 'HSR Layout'],
        'Indiranagar': ['Koramangala', 'Marathahalli'],
        'Bellandur': ['Koramangala', 'HSR Layout', 'Marathahalli'],
        'Marathahalli': ['Bellandur', 'Indiranagar', 'Whitefield'],
        'Whitefield': ['Marathahalli'],
        'Electronic City': ['HSR Layout']
    }
    
    if area2 in adjacent.get(area1, []):
        return 3.5
    elif any(middle in adjacent.get(area1, []) and area2 in adjacent.get(middle, []) for middle in adjacent.keys()):
        return 6.5
    else:
        return 14.2

def calculate_match_percentage(seeker_profile, household_profile):
    if not seeker_profile or not household_profile:
        return 70 # Fallback default match
        
    score = 0
    total_weights = 0
    
    # 1. Food (Weight: 2)
    total_weights += 2
    pref_food = seeker_profile.get('food_preference', 'any')
    house_food = household_profile.get('food_policy', 'veg')
    if pref_food == 'any' or pref_food == house_food:
        score += 2
    elif pref_food == 'eggetarian' and house_food == 'veg':
        score += 1.5
    elif seeker_profile.get('share_kitchen_non_veg', True) and house_food != 'veg':
        score += 1
        
    # 2. Smoking (Weight: 2)
    total_weights += 2
    if not household_profile.get('smoking_allowed', False) or seeker_profile.get('smoking_ok', False):
        score += 2
        
    # 3. Drinking (Weight: 1)
    total_weights += 1
    if not household_profile.get('drinking_allowed', False) or seeker_profile.get('drinking_ok', False):
        score += 1
        
    # 4. Cleanliness (Weight: 2)
    total_weights += 2
    min_clean = int(seeker_profile.get('cleanliness', 3))
    house_clean = int(household_profile.get('cleanliness_level', 3))
    if house_clean >= min_clean:
        score += 2
    elif house_clean == min_clean - 1:
        score += 1
        
    # 5. Noise (Weight: 2)
    total_weights += 2
    max_noise = int(seeker_profile.get('noise_tolerance', 3))
    house_noise = int(household_profile.get('noise_level', 3))
    if house_noise <= max_noise:
        score += 2
    elif house_noise == max_noise + 1:
        score += 1
        
    # 6. Cook/Maid (Weight: 1)
    total_weights += 1
    pref_cook = seeker_profile.get('cook_maid', 'any')
    house_cook = household_profile.get('cook_maid', 'none')
    if pref_cook == 'any' or pref_cook == house_cook:
        score += 1
        
    # 7. Pets (Weight: 1)
    total_weights += 1
    if not household_profile.get('pets_allowed', False) or seeker_profile.get('pets_ok', False):
        score += 1
        
    # 8. Parking (Weight: 1)
    total_weights += 1
    if not seeker_profile.get('parking_needed', False) or household_profile.get('parking_available', False):
        score += 1
        
    return int((score / total_weights) * 100)

@login_required
def search_view(request):
    listings = Listing.objects.filter(status='available').select_related('owner')
    
    # Extract query params
    area = request.GET.get('area')
    max_rent = request.GET.get('max_rent')
    food_policy = request.GET.get('food_policy')
    smoking_allowed = request.GET.get('smoking_allowed')
    drinking_allowed = request.GET.get('drinking_allowed')
    pets_allowed = request.GET.get('pets_allowed')
    parking_available = request.GET.get('parking_available')
    sort_by = request.GET.get('sort_by', 'newest')
    work_location = request.GET.get('work_location', '')

    # Apply standard DB filters
    if area and area != 'All':
        listings = listings.filter(area=area)
    if max_rent:
        try:
            listings = listings.filter(rent__lte=int(max_rent))
        except ValueError:
            pass
            
    # Apply JSON filters
    filtered_listings = []
    for l in listings:
        hp = l.household_profile
        
        if food_policy and food_policy != 'any':
            if hp.get('food_policy') != food_policy:
                continue
        if smoking_allowed == 'no':
            if hp.get('smoking_allowed', False):
                continue
        if drinking_allowed == 'no':
            if hp.get('drinking_allowed', False):
                continue
        if pets_allowed == 'yes':
            if not hp.get('pets_allowed', False):
                continue
        if parking_available == 'yes':
            if not hp.get('parking_available', False):
                continue
                
        # Calculate compatibility match %
        l.match_pct = calculate_match_percentage(request.user.seeker_profile, hp)
        
        # Calculate distance if work location is specified
        if work_location:
            l.distance = get_mock_distance(l.area, work_location)
        else:
            l.distance = None
            
        filtered_listings.append(l)
        
    # Apply Sorting
    if sort_by == 'lowest_rent':
        filtered_listings.sort(key=lambda x: x.rent)
    elif sort_by == 'nearest' and work_location:
        filtered_listings.sort(key=lambda x: x.distance if x.distance is not None else 999)
    else: # newest
        filtered_listings.sort(key=lambda x: x.created_at, reverse=True)
        
    # Areas for picker
    areas = ['All', 'Koramangala', 'HSR Layout', 'Indiranagar', 'BTM Layout', 'Bellandur', 'Marathahalli', 'Whitefield', 'Electronic City', 'Other']
    
    return render(request, 'roommate/search.html', {
        'listings': filtered_listings,
        'areas': areas,
        'selected_area': area or 'All',
        'max_rent': max_rent or '',
        'food_policy': food_policy or 'any',
        'smoking_allowed': smoking_allowed or 'any',
        'drinking_allowed': drinking_allowed or 'any',
        'pets_allowed': pets_allowed or 'any',
        'parking_available': parking_available or 'any',
        'sort_by': sort_by,
        'work_location': work_location
    })

@login_required
def listing_detail_view(request, pk):
    listing = get_object_or_404(Listing.objects.select_related('owner'), pk=pk)
    
    # Calculate match percentage
    match_pct = calculate_match_percentage(request.user.seeker_profile, listing.household_profile)
    
    # Check if user already marked interest
    interest_exists = Interest.objects.filter(
        from_user=request.user, 
        target_type='listing', 
        target_id=listing.id
    ).exists()
    
    # Get matching bullet points
    bullets = []
    sp = request.user.seeker_profile or {}
    hp = listing.household_profile
    
    if sp:
        # Food
        if sp.get('food_preference') == 'any' or sp.get('food_preference') == hp.get('food_policy'):
            bullets.append(("Food preferences match perfectly!", "success"))
        # Cleanliness
        if int(hp.get('cleanliness_level', 3)) >= int(sp.get('cleanliness', 3)):
            bullets.append((f"Cleanliness standards are met ({hp.get('cleanliness_level')}/5)", "success"))
        else:
            bullets.append((f"Cleanliness standards are slightly lower ({hp.get('cleanliness_level')}/5)", "warning"))
        # Noise
        if int(hp.get('noise_level', 3)) <= int(sp.get('noise_tolerance', 3)):
            bullets.append((f"Noise levels are acceptable ({hp.get('noise_level')}/5)", "success"))
        else:
            bullets.append((f"Household has higher noise levels ({hp.get('noise_level')}/5)", "warning"))
        # Pets
        if hp.get('pets_allowed') and sp.get('pets_ok'):
            bullets.append(("Pets are welcome!", "success"))
        elif hp.get('pets_allowed') and not sp.get('pets_ok'):
            bullets.append(("Pets are allowed here (you preferred no pets)", "info"))
        # Parking
        if hp.get('parking_available') and sp.get('parking_needed'):
            bullets.append(("Parking spot available for your vehicle!", "success"))
            
    return render(request, 'roommate/listing_detail.html', {
        'listing': listing,
        'match_pct': match_pct,
        'interest_exists': interest_exists,
        'bullets': bullets
    })

@login_required
@require_POST
def express_interest_view(request, pk):
    listing = get_object_or_404(Listing, pk=pk)
    
    # Prevent self-interest
    if listing.owner == request.user:
        messages.error(request, "You cannot express interest in your own listing.")
        return redirect('listing_detail', pk=pk)
        
    interest, created = Interest.objects.get_or_create(
        from_user=request.user,
        target_type='listing',
        target_id=listing.id,
        defaults={'status': 'interested'}
    )
    
    # Expressing interest automatically opens 1:1 chat thread
    conversation_id = f"{min(request.user.id, listing.owner.id)}_{max(request.user.id, listing.owner.id)}"
    
    # Send a mock initial message if conversation is fresh
    if not Message.objects.filter(conversation_id=conversation_id).exists():
        Message.objects.create(
            conversation_id=conversation_id,
            sender=request.user,
            body=f"Hi {listing.owner.first_name or listing.owner.username}! I am interested in your room listing: {listing.get_type_display()} in {listing.area}. Let's chat!"
        )
        
    if created:
        messages.success(request, f"Expressed interest! A chat has been opened with {listing.owner.first_name}.")
    else:
        messages.info(request, "Opening chat thread...")
        
    return redirect('chat_thread', conversation_id=conversation_id)

@login_required
def interests_view(request):
    # Rooms I am interested in (Outbound Interests)
    my_interests = Interest.objects.filter(from_user=request.user, target_type='listing')
    my_interests_list = []
    for mi in my_interests:
        listing = Listing.objects.filter(pk=mi.target_id).first()
        if listing:
            my_interests_list.append({
                'interest': mi,
                'listing': listing
            })
            
    # People interested in my rooms (Inbound Interests)
    my_listings_ids = Listing.objects.filter(owner=request.user).values_list('id', flat=True)
    inbound_interests = Interest.objects.filter(target_type='listing', target_id__in=my_listings_ids).select_related('from_user')
    inbound_list = []
    for ii in inbound_interests:
        listing = Listing.objects.filter(pk=ii.target_id).first()
        if listing:
            inbound_list.append({
                'interest': ii,
                'user': ii.from_user,
                'listing': listing
            })
            
    return render(request, 'roommate/interests.html', {
        'outbound': my_interests_list,
        'inbound': inbound_list
    })

@login_required
def chat_view(request, conversation_id=None):
    user = request.user
    
    # Fetch all messages involving the user to determine active chats
    # Conversation format is "id1_id2"
    all_msgs = Message.objects.filter(
        Q(conversation_id__startswith=f"{user.id}_") | Q(conversation_id__endswith=f"_{user.id}")
    ).order_by('created_at')
    
    # Build list of active conversations
    active_chats = {}
    for msg in all_msgs:
        cid = msg.conversation_id
        uids = cid.split('_')
        other_uid = int(uids[0]) if int(uids[1]) == user.id else int(uids[1])
        
        if cid not in active_chats:
            other_user = RoomieUser.objects.filter(pk=other_uid).first()
            if other_user:
                active_chats[cid] = {
                    'other_user': other_user,
                    'last_message': msg.body,
                    'last_time': msg.created_at,
                    'conversation_id': cid
                }
        else:
            active_chats[cid]['last_message'] = msg.body
            active_chats[cid]['last_time'] = msg.created_at
            
    # Sort active chats by latest message time
    chat_list = sorted(active_chats.values(), key=lambda x: x['last_time'], reverse=True)
    
    selected_chat = None
    messages_list = []
    
    if conversation_id:
        # Validate that the logged in user belongs to this conversation
        uids = conversation_id.split('_')
        if len(uids) == 2 and (int(uids[0]) == user.id or int(uids[1]) == user.id):
            other_uid = int(uids[0]) if int(uids[1]) == user.id else int(uids[1])
            other_user = get_object_or_404(RoomieUser, pk=other_uid)
            
            selected_chat = {
                'conversation_id': conversation_id,
                'other_user': other_user
            }
            
            # Fetch message history
            messages_list = Message.objects.filter(conversation_id=conversation_id).order_by('created_at')
            
            # Handle sending new messages
            if request.method == 'POST':
                body = request.POST.get('body', '').strip()
                if body:
                    new_msg = Message.objects.create(
                        conversation_id=conversation_id,
                        sender=user,
                        body=body
                    )
                    
                    # Generate a simulated, realistic response from the other user
                    responses = [
                        "Hey! Yes, that sounds great. When are you looking to visit the room?",
                        "Hi there! Yes, we have a few house visits scheduled this weekend. Would you like to join?",
                        "Yes, the room is still open. Tell me a bit about your work schedule and kitchen habits!",
                        "Hey, yes it is available. Are you fine with the rules around no loud noises after 11 PM?",
                        "Hello! The room is available. The flatmates are working professionals. Let me know if you would like to connect on call.",
                    ]
                    simulated_reply = random.choice(responses)
                    Message.objects.create(
                        conversation_id=conversation_id,
                        sender=other_user,
                        body=simulated_reply
                    )
                    
                    return redirect('chat_thread', conversation_id=conversation_id)
        else:
            messages.error(request, "Unauthorized to access this conversation.")
            return redirect('chat')
            
    return render(request, 'roommate/chat.html', {
        'chat_list': chat_list,
        'selected_chat': selected_chat,
        'messages': messages_list
    })

@login_required
def profile_view(request):
    # Renders the profile overview page
    return render(request, 'roommate/profile.html')

