Guion Paso a Paso: Configuración de Servidor Web Debian con Nginx y UFW
Objetivo: Configurar una PC Debian para servir una página web con Nginx, protegerla con UFW, y demostrar el acceso desde una máquina cliente (usando IP y nombre de dominio local).

Hardware/Software Necesario:

PC Servidor: Tu PC física con Debian instalado.
PC Cliente: Otra computadora (Windows, macOS, Linux) en la misma red Wi-Fi que tu PC Debian.
Conexión a Internet para la PC Debian (para instalación de paquetes).
Terminales abiertas en ambas PCs.

Parte 1: Configuración de la PC Servidor (Debian)
Abre una terminal en tu PC Debian. Necesitarás permisos de superusuario (sudo).

Paso 1.1: Confirmar Configuración de Red (IP Estática y Conectividad)
Verifica la IP estática:

Bash

ip a

Verifica: Busca la interfaz de tu Wi-Fi (ej. wlp1s0) y asegúrate de que la inet sea 192.168.1.190 (o la IP que asignaste). Si no es correcta, edita /etc/network/interfaces y reinicia el servicio de red o el sistema.
Bash

# Ejemplo de lo que deberías ver para wlp1s0 con la IP estática
2: wlp1s0: <BROADCAST,MULTICAST,UP,LOWER_UP> mtu 1500 qdisc noqueue state UP group default qlen 1000
    link/ether 00:11:22:33:44:55 brd ff:ff:ff:ff:ff:ff
    inet 192.168.1.190/24 brd 192.168.1.255 scope global dynamic wlp1s0  <-- ¡Esta es tu IP!
       valid_lft 86297sec preferred_lft 86297sec
Verifica la conectividad a Internet:

Bash

ping 8.8.8.8
ping google.com
Verifica: Debes recibir respuestas exitosas. Si no, revisa la configuración de gateway y dns-nameservers en /etc/network/interfaces.
Paso 1.2: Instalar Nginx y Crear Contenido Web
Actualiza los paquetes e instala Nginx:

Bash

sudo apt update
sudo apt install nginx -y
Verifica: Nginx debe instalarse sin errores y el servicio debería iniciar automáticamente.
Crea el directorio para el contenido (si no existe) y la página HTML:
Asumiremos que tu contenido estará en /var/www/html/prueba1/index.html.

Bash

sudo mkdir -p /var/www/html/prueba1/
sudo nano /var/www/html/prueba1/index.html
Pega el siguiente contenido HTML:

HTML

<!DOCTYPE html>
<html>
<head>
    <title>Servidor Web Seguro - TPI Seguridad Informática</title>
    <meta charset="UTF-8">
</head>
<body>
    <h1>¡Bienvenido a nuestro Servidor Web Seguro!</h1>
    <h2>Probando mi primer localhost con Nginx</h2>
    <p>Resultado: Exitoso</p>
    <p>Este sitio es servido por Nginx desde la IP 192.168.1.190 y protegido por UFW.</p>
    <p>Realizado por Giuliana y [Tu Nombre/Nombre de Compañero]</p>
</body>
</html>
Guarda y sal (Ctrl + O, Enter, Ctrl + X).

Configura Nginx para servir el contenido:
Edita el archivo de configuración por defecto de Nginx:

Bash

sudo nano /etc/nginx/sites-available/default
Dentro del bloque server { ... }, realiza los siguientes cambios (busca las líneas listen 80; y server_name y root):

Nginx

server {
    listen 80;
    listen [::]:80; # Para IPv6

    # Agrega tu IP y el nombre de dominio personalizado
    server_name 192.168.1.190 host.lan;

    root /var/www/html; # Asegúrate de que esta sea la raíz de tus archivos

    # Agrega un bloque location para /prueba1/
    location /prueba1/ {
        alias /var/www/html/prueba1/; # Esta es la ruta real al contenido
        index index.html;
        try_files $uri $uri/ =404;
    }

    # Asegúrate de que el bloque location / también esté presente para otras rutas si las necesitas
    location / {
        # Opcional: si tienes un index.html directamente en /var/www/html
        # try_files $uri $uri/ =404;
    }

    # ... (deja el resto del archivo como está)
}
Guarda y sal (Ctrl + O, Enter, Ctrl + X).

Verifica la sintaxis de Nginx y recarga el servicio:

Bash

sudo nginx -t
sudo systemctl reload nginx
Verifica: nginx -t debe mostrar "syntax is ok" y "test is successful". reload no debe mostrar errores.
Verificación interna del sitio web (desde la propia PC Debian):

Bash

curl http://127.0.0.1/prueba1/
Verifica: Debes ver el contenido HTML de tu página.
Paso 1.3: Configurar y Endurecer el Firewall UFW
Instala UFW:

Bash

sudo apt install ufw -y
Establece las políticas por defecto (¡Crucial para la seguridad!):

