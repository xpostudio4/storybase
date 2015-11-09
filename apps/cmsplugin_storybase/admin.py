from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from cms.extensions import TitleExtensionAdmin
from cms.models import Page
from storybase.admin import (StorybaseModelAdmin, StorybaseStackedInline,
        obj_title)
from cmsplugin_storybase.forms import (ActivityTranslationAdminForm, 
    NewsItemTranslationAdminForm)
from cmsplugin_storybase.models import (Activity, ActivityTranslation,
    NewsItem, NewsItemTranslation, TeaserExtension)
    

class ActivityTranslationInline(StorybaseStackedInline):
    model = ActivityTranslation
    form = ActivityTranslationAdminForm
    extra = 1


class ActivityAdmin(StorybaseModelAdmin):
    list_display = (obj_title,)
    search_fields = ['activitytranslation__title',]
    inlines = [ActivityTranslationInline,]
    prefix_inline_classes = ['ActivityTranslationInline',]


class NewsItemTranslationInline(StorybaseStackedInline):
    """Inline for translated fields of a NewsItem"""
    model = NewsItemTranslation
    form = NewsItemTranslationAdminForm 
    extra = 1


class NewsItemAdmin(StorybaseModelAdmin):
    list_display = (obj_title, 'author', 'last_edited', 'status',
            'on_homepage')
    list_filter = ('status', 'author', 'on_homepage')
    search_fields = ['name']
    readonly_fields = ['created', 'last_edited']
    inlines = [NewsItemTranslationInline,]
    prefix_inline_classes = ['NewsItemTranslationInline']

    def save_model(self, request, obj, form, change):
        """Perform pre-save operations and save the News Item 

        Sets the author field to the current user if it wasn't already set

        """
        if obj.author is None:
            obj.author = request.user
        obj.save()


admin.site.register(Activity, ActivityAdmin)
admin.site.register(NewsItem, NewsItemAdmin)
admin.site.register(TeaserExtension, TitleExtensionAdmin)
