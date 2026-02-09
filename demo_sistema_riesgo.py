#!/usr/bin/env python3
"""
DEMOSTRACIÓN DEL SISTEMA DE IDENTIFICACIÓN DE RIESGO ACADÉMICO
GESJ - Plataforma de Gestión Educativa
Provincia de San Juan, República Argentina

Este script demuestra cómo funciona el sistema de identificación temprana
de estudiantes en riesgo académico.
"""

import sys
import os
from datetime import datetime, date
import time

# Agregar el directorio actual al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def mostrar_banner():
    """Mostrar banner del sistema"""
    print("=" * 80)
    print("🏛️  GESJ - SISTEMA DE GESTIÓN EDUCATIVA")
    print("📍 Provincia de San Juan, República Argentina")
    print("=" * 80)
    print("🎯 DEMOSTRACIÓN: Sistema de Identificación de Riesgo Académico")
    print("=" * 80)
    print()

def simular_carga_datos():
    """Simular carga de datos del sistema"""
    print("🔄 Iniciando sistema...")
    time.sleep(1)
    
    print("📊 Cargando datos de alumnos...")
    time.sleep(1)
    
    print("📚 Cargando calificaciones...")
    time.sleep(1)
    
    print("📋 Cargando registros de asistencia...")
    time.sleep(1)
    
    print("✅ Sistema listo para análisis")
    print()

def mostrar_datos_ejemplo():
    """Mostrar datos de ejemplo del sistema"""
    print("📊 DATOS ACTUALES EN EL SISTEMA:")
    print("-" * 50)
    
    # Datos de ejemplo que coinciden con la base de datos
    alumnos_data = [
        {
            "id": 1, "nombre": "Juan Pérez", "curso": "1º Año A",
            "promedio": 8.08, "asistencia": 95, "estado": "✅ Buen rendimiento"
        },
        {
            "id": 2, "nombre": "Ana Gómez", "curso": "2º Año A", 
            "promedio": 8.67, "asistencia": 98, "estado": "✅ Excelente rendimiento"
        },
        {
            "id": 3, "nombre": "Carlos Martínez", "curso": "3º Año A",
            "promedio": 6.92, "asistencia": 85, "estado": "⚠️ Rendimiento regular"
        },
        {
            "id": 4, "nombre": "Laura Díaz", "curso": "1º Año A",
            "promedio": 8.92, "asistencia": 97, "estado": "✅ Excelente rendimiento"
        },
        {
            "id": 5, "nombre": "Mario González", "curso": "2º Año A",
            "promedio": 6.00, "asistencia": 78, "estado": "🚨 EN RIESGO ACADÉMICO"
        },
        {
            "id": 6, "nombre": "Pedro Rodríguez", "curso": "1º Año B",
            "promedio": 5.5, "asistencia": 72, "estado": "🚨 EN RIESGO ACADÉMICO"
        },
        {
            "id": 7, "nombre": "Lucas Herrera", "curso": "3º Año B",
            "promedio": 4.9, "asistencia": 68, "estado": "🚨 RIESGO CRÍTICO"
        }
    ]
    
    print(f"{'ID':<3} {'Alumno':<20} {'Curso':<10} {'Promedio':<9} {'Asist%':<7} {'Estado'}")
    print("-" * 80)
    
    for alumno in alumnos_data:
        print(f"{alumno['id']:<3} {alumno['nombre']:<20} {alumno['curso']:<10} "
              f"{alumno['promedio']:<9.2f} {alumno['asistencia']:<7}% {alumno['estado']}")
    
    print()
    return alumnos_data

def analizar_riesgo_academico(alumnos_data):
    """Analizar y mostrar estudiantes en riesgo"""
    print("🔍 ANÁLISIS DE RIESGO ACADÉMICO:")
    print("-" * 50)
    
    # Criterios de riesgo
    criterios = {
        "promedio_minimo": 6.0,
        "asistencia_minima": 80.0
    }
    
    print(f"📋 Criterios de identificación:")
    print(f"   • Promedio mínimo: {criterios['promedio_minimo']}")
    print(f"   • Asistencia mínima: {criterios['asistencia_minima']}%")
    print()
    
    # Identificar alumnos en riesgo
    alumnos_riesgo = []
    alumnos_critico = []
    
    for alumno in alumnos_data:
        en_riesgo = False
        nivel_riesgo = []
        
        if alumno['promedio'] < criterios['promedio_minimo']:
            en_riesgo = True
            nivel_riesgo.append(f"Promedio bajo ({alumno['promedio']:.2f})")
        
        if alumno['asistencia'] < criterios['asistencia_minima']:
            en_riesgo = True
            nivel_riesgo.append(f"Asistencia baja ({alumno['asistencia']}%)")
        
        if en_riesgo:
            alumno['motivos_riesgo'] = nivel_riesgo
            if alumno['promedio'] < 5.0 or alumno['asistencia'] < 70:
                alumnos_critico.append(alumno)
            else:
                alumnos_riesgo.append(alumno)
    
    return alumnos_riesgo, alumnos_critico

