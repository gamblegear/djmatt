from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin

from django.conf import settings
from django.conf.urls.static import static

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mine.views.home_view', name='home'),
    url(r'^sign_up/$', 'mine.views.sign_up_view', name='sign_up'),
    url(r'^login/$', 'mine.views.login_view', name='login'),
    url(r'^login_user/$', 'mine.views.login_user', name='login'),
    url(r'^logout_user/$', 'mine.views.logout_user', name='logout'),
    

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^mine_field/(?P<panel_id>\d+)/$', 'mine.views.mine_field_view'),
    url(r'^mine_field/(?P<panel_id>\d+)/(?P<from_panel_id>\d+)/$', 'mine.views.mine_field_view'),
    url(r'^session_one/$', 'mine.views.session_one_view'),
    url(r'^begin_session_two/$','mine.views.begin_session_two'),
    url(r'^session_two/$', 'mine.views.session_two_view'),
    url(r'^thanks/$', 'mine.views.thank_you_view'),
    url(r'^mine_admin/$', 'mine.views.mine_admin_view'),
    url(r'^mine_survey/$','mine.views.mine_survey_view'),
    url(r'^mine_instruct/$','mine.views.mine_instruction_view'),
    url(r'^select_mine_field/$', 'mine.views.select_mine_field_view'),
    url(r'^wait_room','mine.views.wait_room'),
    url(r'^switch/(?P<panel_id>\d+)/$', 'mine.views.switch_view'),
    url(r'^switched/$', 'mine.views.switched_view'),
    

    
    
    
    
    
    ##################################################
    url(r'^add_update_game_interact/$', 'mine.interact.add_update_game_interact'),
    url(r'^delete_game_interact/(?P<game_id>.+)/$', 'mine.interact.delete_game_interact'),
    url(r'^active_game_interact/(?P<game_id>.+)/$', 'mine.interact.active_game_interact'),
    url(r'^click_mine_interact/$', 'mine.interact.click_mine_interact'),
    url(r'^create_user_interact/$', 'mine.interact.create_user_interact'),
    
    url(r'^download_log_interact/(?P<game_id>.+)/$', 'mine.interact.download_log_interact'),
    
    
    ###################################################
    (r'^online/', include('online_status.urls')), 

    
)

if settings.DEBUG :
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
