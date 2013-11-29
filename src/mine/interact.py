'''
Created on Jun 30, 2013

@author: johnny
'''
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from models import Game, Group, Panel, Log
from datetime import datetime
from mine.models import UserProfile
from django.contrib.auth.models import User
from django.shortcuts import render
import utils
import json

@login_required
def add_update_game_interact(request):
    
    game_id = request.POST.get('game_id')
    name = request.POST.get('name')
    rows = request.POST.get('rows')
    columns = request.POST.get('columns')
    groups_num = request.POST.get('groups_num')
    panels_per_group = request.POST.get('panels_per_group')
    wait_time = request.POST.get('wait_time')
    total_time = request.POST.get('total_time')
    warning_time = request.POST.get('warning_time')
    switch_cost = request.POST.get('switch_cost')
    
    #parse to int
    try:
        rows = int(rows)
        columns = int(columns)
        groups_num = int(groups_num)
        panels_per_group = int(panels_per_group)
        wait_time = int(wait_time)
    except:
        return HttpResponse('Error')

    try:
        game = Game.objects.get(pk = game_id)
    except:
        game = Game()
        game.create_time = datetime.now()
    
    needInitGroupsPanels = True
    if game.rows and game.columns and game.groups_num \
            and game.panels_per_group \
            and game.rows * game.columns==rows*columns \
            and game.groups_num==groups_num and game.panels_per_group==panels_per_group:
        needInitGroupsPanels = False

    game.name = name
    game.rows = rows
    game.columns = columns
    game.groups_num = groups_num
    game.panels_per_group = panels_per_group
    game.wait_time = wait_time
    game.total_time = total_time
    game.warning_time = warning_time
    game.switch_cost = switch_cost
    
    game.save()


    #initial Groups and Panels
    if needInitGroupsPanels:
        Group.objects.filter(game = game).delete()
        for i in range(groups_num):
            group = Group()
            group.game = game
            group.name = "Group %d" % (i+1) 
            group.save()
            for j in range(panels_per_group):
                panel = Panel()
                panel.group = group
                panel.game = game
                panel.name = "Panel %d" % (j+1)
                panel.progress = '0' * rows * columns
                panel.save()



    nextUrl = reverse('mine.views.mine_admin_view')
    return HttpResponseRedirect(nextUrl)

@login_required
def delete_game_interact(request, game_id):
    try:
        game_id = int(game_id)
        game = Game.objects.get(pk = game_id)
        game.delete()
    except:
        pass
    
    nextUrl = reverse('mine.views.mine_admin_view')
    return HttpResponseRedirect(nextUrl)


def active_game_interact(request, game_id):
    
    try:
        Game.objects.all().update(is_activated = False)
        game_id = int(game_id)
        game = Game.objects.get(pk = game_id)
        game.is_activated = True
        game.save()
        
    except:
        pass
    
    nextUrl = reverse('mine.views.mine_admin_view')
    return HttpResponseRedirect(nextUrl)

@login_required
def click_mine_interact(request):
#     data_dict = {}
    user = request.user;
    userProfile = UserProfile.objects.get(user= user)
    
    mine_index = request.POST.get('mine_index')
    mine_index = int(mine_index)
    panel_id = request.POST.get('panel_id')
    panel_id = int(panel_id)
    panel = Panel.objects.get(pk = panel_id)
    progress = panel.progress

    progress = progress[0:mine_index] + '1' + progress[mine_index+1:]
    panel.progress = progress
    panel.save()


    rows = panel.game.columns
    
    log = Log()
    log.game = panel.game
    log.group = panel.group
    log.panel = panel
    log.action = '\"Click (%d, %d)\"' % (mine_index/rows, mine_index % rows)  
    log.action_time = datetime.now()
    log.user_profile = userProfile
    log.save()
    
    response_data={}
    game = panel.game
    response_data['rowses'] = game.rows
    response_data['columns'] = game.columns
    response_data['progress'] = panel.progress
    response_data['wait_time'] = game.wait_time

    return HttpResponse(json.dumps(response_data), mimetype="application/json")


@login_required
def download_log_interact(request,game_id):
    datetime_format_ISO = '%Y-%m-%d %H:%M:%S'
    game_id = int(game_id)
    
#     id = models.AutoField(primary_key = True)
#     game = models.ForeignKey(Game)
#     group = models.ForeignKey(Group)
#     panel = models.ForeignKey(Panel)
#     user_profile = models.ForeignKey(UserProfile)
#     action = models.CharField(max_length = 200)
#     action_time = models.DateTimeField(blank=True, null=True)
    logs = Log.objects.filter(game__id = game_id)
    header = ['id','user_id','user_name','random_code', 'group_id','group_score', 'panel_id','session_id','action', 'timestamp']
    all_list = []
    all_list.append(','.join(header))
    
    for log in logs:
        a_list=[str(log.id),
                str(log.user_profile.user.id),
                log.user_profile.name,  #uid
                log.user_profile.random_code,
                str(log.group.id),
                str(log.group.score_1 + log.group.score_2),
                str(log.panel.id),
                str(log.panel.session),
                log.action,
                log.action_time.strftime(datetime_format_ISO)
                ]
        tmp_str = ','.join(a_list)
        all_list.append(tmp_str)
        
    try:
        fileContent = '\n'.join(all_list)
        game = Game.objects.get(pk = game_id)
        fileName = game.name
    except:
        fileContent = "File NOT Found!"
        fileName = "FileNotFound"
        
    res = HttpResponse(fileContent)
    res['Content-Disposition'] = 'attachment; filename=%s.csv' % (fileName)
    return res


def create_user_interact(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    tmp = User.objects.filter(username = username)
    try:
        if len(tmp) < 1:
            utils.create_user(username, username, password)
            nextUrl = reverse('mine.views.login_view')
            return HttpResponseRedirect(nextUrl)
        else:
            data_dict = {}
            data_dict['occupy'] = 'true'
            return render(request, 'create_user.html', data_dict)
    except:
        data_dict = {}
        data_dict['occupy'] = 'true'
        return render(request, 'create_user.html', data_dict)
    