from django.contrib import admin
from django.http import HttpRequest
from site_setup.models import MenuLink, SiteSetup


# @admin.register(MenuLink)
# class MenuLinkAdmin(admin.ModelAdmin):
#     class Meta:
#         verbose_name = 'Menu Link'
#         verbose_name_plural = 'Menu Links'

#     list_display = ('id', 'text', 'url_or_path',)
#     list_display_links = ('id', 'text', 'url_or_path',)
#     search_fields = ('id', 'text', 'url_or_path',)

class MenuLinkInline(admin.TabularInline):
    model = MenuLink
    extra = 1

@admin.register(SiteSetup)
class SiteSetupAdmin(admin.ModelAdmin):
    class Meta:
        verbose_name = 'Setup'
        verbose_name_plural = 'Setup'

    list_display = ('title', 'description',)
    inlines = (MenuLinkInline,)

    def has_add_permission(self, request):
        return not SiteSetup.objects.exists()
