from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from home.views import home
from search import views as search_views

urlpatterns = i18n_patterns(
	path('', home, name=''),
	path('i18n/', include('django.conf.urls.i18n')),
	path('django-admin/', admin.site.urls),
	path('admin/', include(wagtailadmin_urls)),
	path('documents/', include(wagtaildocs_urls)),
	path('search/', search_views.search, name='search'),
	path('password-reset/complete/', 
		auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'), 
		name='password_reset_complete'),
	path(_('home/'), include(('home.urls', 'home'), namespace='home')),
	path(_('account/'), include(('account.urls', 'account'), namespace='account')),
	path(_('blog/'), include(('blog.urls', 'blog'), namespace='blog')),
	path(_('cart/'), include(('cart.urls', 'cart'), namespace='cart')),
	path(_('contact/'), include(('contact.urls', 'contact'), namespace='contact')),
	path(_('coupon/'), include(('coupon.urls', 'coupon'), namespace='coupon')),
	path(_('newsletter/'), include(('newsletter.urls', 'newsletter'), namespace='newsletter')),
	path(_('order/'), include(('order.urls', 'order'), namespace='order')),
	path(_('shop/'), include(('shop.urls', 'shop'), namespace='shop')),
	path(_('winwheel/'), include(('winwheel.urls', 'winwheel'), namespace='winwheel')),
	path('rosetta/', include('rosetta.urls')),
)



if settings.DEBUG:
	import debug_toolbar
	from django.conf.urls.static import static
	from django.contrib.staticfiles.urls import staticfiles_urlpatterns

	# Serve static and media files from development server
	urlpatterns += staticfiles_urlpatterns()
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
	urlpatterns += path('__debug__/', include(debug_toolbar.urls)),

urlpatterns = urlpatterns + i18n_patterns(
	# For anything not caught by a more specific rule above, hand over to
	# Wagtail's page serving mechanism. This should be the last pattern in
	# the list:
	path('', include(wagtail_urls)),

	# Alternatively, if you want Wagtail pages to be served from a subpath
	# of your site, rather than the site root:
	#    path("pages/", include(wagtail_urls)),
)
