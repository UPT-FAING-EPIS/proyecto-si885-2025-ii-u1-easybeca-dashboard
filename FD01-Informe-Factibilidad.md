<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *{Nombre de Proyecto}***

Curso: *{Nombre de Asignatura}*

Docente: *{Nombre de Docente}*

Integrantes:

***{Apellidos y nombres del estudiante (código universitario)}***

**Tacna – Perú**

***{Año}***

**  
**
</center>
<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

Sistema *{Nombre del Sistema}*

Informe de Factibilidad

Versión *{1.0}*

|CONTROL DE VERSIONES||||||
| :-: | :- | :- | :- | :- | :- |
|Versión|Hecha por|Revisada por|Aprobada por|Fecha|Motivo|
|1\.0|MPV|ELV|ARV|10/10/2020|Versión Original|

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

## ÍNDICE GENERAL

1. **Descripción del Proyecto** ......................................................... 3
   - 1.1. Nombre del proyecto
   - 1.2. Duración del proyecto
   - 1.3. Descripción
   - 1.4. Objetivos
     - 1.4.1 Objetivo general
     - 1.4.2 Objetivos específicos

2. **Riesgos** ......................................................................... 5

3. **Análisis de la Situación Actual** ................................................ 6
   - 3.1. Planteamiento del problema
   - 3.2. Consideraciones de hardware y software

4. **Estudio de Factibilidad** ......................................................... 8
   - 4.1. Factibilidad Técnica
   - 4.2. Factibilidad Económica
     - 4.2.1. Costos Generales
     - 4.2.2. Costos operativos durante el desarrollo
     - 4.2.3. Costos del ambiente
     - 4.2.4. Costos de personal
     - 4.2.5. Costos totales del desarrollo del sistema
   - 4.3. Factibilidad Operativa
   - 4.4. Factibilidad Legal
   - 4.5. Factibilidad Social
   - 4.6. Factibilidad Ambiental

5. **Análisis Financiero** ............................................................ 15

6. **Conclusiones** ................................................................... 16

---

## 1. DESCRIPCIÓN DEL PROYECTO

### 1.1. Nombre del proyecto

**"BecasPerú Analytics Dashboard - Sistema Inteligente de Análisis y Visualización de Becas Educativas"**

### 1.2. Duración del proyecto

**Duración total:** 6 meses (24 semanas)

**Fases del proyecto:**
- **Fase 1 - Análisis y Diseño:** 4 semanas
- **Fase 2 - Desarrollo del Backend:** 8 semanas
- **Fase 3 - Desarrollo del Frontend:** 6 semanas
- **Fase 4 - Integración con Power BI:** 3 semanas
- **Fase 5 - Pruebas y Despliegue:** 2 semanas
- **Fase 6 - Documentación y Capacitación:** 1 semana

### 1.3. Descripción

**En qué consiste el proyecto:**

El proyecto "BecasPerú Analytics Dashboard" consiste en el desarrollo de un sistema integral de inteligencia de negocios que automatiza la recopilación, procesamiento y análisis de información sobre becas educativas disponibles en el Perú. El sistema utiliza técnicas de web scraping para extraer datos de múltiples fuentes oficiales, los procesa y almacena en una base de datos estructurada, y presenta la información a través de dashboards interactivos desarrollados en Power BI.

**Importancia del proyecto:**

En el contexto educativo peruano, existe una gran dispersión de información sobre oportunidades de becas, lo que dificulta el acceso equitativo a la educación superior. Estudiantes de bajos recursos económicos frecuentemente pierden oportunidades por falta de información centralizada y actualizada. Este proyecto democratiza el acceso a la información educativa y contribuye a reducir la brecha de desigualdad en la educación superior.

**Contexto en que se va a desenvolver:**

El proyecto se desarrolla en el marco académico de la Universidad Privada de Tacna, específicamente para el curso de Inteligencia de Negocios. Sin embargo, tiene proyección de implementación real para beneficiar a estudiantes de todo el Perú. El sistema se enfoca inicialmente en becas de PRONABEC, Banco de Crédito del Perú, y universidades públicas y privadas.

