from django.contrib import admin

from .models import Category, Book, Author, Activity
from .forms import ActivityAdminForm

LIST_PER_PAGE = 20

class ActivityAdmin(admin.ModelAdmin):
  form = ActivityAdminForm

  list_per_page = LIST_PER_PAGE
  list_display = ('user', 'target_object', 'status_text', 'created_at', 'updated_at')
  list_filter = ('user', 'status', 'created_at', 'updated_at')

  fieldsets = (
      (None, {
        'fields': ('status',)
      }),
    )

  def get_search_results(self, request, queryset, search_term):
    queryset, use_distinct = super().get_search_results(request, queryset, search_term)
    queryset = queryset.filter(action_type=Activity.BUY)
    return queryset, use_distinct

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Book)
admin.site.register(Activity, ActivityAdmin)
