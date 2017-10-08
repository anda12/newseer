""" Views for the base application """
from django.conf import settings
from django.shortcuts import render_to_response
from django.utils._os import safe_join
from django.http import Http404, HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.template import Template, Context, RequestContext
import os
from django.contrib.sessions.models import Session
import json
from django.template.context_processors import request
import codecs




def get_page_or_404(name):
    """Return page content as a Django template or raise 404 error."""
    try:
        file_path = safe_join(settings.SITE_PAGES_DIRECTORY, name)
        print("+++++++++++++"+file_path)
    except ValueError:
        raise Http404('Page Not Found')
    else:
        if not os.path.exists(file_path):
            raise Http404('Page Not Found')

    with codecs.open(file_path, 'r', 'utf-8') as f:
        page = Template(f.read())

    print('============\n'+page.__str__())
    return page


def page(request, slug='dashboard'):
    """Render the requested page if found."""

    if slug[-5:] == '.html':
        slug = slug[0:-5]

    context = {
            "par_page": slug, 
            "cur_page": "tttt",
            'slug' : slug,
            'menus':request.session['menus'],
        }
    
    funcs = 'jddsj.'+slug
    try:
        func = eval(funcs)
        return func(request, slug, context)
    except Exception:
        func = jddsj.overview

    mn = jddsj.get_menu_info(slug)
    if mn =={}:
        func = jddsj.overview
    else:
        try:
            print(mn.get('page'))
            func = eval('jddsj.'+mn.get('page'))
        except Exception:
            func = jddsj.overview
    
    return func(request, slug, context)



class jddsj():
    @staticmethod
    def get_menu():
        pidai = {'name':'皮带系统', 'subs':[{'name':'皮带系统概况', 'value':'pidaiview', 'page':'sysview'}, {'name':'东一皮带', 'value':'dongyi', 'page':'sysview'}, {'name':'东二皮带','value':'donger', 'page':'sysview'}]}
        paishui = {'name': '排水系统', 'subs':[{'name':'排水系统概况', 'value':'paishuiview', 'page':'sysview'}, {'name':'-800水泵房', 'value':'s800', 'page':'sysview'}, {'name':'-400水泵房','value':'s400', 'page':'sysview'},{'name':'950水泵房','value':'s950', 'page':'sysview'}] }
        tisheng = {'name':'提升系统', 'subs':[{'name':'提升系统概况', 'value':'tishengview', 'page':'sysview'}, {'name':'主井', 'value':'jz', 'page':'sysview'}, {'name':'副井','value':'jf', 'page':'sysview'}, {'name':'8号井', 'value':'j8', 'page':'sysview'}, {'name':'9#','value':'j9', 'page':'sysview'}]}
        configure = {'name':'系统设置', 'subs':[{'name':'系统配置概况', 'value':'syscfgview','page':'syscfgview'} ]}
        
        return [pidai, paishui, tisheng, configure]
    
    @staticmethod
    def get_menu_info(value):
        rlt={'pidaiview':{'name':'皮带系统概况', 'value':'pidaiview', 'page':'sysview', 'sys_code':"111"},
             'dongyi':{'name':'东一皮带', 'value':'dongyi', 'page':'sysview','sys_code':"112"},
             'donger':{'name':'东二皮带','value':'donger', 'page':'sysview','sys_code':"113"},
             'paishuiview':{'name':'排水系统概况', 'value':'paishuiview', 'page':'sysview','sys_code':"114"},
             's800':{'name':'-800水泵房', 'value':'s800', 'page':'sysview','sys_code':"115"}, 
             's400':{'name':'-400水泵房','value':'s400', 'page':'sysview','sys_code':"116"},
             's950':{'name':'950水泵房','value':'s950', 'page':'sysview','sys_code':"117"},
             'tishengview':{'name':'提升系统概况', 'value':'tishengview', 'page':'sysview','sys_code':"118"}, 
             'jz':{'name':'主井', 'value':'jz', 'page':'sysview','sys_code':"119"}, 
             'jf':{'name':'副井','value':'jf', 'page':'sysview','sys_code':"110"}, 
             'j8':{'name':'8号井', 'value':'j8', 'page':'sysview','sys_code':"121"}, 
             'j9':{'name':'9#','value':'j9', 'page':'sysview','sys_code':"122"},
             'syscfgview':{'name':'系统配置概况', 'value':'syscfgview','page':'syscfgview','sys_code':"123"}
             }
        
        return rlt[value]
    
    @staticmethod
    def _init_page(request, template, param, flag, slug='dashboard'):
        """ Default view for the root """
        print('----------')
        #print locals()
        page = get_page_or_404( os.path.join(settings.SITE_PAGES_DIRECTORY, template) )

        try:
            menus = request.session.get('menus', jddsj.get_menu())
            '''
            s = Session.objects.get(pk=request.COOKIES['sessionid'])
            if s.get_decoded().get('menus') == None:
                menus = ZmqAPI.get_menu()
                print(request.session['menus'])
                print(str(type(request.session['menus'])))
                #print(context['menus'] + str(type(context['menus'])))
            else:
                menus = s.get_decoded().get('menus')
                print(request.session['menus'])
                print(str(type(request.session['menus'])))
                #print(context['menus'] + str(type(context['menus'])))
            '''
        except:
            menus = get_menu()


        
        param['page'] = page
        param['menus'] = menus
        
        tl = template.split('.')
        print(tl)
        if slug != tl[0]:
            slug=tl[0]
        
        print (slug)
        print (slug)
        print (slug)
        print (slug)
        print (slug)
        if flag == 'render':
            return render(request, 'page/'+slug+'.html', param)
        elif flag == 'render_to_response':
            return render_to_response('page/'+slug+'.html', param)
        elif flag == 'redirect':
            return HttpResponseRedirect('page/'+slug+'.html')

    @staticmethod
    def home(request, slug='home', context={}):
        """ Default view for the root """

        context['page'] = page
        return jddsj._init_page(request, 'home.html', context, 'render', slug)        
