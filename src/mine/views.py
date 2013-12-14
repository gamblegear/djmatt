# Create your views here.

from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from datetime import datetime, timedelta
import random
import string
import time
import utils
from models import Game, Group, Panel, UserProfile, Log, UserSurvey
from forms import SurveyForm, InstructionForm
import collections

import json

import gviz_api
import djmatt

from django.views.decorators.csrf import ensure_csrf_cookie

def sign_up_view(request):
    data_dict = {}
    return render(request, 'create_user.html', data_dict)

def login_view(request):
    data_dict = {}
    return render(request, 'login.html', data_dict)

def login_user(request):
    
    username = password = ''
    nextUrl = nextUrlDefault = reverse('mine.views.home_view')

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        nextUrl = request.POST.get('next')
        if not nextUrl or nextUrl=='':
            nextUrl = nextUrlDefault
        
        if user is not None:
            if user.is_active:
                login(request, user)
                fuuser = UserProfile.objects.filter(user = user)
                if not fuuser:
                    fuuser = UserProfile()
                    fuuser.user = user
                    fuuser.name = user.username
                    fuuser.random_code = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
                    fuuser.save()
                fuuser = UserProfile.objects.filter(user = user)[0]
                if fuuser.random_code == '':
                    fuuser.random_code = ''.join(random.choice('0123456789ABCDEF') for i in range(10))
                    fuuser.save()    
                return HttpResponseRedirect(nextUrl)
        
        
    return HttpResponse("Account Password Incrrect!")
    data_dict = {}
    return render(request, 'home.html', data_dict)

@login_required
def logout_user(request):
    logout(request)
    return redirect(djmatt.settings.LOGIN_URL)

@login_required
def home_view(request):
    data_dict = {}
    return render(request, 'home.html', data_dict)


@login_required
def mine_instruction_view(request):
    if request.method == 'GET':
        user = request.user
        data_dict = {}
        data_dict['survey'] = InstructionForm();
        panels = Panel.objects.filter(user = user)
        if len(panels) > 1:
            return HttpResponseRedirect("/thanks")
        if UserSurvey.objects.filter(user_profile = request.user.userprofile):#request.user.userprofile.usersurvey:
            return HttpResponseRedirect("/wait_room")

        return render(request, 'instructions.html', data_dict)
    else:
        f = InstructionForm(request.POST)
        if f.is_valid():
            if f['q1'].value() == 'False' and f['q2'].value() == '3' and f['q3'].value() == '3' and f['q4'].value() == 'True' and f['q5'].value() == 'True':
                return HttpResponseRedirect("/mine_survey")
        error_dict = {}
        error_dict['error'] = "Answers are incorrect!"
        error_dict['relocation'] = "/mine_instruct"
        return render(request, 'error.html', error_dict)

@login_required
def mine_survey_view(request):
    if request.method == 'GET':
        user = request.user
        data_dict = {}
        data_dict['survey'] = SurveyForm();
        panels = Panel.objects.filter(user = user)
        if len(panels) > 1:
            return HttpResponseRedirect("/thanks")
        if UserSurvey.objects.filter(user_profile = request.user.userprofile):#request.user.userprofile.usersurvey:
            return HttpResponseRedirect("/wait_room")

        return render(request, 'survey.html', data_dict)
    else:
        # if UserSurvey.objects.filter(user_profile = request.user.userprofile):#request.user.userprofile.usersurvey:
        #     return HttpResponseRedirect("/wait_room")# HttpResponse('Already there')
        profile = UserSurvey(user_profile = request.user.userprofile)
        f = SurveyForm(request.POST, instance = profile)
        if f.is_valid():
            f.save()
            return HttpResponseRedirect("/wait_room")
        error_dict = {}
        error_dict['error'] = "Form invalid!"
        error_dict['relocation'] = "/mine_survey"
        return render(request, 'error.html', error_dict)


@login_required
def thank_you_view(request):
    user = request.user
    data_dict = {}
    data_dict['random_code'] = UserProfile.objects.filter(user = user)[0].random_code
    return render(request, 'thank_you.html', data_dict)

#when session one ends
@login_required
def session_one_view(request):
    user = request.user
    panel = Panel.objects.filter(user = user, session = 0)[0]
    group = panel.group
    #calculate the score for this session
    gp_panels = Panel.objects.filter(group = group, session = 0)
    minimum = 10000000
    for gp_p in gp_panels:
        minimum = min(minimum, gp_p.progress.count('1'))
    group.score_1 = minimum
    group.save()
    data_dict = {}
    data_dict['group_score'] = minimum
    return render(request, 'session_one.html', data_dict)

#when session_ii ends.

@login_required
def session_two_view(request):
    user = request.user
    panel = Panel.objects.filter(user = user, session = 1)[0]
    group = panel.group
    #calculate the score for this session
    gp_panels = Panel.objects.filter(group = group, session = 1)
    minimum = 10000000
    for gp_p in gp_panels:
        minimum = min(minimum, gp_p.progress.count('1'))
    if len(gp_panels) < 3:
        minimum = 1
    group.score_2 = minimum
    group.save()
    data_dict = {}
    data_dict['group_score'] = minimum
    return render(request, 'session_two.html', data_dict)