### 1.4. Objetivos

#### 1.4.1 Objetivo General

Desarrollar un sistema de inteligencia de negocios que automatice la recopilación, análisis y visualización de información sobre becas educativas en el Perú, proporcionando una plataforma centralizada que facilite el acceso a oportunidades educativas para estudiantes de todos los niveles socioeconómicos.

#### 1.4.2 Objetivos Específicos

1. **Automatizar la recopilación de datos:**
   - Implementar scrapers web para extraer información de al menos 5 fuentes oficiales de becas
   - Lograr una actualización automática de datos cada 24 horas
   - Garantizar una precisión del 95% en la extracción de datos

2. **Desarrollar una base de datos robusta:**
   - Diseñar e implementar una base de datos MySQL optimizada para consultas analíticas
   - Establecer un sistema de respaldo automático diario
   - Implementar validación de datos para garantizar integridad

3. **Crear dashboards interactivos:**
   - Desarrollar al menos 5 dashboards especializados en Power BI
   - Implementar filtros dinámicos por región, tipo de beca, y nivel educativo
   - Lograr tiempos de carga menores a 3 segundos

4. **Implementar análisis predictivo:**
   - Desarrollar modelos para predecir tendencias en convocatorias
   - Crear alertas automáticas para nuevas oportunidades
   - Implementar análisis de patrones históricos

5. **Garantizar accesibilidad y usabilidad:**
   - Desarrollar una interfaz web responsive
   - Implementar funcionalidades de accesibilidad (WCAG 2.1)
   - Lograr una puntuación de usabilidad superior a 4.0/5.0

---

## 2. RIESGOS

Los siguientes riesgos han sido identificados como potenciales amenazas para el éxito del proyecto:

### Riesgos Técnicos

| Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
|--------|--------------|---------|-------------------------|
| **Cambios en estructura de sitios web** | Alta (80%) | Alto | Implementar monitoreo automático y sistema de notificaciones para cambios |
| **Fallas en el scraping por medidas anti-bot** | Media (60%) | Alto | Usar proxies rotativos, delays aleatorios y headers realistas |
| **Sobrecarga del servidor de base de datos** | Media (40%) | Medio | Implementar cache, optimización de consultas y monitoreo de performance |
| **Pérdida de datos por fallas del sistema** | Baja (20%) | Alto | Sistema de backup automático cada 6 horas y replicación |

### Riesgos de Proyecto

| Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
|--------|--------------|---------|-------------------------|
| **Retrasos en el cronograma** | Media (50%) | Medio | Buffer de tiempo del 20% en cada fase crítica |
| **Falta de experiencia del equipo** | Media (60%) | Medio | Capacitación continua y mentoría técnica |
| **Cambios en requerimientos** | Baja (30%) | Medio | Metodología ágil con sprints cortos |
| **Problemas de integración con Power BI** | Media (40%) | Alto | Pruebas de integración tempranas y documentación detallada |

### Riesgos Externos

| Riesgo | Probabilidad | Impacto | Estrategia de Mitigación |
|--------|--------------|---------|-------------------------|
| **Cambios en políticas de acceso a datos** | Baja (25%) | Alto | Diversificar fuentes de datos y mantener contacto con instituciones |
| **Problemas de conectividad a internet** | Media (45%) | Medio | Implementar modo offline y sincronización posterior |
| **Restricciones legales sobre scraping** | Baja (20%) | Alto | Revisar términos de servicio y implementar APIs cuando estén disponibles |

---

## 3. ANÁLISIS DE LA SITUACIÓN ACTUAL

### 3.1. Planteamiento del problema

**Antecedentes:**

En el Perú, existen múltiples instituciones que ofrecen becas educativas: PRONABEC (Programa Nacional de Becas y Crédito Educativo), bancos privados como el BCP, universidades públicas y privadas, fundaciones, y organizaciones internacionales. Sin embargo, la información sobre estas oportunidades se encuentra dispersa en diferentes sitios web, con formatos heterogéneos y frecuencias de actualización variables.

