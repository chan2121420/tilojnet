from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from core import views as core_views
from services import views as service_views
from projects import views as project_views
from contact import views as contact_views

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),
    
    # Core pages
    path('', core_views.home, name='home'),
    path('about/', core_views.about, name='about'),
    
    # Categories & Services
    path('categories/', service_views.categories_list, name='categories_list'),
    path('categories/search/', service_views.search_categories, name='search_categories'),
    path('categories/<slug:slug>/', service_views.category_detail, name='category_detail'),
    path('categories/<slug:category_slug>/<slug:item_slug>/', service_views.category_item_detail, name='category_item_detail'),
    
    # Projects/Portfolio
    path('projects/', project_views.projects_list, name='projects_list'),
    path('projects/<slug:slug>/', project_views.project_detail, name='project_detail'),

    # Contact
    path('contact/', contact_views.contact, name='contact'),
    path('quote/', contact_views.quote_request, name='quote_request'),
    path('newsletter/subscribe/', contact_views.newsletter_subscribe, name='newsletter_subscribe'),
    
    # CKEditor
    path('ckeditor/', include('ckeditor_uploader.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'

# Customize admin
admin.site.site_header = "Tilojnet Exclusive Admin"
admin.site.site_title = "Tilojnet Admin Portal"
admin.site.index_title = "Welcome to Tilojnet Exclusive Administration"