def mostrar_alumnos_riesgo(alumnos_riesgo, alumnos_critico):
    """Mostrar resultados del análisis de riesgo"""
    print("🚨 ESTUDIANTES IDENTIFICADOS EN RIESGO:")
    print("=" * 60)
    
    if alumnos_critico:
        print("🔴 RIESGO CRÍTICO (Requiere intervención inmediata):")
        print("-" * 60)
        for alumno in alumnos_critico:
            print(f"👤 {alumno['nombre']} - {alumno['curso']}")
            print(f"   📊 Promedio: {alumno['promedio']:.2f}")
            print(f"   📋 Asistencia: {alumno['asistencia']}%")
            print(f"   ⚠️  Motivos: {', '.join(alumno['motivos_riesgo'])}")
            print()
    
    if alumnos_riesgo:
        print("🟡 RIESGO MODERADO (Requiere seguimiento):")
        print("-" * 60)
        for alumno in alumnos_riesgo:
            print(f"👤 {alumno['nombre']} - {alumno['curso']}")
            print(f"   📊 Promedio: {alumno['promedio']:.2f}")
            print(f"   📋 Asistencia: {alumno['asistencia']}%")
            print(f"   ⚠️  Motivos: {', '.join(alumno['motivos_riesgo'])}")
            print()
    
    if not alumnos_riesgo and not alumnos_critico:
        print("✅ ¡Excelente! No se detectaron estudiantes en riesgo académico.")
        print()

def simular_acciones_automaticas(alumnos_riesgo, alumnos_critico):
    """Simular las acciones automáticas del sistema"""
    total_riesgo = len(alumnos_riesgo) + len(alumnos_critico)
    
    if total_riesgo == 0:
        print("✅ No se requieren acciones automáticas.")
        return
    
    print("🤖 ACCIONES AUTOMÁTICAS DEL SISTEMA:")
    print("=" * 50)
    
    print("📧 Generando notificaciones automáticas...")
    time.sleep(1)
    
    # Simular envío de emails
    print("📨 Enviando alertas a preceptores:")
    preceptores = ["preceptor1@gesj.edu.ar", "preceptor.general@gesj.edu.ar"]
    for email in preceptores:
        print(f"   ✅ Enviado a: {email}")
        time.sleep(0.5)
    
    print()
    print("📨 Enviando notificaciones a padres:")
    for alumno in alumnos_riesgo + alumnos_critico:
        email_padre = f"padre.{alumno['nombre'].split()[0].lower()}@gmail.com"
        print(f"   ✅ Enviado a: {email_padre} (Padre de {alumno['nombre']})")
        time.sleep(0.5)
    
    print()
    print("📊 Generando reportes automáticos...")
    time.sleep(1)
    
    reportes = [
        "Reporte_Alumnos_Riesgo_2025.xlsx",
        "Estadisticas_Rendimiento_Academico.xlsx",
        "Plan_Intervencion_Sugerido.xlsx"
    ]
    
    for reporte in reportes:
        print(f"   📄 Generado: {reporte}")
        time.sleep(0.5)
    
    print()

def mostrar_planes_intervencion(alumnos_riesgo, alumnos_critico):
    """Mostrar planes de intervención sugeridos"""
    total_riesgo = len(alumnos_riesgo) + len(alumnos_critico)
    
    if total_riesgo == 0:
        return
    
    print("📋 PLANES DE INTERVENCIÓN SUGERIDOS:")
    print("=" * 50)
    
    planes = {
        "critico": [
            "🔴 Evaluación psicopedagógica inmediata",
            "🔴 Plan de recuperación intensiva",
            "🔴 Reunión urgente con padres",
            "🔴 Seguimiento semanal personalizado"
        ],
        "moderado": [
            "🟡 Tutoría académica adicional",
            "🟡 Plan de reforzamiento",
            "🟡 Comunicación con padres",
            "🟡 Seguimiento quincenal"
        ]
    }
    
    if alumnos_critico:
        print("🔴 Para estudiantes en RIESGO CRÍTICO:")
        for plan in planes["critico"]:
            print(f"   {plan}")
        print()
    
    if alumnos_riesgo:
        print("🟡 Para estudiantes en RIESGO MODERADO:")
        for plan in planes["moderado"]:
            print(f"   {plan}")
        print()