**Situación actual:**

Actualmente, los estudiantes que buscan becas deben:
1. Visitar múltiples sitios web individualmente
2. Revisar manualmente cada convocatoria
3. Comparar requisitos y beneficios sin herramientas de análisis
4. Mantenerse actualizados sobre nuevas convocatorias sin sistema de alertas
5. Tomar decisiones sin acceso a análisis históricos o predictivos

**Problemática identificada:**

1. **Dispersión de información:** No existe una fuente centralizada de información sobre becas
2. **Falta de actualización:** Los estudiantes pierden oportunidades por información desactualizada
3. **Ausencia de análisis:** No hay herramientas para analizar tendencias o patrones
4. **Inequidad en el acceso:** Estudiantes de zonas rurales o con menor acceso tecnológico están en desventaja
5. **Ineficiencia en la búsqueda:** El proceso manual consume tiempo valioso de estudio

**Necesidad que será resuelta:**

El proyecto resolverá estas problemáticas mediante:
- Centralización automática de información de becas
- Actualización en tiempo real de convocatorias
- Análisis inteligente de datos para identificar oportunidades
- Democratización del acceso a información educativa
- Optimización del tiempo de búsqueda de becas

### 3.2. Consideraciones de hardware y software

**Hardware existente y alcanzable:**

**Equipos de desarrollo:**
- Laptops con procesador Intel i5 o superior (disponible)
- 8GB RAM mínimo, 16GB recomendado (disponible)
- 500GB de almacenamiento SSD (disponible)
- Conexión a internet estable de 50 Mbps (disponible)

**Servidor de producción:**
- VPS con 4 vCPUs, 8GB RAM, 100GB SSD (costo: $50/mes)
- Alternativa: Servidor local con especificaciones similares
- Sistema de backup externo (Google Drive Business o similar)

**Software posible para implementación:**

**Tecnologías de desarrollo:**
- **Python 3.9+:** Lenguaje principal para backend y scraping
- **FastAPI:** Framework web moderno y eficiente
- **Beautiful Soup + Selenium:** Librerías para web scraping
- **MySQL 8.0:** Base de datos relacional principal
- **SQLite:** Base de datos local para desarrollo

**Herramientas de análisis:**
- **Power BI Desktop:** Herramienta principal de visualización (licencia educativa gratuita)
- **Pandas + NumPy:** Procesamiento y análisis de datos
- **Scikit-learn:** Machine learning para análisis predictivo

**Infraestructura:**
- **Docker:** Containerización para despliegue
- **Git + GitHub:** Control de versiones
- **VS Code:** Entorno de desarrollo integrado
- **Postman:** Testing de APIs

**Evaluación de tecnología utilizable:**

| Tecnología | Disponibilidad | Costo | Viabilidad | Justificación |
|------------|----------------|-------|------------|---------------|
| **Python** | Alta | Gratuito | Alta | Ecosistema robusto para scraping y análisis |
| **MySQL** | Alta | Gratuito | Alta | Base de datos confiable y escalable |
| **Power BI** | Media | Educativa gratuita | Alta | Herramienta líder en visualización |
| **FastAPI** | Alta | Gratuito | Alta | Framework moderno con documentación automática |
| **Docker** | Alta | Gratuito | Media | Facilita despliegue y escalabilidad |

---

## 4. ESTUDIO DE FACTIBILIDAD

**Resultados esperados del estudio de factibilidad:**

Se espera demostrar que el proyecto "BecasPerú Analytics Dashboard" es viable desde las perspectivas técnica, económica, operativa, legal, social y ambiental. El estudio proporcionará una base sólida para la toma de decisiones sobre la implementación del proyecto.

**Actividades realizadas para la evaluación:**

1. Análisis de tecnologías disponibles y requerimientos técnicos
2. Estimación detallada de costos de desarrollo e implementación
3. Evaluación de capacidades operativas del equipo y la institución
4. Revisión de marco legal y normativo aplicable
5. Análisis de impacto social y beneficiarios potenciales
6. Evaluación de impacto ambiental del proyecto

