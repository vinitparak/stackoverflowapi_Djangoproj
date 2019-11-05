from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework import status
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator
import requests as req
from datetime import datetime
from django.http import HttpResponse
from datetime import date
from datetime import time
from django.shortcuts import redirect
from django.template import RequestContext
# Create your views here.

#to check the count limit permin(5) and per day (100) and limit the search if true it will post the data and list the result in paginations
@api_view(['GET'])
def answers(request):
	spent = datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S') - datetime.strptime(
		request.session['time'], '%H:%M:%S')
	xyz=spent.__str__().split(':')
	sec=((int(xyz[0])*3600)+(int(xyz[1])*60)+int(xyz[2]))
	if request.session['count']<5 and sec<60 and request.session['count_day'] <100 :

		question = request.GET.get('question')

		print(question)
		request.session['count'] = int(request.session['count']) + 1
		request.session['count_day'] =int(request.session['count_day']) +1
		print(request.session['count'])
		print(request.session['time'])
		print(datetime.strptime(datetime.time(datetime.now()).__str__().split('.')[0], '%H:%M:%S') - datetime.strptime(
			request.session['time'], '%H:%M:%S'))
		data = getAnswers(question)
		paginator = Paginator(data, 10)

		page = request.GET.get('page', 1)
		answers = paginator.get_page(page)

		print(paginator.num_pages)

		data = {'answers': answers.object_list}
		if answers.has_previous():
			data['has_previous'] = answers.has_previous()
			data['previous_page_number'] = answers.previous_page_number()

		if answers.has_next():
			data['has_next'] = answers.has_next()
			data['next_page_number'] = answers.next_page_number()

		data['last_page'] = paginator.num_pages
		data['current'] = page
		print('Page', data['current'])

		return JsonResponse(data)
	else:
		if sec>60:
			request.session['count'] = 0
			strg = datetime.time(datetime.now()).__str__()
			request.session['time'] = strg.split('.')[0]
			data = {'answers': [{'title': 'You got 5 new search limit for this minute please search again'}]}
		else:
			data={'answers': [{'title': 'search limit over Please try after one min or start a new session', 'is_answered':'Day Count Left='+str(100-request.session['count_day']),'tags':['you can retry after: '+str(60-sec)+' seconds']}]}

		return JsonResponse(data)

#restapi to get data from stackexchage api
def getAnswers(question):
	
	url = 'http://api.stackexchange.com/2.2/search/advanced'


	params = {'q': question,
				'site': 'stackoverflow',
				'order': 'desc',
				'sort': 'activity'}


	data = req.get(url=url, params=params).json()['items']

	'''answers = {}
				for i, answer in enumerate(data):
					answers[i] = {}
					answers[i]['tags'] = answer['tags']
					answers[i]['title'] = answer['title']
					answers[i]['is_answered'] = answer['is_answered']
					answers[i]['link'] = answer['link']'''

	return data
#to access form data from html page and request session for search limit
@csrf_exempt
def qform(request):

	if request.method == 'GET':
		response=render(request, 'form.html', {})
		if 'count' not in request.session:
			request.session['count'] = 0
			strg=datetime.time(datetime.now()).__str__()
			request.session['time']=strg.split('.')[0]
			request.session['count_day'] = 0
			strg = datetime.time(datetime.now()).__str__()
			request.session['time_day'] = strg.split('.')[0]

		return  response
	'''else:
			question = request.GET.get('q')
			data = getAnswers(question)
			paginator = Paginator(data, 10)

			page = request.GET.get('page')
			answers = paginator.get_page(page)

			return render(request, 'form.html', {'answers': answers})
	if request.method == 'POST':
		question = request.POST.get('question')
		data = getAnswers(question)
		paginator = Paginator(data, 10)

		answers = paginator.get_page(1)

		return render(request, 'form.html', {'answers': answers, 'question': question})'''

#to reset the session from the session button	
def delsession(request):
	del request.session['count']
	del request.session['count_day']
	response = redirect('/')
	return response