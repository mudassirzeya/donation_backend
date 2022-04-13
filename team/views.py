# from tkinter import image_names
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.core import serializers
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.core.paginator import Paginator, EmptyPage
from django.contrib import messages
from django.db.models import Q
# from sqlalchemy import JSON
from .models import Member_Donation, Member_Info, Remark_Member, UserProfile
from .serializers import DonationSerializer, MemberSerializer, RemarkSerializer
import json
# Create your views here.


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print("user", password, username)
        user = authenticate(request, username=username, password=password)
        print("us", user)
        if user is not None:
            login(request, user)
            staffProfile = UserProfile.objects.get(user=user)
            usertype = staffProfile.user_type
            if usertype == 'admin':
                return redirect('admin_page')
            elif usertype == 'app_user':
                return redirect('/')
        else:
            messages.info(request, 'Username or Password is incorrect')
    context = {}
    return render(request, 'login.html', context)


@api_view(['POST'])
@permission_classes([AllowAny])
def mobile_login(request):
    if request.method == 'POST':
        reqBody = request.data
        print('req', reqBody)
        phone = reqBody['phone']
        password = reqBody['password']
        # print('data', phone, password)
        account_user = authenticate(
            request, username=phone, password=password)
        # print("user", account_user)
        if account_user is not None:
            login(request, account_user)
            token = Token.objects.get_or_create(user=account_user)[0].key
            return Response({'token': token, 'msg': 'success'})
        else:
            return Response({'msg': 'failed'})
    else:
        return Response({'msg': 'failed'})


def logout_user(request):
    logout(request)
    return redirect('user_login')


@login_required(login_url='user_login')
def admin_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'app_user':
        return redirect('/')
    all_members = Member_Info.objects.all()
    total_members = all_members.count()
    mobile_users = UserProfile.objects.filter(user_type='app_user')
    total_mobile_users = mobile_users.count()
    all_remarks = Remark_Member.objects.all()
    total_remark = all_remarks.count()
    context = {'total_members': total_members,
               'total_mobile_users': total_mobile_users,
               'total_remark': total_remark}
    return render(request, "admin_home.html", context)


@login_required(login_url='user_login')
def home_page(request):
    context = {}
    return render(request, 'home_page.html', context)


