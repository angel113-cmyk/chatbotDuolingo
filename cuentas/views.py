from random import choice, random, shuffle

from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# 1. LOGICA DE REGISTRO
def registro_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Creamos el usuario vacío primero
        nuevo_usuario = User(username=usuario, email=correo)
        # Forzamos a Django a encriptar la contraseña correctamente
        nuevo_usuario.set_password(clave)
        # Guardamos en la base de datos SQLite
        nuevo_usuario.save()
        
        return redirect('login')
        
    return render(request, 'cuentas/registro.html')

# 2. LOGICA DE INICIO DE SESIÓN
def login_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        
        # Django verifica automáticamente si el usuario y la clave coinciden
        user = authenticate(request, username=usuario, password=clave)
        
        if user is not None:
            auth_login(request, user) # Inicia la sesión en el navegador
            return redirect('home')  # Lo manda a la pantalla principal del juego
        else:
            # Si falla, recarga la página mostrando un mensaje de error
            return render(request, 'cuentas/login.html', {'error': 'Usuario o contraseña incorrectos'})
            
    return render(request, 'cuentas/login.html')

# 3. PANTALLA PRINCIPAL (El juego/chatbot)
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required

# 1. VISTA DE REGISTRO
def registro_usuario(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Validar si el usuario ya existe para evitar errores de restricción UNIQUE
        if User.objects.filter(username=usuario).exists():
            return render(request, 'cuentas/registro.html', {'error': 'El nombre de usuario ya existe.'})
            
        nuevo_usuario = User(username=usuario, email=correo)
        nuevo_usuario.set_password(clave)
        nuevo_usuario.save()
        return redirect('login')
    return render(request, 'cuentas/registro.html')

# 2. VISTA DE LOGIN
def login_usuario(request):
    error = None
    if request.method == 'POST':
        usuario = request.POST.get('username')
        clave = request.POST.get('password')
        user = authenticate(request, username=usuario, password=clave)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            error = "Usuario o contraseña incorrectos"
    return render(request, 'cuentas/login.html', {'error': error})

# 3. VISTA HOME (MANEJA EL JUEGO COMPLETO)
def home(request):
    # Si el usuario no está autenticado en Django y es una petición normal, lo mandamos al login
    if not request.user.is_authenticated and request.headers.get('x-requested-with') != 'XMLHttpRequest':
        return redirect('login')

    # Inicializar las variables de la sesión si no existen
    if 'exp' not in request.session:
        request.session['exp'] = 0
    if 'gemas' not in request.session:
        request.session['gemas'] = 505
    if 'vidas' not in request.session:
        request.session['vidas'] = 5

    # Banco de 10 preguntas básicas estilo Duolingo
    banco_preguntas = [
        {"ingles": "The milk is cold", "correcta": "La leche está fría", "incorrecta": "La leche está caliente"},
        {"ingles": "The cat is sleeping", "correcta": "El gato está durmiendo", "incorrecta": "El perro está corriendo"},
        {"ingles": "I want an apple", "correcta": "Yo quiero una manzana", "incorrecta": "Yo como un plátano"},
        {"ingles": "The car is red", "correcta": "El carro es rojo", "incorrecta": "El carro es azul"},
        {"ingles": "Where is the bathroom?", "correcta": "¿Dónde está el baño?", "incorrecta": "¿Qué hora es?"},
        {"ingles": "Good morning, friend", "correcta": "Buen día, amigo", "incorrecta": "Buenas noches, mamá"},
        {"ingles": "She likes water", "correcta": "A ella le gusta el agua", "incorrecta": "Ella quiere comer pan"},
        {"ingles": "The boy has a book", "correcta": "El niño tiene un libro", "incorrecta": "El niño juega fútbol"},
        {"ingles": "Thank you very much", "correcta": "Muchas gracias", "incorrecta": "Por favor, de nada"},
        {"ingles": "He lives in a big house", "correcta": "Él vive en una casa grande", "incorrecta": "Él tiene un perro grande"}
    ]

    # SI EL USUARIO COMPRUEBA UNA RESPUESTA VÍA AJAX
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        eleccion = request.POST.get('respuesta_usuario')
        respuesta_correcta_anterior = request.POST.get('respuesta_correcta_hidden')
        
        if eleccion == respuesta_correcta_anterior:
            request.session['exp'] = min(request.session['exp'] + 10, 100)
            status = 'correcto'
        else:
            request.session['vidas'] = max(request.session['vidas'] - 1, 0)
            status = 'incorrecto'
            
        request.session.modified = True

        # Elegimos inmediatamente la SIGUIENTE pregunta para el JSON
        siguiente_pregunta = choice(banco_preguntas)
        nuevas_opciones = [siguiente_pregunta['correcta'], siguiente_pregunta['incorrecta']]
        shuffle(nuevas_opciones)

        return JsonResponse({
            'status': status,
            'exp': request.session['exp'],
            'vidas': request.session['vidas'],
            'progreso_porcentaje': min((request.session['exp'] / 100) * 100, 100),
            'siguiente_ingles': siguiente_pregunta['ingles'],
            'siguiente_correcta': siguiente_pregunta['correcta'],
            'nuevas_opciones': nuevas_opciones,
            'respuesta_correcta_anterior': respuesta_correcta_anterior
        })

    # CARGA INICIAL DE LA PÁGINA (Petición normal)
    pregunta_actual = choice(banco_preguntas)
    opciones = [pregunta_actual['correcta'], pregunta_actual['incorrecta']]
    shuffle(opciones)

    context = {
        'exp': request.session['exp'],
        'gemas': request.session['gemas'],
        'vidas': request.session['vidas'],
        'progreso_porcentaje': min((request.session['exp'] / 100) * 100, 100),
        'pregunta': pregunta_actual,
        'opciones': opciones
    }
    return render(request, 'cuentas/home.html', context)

@login_required(login_url='login')
def buhobot(request):
    return render(request, 'cuentas/buhobot.html')