Bash

sudo ufw default deny incoming
sudo ufw default allow outgoing
Permite el tráfico necesario:

Bash

sudo ufw allow ssh        # Puerto 22 para administración remota
sudo ufw allow http       # Puerto 80 para Nginx
sudo ufw allow https      # Puerto 443 para futuro HTTPS
sudo ufw allow 53/udp     # Para DNS (opcional, allow outgoing ya ayuda)
sudo ufw allow 53/tcp     # Para DNS (opcional)
Endurecimiento de ICMP (Bloquear Ping):

Haz copia de seguridad de las reglas "before":

Bash

sudo cp /etc/ufw/before.rules /etc/ufw/before.rules.bak
sudo cp /etc/ufw/before6.rules /etc/ufw/before6.rules.bak
Edita before.rules (IPv4):

Bash

sudo nano /etc/ufw/before.rules
Busca la línea -A ufw-before-input -p icmp --icmp-type echo-request -j ACCEPT y coméntala (pon un # al principio).
Guarda y sal.

Edita before6.rules (IPv6):

Bash

sudo nano /etc/ufw/before6.rules
Busca la línea -A ufw6-before-input -p icmpv6 --icmpv6-type echo-request -j ACCEPT y coméntala.
Guarda y sal.

Habilita UFW:

Bash

sudo ufw enable
Verifica: Confirma con y.
Verifica el estado de UFW (debe decir "active" y las reglas permitidas):

Bash

sudo ufw status verbose
Paso 1.4: Configurar la Resolución de Nombre Local (host.lan)
Edita el archivo /etc/hosts:

Bash

sudo nano /etc/hosts
Agrega la siguiente línea al final del archivo:

192.168.1.190   host.lan
Guarda y sal (Ctrl + O, Enter, Ctrl + X).

Vacía la caché DNS del sistema (opcional, pero buena práctica):

Bash

sudo systemd-resolve --flush-caches
Verifica: host host.lan debe resolver a 192.168.1.190.
Paso 1.5: Reiniciar el Sistema (¡Recomendado para aplicar todo!)
Para asegurarte de que todas las configuraciones (red, Nginx, UFW) se carguen limpiamente:

Bash

sudo reboot
Espera a que tu PC Debian se reinicie completamente.

Parte 2: Verificación desde la PC Cliente
En tu PC Cliente (Windows, macOS, o Linux), abre una terminal (CMD en Windows) y un navegador web.

Paso 2.1: Verificar Conectividad General (Pre-Firewall)
Intenta hacer ping a la IP de tu PC Debian (192.168.1.190) ANTES de iniciar esta parte del guion (solo si estás haciendo la demostración de "ping falla").
DOS

ping 192.168.1.190
Verifica: Si seguiste el paso 1.5 y reiniciaste Debian, este ping debería fallar ("Tiempo de espera agotado"). Esto es una buena señal de que UFW está activo y bloqueando ICMP.
Paso 2.2: Acceder al Servidor Web por IP
Abre tu navegador.
En la barra de direcciones, ingresa la IP y la ruta:
http://192.168.1.190/prueba1/
Verifica: Tu página HTML ("¡Bienvenido a nuestro Servidor Web Seguro!") debe cargarse correctamente. Si no lo hace, el problema es de Nginx o de las reglas básicas de UFW (revisa sudo ufw status verbose en Debian).
Paso 2.3: Configurar la Resolución de Nombre Local en la PC Cliente
Para que esta PC cliente entienda host.lan.

En la PC Cliente (Windows):

Abre el Bloc de notas como Administrador.
Ve a Archivo -> Abrir.
Navega a C:\Windows\System32\drivers\etc.
Cambia el tipo de archivo a "Todos los archivos (*.*)".
Abre el archivo hosts.
Añade la línea al final:
192.168.1.190   host.lan
Guarda el archivo.
Vacía la caché DNS de Windows: Abre CMD como Administrador y ejecuta:
DOS

ipconfig /flushdns
Cierra y vuelve a abrir tu navegador.
En la PC Cliente (macOS/Linux):

Abre una terminal.
Edita el archivo hosts:
Bash

sudo nano /etc/hosts
Añade la línea:
192.168.1.190   host.lan
Guarda y sal.
Vacía la caché DNS (ej. macOS):
Bash

sudo killall -HUP mDNSResponder
sudo dscacheutil -flushcache
Cierra y vuelve a abrir tu navegador.
Paso 2.4: Acceder al Servidor Web por Nombre de Dominio Personalizado
Abre tu navegador en la PC Cliente.
En la barra de direcciones, ingresa el nombre de dominio y la ruta:
http://host.lan/prueba1/
Verifica: Tu página HTML debe cargarse correctamente. Si no lo hace, revisa los pasos de configuración del hosts en la PC cliente y la caché DNS del navegador.