**Aprobación:**

Este estudio ha sido preparado bajo la supervisión del Ing. Patrick Cuadros, docente del curso de Inteligencia de Negocios de la Universidad Privada de Tacna.

### 4.1. Factibilidad Técnica

**Evaluación de recursos tecnológicos disponibles:**

El análisis técnico demuestra que el proyecto es completamente viable con la tecnología actual disponible. Se han identificado todas las herramientas necesarias y se cuenta con el conocimiento técnico requerido.

**Hardware requerido:**

**Equipos de desarrollo:**
- **Computadoras personales:** Disponibles (2 laptops con i5, 8GB RAM)
- **Capacidad de almacenamiento:** 500GB SSD por equipo (suficiente)
- **Conectividad:** Internet banda ancha 50 Mbps (disponible)

**Servidor de producción:**
- **Especificaciones mínimas:** 4 vCPUs, 8GB RAM, 100GB SSD
- **Opciones evaluadas:**
  - VPS en DigitalOcean: $50/mes
  - AWS EC2 t3.medium: $45/mes
  - Servidor local: Inversión única de $800
- **Recomendación:** VPS por flexibilidad y mantenimiento

**Software y aplicaciones:**

**Sistema operativo:**
- **Desarrollo:** Windows 11 (disponible)
- **Producción:** Ubuntu 20.04 LTS (gratuito)
- **Compatibilidad:** Todas las tecnologías son multiplataforma

**Navegadores soportados:**
- Chrome 90+ (para scraping y testing)
- Firefox 88+ (testing adicional)
- Edge 90+ (compatibilidad empresarial)

**Infraestructura de red:**
- **Conexión a internet:** Fibra óptica 50 Mbps (disponible)
- **Backup de conectividad:** Datos móviles 4G (disponible)
- **Seguridad:** VPN institucional (disponible)

**Dominio e hosting:**
- **Dominio:** becasperu.com (disponible, $15/año)
- **Certificado SSL:** Let's Encrypt (gratuito)
- **CDN:** Cloudflare (plan gratuito disponible)

**Evaluación de viabilidad técnica:**

| Componente | Disponibilidad | Complejidad | Riesgo | Evaluación |
|------------|----------------|-------------|--------|------------|
| **Web Scraping** | Alta | Media | Medio | Viable con monitoreo |
| **Base de datos** | Alta | Baja | Bajo | Completamente viable |
| **API REST** | Alta | Baja | Bajo | Tecnología madura |
| **Power BI** | Alta | Media | Bajo | Licencia educativa disponible |
| **Despliegue** | Alta | Media | Medio | Docker simplifica proceso |

**Conclusión técnica:** El proyecto es técnicamente viable con un riesgo bajo a medio, utilizando tecnologías probadas y con amplio soporte de la comunidad.

### 4.2. Factibilidad Económica

**Propósito del análisis económico:**

Determinar si los beneficios económicos y sociales del proyecto justifican la inversión requerida, considerando tanto costos directos como indirectos del desarrollo e implementación.

**Evaluación de infraestructura existente:**

La institución cuenta con la infraestructura básica necesaria (computadoras, internet, software de desarrollo), lo que reduce significativamente la inversión inicial requerida.

#### 4.2.1. Costos Generales

**Material de oficina y accesorios:**

| Concepto | Cantidad | Precio Unitario | Total |
|----------|----------|-----------------|-------|
| **Papel bond A4** | 2 millares | S/. 25.00 | S/. 50.00 |
| **Cartuchos de tinta** | 4 unidades | S/. 45.00 | S/. 180.00 |
| **Útiles de escritorio** | 1 set | S/. 80.00 | S/. 80.00 |
| **Folders y archivadores** | 10 unidades | S/. 8.00 | S/. 80.00 |
| **USB 64GB** | 2 unidades | S/. 35.00 | S/. 70.00 |
| **Disco duro externo 1TB** | 1 unidad | S/. 250.00 | S/. 250.00 |
| **Cable HDMI** | 2 unidades | S/. 25.00 | S/. 50.00 |
| **Mouse y teclado backup** | 1 set | S/. 120.00 | S/. 120.00 |
| **Webcam HD** | 1 unidad | S/. 150.00 | S/. 150.00 |
| **Audífonos** | 2 unidades | S/. 80.00 | S/. 160.00 |
| **SUBTOTAL COSTOS GENERALES** | | | **S/. 1,190.00** |

