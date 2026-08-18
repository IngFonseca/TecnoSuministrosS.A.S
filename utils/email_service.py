"""Servicio de correo electrónico para TecnoSuministros."""
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv

load_dotenv()


def _build_base_html(titulo: str, contenido: str) -> str:
    return f"""
    <html><body style="font-family:Arial,sans-serif;background:#f4f6f9;margin:0;padding:20px;">
    <div style="max-width:600px;margin:auto;background:#ffffff;border-radius:8px;
                box-shadow:0 2px 8px rgba(0,0,0,0.1);overflow:hidden;">
      <div style="background:#1a3a5c;padding:24px;text-align:center;">
        <h1 style="color:#ffffff;margin:0;font-size:22px;">TecnoSuministros S.A.S.</h1>
        <p style="color:#a8c4e0;margin:4px 0 0;">Sistema de Gestión Empresarial</p>
      </div>
      <div style="padding:32px;">
        <h2 style="color:#1a3a5c;border-bottom:2px solid #e8f0fe;padding-bottom:12px;">{titulo}</h2>
        {contenido}
      </div>
      <div style="background:#f0f4f8;padding:16px;text-align:center;">
        <p style="color:#666;font-size:12px;margin:0;">
          Este correo fue generado automáticamente por TecnoSuministros S.A.S.<br>
          Por favor no responder a este mensaje.
        </p>
      </div>
    </div>
    </body></html>
    """


def send_email(to: str, subject: str, html_body: str) -> bool:
    """Envía un correo electrónico HTML mediante SMTP."""

    host = os.getenv("EMAIL_HOST", "smtp.gmail.com").strip()
    port = int(os.getenv("EMAIL_PORT", "587").strip())

    user = os.getenv("EMAIL_USER", "").strip()

    # Las contraseñas de aplicación de Gmail suelen mostrarse
    # separadas por espacios. Los quitamos antes de autenticar.
    password = os.getenv("EMAIL_PASSWORD", "").replace(" ", "").strip()

    from_name = os.getenv(
        "EMAIL_FROM_NAME",
        "TecnoSuministros S.A.S."
    ).strip()

    to = to.strip()

    if not user:
        print("[Email] ERROR: EMAIL_USER no está configurado.")
        return False

    if not password:
        print("[Email] ERROR: EMAIL_PASSWORD no está configurado.")
        return False

    if not to:
        print("[Email] ERROR: el destinatario está vacío.")
        return False

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = f"{from_name} <{user}>"
    msg["To"] = to

    msg.attach(
        MIMEText(
            html_body,
            "html",
            "utf-8"
        )
    )

    try:
        print(f"[Email] Conectando a {host}:{port}...")
        
        with smtplib.SMTP(
            host,
            port,
            timeout=20
        ) as server:

            server.ehlo()

            # Cifrado TLS
            server.starttls()

            server.ehlo()

            print(f"[Email] Autenticando como {user}...")

            server.login(
                user,
                password
            )

            print(f"[Email] Enviando correo a {to}...")

            server.sendmail(
                user,
                [to],
                msg.as_string()
            )

        print(f"[Email] Correo enviado correctamente a {to}.")
        return True

    except smtplib.SMTPAuthenticationError as e:
        print(
            "[Email] ERROR DE AUTENTICACIÓN SMTP. "
            "Comprueba EMAIL_USER y la contraseña de aplicación de Gmail."
        )
        print(f"[Email] Detalle: {e}")
        return False

    except smtplib.SMTPConnectError as e:
        print(
            "[Email] ERROR DE CONEXIÓN SMTP. "
            "No se pudo conectar con el servidor."
        )
        print(f"[Email] Detalle: {e}")
        return False

    except smtplib.SMTPException as e:
        print(f"[Email] ERROR SMTP: {e}")
        return False

    except Exception as e:
        print(f"[Email] ERROR GENERAL: {type(e).__name__}: {e}")
        return False


