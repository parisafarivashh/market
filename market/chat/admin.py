from django.contrib import admin

# Register your models here.
from chat.models import Direct, Message, ChatMember


@admin.register(Direct)
class DirectAdmin(admin.ModelAdmin):
    list_display = ['title', 'creator', 'receiver', 'date_create']
    list_filter = ['title', 'creator', 'receiver', 'date_create']
    search_fields = ['title', 'creator', 'receiver']
    readonly_fields = ['title', 'creator', 'receiver', 'date_create']


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'direct_title']
    list_filter = ['date_create']
    search_fields = ['sender__username', 'receiver__username', 'text']
    readonly_fields = ['sender', 'receiver', 'direct', 'date_create']

    def direct_title(self, obj):
        return obj.direct.title


@admin.register(ChatMember)
class ChatMemberAdmin(admin.ModelAdmin):
    list_display = ['member', 'member_name', 'direct_title']
    list_filter = ['id']
    search_fields = ['member__username', 'direct__title']
    readonly_fields = ['member', 'direct']

    def direct_title(self, obj):
        return obj.direct.title

    def member_name(self, obj):
        return obj.member.username