#### 4.2.2. Costos operativos durante el desarrollo

**Servicios básicos y operación (6 meses):**

| Concepto | Costo Mensual | Meses | Total |
|----------|---------------|-------|-------|
| **Internet fibra óptica** | S/. 120.00 | 6 | S/. 720.00 |
| **Electricidad adicional** | S/. 80.00 | 6 | S/. 480.00 |
| **Espacio de trabajo** | S/. 200.00 | 6 | S/. 1,200.00 |
| **Teléfono/comunicaciones** | S/. 50.00 | 6 | S/. 300.00 |
| **Seguro de equipos** | S/. 30.00 | 6 | S/. 180.00 |
| **SUBTOTAL COSTOS OPERATIVOS** | | | **S/. 2,880.00** |

#### 4.2.3. Costos del ambiente

**Infraestructura tecnológica:**

| Concepto | Especificación | Costo Mensual | Meses | Total |
|----------|----------------|---------------|-------|-------|
| **VPS Servidor** | 4 vCPU, 8GB RAM, 100GB SSD | S/. 165.00 | 6 | S/. 990.00 |
| **Dominio web** | becasperu.com | S/. 4.00 | 12 | S/. 48.00 |
| **Certificado SSL** | Let's Encrypt | S/. 0.00 | 12 | S/. 0.00 |
| **CDN Cloudflare** | Plan Pro | S/. 65.00 | 6 | S/. 390.00 |
| **Base de datos backup** | MySQL managed | S/. 45.00 | 6 | S/. 270.00 |
| **Monitoreo y logs** | Herramientas de monitoreo | S/. 25.00 | 6 | S/. 150.00 |
| **SUBTOTAL COSTOS DE AMBIENTE** | | | | **S/. 1,848.00** |

#### 4.2.4. Costos de personal

**Recurso humano para desarrollo:**

**Organización del equipo:**
- **Líder de proyecto:** Angel Jose Vargas Gutierrez
- **Desarrollador Backend:** Andy Michael Calizaya Ladera
- **Analista de datos:** Ambos (trabajo colaborativo)
- **Tester/QA:** Ambos (trabajo colaborativo)

**Horario de trabajo:**
- **Lunes a Viernes:** 4 horas diarias (6:00 PM - 10:00 PM)
- **Sábados:** 6 horas (8:00 AM - 2:00 PM)
- **Total semanal:** 26 horas por persona
- **Total proyecto:** 624 horas por persona (24 semanas)

| Rol | Horas Totales | Tarifa/Hora | Total |
|-----|---------------|-------------|-------|
| **Líder de Proyecto** | 624 | S/. 25.00 | S/. 15,600.00 |
| **Desarrollador Backend** | 624 | S/. 22.00 | S/. 13,728.00 |
| **Analista de Datos** | 312 | S/. 20.00 | S/. 6,240.00 |
| **Tester/QA** | 156 | S/. 18.00 | S/. 2,808.00 |
| **SUBTOTAL COSTOS DE PERSONAL** | | | **S/. 38,376.00** |

#### 4.2.5. Costos totales del desarrollo del sistema

**Resumen de costos:**

| Categoría | Monto |
|-----------|-------|
| **Costos Generales** | S/. 1,190.00 |
| **Costos Operativos** | S/. 2,880.00 |
| **Costos de Ambiente** | S/. 1,848.00 |
| **Costos de Personal** | S/. 38,376.00 |
| **TOTAL DESARROLLO** | **S/. 44,294.00** |

**Costos adicionales (contingencia 10%):** S/. 4,429.40

**COSTO TOTAL DEL PROYECTO:** **S/. 48,723.40**

