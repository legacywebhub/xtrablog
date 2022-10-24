from django.contrib import admin
from .models import *

class PostAdmin(admin.ModelAdmin):
    exclude = ( 'author',)
    list_display = ('less_title', 'category', 'created_at', 'author')
    list_filter = ('created_at','modified_at','category')
    #radio_fields = {'category':admin.HORIZONTAL}
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.author = request.user
        obj.save()

    def less_title(self, obj):
        title = obj.title

        if len(obj.title) > 30:
            title = f'{obj.title[:30]}...'
        return title

class CommentAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('less_comment', 'user', 'less_post', 'date')
    list_filter = ('date',)
    list_per_page = 10 

    def less_comment(self, obj):
        return obj.comment[:20]

    def less_post(self, obj):
        return obj.post.title[:20]

class ReplyAdmin(admin.ModelAdmin):
    exclude = ()
    list_display = ('less_reply', 'user', 'less_comment', 'date')
    list_filter = ('date',)
    list_per_page = 10 

    def less_reply(self, obj):
        return obj.reply[:20]

    def less_comment(self, obj):
        return obj.comment.comment[:20]

class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'date_subscibed')
    list_filter = ('date_subscibed',)
    list_per_page = 30

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'date')
    list_filter = ('date',)
    list_per_page = 20

# Register your models here.
admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Reply,ReplyAdmin)
admin.site.register(PostCategory)
admin.site.register(XtraBlog)
admin.site.register(Message, MessageAdmin)
admin.site.register(Subscriber, SubscriberAdmin)
