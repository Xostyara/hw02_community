from urllib import request
from django.views.generic.base import TemplateView
from django.shortcuts import render

# Create your views here.

# class JustStaticPage(TemplateView):
#     # template_name = 'app_name/just_page.html'
    
#     def AboutAuthorView(request):
#         template = 'about/author.html'

#         return render(request, template)

#     def AboutTechView(request):
#         template = 'about/tech.html'

#         return render(request, template)


class AboutAuthorView(TemplateView):
    template_name: str = 'about/author.html'

    def AboutAuthorView(request, template_name):
        
        return render(request, template_name)


class AboutTechView(TemplateView):
    template_name: str = 'about/tech.html'
    
    def AboutTechView(request, template_name):
        
        return render(request, template_name)