**Forma de pago:**
- **30% al inicio:** S/. 14,617.02
- **40% a mitad del proyecto:** S/. 19,489.36
- **30% al finalizar:** S/. 14,617.02

### 4.3. Factibilidad Operativa

**Beneficios del producto:**

1. **Para estudiantes:**
   - Acceso centralizado a información de becas
   - Ahorro de tiempo en búsqueda (estimado: 15 horas/mes por estudiante)
   - Alertas automáticas de nuevas oportunidades
   - Análisis personalizado de elegibilidad

2. **Para instituciones educativas:**
   - Herramienta para orientar a estudiantes
   - Datos estadísticos sobre tendencias de becas
   - Reducción de carga administrativa

3. **Para el sector educativo:**
   - Democratización del acceso a información
   - Datos para políticas públicas educativas
   - Reducción de la brecha de desigualdad

**Capacidad de mantenimiento:**

**Por parte del equipo desarrollador:**
- Conocimiento completo del código fuente
- Documentación técnica detallada
- Experiencia en las tecnologías utilizadas
- Disponibilidad para soporte post-implementación

**Por parte de la institución:**
- Infraestructura tecnológica adecuada
- Personal técnico capacitado en la universidad
- Presupuesto para mantenimiento continuo
- Políticas de respaldo y seguridad establecidas

**Impacto en usuarios:**

**Usuarios directos:**
- **Estudiantes de educación superior:** 1.2 millones en Perú
- **Estudiantes de educación técnica:** 400,000 en Perú
- **Padres de familia:** 1.6 millones aproximadamente

**Usuarios indirectos:**
- **Orientadores educativos:** 5,000 profesionales
- **Instituciones educativas:** 3,000 centros
- **Organizaciones que otorgan becas:** 150 instituciones

**Lista de interesados (stakeholders):**

| Stakeholder | Interés | Influencia | Estrategia |
|-------------|---------|------------|------------|
| **Estudiantes** | Alto | Media | Comunicación directa, feedback continuo |
| **PRONABEC** | Alto | Alta | Colaboración oficial, validación de datos |
| **Universidades** | Medio | Alta | Presentación de beneficios, piloto |
| **Bancos** | Medio | Media | Propuesta de valor agregado |
| **Ministerio de Educación** | Alto | Alta | Alineación con políticas públicas |
| **UPT** | Alto | Alta | Apoyo institucional, recursos |

### 4.4. Factibilidad Legal

**Marco legal aplicable:**

**Leyes nacionales:**

1. **Ley N° 29733 - Ley de Protección de Datos Personales:**
   - **Cumplimiento:** El sistema no recopila datos personales de usuarios
   - **Datos públicos:** Solo se extraen datos públicos de convocatorias
   - **Consentimiento:** No se requiere para información pública

2. **Decreto Legislativo N° 822 - Ley sobre el Derecho de Autor:**
   - **Cumplimiento:** Se respetan derechos de autor de contenido
   - **Uso justo:** Extracción de datos públicos para fines educativos
   - **Atribución:** Se mantienen referencias a fuentes originales

3. **Ley N° 27309 - Ley que incorpora los delitos informáticos:**
   - **Cumplimiento:** No se realizan actividades de hacking o acceso no autorizado
   - **Scraping ético:** Se respetan robots.txt y términos de servicio
   - **Frecuencia controlada:** Requests limitados para no sobrecargar servidores

**Regulaciones específicas:**

**Términos de servicio de sitios web:**
- **PRONABEC:** Permite uso de información pública para fines educativos
- **BCP:** Términos revisados, no prohíben scraping de información pública
- **Universidades:** Políticas variables, se implementará respeto a robots.txt

**Propiedad intelectual:**
- **Código fuente:** Licencia MIT para el proyecto
- **Base de datos:** Estructura original, no copia de esquemas existentes
- **Interfaz:** Diseño original, no copia de interfaces existentes

