# GESJ - Sistema de Gestión Educativa
**Provincia de San Juan, República Argentina**

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8+
- MySQL/MariaDB
- pip (gestor de paquetes de Python)

### 2. Instalación de Dependencias
```bash
pip install mysql-connector-python
pip install pillow
pip install openpyxl  # Para exportar a Excel
```

### 3. Configuración de Base de Datos

#### Opción A: MySQL/phpMyAdmin
1. Abrir phpMyAdmin
2. Crear nueva base de datos: `gestion_escolar`
3. Importar archivos SQL en orden:
   - `server/gestion_escolar.sql` (usuarios básicos)
   - `server/calificaciones_schema.sql` (sistema completo)

#### Opción B: Línea de comandos
```bash
mysql -u root -p < server/gestion_escolar.sql
mysql -u root -p < server/calificaciones_schema.sql
```

### 4. Configurar Conexión
Editar `server/database.py` si es necesario:
```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'gestion_escolar',
    'user': 'root',
    'password': '',  # Tu contraseña de MySQL
    'port': 3306
}
```

### 5. Ejecutar la Aplicación
```bash
python main.py
```

## 👥 Usuarios de Prueba

| Rol | Usuario | Contraseña |
|-----|---------|------------|
| Padre | `padre1` | `1234` |
| Docente | `docente1` | `abcd` |
| Preceptor | `preceptor1` | `5678` |
| Administrador | `admin1` | `adminpass` |

## 📁 Estructura del Proyecto

```
GESJ/
├── main.py                 # Archivo principal
├── ui/                     # Interfaz de usuario
│   ├── main_window.py      # Ventana principal
│   ├── auth.py             # Sistema de autenticación
│   ├── user_management.py  # Gestión de usuarios
│   └── sections/           # Secciones por rol
│       ├── padres.py       # Interfaz para padres
│       ├── docentes.py     # Interfaz para docentes
│       ├── preceptores.py  # Interfaz para preceptores
│       └── administradores.py # Interfaz para administradores
├── server/                 # Backend y base de datos
│   ├── database.py         # Conexión a MySQL
│   ├── calificaciones_operations.py # Operaciones de calificaciones
│   ├── email_notifier.py   # Sistema de notificaciones
│   ├── excel_exporter.py   # Exportación a Excel
│   ├── gestion_escolar.sql # Base de datos básica
│   └── calificaciones_schema.sql # Sistema completo
└── README.md               # Este archivo
```

## ✨ Funcionalidades Principales

### 👨‍👩‍👧‍👦 Para Padres
- ✅ Consulta de calificaciones y promedios
- ✅ Seguimiento de asistencia
- ✅ Justificación de inasistencias
- ✅ Mensajería con preceptores
- ✅ Historial académico completo

### 👨‍🏫 Para Docentes
- ✅ Gestión completa de calificaciones
- ✅ Registro por tipos de evaluación
- ✅ Exportación a Excel y PDF
- ✅ Identificación de alumnos en riesgo
- ✅ Notificaciones automáticas

### 👨‍💼 Para Preceptores
- ✅ Dashboard de seguimiento académico
- ✅ Gestión disciplinaria
- ✅ Sistema de alertas configurables
- ✅ Comunicación con padres y docentes
- ✅ Reportes estadísticos

### 🏛️ Para Administradores
- ✅ Dashboard ejecutivo con KPIs
- ✅ Gestión de recursos humanos
- ✅ Control presupuestario
- ✅ Business Intelligence educativo
- ✅ Configuración del sistema

### 📅 Módulo de Asistencia
- ✅ Registro diario de asistencia
- ✅ Control de llegadas tarde
- ✅ Gestión de justificaciones
- ✅ Reportes de asistencia
- ✅ Alertas automáticas por inasistencias

### 📚 Módulo de Biblioteca
- ✅ Catálogo digital de recursos
- ✅ Gestión de préstamos
- ✅ Control de inventario
- ✅ Biblioteca digital
- ✅ Recursos multimedia

### 🎯 Módulo de Eventos
- ✅ Calendario institucional
- ✅ Organización de eventos
- ✅ Actividades extracurriculares
- ✅ Gestión de reuniones
- ✅ Control de participación

### 💬 Módulo de Comunicación
- ✅ Chat en tiempo real
- ✅ Mensajería institucional
- ✅ Anuncios y noticias
- ✅ Foro por materias
- ✅ Notificaciones push

### 📊 Módulo de Evaluaciones
- ✅ Encuestas de satisfacción
- ✅ Evaluación de clima institucional
- ✅ Autoevaluación institucional
- ✅ Planes de mejora continua
- ✅ Indicadores de calidad

## 🔧 Solución de Problemas

### Error de Conexión a MySQL
```
❌ Error al conectar a MySQL: Access denied
```
**Solución**: Verificar credenciales en `server/database.py`

### Error de Módulos
```
❌ ModuleNotFoundError: No module named 'mysql.connector'
```
**Solución**: `pip install mysql-connector-python`

### Error de Base de Datos
```
❌ Table 'usuarios' doesn't exist
```
**Solución**: Importar los archivos SQL en phpMyAdmin

## 📞 Soporte

Para soporte técnico o consultas:
- 📧 Email: soporte@gesj.edu.ar
- 🏛️ Institución: Provincia de San Juan
- 📍 Argentina

---
**GESJ - Conectando las trayectorias escolares hacia un futuro brillante** ✨