@login_required(login_url='user_login')
def members_info_page(request):
    user = request.user
    staffProfile = UserProfile.objects.get(user=user)
    usertype = staffProfile.user_type
    if usertype == 'app_user':
        return redirect('/')
    if request.method == "POST":
        name = request.POST.get("name")
        father_name = request.POST.get("father_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        photo = request.POST.get("photo")
        address = request.POST.get("address")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        note = request.POST.get("note")

        Member_Info.objects.create(
            name=name,
            father_name=father_name,
            mobile_number=phone_number,
            email=email,
            profile_pic=photo,
            address=address,
            map_lat=lat,
            map_lon=lon,
            note=note
        )
        return redirect('members')
    if request.method == "GET":
        members = Member_Info.objects.all()
        # contact = Contact.objects.all()
        searched_text = request.GET.get("text")
        if searched_text:
            split_text = searched_text.split()
            for text in split_text:
                members = members.filter(
                    Q(name__contains=text) | Q(father_name__contains=text)
                    | Q(mobile_number__contains=text) | Q(email__contains=text)
                    | Q(address__contains=text)
                )
        # all_contact = Contact.objects.all()

        pages = Paginator(members, 100)
        page_num = request.GET.get('page', 1)
        try:
            page = pages.page(page_num)
        except EmptyPage:
            page = pages.page(1)
        context = {'members': page, 'text': searched_text}
        return render(request, 'members.html', context)
    context = {}
    return render(request, 'members.html', context)


def send_member_data(request):
    if request.method == "POST":
        data = json.loads(request.body)
        print("data", data)
        member_id = data["data_obj"][0]
        print("id", member_id['contact_id'])
        member = Member_Info.objects.filter(
            id=int(member_id['contact_id']))
        print('con', member)
        contact_json = serializers.serialize('json', member)
        print('contact', contact_json)
        return JsonResponse({"msg": "success", "data": contact_json})
    context = {}
    return render(request, "members.html", context)


def edit_member_info(request):
    if request.method == "POST":
        contact_id = request.POST.get('member_id')
        # print("contact", contact_id)
        name = request.POST.get("name")
        father_name = request.POST.get("father_name")
        phone_number = request.POST.get("phone_number")
        email = request.POST.get("email")
        photo = request.POST.get("photo")
        address = request.POST.get("address")
        lat = request.POST.get("lat")
        lon = request.POST.get("lon")
        note = request.POST.get("note")
        contact = Member_Info.objects.get(id=int(contact_id))

        # editing the field below
        contact.name = name
        contact.father_name = father_name
        contact.mobile_number = phone_number
        contact.email = email
        contact.profile_pic = photo
        contact.address = address
        contact.map_lat = lat
        contact.map_lon = lon
        contact.note = note
        contact.save()
        return redirect('members')
    context = {}
    return render(request, "members.html", context)


def delete_member(request):
    if request.method == "POST":
        contact_id = request.POST.get('delete_id')
        contact = Member_Info.objects.get(id=int(contact_id))
        contact.delete()
        print("del", contact)
        return redirect('members')
    context = {}
    return render(request, "members.html", context)


@login_required(login_url='user_login')
def member_remark(request):
    remarks = Remark_Member.objects.all()
    context = {'remarks': remarks}
    return render(request, 'member_remark.html', context)


@login_required(login_url='user_login')
def mobile_user_page(request):
    all_user = UserProfile.objects.filter(user_type='app_user')
    if request.method == "POST":
        username = request.POST.get("username")
        passcode = request.POST.get("passcode")
        name = request.POST.get("name")
        try:
            already_user = User.objects.get(username=username)
        except Exception:
            already_user = None
            print('user', already_user)
        if already_user is None:
            new_user = User.objects.create_user(
                username=username, password=passcode, first_name=name)
            Token.objects.get_or_create(user=new_user)[0].key
            UserProfile.objects.create(
                user=new_user,
                username=username,
                password=passcode,
                user_type='app_user',
            )
            return redirect('mobile_access_member')
        else:
            messages.info(
                request, 'This Username is already exist in our DataBase')
            return redirect('mobile_access_member')
    context = {'all_user': all_user}
    return render(request, 'mobile_users.html', context)


@login_required(login_url='user_login')
def admin_team_page(request):
    admin_user = UserProfile.objects.filter(user_type='admin')
    if request.method == "POST":
        username = request.POST.get("username")
        passcode = request.POST.get("passcode")
        name = request.POST.get("name")
        try:
            already_user = User.objects.get(username=username)
        except Exception:
            already_user = None
            print('user', already_user)
        if already_user is None:
            new_user = User.objects.create_user(
                username=username, password=passcode, first_name=name)
            Token.objects.get_or_create(user=new_user)[0].key
            UserProfile.objects.create(
                user=new_user,
                username=username,
                password=passcode,
                user_type='admin',
            )
            return redirect('admin_team')
        else:
            messages.info(
                request, 'This Username is already exist in our DataBase')
            return redirect('admin_team')
    context = {'admin_user': admin_user}
    return render(request, 'admin_team.html', context)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def member_search_mobile(request):
    if request.method == 'POST':
        data = request.data
        print("data", data['body'])
        recieved_text = data['body']
        split_text = recieved_text.split()
        # final_list = []
        contact = Member_Info.objects.all()
        for text in split_text:
            contact = contact.filter(
                Q(name__contains=text) | Q(father_name__contains=text)
                | Q(mobile_number__contains=text) | Q(email__contains=text)
                | Q(address__contains=text)
            )
        print("con", contact)
        first_200 = contact[:100]
        # print('first_200', first_200)
        serializer = MemberSerializer(first_200, many=True)
        if contact:
            return Response({'msg': 'yes', 'data': serializer.data})
        else:
            return Response({'msg': 'no'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def member_create_mobile(request):
    if request.method == 'POST':
        data = request.data
        print("data", data)
        name = data['name']
        father = data['father']
        phone = data['phone']
        email = data['email']
        lat = data['lat']
        lon = data['lon']
        note = data['note']
        try:
            photo = data['profile']
        except Exception:
            photo = ''

        print("data", photo)
        # print('image type', photo)
        new_member = Member_Info.objects.create(
            profile_pic=photo,
            name=name,
            father_name=father,
            mobile_number=phone,
            email=email,
            address='',
            map_lat=lat,
            map_lon=lon,
            note=note,
        )
        member_json = MemberSerializer(new_member)
        return Response({"msg": "success", "data": member_json.data})
    return Response({"msg": "failed"})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def member_remark_mobile(request):
    user = request.user
    if request.method == 'POST':
        data = request.data
        remark = data['body']
        userid = data['uid']
        member = Member_Info.objects.get(id=int(userid))
        Remark_Member.objects.create(
            remark_by=user,
            member=member,
            report_note=remark
        )
        print("data", data)
        return Response({"msg": "yes"})
    elif request.method == 'GET':
        user_id = request.GET.get("uid")
        print("user id", user_id)
        member = Member_Info.objects.get(id=int(user_id))
        member_remarks = Remark_Member.objects.filter(member=member)
        print('member', member)
        remarks_json = RemarkSerializer(member_remarks, many=True)
        if member_remarks:
            return Response({'msg': 'yes', 'data': remarks_json.data})
        else:
            return Response({'msg': 'no'})
        # return Response({"msg": "success", "data": remarks_json.data})
    return Response({"msg": "failed"})


@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def member_donation_mobile(request):
    user = request.user
    if request.method == 'POST':
        data = request.data
        money = data['money']
        userid = data['uid']
        date_time = data['date']
        note = data['body']
        member = Member_Info.objects.get(id=int(userid))
        Member_Donation.objects.create(
            received_by=user,
            member=member,
            amount=money,
            note=note,
            added_date=date_time
        )
        print("data", data)
        return Response({"msg": "yes"})
    elif request.method == 'GET':
        user_id = request.GET.get("uid")
        print("user id", user_id)
        member = Member_Info.objects.get(id=int(user_id))
        member_donations = Member_Donation.objects.filter(member=member)
        print('member', member)
        donation_json = DonationSerializer(member_donations, many=True)
        if member_donations:
            return Response({'msg': 'yes', 'data': donation_json.data})
        else:
            return Response({'msg': 'no'})
        # return Response({"msg": "success", "data": remarks_json.data})
    return Response({"msg": "failed"})