@login_required
def mine_field_view(request, panel_id, from_panel_id = None):
    user = request.user;
    userProfile = UserProfile.objects.get(user= user)
    
    data_dict = {}
    
    panel_id = int(panel_id)
    panel = Panel.objects.get(pk = panel_id)
    
    
    if from_panel_id:
        from_panel_id = int(from_panel_id)
        from_panel = Panel.objects.get(pk = from_panel_id)
        from_group_name = from_panel.group.name
        from_panel_name = from_panel.name
        data_dict['from_panel_id'] = from_panel_id
        data_dict['from_group_name'] = from_group_name
        data_dict['from_panel_name'] = from_panel_name
        data_dict['flag'] = 'switch_back'    #show the switch button
    
    
    group_name = panel.group.name
    panel_name = panel.name
    group_id = panel.group.id
    game = panel.game
    
    
    rows = game.rows
    columns = game.columns
    progress = panel.progress
    wait_time = game.wait_time
    data_dict['rows'] = rows
    data_dict['columns'] = columns
    data_dict['progress'] = progress
    data_dict['group_id'] = group_id
    data_dict['panel_id'] = panel_id
    
    data_dict['group_name'] = group_name
    data_dict['panel_name'] = panel_name
    data_dict['session_id'] = panel.session
    data_dict['wait_time'] = wait_time
    if not data_dict.has_key('flag'):
        data_dict['flag'] = 'switch'    #show the switch button

    
    datetime_format_ISO = '%Y-%m-%d %H:%M:%S'


    data_dict['server_time'] = int(round(time.time() * 1000))
    
    total_time = game.total_time
    warning_time = game.warning_time
    # nr_delta = 1
    # if len(Panel.objects.filter(user = user)) == 2:
    #     nr_delta = 2
    # if not userProfile.final_time:
    #     userProfile.final_time = datetime.now()+nr_delta*timedelta(minutes = total_time)
    #     userProfile.save()
    # userProfile.final_time = datetime.now()+timedelta(minutes = total_time)
    # userProfile.save()
    f_time = 0
    if panel.session == 1:
        if not userProfile.final_time:
            userProfile.final_time = datetime.now()+timedelta(minutes = total_time)
            userProfile.save()
        f_time = userProfile.final_time
    else:
        if not userProfile.final_time_two:
            userProfile.final_time_two = datetime.now()+timedelta(minutes = total_time)
            userProfile.save()
        f_time = userProfile.final_time_two
    warning_final_time =  f_time- timedelta(minutes = warning_time)
    
    final_time =f_time.strftime(datetime_format_ISO)
    warning_final_time = warning_final_time.strftime(datetime_format_ISO)
    data_dict['final_time'] = final_time
    data_dict['warning_final_time'] = warning_final_time
    
        
    return render(request, 'mine_field.html', data_dict)

@login_required
def mine_admin_view(request):
    data_dict = {}
    game_list = Game.objects.all().order_by('-create_time')
    if game_list:
        data_dict['game_list'] = list(game_list)
    else:
        data_dict['game_list'] = []
    return render(request, 'mine_admin.html', data_dict)

@login_required
def begin_session_two(request):
    user = request.user

    user_panel = Panel.objects.filter(user = user)[0]
    group = user_panel.group
    length = len(Panel.objects.filter(group = group))
    new_panel = Panel.objects.create(game = group.game,
            group = group,
            name = str(length + 1),
            user = user,
            session = 1,
            progress ='0010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    
    )
    url = "/mine_field/" + str(new_panel.id)
    return HttpResponseRedirect(url);

@login_required
def wait_room(request):
    user = request.user
    if request.method == 'GET':
        data_dict = {}       
        return render(request, 'wait_page.html', data_dict)
    else:
        user_panel = Panel.objects.filter(user = user)
        if user_panel:
            lens = len(Panel.objects.filter(group = user_panel[0].group, session = 0))
            if lens < 3:
                return HttpResponse(0 - lens, content_type="text/plain")
            else:
                return HttpResponse(str(Panel.objects.filter(user = user)[0].id), content_type="text/plain")
        
        if len(Group.objects.all()) == 0:
            Group.objects.create(name = '1', game = Game.objects.latest('id'))
            
        last_group = Group.objects.latest('id')
        select_panels = Panel.objects.filter(group = last_group, session = 0)
        length = len(select_panels)
        if length < 3:
            new_panel = Panel.objects.create(game = last_group.game,
                group = last_group,
                name = str(length + 1),
                user = user,
                session = 0,
                progress ='0010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
)
        else:
            game_f = Game.objects.filter(is_activated = True)[0]		
            new_group = Group.objects.create(game = game_f,
             name = str(len(Group.objects.all()) + 1),
                )
            new_panel = Panel.objects.create(game = game_f,
                group = new_group,
                user = user,
                session = 0,
                name = str(length + 1), progress ='0010000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000'
    );

        panel = Panel.objects.filter(user = user, session = 0)[0]
        group = panel.group
        panels_size = len(Panel.objects.filter(group = group, session = 0))
        if panels_size < 3:
            return HttpResponse(0 - panels_size, content_type="text/plain")
        else:     
            return HttpResponse(str(Panel.objects.filter(user = user, session = 0)[0].id), content_type="text/plain")
        


