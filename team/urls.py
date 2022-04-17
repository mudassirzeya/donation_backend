from django.urls import path
from .views import login_page, admin_page, home_page, logout_user, members_info_page, member_remark, mobile_user_page, admin_team_page, delete_member, send_member_data, edit_member_info, member_search_mobile, member_create_mobile, member_remark_mobile, member_donation_mobile, mobile_login, user_donation_report, money_overflow_page, all_donation

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home_page, name='home_page'),
    path('user_login/', login_page, name='user_login'),
    path('user_mobile_login/', mobile_login, name='user_mobile_login'),
    path('logout/', logout_user, name='logout'),
    path('admin_page/', admin_page, name='admin_page'),
    path('members/', members_info_page, name='members'),
    path('money_overflow/', money_overflow_page, name='money_overflow'),
    path('donations/', all_donation, name='donations'),
    path('send_member_data/', send_member_data, name='send_member_data'),
    path('edit_member_info/', edit_member_info, name='edit_member_info'),
    path('delete_member/', delete_member, name='delete_member'),
    path('members_remark/', member_remark, name='members_remark'),
    path('mobile_access_member/', mobile_user_page,
         name='mobile_access_member'),
    path('admin_team/', admin_team_page, name='admin_team'),
    path('search_member_mobile/', member_search_mobile,
         name='search_member_mobile'),
    path('member_create_mobile/', member_create_mobile,
         name='member_create_mobile'),
    path('member_remark_mobile/', member_remark_mobile,
         name='member_remark_mobile'),
    path('member_donation_mobile/', member_donation_mobile,
         name='member_donation_mobile'),
    path('user_donation_report/', user_donation_report,
         name='user_donation_report'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
