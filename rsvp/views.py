from django.shortcuts import render, redirect

from django.http import HttpResponse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.core.mail import send_mail

from .models import *

SENDER_EMAIL = 'chengxinghao@hotmail.com'

def index(request):
	next = request.GET.get('next')
	return render(request, 'index.html', {'next':next})

def register_page(request):
	return render(request, 'register.html')

def user_login(request):
	redirect_to = request.GET.get('next', '/main')
	username = request.POST.get('username')
	password = request.POST.get('password')
	user = authenticate(username=username, password=password)
	if user is None:
		return render(request, 'index.html', {'msg':'Wrong username or password!'})
	login(request, user)
	return redirect(redirect_to)

def register(request):
	username = request.POST.get('username')
	password = request.POST.get('password')
	firstname = request.POST.get('firstname')
	lastname = request.POST.get('lastname')
	email = request.POST.get('email')
	if User.objects.filter(username=username).exists():
		return render(request,'register.html',{'msg':'Username existed!'})
	elif User.objects.filter(email=email).exists():
		return render(request,'register.html',{'msg':'Email existed!'})
	user = User.objects.create_user(username, email, password)
	user.first_name = firstname
	user.last_name = lastname
	user.save()
	return render(request,'index.html', {'msg':'Register Success!'})

@login_required
def main_page(request):
 	return render(request, 'main.html',{'name':request.user.first_name})

@login_required
def user_logout(request):
	logout(request)
	return redirect('/')

@login_required
def create_event_page(request):
	return render(request, 'event.html')

@login_required
def create_event(request):
	name = request.POST.get('name')
	date = request.POST.get('date')
	i = 0
	free_text_questions = []
	while request.POST.get('ft_'+str(i)) is not None:
		print(request.POST.get('ft_'+str(i)))
		free_text_questions.append(request.POST.get('ft_'+str(i)))
		i += 1
	print(free_text_questions)
	return render(request, 'event.html')
'''
@login_required
def edit_event_page(request):
	return render(request, 'event.html')
'''
def send_email(request):
	subject = 'Hello'
	message = 'test'
	recipients = ['chengxinghao93@gmail.com']
	send_mail(subject, message, SENDER_EMAIL, recipients, fail_silently=False)
	return HttpResponse("success")

def get_free_text(request, event):
	ret = []
	i=0
	while request.POST.get('ft_'+str(i)) is not None:
		ret.append(request.POST.get('ft_'+str(i)))
		print(ret[-1])
		see = False
		if request.POST.get('ft_cb_'+str(i)) == 'on':
			see = True
		tmp = FT_Q(eid=event,question=ret[-1],vendor_can_see=see,is_finalized=False)
		tmp.save()
		i += 1
	return ret

class MultiChoice:
	def __init__(self):
		self.choices = []
		self.question = ""
	def __str__(self):
		return "Question: "+self.question+"/choices are: "+str(self.choices)

def get_mc(request,event):
	ret = []
	i = 0
	while request.POST.get('mc_'+str(i)) is not None:
		tmp = MultiChoice()
		tmp.question = request.POST.get('mc_'+str(i))
		see = False
		if request.POST.get('mc_cb_'+str(i)) == 'on':
			see = True
		q = MC_Q(eid=event,question=tmp.question,vendor_can_see=see,is_finalized=False)
		q.save()
		j = 0
		while request.POST.get('mc_'+str(i)+'_'+str(j)) is not None:
			tmp.choices.append(request.POST.get('mc_'+str(i)+'_'+str(j)))
			c = MC_Choice(qid = q, choice=tmp.choices[-1])
			c.save()
			j+=1
		ret.append(tmp)
		i+=1
	return ret

def test2(request):
	name = request.POST.get('name')
	date = request.POST.get('date')
	num = request.POST.get('num')
	event = Event(name=name,date=date,num=num)
	event.save()
	a = access(eid=event, username=request.user.username, role='Owner')
	a.save()
	free_text = get_free_text(request,event)
	multi_choice = get_mc(request,event)

	print(name)
	print(date)
	print(num)
	print(free_text)
	for mc in multi_choice:
		print(mc)
	
	return render(request,'event.html')

def test(request):
	return render(request,'event.html')

def read_ft(id):
	res = FT_Q.objects.filter(eid=id)
	return [q for q in res]

def get_choice(id):
	res = MC_Choice.objects.filter(qid=id)
	return [q for q in res]