**Cumplimiento de estándares:**
- **ISO 27001:** Implementación de controles de seguridad
- **GDPR (referencia):** Aunque no aplica directamente, se siguen mejores prácticas
- **Directivas ONGEI:** Cumplimiento con estándares de gobierno electrónico

**Evaluación de riesgos legales:**

| Riesgo Legal | Probabilidad | Impacto | Mitigación |
|--------------|--------------|---------|------------|
| **Cambio en términos de servicio** | Media | Medio | Monitoreo continuo, APIs alternativas |
| **Reclamos por scraping** | Baja | Alto | Scraping ético, respeto a límites |
| **Problemas de derechos de autor** | Baja | Medio | Atribución correcta, uso justo |
| **Regulaciones de datos** | Baja | Alto | No recopilación de datos personales |



### 4.5. Factibilidad Social

**Influencias sociales y culturales:**

**Clima político:**
- **Estabilidad:** El proyecto se alinea con políticas de inclusión educativa
- **Apoyo gubernamental:** Iniciativas como "Beca 18" respaldan el objetivo
- **Continuidad:** Independiente de cambios políticos por ser de utilidad pública

**Códigos de conducta y ética:**

**Principios éticos del proyecto:**
1. **Transparencia:** Información clara sobre fuentes y metodología
2. **Equidad:** Acceso gratuito para todos los usuarios
3. **Veracidad:** Datos verificados y actualizados
4. **Privacidad:** No recopilación de datos personales innecesarios
5. **Responsabilidad:** Compromiso con la calidad de la información

**Impacto social positivo:**

**Reducción de desigualdades:**
- **Acceso equitativo:** Estudiantes rurales tendrán la misma información
- **Democratización:** Eliminación de barreras informativas
- **Oportunidades:** Mayor visibilidad de becas disponibles

**Beneficios comunitarios:**
- **Educación:** Contribución al desarrollo educativo nacional
- **Movilidad social:** Facilitación del acceso a educación superior
- **Desarrollo regional:** Estudiantes capacitados regresan a sus regiones

**Aceptación cultural:**

**Factores favorables:**
- **Valoración de la educación:** Alta en la cultura peruana
- **Adopción tecnológica:** Creciente uso de plataformas digitales
- **Confianza institucional:** Respaldo de universidad reconocida

**Posibles resistencias:**
- **Brecha digital:** Algunos usuarios pueden tener limitaciones tecnológicas
- **Desconfianza inicial:** Necesidad de demostrar confiabilidad
- **Preferencia por métodos tradicionales:** Algunos usuarios prefieren consultas presenciales

**Estrategias de adopción:**
1. **Capacitación:** Talleres en instituciones educativas
2. **Testimonios:** Casos de éxito de usuarios
3. **Simplicidad:** Interfaz intuitiva y fácil de usar
4. **Soporte:** Canal de ayuda y asistencia técnica

### 4.6. Factibilidad Ambiental

**Evaluación de impacto ambiental:**

**Impactos positivos:**

**Reducción de papel:**
- **Digitalización:** Eliminación de folletos y material impreso
- **Estimación:** Ahorro de 50,000 hojas/año en información de becas
- **Equivalencia:** Preservación de aproximadamente 6 árboles/año

**Reducción de transporte:**
- **Consultas virtuales:** Menos viajes a oficinas de información
- **Estimación:** 10,000 viajes evitados/año
- **Reducción CO2:** Aproximadamente 2.5 toneladas/año

**Optimización de recursos:**
- **Centralización:** Evita duplicación de esfuerzos
- **Eficiencia:** Menor consumo de recursos por consulta
- **Escalabilidad:** Mayor beneficio con más usuarios

**Impactos negativos (mínimos):**

**Consumo energético:**
- **Servidores:** Consumo estimado de 2,000 kWh/año
- **Equipos usuario:** Incremento marginal en uso de dispositivos
- **Mitigación:** Uso de energía renovable en data centers

**Residuos electrónicos:**
- **Equipos de desarrollo:** Vida útil extendida por uso eficiente
- **Servidores:** Hardware con ciclo de vida de 5+ años
- **Mitigación:** Reciclaje responsable al final de vida útil

