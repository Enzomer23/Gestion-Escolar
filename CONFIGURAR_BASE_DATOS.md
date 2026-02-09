# 🗄️ CONFIGURAR BASE DE DATOS MYSQL - GESJ

## 🎯 **PASOS PARA ACTIVAR LA BASE DE DATOS REAL**

### **1️⃣ INSTALAR MYSQL**
```bash
# Opción A: XAMPP (Recomendado para Windows)
# Descargar desde: https://www.apachefriends.org/

# Opción B: MySQL directo
# Descargar desde: https://dev.mysql.com/downloads/
```

### **2️⃣ INSTALAR LIBRERÍA PYTHON**
```bash
pip install mysql-connector-python
```

### **3️⃣ CREAR BASE DE DATOS**

**Opción A: Con phpMyAdmin (XAMPP)**
1. Abrir http://localhost/phpmyadmin
2. Crear base de datos: `gestion_escolar`
3. Importar archivo: `supabase/migrations/20250726220923_tiny_resonance.sql`

**Opción B: Línea de comandos**
```bash
mysql -u root -p < supabase/migrations/20250726220923_tiny_resonance.sql
```

### **4️⃣ CONFIGURAR CONEXIÓN**

Editar `server/database.py`:
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'gestion_escolar',
    'user': 'root',
    'password': '',  # Tu contraseña de MySQL
    'port': 3306
}
```

### **5️⃣ PROBAR CONEXIÓN**
```bash
python server/test_connection.py
```

## ✅ **USUARIOS DE PRUEBA**
- **Padre**: `padre1` / `1234`
- **Docente**: `docente1` / `abcd`
- **Preceptor**: `preceptor1` / `5678`
- **Admin**: `admin1` / `adminpass`

## 🎉 **RESULTADO**
Cuando funcione verás:
```
✅ Base de datos conectada. X usuarios encontrados.
```

En lugar de:
```
❌ Módulo de base de datos no disponible. Usando datos de ejemplo.
```