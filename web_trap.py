from flask import Flask, render_template_string, request, send_from_directory
import os

app = Flask(__name__)

# --- DISEÑO VPN CORPORATIVO CON FONDO AZUL ---
HTML_LOGIN = """
<!DOCTYPE html>
<html>
<head>
    <title>Acceso Remoto - Sentinel Corp</title>
    <link rel="icon" type="image/jpg" href="/favicon.ico">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        body { 
            background: linear-gradient(135deg, #001a33 0%, #004080 100%); 
            display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        }
        .login-card { 
            width: 420px; padding: 45px; background: white; border-radius: 12px; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.3); border-top: 6px solid #0056b3; 
        }
        .logo { text-align: center; margin-bottom: 25px; color: #0056b3; font-weight: bold; font-size: 28px; letter-spacing: 1px; }
        .btn-primary { background-color: #0056b3; border: none; width: 100%; padding: 12px; font-weight: bold; }
        .btn-primary:hover { background-color: #004494; }
        .warning-text { font-size: 11px; color: #777; text-align: center; margin-top: 25px; line-height: 1.4; }
    </style>
</head>
<body>
    <div class="login-card">
        <div class="logo">SENTINEL <span style="color: #333;">VPN</span></div>
        <h5 class="text-center mb-4" style="color: #444;">Autenticación de Empleado</h5>
        <form action="/login" method="post">
            <div class="mb-3">
                <label class="form-label">ID de Usuario</label>
                <input type="text" name="username" class="form-control" placeholder="Ej: Alberto Gonzalez" required>
            </div>
            <div class="mb-3">
                <label class="form-label">Contraseña de Red</label>
                <input type="password" name="password" class="form-control" placeholder="••••••••" required>
            </div>
            <button type="submit" class="btn btn-primary">INICIAR SESIÓN SEGURA</button>
        </form>
        <div class="warning-text">
            SISTEMA RESTRINGIDO. El acceso está sujeto a los términos de seguridad de Sentinel Corp. 
            Toda actividad está siendo grabada y geolocalizada.
        </div>
    </div>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_LOGIN)

@app.route('/login', methods=['POST'])
def login():
    user = request.form.get('username')
    pwd = request.form.get('password')
    ip = request.remote_addr
    
    # Registro con formato compatible para el monitor
    log_entry = f"WEB_ATTACK | IP: {ip} | User: {user} | Pwd: {pwd}\\n"
    
    if not os.path.exists("logs"): os.makedirs("logs")
    with open("logs/attacks.log", "a") as f:
        f.write(log_entry)
    
    return "<h3>Error de Protocolo 503: El servidor de autenticación no responde. Reintentando...</h3><script>setTimeout(function(){location.href='/';}, 3000);</script>"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.getcwd(), 'Sentinel.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