**Medidas de sostenibilidad:**

1. **Eficiencia energética:**
   - Optimización de código para menor consumo
   - Uso de CDN para reducir transferencia de datos
   - Compresión de imágenes y recursos

2. **Hosting verde:**
   - Selección de proveedores con energía renovable
   - Servidores con certificación de eficiencia energética
   - Políticas de compensación de carbono

3. **Diseño sostenible:**
   - Interfaz minimalista para menor consumo de datos
   - Caching inteligente para reducir requests
   - Optimización de base de datos

5. <span id="_Toc52661356" class="anchor"></span>**Análisis Financiero**

    El plan financiero se ocupa del análisis de ingresos y gastos asociados a cada proyecto, desde el punto de vista del instante temporal en que se producen. Su misión fundamental es detectar situaciones financieramente inadecuadas.
    Se tiene que estimar financieramente el resultado del proyecto.

    5.1. Justificación de la Inversión

        5.1.1. Beneficios del Proyecto

            El beneficio se calcula como el margen económico menos los costes de oportunidad, que son los márgenes que hubieran podido obtenerse de haber dedicado el capital y el esfuerzo a otras actividades.
            El beneficio, obtenido lícitamente, no es sólo una recompensa a la inversión, al esfuerzo y al riesgo asumidos por el empresario, sino que también es un factor esencial para que las empresas sigan en el  mercado e incorporen nuevas inversiones al tejido industrial y social de las naciones.
            Describir beneficios tangibles e intangibles*
            Beneficios tangibles: son de fácil cuantificación, generalmente están relacionados con la reducción de recursos o talento humano.
            Beneficios intangibles: no son fácilmente cuantificables y están relacionados con elementos o mejora en otros procesos de la organización.
>
            Ejemplo de beneficios:

            - Mejoras en la eficiencia del área bajo estudio.
            - Reducción de personal.
            - Reducción de futuras inversiones y costos.
            - Disponibilidad del recurso humano.
            - Mejoras en planeación, control y uso de recursos.
            - Suministro oportuno de insumos para las operaciones.
            - Cumplimiento de requerimientos gubernamentales.
            - Toma acertada de decisiones.
            - Disponibilidad de información apropiada.
            - Aumento en la confiabilidad de la información.
            - Mejor servicio al cliente externo e interno
            - Logro de ventajas competitivas.
            - Valor agregado a un producto de la compañía.
        
        5.1.2. Criterios de Inversión

            5.1.2.1. Relación Beneficio/Costo (B/C)

                En base a los costos y beneficios identificados se evalúa si es factible el desarrollo del proyecto. 
                Si se presentan varias alternativas de solución se evaluará cada una de ellas para determinar la mejor solución desde el punto de vista del > retorno de la inversión
                El B/C si es mayor a uno, se acepta el proyecto; si el B/C es igual a uno es indiferente aceptar o rechazar el proyecto y si el B/C es menor a uno se rechaza el proyecto

            5.1.2.2. Valor Actual Neto (VAN)
            
                Valor actual de los beneficios netos que genera el proyecto. Si el VAN es mayor que cero, se acepta el proyecto; si el VAN es igual a cero es indiferente aceptar o rechazar el proyecto y si el VAN es menor que cero se rechaza el proyecto

            5.1.2.3 Tasa Interna de Retorno (TIR)*
                Es la tasa porcentual que indica la rentabilidad promedio anual que genera el capital invertido en el proyecto. Si la TIR es mayor que el costo de oportunidad se acepta el proyecto, si la TIR es igual al costo de oportunidad es indiferente aceptar o rechazar el proyecto, si la TIR es menor que el costo de oportunidad se rechaza el proyecto

                Costo de oportunidad de capital (COK) es la tasa de interés que podría haber obtenido con el dinero invertido en el proyecto

<div style="page-break-after: always; visibility: hidden">\pagebreak</div>

6. <span id="_Toc52661357" class="anchor"></span>**Conclusiones**

Explicar los resultados del análisis de factibilidad que nos indican si el proyecto es viable y factible.
