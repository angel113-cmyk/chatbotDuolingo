# Sistema de Rate Limiting Gratuito - DuolingoChat

## 📋 ¿Qué hace?

Tu aplicación ahora tiene un **sistema inteligente de control de cuota** para respetar el límite gratuito de **20 solicitudes por minuto** de Gemini API.

## 🔧 Características Implementadas

### 1. **Verificación de Tasa de Solicitudes**
- Cada usuario tiene un límite independiente de 20 solicitudes/minuto
- Si intenta exceder, recibe un error `429` con el tiempo de espera

### 2. **Caché de Respuestas**
- Respuestas idénticas se almacenan hasta 1 hora
- Evita solicitudes repetidas a la API (¡ahorra cuota!)
- Si pregunta lo mismo, obtiene la respuesta en caché instantáneamente

### 3. **Respuesta al Cliente**
Si alcanzas el límite, verás:
```json
{
  "status": "rate_limit",
  "message": "⏳ Límite de solicitudes alcanzado. Espera 45 segundos.",
  "wait_time": 45
}
```

Si usa caché:
```json
{
  "status": "success",
  "reply": "Good morning!",
  "cached": true
}
```

## 📊 Cálculo de Cuota

- **Límite**: 20 solicitudes/minuto
- **Ventana**: 60 segundos
- **Caché**: Evita solicitudes duplicadas (válido 1 hora)

### Ejemplo de uso seguro:
```
- Minuto 1: Haces 15 solicitudes ✅
- Minuto 2: Puedes hacer 5 solicitudes más ✅
- Si intentas hacer más de 20 en 60 segundos → ⏳ Esperar
```

## 🛡️ Ventajas

✅ **Sin gastar dinero** - Funciona con el plan gratuito
✅ **Inteligente** - Cachea respuestas repetidas
✅ **Fácil** - Manejo automático, el usuario no necesita configurar nada
✅ **Informativo** - Dice cuánto tiempo esperar
✅ **Por usuario** - Cada usuario tiene su propia cuota

## ⚙️ Archivos Modificados

1. **cuentas/views.py**
   - Agregada clase `RateLimiter`
   - Verificación en función `buhobot()`
   - Caché automático de respuestas

2. **DuolingoChat/settings.py**
   - Configuración de caché en memoria (LocMemCache)
   - No requiere base de datos externa

## 📝 Notas Técnicas

- Usa `django.core.cache` con backend `LocMemCache` (en memoria)
- Almacena timestamps de solicitudes por usuario
- Genera hash SHA256 de prompts para caché
- Límites se reinician cada minuto automáticamente

## ✨ Próximos Pasos (Opcional)

Si necesitas más solicitudes en el futuro:
1. **Cambiar a modelo más barato**: `gemini-1.5-flash` (aún más límite)
2. **Usar Redis en caché**: Más eficiente que memoria
3. **Implementar cola de espera**: Para usuario premium (futuro)

