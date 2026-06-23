# net_contingency.py
Un script ligero en Python 3 para el diagnóstico operativo de la pila de red
y la mitigación automática de fallos en el archivo de resolución DNS en entornos de auditoría Linux.

## 📊 Arquitectura del Script

El siguiente diagrama detalla el flujo lógico automatizado que ejecuta la herramienta para diagnosticar y mitigar fallos en la pila de red:

```mermaid
graph TD
    A[Inicio: Ejecución de net_contingency.py] --> B{¿Existe Ruta por Defecto?}
    B -- NO --> C[⚠️ Alerta: Interfaz Desconectada / Sin Gateway]
    B -- SÍ --> D{¿Resuelve DNS google.com?}
    
    D -- SÍ --> E[✅ Red Operativa: Todo OK]
    D -- NO --> F[🚨 Anomalía Detectada: Ruta Activa pero DNS Caído]
    
    F --> G{¿Usuario cuenta con privilegios Root?}
    G -- NO --> H[❌ Error: Sudo requerido para la remediación]
    G -- SÍ --> I[⚙️ Reescritura Atómica: Inyección de Nameservers en /etc/resolv.conf]
    
    I --> J[🔄 Re-verificación de Conectividad]
    J --> E
    
    style E fill:#1b4d3e,stroke:#3cd070,stroke-width:2px,color:#fff
    style C fill:#4a1515,stroke:#e05656,stroke-width:2px,color:#fff
    style H fill:#4a1515,stroke:#e05656,stroke-width:2px,color:#fff

# 🛠️ net_contingency.py

![Python Version](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)
![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Kali-kali?style=for-the-badge&logo=kali-linux)

Un script ligero y modular en Python 3 diseñado para el diagnóstico operativo de la pila de red y la mitigación automática de fallos en el archivo de resolución DNS dentro de entornos de auditoría y laboratorios Linux.

---

## 🎯 Problema que Resuelve

Durante auditorías de red o despliegues en entornos virtuales, es común experimentar pérdidas de conectividad debido a la corrupción o mala configuración del archivo de resolución de nombres (`/etc/resolv.conf`). Este script automatiza la verificación de la puerta de enlace y aplica un hotfix atómico inyectando servidores DNS confiables si detecta anomalías.

---

## 📊 Arquitectura del Script

El siguiente diagrama detalla el flujo lógico automatizado que ejecuta la herramienta para diagnosticar y mitigar fallos en la pila de red:

```mermaid
graph TD
    A[Inicio: Ejecución de net_contingency.py] --> B{¿Existe Ruta por Defecto?}
    B -- NO --> C[⚠️ Alerta: Interfaz Desconectada / Sin Gateway]
    B -- SÍ --> D{¿Resuelve DNS google.com?}
    
    D -- SÍ --> E[✅ Red Operativa: Todo OK]
    D -- NO --> F[🚨 Anomalía Detectada: Ruta Activa pero DNS Caído]
    
    F --> G{¿Usuario cuenta con privilegios Root?}
    G -- NO --> H[❌ Error: Sudo requerido para la remediación]
    G -- SÍ --> I[⚙️ Reescritura Atómica: Inyección de Nameservers en /etc/resolv.conf]
    
    I --> J[🔄 Re-verificación de Conectividad]
    J --> E
    
    style E fill:#1b4d3e,stroke:#3cd070,stroke-width:2px,color:#fff
    style C fill:#4a1515,stroke:#e05656,stroke-width:2px,color:#fff
    style H fill:#4a1515,stroke:#e05656,stroke-width:2px,color:#fff
