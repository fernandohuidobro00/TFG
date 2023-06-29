from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login

from django.urls import reverse_lazy
from django.views.generic.edit import CreateView

from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login, authenticate
from django.contrib import messages

from django.contrib.auth.forms import AuthenticationForm
from .models import Attribute, Business, User, Category, Checkin,Review, Hours, Tip
import json


dic_results = []
route_results = '/home/fernando/Escritorio/TFG/proyect/info/dic_information.json'
with open(route_results, "r") as archivo:
	lineas = archivo.readlines()  # leer todas las líneas en una lista
	
	for linea in lineas:
		data = json.loads(linea)
		dic_results.append(data)
archivo.close()

with open('/home/fernando/Escritorio/TFG/proyect/info/categories.json','r') as archivo2:
	categories_dict = json.load(archivo2)
archivo2.close()

#Los business ids elegidos
business_ids = ['mYMPepp0QIZRk_52pWzeoA','JzQsy7_G0p-UZGYFMCEHvQ', 'o_5z2Qt335Or-TTnECOIiw', 'KhBUg5QhBYuK8RZAe5gDMQ', 
                'BGc_EYORXo9O9A9IQ2MkxA', 'sPy8XUOJ0ax5Zh2yEsl4cA', 'c_4c5rJECZSfNgFj7frwHQ', 
                'vWRdL8B9o2CmUmfJgNgMqQ', 'HgPTy_OGoaxllb2EXkC1sQ', 'n_7EQxn0ciucIOJfpWVaTQ']

#los user ids elegidos
user_ids = [ 'RwPKUrc0ae54hV1DWU1MsQ', 'I2XpWCHAom1JRyHXZQrnfg',
                  'vffKQc_WQMYFGY4JS5VAOw', 'AaJ9d4OrFmgc4S_U2QiSZg', 'pou3BbKsIozfH50rxmnMew', 'fr1Hz2acAb3OaL3l6DyKNg']

#diccionario que relaciona las claves con los nombres de los usuarios
user_name_dic={'RwPKUrc0ae54hV1DWU1MsQ' : 'Mike','I2XpWCHAom1JRyHXZQrnfg': 'Kathy',
                  'vffKQc_WQMYFGY4JS5VAOw' : 'michelle', 'AaJ9d4OrFmgc4S_U2QiSZg' : 'Steve', 'pou3BbKsIozfH50rxmnMew' : 'Brett', 'fr1Hz2acAb3OaL3l6DyKNg' : 'Boon'}

#diccionario que relaciona las claves con los nombres de los business
business_name_dic = {'mYMPepp0QIZRk_52pWzeoA':'Seasons 52','JzQsy7_G0p-UZGYFMCEHvQ':'Yummy House South', 'o_5z2Qt335Or-TTnECOIiw': 'Bull Grill Brazilian Steakhouse',
		     	 'KhBUg5QhBYuK8RZAe5gDMQ': 'The Independent', 'BGc_EYORXo9O9A9IQ2MkxA':'Arco-Iris Restaurant', 'sPy8XUOJ0ax5Zh2yEsl4cA':"Nico's Arepas Grill",
				   'c_4c5rJECZSfNgFj7frwHQ': 'Tampa International Airport', 'vWRdL8B9o2CmUmfJgNgMqQ':"Rick's On the River",
				     'HgPTy_OGoaxllb2EXkC1sQ':'Happy Fish',
				     'n_7EQxn0ciucIOJfpWVaTQ': 'Saigon Deli'}

#lista de usuarios
users = []
for uid in user_ids:
		b = User.objects.get(user_id = uid)
		users.append(b)
#lista de business
businesses = []
for bid in business_ids:
		b = Business.objects.get(business_id = bid)
		businesses.append(b)


