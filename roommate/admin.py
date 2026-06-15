from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import RoomieUser, Listing, Interest, Message

class RoomieUserAdmin(UserAdmin):
    model = RoomieUser
    list_display = ['username', 'phone', 'email', 'phone_verified', 'email_verified', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('FindMyRoomie Fields', {'fields': ('phone', 'phone_verified', 'email_verified', 'age', 'gender', 'occupation', 'languages', 'roles', 'seeker_profile')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('FindMyRoomie Fields', {'fields': ('phone', 'phone_verified', 'email_verified', 'age', 'gender', 'occupation', 'languages', 'roles', 'seeker_profile')}),
    )

class ListingAdmin(admin.ModelAdmin):
    list_display = ['type', 'area', 'rent', 'deposit', 'owner', 'status', 'created_at']
    list_filter = ['type', 'area', 'status']
    search_fields = ['owner__username', 'owner__phone', 'area', 'house_rules']

class InterestAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'target_type', 'target_id', 'status', 'created_at']
    list_filter = ['target_type', 'status']
    search_fields = ['from_user__username', 'from_user__phone']

class MessageAdmin(admin.ModelAdmin):
    list_display = ['conversation_id', 'sender', 'body_preview', 'created_at']
    search_fields = ['conversation_id', 'sender__username', 'body']
    
    def body_preview(self, obj):
        return obj.body[:50] + '...' if len(obj.body) > 50 else obj.body
    body_preview.short_description = 'Body Preview'

admin.site.register(RoomieUser, RoomieUserAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Message, MessageAdmin)
