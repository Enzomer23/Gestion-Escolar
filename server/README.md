# Servidor de Base de Datos - GESJ

Este directorio contiene los archivos relacionados con la base de datos del sistema GESJ.

## Archivos

- `database.py`: Módulo de conexión y operaciones con MySQL
- `gestion_escolar.sql`: Script SQL para crear la base de datos y tablas iniciales
- `calificaciones_schema.sql`: Sistema completo de gestión de calificaciones
- `calificaciones_operations.py`: Operaciones de base de datos para calificaciones
- `setup_calificaciones.py`: Script de configuración automática

## Configuración de la Base de Datos

### 1. Instalar MySQL/MariaDB

Asegúrate de tener MySQL o MariaDB instalado en tu sistema.

### 2. Crear la Base de Datos

Ejecuta el archivo SQL en tu servidor de base de datos:

```bash
mysql -u root -p < server/gestion_escolar.sql
```

### 3. Configurar Sistema de Calificaciones

```bash
cd server
python setup_calificaciones.py
```

O manualmente:
```bash
mysql -u root -p < server/calificaciones_schema.sql
```

O desde phpMyAdmin:
1. Abre phpMyAdmin
2. Crea una nueva base de datos llamada `gestion_escolar`
3. Importa los archivos `gestion_escolar.sql` y `calificaciones_schema.sql`

### 4. Configurar Conexión

Edita el archivo `database.py` si necesitas cambiar los parámetros de conexión:

```python
DB_CONFIG = {
    'host': '127.0.0.1',
    'database': 'gestion_escolar',
    'user': 'root',  # Cambia si usas otro usuario
    'password': '',  # Cambia por tu contraseña de MySQL
    'port': 3306
}
```

## Usuarios de Prueba

El archivo SQL incluye usuarios de prueba:

- **Padre**: usuario: `padre1`, contraseña: `1234`
- **Docente**: usuario: `docente1`, contraseña: `abcd`
- **Preceptor**: usuario: `preceptor1`, contraseña: `5678`
- **Administrativo**: usuario: `admin1`, contraseña: `adminpass`

## Sistema de Calificaciones

### Características Principales

- ✅ **Gestión de Alumnos**: Registro y seguimiento de estudiantes por curso
- ✅ **Materias por Docente**: Asignación de materias específicas a cada docente
- ✅ **Períodos de Evaluación**: Cuatrimestres y períodos académicos
- ✅ **Tipos de Evaluación**: Diaria, mensual, cuatrimestral con pesos específicos
- ✅ **Registro de Calificaciones**: Sistema completo de notas con observaciones
- ✅ **Cálculo Automático de Promedios**: Promedios por materia y general
- ✅ **Reportes y Estadísticas**: Análisis de rendimiento académico
- ✅ **Alumnos en Riesgo**: Identificación automática de estudiantes con bajo rendimiento
- ✅ **Interfaz Intuitiva**: Ventana dedicada para docentes con todas las funcionalidades

### Tablas del Sistema

- `alumnos`: Información de estudiantes
- `materias`: Materias por curso y docente
- `calificaciones`: Registro de notas
- `periodos_evaluacion`: Períodos académicos
- `tipos_evaluacion`: Tipos de evaluación
- `promedios_alumnos`: Promedios calculados (optimización)

### Vistas y Funciones

- `vista_calificaciones`: Consulta completa de calificaciones
- `vista_promedios`: Promedios por alumno y materia
- `CalcularPromedios()`: Procedimiento para actualizar promedios
- `PromedioGeneralAlumno()`: Función para calcular promedio general

## Estructura de la Base de Datos

### Tabla `usuarios`
- `id`: Identificador único (AUTO_INCREMENT)
- `nombre_usuario`: Nombre de usuario (UNIQUE)
- `contrasena`: Contraseña del usuario
- `tipo_usuario`: Rol del usuario (Padre, Docente, Preceptor, Administrativo)