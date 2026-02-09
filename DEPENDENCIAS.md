# 📚 LIBRERÍAS DEL SISTEMA GESJ

## 🎯 **RESUMEN EJECUTIVO**
El sistema GESJ utiliza **4 librerías principales** + librerías estándar de Python.

---

## 📦 **LIBRERÍAS PRINCIPALES**

### **1. 🗄️ BASE DE DATOS**
```python
import mysql.connector
from mysql.connector import Error
```
- **Librería**: `mysql-connector-python`
- **Versión**: 8.2.0
- **Propósito**: Conexión y operaciones con MySQL/MariaDB
- **Instalación**: `pip install mysql-connector-python`
- **Estado**: ✅ **OBLIGATORIA**

### **2. 🖥️ INTERFAZ GRÁFICA**
```python
import tkinter as tk
from tkinter import messagebox, ttk, filedialog
```
- **Librería**: `tkinter`
- **Versión**: Incluida en Python
- **Propósito**: Interfaz gráfica de usuario (GUI)
- **Instalación**: ✅ **Ya incluida en Python**
- **Estado**: ✅ **OBLIGATORIA**

### **3. 📊 EXPORTACIÓN EXCEL**
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
```
- **Librería**: `openpyxl`
- **Versión**: 3.1.2
- **Propósito**: Crear y exportar archivos Excel (.xlsx)
- **Instalación**: `pip install openpyxl`
- **Estado**: 🟡 **RECOMENDADA**

### **4. 🖼️ MANEJO DE IMÁGENES**
```python
from PIL import Image, ImageTk
```
- **Librería**: `Pillow`
- **Versión**: 10.1.0
- **Propósito**: Cargar y redimensionar imágenes en la interfaz
- **Instalación**: `pip install Pillow`
- **Estado**: 🟡 **RECOMENDADA**

---

## 📄 **LIBRERÍAS OPCIONALES**

### **5. 📑 EXPORTACIÓN PDF**
```python
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Table
```
- **Librería**: `reportlab`
- **Versión**: 4.0.7
- **Propósito**: Generar reportes en formato PDF
- **Instalación**: `pip install reportlab`
- **Estado**: 🔵 **OPCIONAL** (Requiere compilación)

---

## 🐍 **LIBRERÍAS ESTÁNDAR DE PYTHON**

### **Incluidas automáticamente:**
```python
import os           # Manejo del sistema operativo
import sys          # Configuración del sistema Python
import datetime     # Manejo de fechas y horas
from datetime import datetime, date
from typing import List, Dict, Optional, Tuple  # Type hints
import subprocess   # Ejecutar comandos del sistema
import platform     # Información del sistema operativo
```

---

## 📧 **LIBRERÍAS DE NOTIFICACIONES**

### **Para el sistema de emails:**
```python
import smtplib                    # Servidor SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
```
- **Estado**: ✅ **Incluidas en Python**
- **Propósito**: Sistema de notificaciones por email

---

## 🚀 **INSTALACIÓN RÁPIDA**

### **Opción 1: Archivo requirements.txt**
```bash
pip install -r requirements.txt
```

### **Opción 2: Instalación individual**
```bash
# Obligatorias
pip install mysql-connector-python

# Recomendadas
pip install openpyxl
pip install Pillow

# Opcional (solo si quieres PDF)
pip install reportlab
```

### **Opción 3: Instalación mínima**
```bash
# Solo lo esencial para que funcione
pip install mysql-connector-python
```

---

## ✅ **VERIFICACIÓN DE INSTALACIÓN**

### **Script de verificación:**
```python
def verificar_dependencias():
    try:
        import mysql.connector
        print("✅ mysql-connector-python: OK")
    except ImportError:
        print("❌ mysql-connector-python: FALTA")
    
    try:
        import tkinter
        print("✅ tkinter: OK")
    except ImportError:
        print("❌ tkinter: FALTA")
    
    try:
        import openpyxl
        print("✅ openpyxl: OK")
    except ImportError:
        print("🟡 openpyxl: OPCIONAL")
    
    try:
        from PIL import Image
        print("✅ Pillow: OK")
    except ImportError:
        print("🟡 Pillow: OPCIONAL")

verificar_dependencias()
```

---

## 📊 **ESTADÍSTICAS DE LIBRERÍAS**

| Categoría | Cantidad | Estado |
|-----------|----------|--------|
| **Obligatorias** | 2 | ✅ Críticas |
| **Recomendadas** | 2 | 🟡 Mejoran funcionalidad |
| **Opcionales** | 1 | 🔵 Características extra |
| **Estándar Python** | 8+ | ✅ Incluidas |
| **Total** | 13+ | 🎯 Sistema completo |

---

## 🎯 **RECOMENDACIÓN FINAL**

### **Para uso básico:**
```bash
pip install mysql-connector-python
```

### **Para uso completo:**
```bash
pip install mysql-connector-python openpyxl Pillow
```

### **Para uso profesional:**
```bash
pip install mysql-connector-python openpyxl Pillow reportlab
```

---

## 💡 **NOTAS IMPORTANTES**

1. **tkinter**: Ya viene con Python, no necesita instalación
2. **mysql-connector-python**: Esencial para la base de datos
3. **openpyxl**: Muy recomendada para exportar calificaciones
4. **Pillow**: Necesaria para las imágenes de la interfaz
5. **reportlab**: Solo si quieres exportación PDF (opcional)

¡Con estas librerías el sistema GESJ funciona perfectamente! 🚀