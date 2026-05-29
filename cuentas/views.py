from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login

# 1. LOGICA DE REGISTRO
def registro_usuario(request):
    if request.method == 'POST':
        # Capturamos lo que escribió el usuario en el HTML
        usuario = request.POST.get('username')
        correo = request.POST.get('email')
        clave = request.POST.get('password')
        
        # Guardamos el usuario de forma segura en la base de datos de Django
        nuevo_usuario = User.objects.create_user(username=usuario, email=correo, password=clave)
        nuevo_usuario.save()
        
        # Una vez creado, lo mandamos directo al Login
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
def home(request):
    return render(request, 'cuentas/home.html')