def mostrar_estadisticas_generales(alumnos_data, alumnos_riesgo, alumnos_critico):
    """Mostrar estadísticas generales del análisis"""
    total_alumnos = len(alumnos_data)
    total_riesgo = len(alumnos_riesgo) + len(alumnos_critico)
    total_ok = total_alumnos - total_riesgo
    
    print("📈 ESTADÍSTICAS GENERALES:")
    print("=" * 40)
    print(f"👥 Total de estudiantes: {total_alumnos}")
    print(f"✅ Sin riesgo académico: {total_ok} ({(total_ok/total_alumnos)*100:.1f}%)")
    print(f"🟡 Riesgo moderado: {len(alumnos_riesgo)} ({(len(alumnos_riesgo)/total_alumnos)*100:.1f}%)")
    print(f"🔴 Riesgo crítico: {len(alumnos_critico)} ({(len(alumnos_critico)/total_alumnos)*100:.1f}%)")
    print(f"🚨 Total en riesgo: {total_riesgo} ({(total_riesgo/total_alumnos)*100:.1f}%)")
    print()
    
    # Promedio general
    promedio_general = sum(a['promedio'] for a in alumnos_data) / len(alumnos_data)
    asistencia_general = sum(a['asistencia'] for a in alumnos_data) / len(alumnos_data)
    
    print(f"📊 Promedio general del curso: {promedio_general:.2f}")
    print(f"📋 Asistencia promedio: {asistencia_general:.1f}%")
    print()

def mostrar_beneficios_sistema():
    """Mostrar los beneficios del sistema digitalizado"""
    print("🎯 BENEFICIOS DEL SISTEMA DIGITALIZADO:")
    print("=" * 50)
    
    beneficios = [
        "✅ Identificación automática y temprana de estudiantes en riesgo",
        "✅ Reducción de errores humanos en cálculos y registros",
        "✅ Notificaciones automáticas a preceptores y padres",
        "✅ Generación automática de reportes y estadísticas",
        "✅ Seguimiento integral de trayectorias escolares",
        "✅ Planes de intervención personalizados",
        "✅ Comunicación eficiente entre docentes, preceptores y padres",
        "✅ Ahorro de tiempo en procesos administrativos",
        "✅ Mejor toma de decisiones basada en datos",
        "✅ Intervención oportuna para mejorar el rendimiento académico"
    ]
    
    for beneficio in beneficios:
        print(f"   {beneficio}")
        time.sleep(0.3)
    
    print()

def main():
    """Función principal de la demostración"""
    try:
        mostrar_banner()
        
        print("🚀 Iniciando demostración del sistema...")
        print()
        
        # Simular carga del sistema
        simular_carga_datos()
        
        # Mostrar datos actuales
        alumnos_data = mostrar_datos_ejemplo()
        
        # Analizar riesgo académico
        alumnos_riesgo, alumnos_critico = analizar_riesgo_academico(alumnos_data)
        
        # Mostrar resultados
        mostrar_alumnos_riesgo(alumnos_riesgo, alumnos_critico)
        
        # Simular acciones automáticas
        simular_acciones_automaticas(alumnos_riesgo, alumnos_critico)
        
        # Mostrar planes de intervención
        mostrar_planes_intervencion(alumnos_riesgo, alumnos_critico)
        
        # Mostrar estadísticas
        mostrar_estadisticas_generales(alumnos_data, alumnos_riesgo, alumnos_critico)
        
        # Mostrar beneficios
        mostrar_beneficios_sistema()
        
        print("🎉 DEMOSTRACIÓN COMPLETADA")
        print("=" * 50)
        print("💡 Para ver el sistema completo en funcionamiento:")
        print("   1. Ejecuta: python main.py")
        print("   2. Login como docente: docente1 / abcd")
        print("   3. Explora 'Sistema de Calificaciones Avanzado'")
        print("   4. Prueba 'Alumnos en Riesgo' y 'Exportar a Excel'")
        print()
        print("✨ ¡El sistema GESJ está listo para identificar y ayudar")
        print("   a estudiantes en riesgo académico!")
        
    except KeyboardInterrupt:
        print("\n\n⏹️  Demostración interrumpida por el usuario.")
    except Exception as e:
        print(f"\n❌ Error durante la demostración: {e}")

if __name__ == "__main__":
    main()