def send_welcome_email(nombre: str, usuario: str, correo: str, rol: str) -> bool:
    """Correo de bienvenida a nuevo usuario."""
    rol_label = rol.capitalize() if rol else "Sin asignar"
    contenido = f"""
    <p style="color:#333;font-size:16px;">Hola, <strong>{nombre}</strong> 👋</p>
    <p style="color:#555;">Tu cuenta en TecnoSuministros S.A.S. ha sido creada exitosamente.
       A continuación tus credenciales de acceso:</p>
    <table style="width:100%;border-collapse:collapse;margin:20px 0;">
      <tr style="background:#e8f0fe;">
        <td style="padding:10px;font-weight:bold;color:#1a3a5c;width:40%;">Usuario</td>
        <td style="padding:10px;color:#333;">{usuario}</td>
      </tr>
      <tr>
        <td style="padding:10px;font-weight:bold;color:#1a3a5c;">Correo</td>
        <td style="padding:10px;color:#333;">{correo}</td>
      </tr>
      <tr style="background:#e8f0fe;">
        <td style="padding:10px;font-weight:bold;color:#1a3a5c;">Rol asignado</td>
        <td style="padding:10px;color:#333;">{rol_label}</td>
      </tr>
    </table>
    <p style="color:#555;">Por seguridad, te recomendamos cambiar tu contraseña en tu primer inicio de sesión.</p>
    <p style="color:#555;">Bienvenido al equipo. 🎉</p>
    """
    html = _build_base_html("¡Bienvenido al sistema!", contenido)
    return send_email(correo, "Bienvenido a TecnoSuministros S.A.S.", html)


def send_new_user_notification_to_manager(manager_email: str, manager_nombre: str,
                                          nuevo_nombre: str, nuevo_usuario: str,
                                          nuevo_correo: str) -> bool:
    """Notifica al gerente que un nuevo usuario se registró y necesita rol."""
    contenido = f"""
    <p style="color:#333;font-size:16px;">Hola, <strong>{manager_nombre}</strong></p>
    <p style="color:#555;">Se ha registrado un nuevo usuario en el sistema que requiere
       que le asignes un rol para poder acceder:</p>
    <table style="width:100%;border-collapse:collapse;margin:20px 0;">
      <tr style="background:#fff3cd;">
        <td style="padding:10px;font-weight:bold;color:#856404;width:40%;">Nombre completo</td>
        <td style="padding:10px;color:#333;">{nuevo_nombre}</td>
      </tr>
      <tr>
        <td style="padding:10px;font-weight:bold;color:#1a3a5c;">Usuario</td>
        <td style="padding:10px;color:#333;">{nuevo_usuario}</td>
      </tr>
      <tr style="background:#fff3cd;">
        <td style="padding:10px;font-weight:bold;color:#856404;">Correo</td>
        <td style="padding:10px;color:#333;">{nuevo_correo}</td>
      </tr>
      <tr>
        <td style="padding:10px;font-weight:bold;color:#1a3a5c;">Estado</td>
        <td style="padding:10px;color:#dc3545;"><strong>⏳ Sin rol asignado</strong></td>
      </tr>
    </table>
    <p style="color:#555;">Por favor ingresa al módulo de <strong>Trabajadores</strong>
       y asígnale el rol correspondiente.</p>
    """
    html = _build_base_html("Nuevo usuario registrado – acción requerida", contenido)
    return send_email(manager_email, "⚠️ Nuevo usuario requiere asignación de rol", html)


def send_low_stock_alert(proveedor_email: str, proveedor_nombre: str,
                         productos: list) -> bool:
    """Alerta al proveedor por stock bajo."""
    filas = "".join([
        f"""<tr style="{'background:#f8f9fa' if i % 2 == 0 else ''}">
            <td style="padding:8px;border:1px solid #dee2e6;">{p['codigo']}</td>
            <td style="padding:8px;border:1px solid #dee2e6;">{p['nombre']}</td>
            <td style="padding:8px;border:1px solid #dee2e6;color:#dc3545;font-weight:bold;">{p['cantidad']}</td>
        </tr>"""
        for i, p in enumerate(productos)
    ])
    contenido = f"""
    <p style="color:#333;">Estimado(a) <strong>{proveedor_nombre}</strong>,</p>
    <p style="color:#555;">Los siguientes productos de nuestro inventario se encuentran
       con <strong style="color:#dc3545;">stock crítico (≤ 5 unidades)</strong> y
       requerimos reabastecimiento urgente:</p>
    <table style="width:100%;border-collapse:collapse;margin:20px 0;">
      <thead>
        <tr style="background:#1a3a5c;color:white;">
          <th style="padding:10px;text-align:left;">Código</th>
          <th style="padding:10px;text-align:left;">Producto</th>
          <th style="padding:10px;text-align:left;">Stock actual</th>
        </tr>
      </thead>
      <tbody>{filas}</tbody>
    </table>
    <p style="color:#555;">Por favor comuníquese con nosotros a la brevedad para
       coordinar el pedido. Gracias.</p>
    """
    html = _build_base_html("🚨 Alerta de Stock Bajo – Reabastecimiento Requerido", contenido)
    return send_email(proveedor_email, "🚨 Alerta de stock bajo – TecnoSuministros S.A.S.", html)