@login_required
def select_mine_field_view(request):
    data_dict = {}
    game = Game.objects.filter(is_activated = True)
    if game :
        game = game[0]
    else:
        return HttpResponse("ERROR: No activated game !")
    
#     groups_num = game.groups_num
#     panels_per_group = game.panels_per_group
    groups = Group.objects.filter(game = game)
    group_panels_dict = dict()
    for group in groups:
        panels = Panel.objects.filter(game = game, group = group)
#         panels_list = list()
        panel_id_name_dict = {}
        for panel in panels:
            panel_id_name_dict[panel.id] = panel.name
#             panels_list.append(panel.id)
#         group_panels_dict[group.id] = panels_list
        group_panels_dict[group.id] = {'group_name': group.name, 'panels': panel_id_name_dict}

    group_panels_json = json.dumps(group_panels_dict)
    data_dict['group_panels_json'] = group_panels_json
    #return HttpResponse(group_panels_json)
    return render(request, 'select_mine_field.html', data_dict)

@login_required
def switch_view(request, panel_id):
    data_dict = {}
    user = request.user;
    userProfile = UserProfile.objects.get(user= user)
    panel_id = int(panel_id)
    panel = Panel.objects.get(pk = panel_id)
    session_id = panel.session
    group_id = panel.group.id
    
    
    group_name = panel.group.name
    panel_name = panel.name
    
    game = panel.game
    count = 0
    for tmp in panel.progress:
        if tmp == '1':
            count += 1
    cost = utils.cost(game.switch_cost)
    if count < cost:
        #cannot switch
        log = Log()
        log.game = game
        log.group = panel.group
        log.panel = panel
        log.user_profile = userProfile
        log.action = '\"Switch failed, Not enough credit\"'
        log.action_time = datetime.now()
        log.save()
        data_dict['panel_id'] = panel_id 
        nextUrl = reverse('mine.views.mine_field_view', args=(panel_id,))
        return HttpResponseRedirect(nextUrl)
    else:
        log = Log()
        log.game = game
        log.group = panel.group
        log.panel = panel
        log.user_profile = userProfile
        log.action = '\"Go to Switch page, cost %s\"' % cost
        log.action_time = datetime.now()
        log.save()
        
    #cost
    index = 0
    for s in panel.progress:
        if cost == 0:
            break
        if s == '1':
            cost -= 1
        index += 1
        
    panel.progress = '0'*(index+1) + panel.progress[index+1:]
    panel.save()
    
    panels = Panel.objects.filter(group__id = group_id, session = session_id)
    panel_id_status_dict={}
    for panel in panels:
        progress = panel.progress
        count = 0
        for s in progress:
            if s == '1':
                count +=1
        
        panel_id_status_dict[panel.id] = {'current': count, 'total': len(progress), 'panel_name': panel.name}
    panel_id_status_json = json.dumps(panel_id_status_dict)
    data_dict['panel_id_status_json'] = panel_id_status_json
    data_dict['panel_id'] = panel_id
    
    data_dict['group_name'] = group_name
    data_dict['panel_name'] = panel_name
    
    return render(request, 'switch.html', data_dict)


@login_required
def switched_view(request):
    data_dict = {}
    panel_id = request.POST.get('panel_id')
    from_panel_id = request.POST.get('from_panel_id')
    
    from_group_name = request.POST.get('from_group_name')
    from_panel_name = request.POST.get('from_panel_name')
    
    group_name = request.POST.get('group_name')
    panel_name = request.POST.get('panel_name')
    
    panel_id = int(panel_id)
    panel = Panel.objects.get(pk = panel_id)
    group_id = panel.group.id
    game = panel.game
    rows = game.rows
    columns = game.columns
    progress = panel.progress
    wait_time = game.wait_time
    data_dict['rows'] = rows
    data_dict['columns'] = columns
    data_dict['progress'] = progress
    data_dict['group_id'] = group_id
    data_dict['panel_id'] = panel_id
    
    
    data_dict['group_name'] = group_name
    data_dict['panel_name'] = panel_name
    
    data_dict['wait_time'] = wait_time
    data_dict['flag'] = 'switch_back'    #show the switch button
    data_dict['from_panel_id'] = from_panel_id
    
    data_dict['from_group_name'] = from_group_name
    data_dict['from_panel_name'] = from_panel_name

    
    
    
    return render(request, 'mine_field.html', data_dict)
