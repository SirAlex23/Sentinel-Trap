# 🛡️ Sentinel Honeypot: Detección y Geolocalización Proactiva

<p align="center">
  <img src="Sentinel.jpg" width="150" alt="Sentinel Logo">
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.x-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Framework-Flask-lightgrey.svg" alt="Flask">
  <img src="https://img.shields.io/badge/Security-Honeypot-red.svg" alt="Honeypot">
  <img src="https://img.shields.io/badge/Alerts-Telegram-blue.svg" alt="Telegram">
</p>

---

## 📖 Descripción
**Sentinel Honeypot** es una herramienta de ciberseguridad defensiva diseñada para engañar a posibles atacantes mediante un portal VPN corporativo falso. El sistema no solo captura credenciales en un entorno controlado, sino que rastrea la ubicación del intruso en tiempo real y envía alertas instantáneas con mapas detallados a un bot privado de Telegram.

## ✨ Características Principales
* **🌐 Interfaz Realista:** Clon de acceso VPN de Sentinel Corp para maximizar la efectividad del engaño.
* **📍 Geolocalización IP:** Identificación automática de Ciudad, País e ISP del atacante.
* **📱 Alertas Telegram:** Notificaciones push con enlace directo a Google Maps con las coordenadas del incidente.
* **🔒 Seguridad de Credenciales:** Implementación de variables de entorno (`.env`) para proteger tokens y IDs de API.
* **📊 Registro Forense:** Almacenamiento local de logs para análisis posterior de ataques.