# funcion que va a mostrar los resultados del recomendador
def resultados(request):
	get_key_user = None
	get_key_business = None
	final_resultado = {}
	chosen_items_dic = []
	if request.method == 'POST':
		#elegidos usuario y business por formulario
		selected_user = request.POST.get('select_user')
		selected_business = request.POST.get('select_business')

		#obtenemos la clave del usuario que coincida con el diccionario
		for key, value in user_name_dic.items():
			if value == selected_user:
				get_key_user = key
				print(get_key_user)
		#obtenemos la clave del business que coincida con el diccionario
		for key, value in business_name_dic.items():
			if value == selected_business:
				get_key_business = key
				print(get_key_business)
		#obtenemos el diccionario que coincida con el usuario y business elegidos
		for d in dic_results:
			if get_key_user in d:
				if get_key_business == d[get_key_user]['business']:
					chosen_items_dic.append(d)


		print(chosen_items_dic)
		

		#los ordenamos por el resultado de la predicción y hacemos el pop del primero
		sorted_data = sorted(chosen_items_dic, key=lambda x: x[list(x.keys())[0]]['predic'])
		print(sorted_data)
		result = sorted_data.pop()	

		categories_number = result[get_key_user]['categories']
		list_categories_number_choosen = [int(i) for i in categories_number.split("-")]
		
		category_string = ""
		for key,value in categories_dict.items():
			if value in list_categories_number_choosen:
				category_string += (key + ", ")

		#quitar la ultima coma y espacio
		if category_string.endswith(", "):
			category_string = category_string.rstrip(", ")

		#creamos el diccionario para pasarlo por contexto al html
		final_resultado['name'] = selected_user
		final_resultado['business'] = selected_business
		final_resultado['popular'] = 'Popular' if result[get_key_user]['popular'] == 'Pop' else 'No Popular'		
		final_resultado['parking'] = 'Hay Parking' if result[get_key_user]['parking'] == 'Gar' else 'No hay Parking Parking'		
		final_resultado['day'] = 'Fin de Semana' if result[get_key_user]['day'] == 'WE' else 'Dia de Diario'		
		final_resultado['hour'] = 'Cena' if result[get_key_user]['hour'] == 'Din' else 'Comida'
		final_resultado['predic'] = result[get_key_user]['predic']
		final_resultado['categories'] = category_string


		lista_resultados_restantes = []

		for data in sorted_data:
			new_result = {}

			new_result['day'] = 'Fin de Semana' if data[get_key_user]['day'] == 'WE' else 'Dia de Diario'		
			new_result['hour'] = 'Cena' if data[get_key_user]['hour'] == 'Din' else 'Comida'
			lista_resultados_restantes.append(new_result)
		
		final_resultado['others_results'] = lista_resultados_restantes

				
		return render(request, 'app/resultado.html', context=final_resultado)



def ver_diccionarios(request):
	contexto = {'lista_diccionarios': dic_results}
	return render(request, 'app/ver_diccionarios.html', context = contexto)

def business_list(request):
	dict = {}
	dict['businesses'] = businesses
	return render(request, template_name='app/business_list.html', context=dict)

def user_list(request):
	
	dict = {}
	dict['users'] = users
	return render(request, template_name='app/user_list.html', context=dict)



def user_detail(request, user_id):
    dict= {}
    user = get_object_or_404(User, user_id=user_id)
    reviews = list(Review.objects.filter(user = user, business__city='Tampa',  user__review_count__gt=800))
    num_reviews = len(reviews)
    dict['user'] = user
    dict['reviews'] = reviews
    dict['num_reviews'] = num_reviews
	
    
    return render(request, 'app/user_detail.html', context=dict)

def business_detail(request, business_id):
    dict= {}
    business = get_object_or_404(Business, business_id=business_id)
    reviews = list(Review.objects.filter(business = business, business__city='Tampa',  user__review_count__gt=800))
    num_reviews = len(reviews)

    is_open = 'Abierto' if business.is_open == 1 else 'Cerrado'
    dict['business'] = business
    dict['reviews'] = reviews
    dict['num_reviews'] = num_reviews
    dict['is_open'] = is_open
    

	
    
    return render(request, 'app/business_detail.html', context=dict)


def review_detail(request, review_id):
	dict= {}
	review = get_object_or_404(Review, review_id=review_id)
	dict['review'] = review
	
	return render(request, 'app/review_detail.html', context=dict)

	
    
def index(request):
    dict =  {}
    dict['users'] = users
    dict['businesses']= businesses
    return render(request, 'app/home.html', context=dict)

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("app:homepage")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="app/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("app:homepage")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="app/login.html", context={"login_form":form})