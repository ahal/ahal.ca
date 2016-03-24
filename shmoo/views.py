from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail
from django.template import RequestContext
from forms import ContactForm
from bs4 import BeautifulSoup
import ConfigParser
import os
import urllib2

config = ConfigParser.ConfigParser()
config.read('/home/ahal/.shmoo_config')

def projects(request):
    """
    Index for the projects page
    """
    return render_to_response('projects/base.html', {'page_name':'projects'})

def gallery(request):
    """
    Index for the gallery page
    """
    data = urllib2.urlopen('http://500px.com/ahal/sets')
    soup = BeautifulSoup(data.read())

    sets = soup.find_all(id='sets')[0]
    for a in sets.find_all('a'):
        a['href'] = 'http://500px.com%s' % a['href']

    for h in sets.find_all('div', class_='header'):
        h['class'] = 'set-header'

    for c in sets.find_all('div', class_='content'):
        c['class'] = 'set-content'

    for s in sets.find_all('div', class_='set-big'):
        title = s.find_all('div', class_='set-header')[0].a.text.replace(' ', '_')
        img_dir = os.path.join(config.get('general', 'root'), 'static', 'img', 'gallery', title)

        if not os.path.isdir(img_dir):
            os.makedirs(img_dir)
            for i, img in enumerate(s.find_all('img')):
                data = urllib2.urlopen(img['src'])
                with open(os.path.join(img_dir, str(i) + '.jpg'), 'wb') as pic:
                    pic.write(data.read())

        for i, img in enumerate(s.find_all('img')):
            img['src'] = '/static/img/gallery/%s/%s.jpg' % (title, i)
    
    return render_to_response('gallery/base.html', {'page_name':'gallery',
                                                    'sets': sets.prettify()})

def about(request):
    """
    Main index view for the root website
    """
    return render_to_response('about/base.html', {'page_name':'about'})

def contact(request):
    """
    Index for the contact page
    """
    context = RequestContext(request, {'page_name':'contact'})
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            send_mail("", message, email, ["halbersa+blog@gmail.com"])
            context['processed'] = True
        else:
            context['invalid'] = True
    context['form'] = ContactForm()
    return render_to_response('contact/base.html', context)


def can(request):
    return HttpResponse("Yes he can!")
