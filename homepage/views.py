import random
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from quotes.models import Quote

class HomePage(ListView):
    def check_logged(self, request):
        if request.user.is_authenticated:
            current_user = request.user
            return True, current_user
        return False, None
    
    def get(self, request, *args, **kwargs):
        template_name = 'home/index.html'
        logged, current_user = self.check_logged(request)
        quotes = Quote.objects.all()
        quote = random.choice(quotes)
        obj = {
            'current_user': current_user,
            'logged': logged,
            'quote': quote
        }
        return render(request, template_name, obj)