def read_mc(id):
	mc = MC_Q.objects.filter(eid=id)
	res = []
	for i in range(len(mc)):
		res.append({'a':mc[i],'b':get_choice(mc[i].id),'c':'on'})
		if mc[i].vendor_can_see:
			res[-1]['c'] = 'off'
	return res

def edit_page(request, id):
	event = Event.objects.filter(id=id)[0]
	ft = read_ft(id)
	res = read_mc(id)
	context = {}
	context['name'] = event.name
	context['date'] = str(event.date)
	context['num'] = event.num
	context['fts'] = ft
	context['res'] = res
	context['id'] = id
	return render(request,'edit_event.html',context)

def edit_ft(request, event):
	fts = read_ft(event.id)
	qs = [ft.question for ft in fts]
	ret = []
	i=0
	while request.POST.get('ft_'+str(i)) is not None:
		ret.append(request.POST.get('ft_'+str(i)))
		print(ret[-1])
		see = False
		if request.POST.get('ft_cb_'+str(i)) == 'on':
			see = True
		if ret[-1] not in qs:
			tmp = FT_Q(eid=event,question=ret[-1],vendor_can_see=see,is_finalized=False)
			tmp.save()
		else:
			for ft in fts:
				if ft.question == ret[-1]:
					if not (ft.vendor_can_see == see):
						ft.vendor_can_see = see
						ft.save()
					break
		i += 1
	for ft in fts:
		if ft.question not in ret:
			ft.delete()

def edit_choice(request, q, i):
	j = 0
	original = get_choice(q.id)
	original_name = [o.choice for o in original]
	choice_name = []
	while request.POST.get('mc_'+str(i)+'_'+str(j)) is not None:
		choice_name.append(request.POST.get('mc_'+str(i)+'_'+str(j)))
		if choice_name[-1] not in original_name:
			c = MC_Choice(qid = q, choice=choice_name[-1])
			c.save()
		j+=1
	for o in original:
		if o.choice not in choice_name:
			o.delete()

def edit_mc(request,event):
	res = read_mc(event.id)
	tmp_dict = {}
	for d in res:
		tmp_dict[d['a'].question] = [d['a'],d['b']] #mc, mc_choices
	res = tmp_dict
	ret = []
	qs = []
	i = 0
	print(res)
	while request.POST.get('mc_'+str(i)) is not None:
		tmp = MultiChoice()
		tmp.question = request.POST.get('mc_'+str(i))
		see = False
		if request.POST.get('mc_cb_'+str(i)) == 'on':
			see = True
		if tmp.question not in res:
			q = MC_Q(eid=event,question=tmp.question,vendor_can_see=see,is_finalized=False)
			q.save()
			j = 0
			while request.POST.get('mc_'+str(i)+'_'+str(j)) is not None:
				tmp.choices.append(request.POST.get('mc_'+str(i)+'_'+str(j)))
				c = MC_Choice(qid = q, choice=tmp.choices[-1])
				c.save()
				j+=1
			ret.append(tmp)
		else:
			res[tmp.question][0].vendor_can_see = see
			res[tmp.question][0].save()
			edit_choice(request, res[tmp.question][0], i)
		qs.append(tmp.question)
		i+=1

	for key in res:
		if key not in qs:
			res[key][0].delete()

def edit(request, id):
	event = Event.objects.filter(id=id)[0]
	event.name = request.POST.get('name')
	event.date = request.POST.get('date')
	event.num = request.POST.get('num')
	event.save()
	edit_ft(request,event)
	edit_mc(request,event)
	return redirect('/edit_page/'+str(id))

def add_role_page(request, id):
	users = access.objects.filter(eid=id)
	owner = []
	vendor = []
	guest = []
	for user in users:
		if user.role == 'Owner':
			owner.append(user.username)
		elif user.role == 'Vendor':
			vendor.append(user.username)
		else :
			guest.append(user.username)
	owner_str = ', '.join(owner)
	vendor_str = ', '.join(vendor)
	guest_str = ', '.join(guest)
	return render(request, 'add_role.html', {'id':id, 'owner':owner_str , 'vendor':vendor_str, 'guest':guest_str})


def add_role(request, id):
	username = request.POST.get('username')
	role = request.POST.get('role')	
	if not access.objects.filter(eid=id).filter(username=username).filter(role=role).exists():
		event = Event.objects.filter(id=id)[0]
		tmp = access(eid=event, username = username, role = role)
		tmp.save()
	return redirect('/add_role_page/'+str(id))

def reponse_page(request, id):
	event = Event.objects.filter(id=id)[0]
	
	return render(request, 'response.html')

def reponse(request, id):
