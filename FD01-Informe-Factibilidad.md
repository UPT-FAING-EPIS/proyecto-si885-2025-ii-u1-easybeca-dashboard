<center>

[comment]: <img src="./media/media/image1.png" style="width:1.088in;height:1.46256in" alt="escudo.png" />

![./media/media/image1.png](./media/logo-upt.png)

**UNIVERSIDAD PRIVADA DE TACNA**

**FACULTAD DE INGENIERIA**

**Escuela Profesional de Ingeniería de Sistemas**

**Proyecto *{Nombre de Proyecto}***

**Curso:** Inteligencia de Negocios  
**Docente:** Ing. Patrick Cuadros Quiroga

**Estudiantes:**
- Angel Jose VARGAS GUTIERREZ (2020066922)
- ANDY MICHAEL CALIZAYA LADERA (2022074258)

**Tacna – Perú**

***2025***

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

## 5. ANÁLISIS FINANCIERO

El plan financiero se ocupa del análisis de ingresos y gastos asociados al proyecto "BecasPerú Analytics Dashboard", desde el punto de vista del instante temporal en que se producen. Su misión fundamental es detectar situaciones financieramente inadecuadas y estimar financieramente el resultado del proyecto.

### 5.1. Justificación de la Inversión

#### 5.1.1. Beneficios del Proyecto

El beneficio se calcula como el margen económico menos los costes de oportunidad, que son los márgenes que hubieran podido obtenerse de haber dedicado el capital y el esfuerzo a otras actividades. El beneficio, obtenido lícitamente, no es sólo una recompensa a la inversión, al esfuerzo y al riesgo asumidos, sino que también es un factor esencial para que las organizaciones sigan en el mercado e incorporen nuevas inversiones al tejido educativo y social.

**Beneficios Tangibles (Cuantificables):**

1. **Reducción de tiempo de búsqueda de becas:**
   - Ahorro promedio: 15 horas/mes por estudiante
   - Valor del tiempo: S/. 10/hora (costo oportunidad)
   - Beneficio por estudiante: S/. 150/mes
   - Con 10,000 usuarios activos: S/. 1,500,000/mes
   - **Beneficio anual:** S/. 18,000,000

2. **Reducción de costos administrativos en instituciones:**
   - Ahorro en personal de orientación: 2 horas/día por institución
   - Costo hora profesional: S/. 25/hora
   - 100 instituciones usuarias: S/. 5,000/día
   - **Beneficio anual:** S/. 1,825,000

3. **Incremento en acceso a becas:**
   - Aumento estimado del 25% en postulaciones exitosas
   - Valor promedio de beca: S/. 15,000
   - 500 becas adicionales anuales: S/. 7,500,000
   - **Beneficio social anual:** S/. 7,500,000

4. **Reducción de costos de publicidad para instituciones:**
   - Ahorro en marketing de convocatorias: S/. 50,000/año por institución
   - 20 instituciones participantes
   - **Beneficio anual:** S/. 1,000,000

**Total Beneficios Tangibles Anuales:** S/. 28,325,000

**Beneficios Intangibles (No fácilmente cuantificables):**

1. **Mejoras en la eficiencia del sector educativo:**
   - Optimización de procesos de selección de becarios
   - Mejor asignación de recursos educativos
   - Reducción de duplicidad de esfuerzos

2. **Democratización del acceso a la educación:**
   - Reducción de la brecha de desigualdad educativa
   - Mayor acceso para estudiantes de zonas rurales
   - Inclusión de poblaciones vulnerables

3. **Mejoras en planeación y control de recursos:**
   - Datos estadísticos para políticas públicas
   - Análisis predictivo de tendencias educativas
   - Optimización de presupuestos de becas

4. **Disponibilidad de información apropiada:**
   - Centralización de datos dispersos
   - Información actualizada en tiempo real
   - Análisis históricos y predictivos

5. **Aumento en la confiabilidad de la información:**
   - Validación automática de datos
   - Reducción de errores humanos
   - Trazabilidad de fuentes de información

6. **Mejor servicio al cliente externo e interno:**
   - Interfaz amigable y accesible
   - Alertas personalizadas
   - Soporte técnico especializado

7. **Logro de ventajas competitivas:**
   - Posicionamiento como líder en tecnología educativa
   - Diferenciación en el mercado de servicios educativos
   - Atracción de talento y recursos

8. **Valor agregado al sector educativo:**
   - Innovación tecnológica en educación
   - Modelo replicable en otros países
   - Contribución al desarrollo sostenible

#### 5.1.2. Criterios de Inversión

**Datos para el análisis:**
- **Inversión inicial:** S/. 48,723.40
- **Beneficios anuales tangibles:** S/. 28,325,000
- **Costos operativos anuales:** S/. 24,000 (mantenimiento y hosting)
- **Beneficios netos anuales:** S/. 28,301,000
- **Período de análisis:** 5 años
- **Tasa de descuento (COK):** 12% anual

##### 5.1.2.1. Relación Beneficio/Costo (B/C)

**Cálculo del B/C:**

**Valor presente de beneficios (5 años):**
- Año 1: S/. 28,301,000 / (1.12)¹ = S/. 25,268,750
- Año 2: S/. 28,301,000 / (1.12)² = S/. 22,561,563
- Año 3: S/. 28,301,000 / (1.12)³ = S/. 20,144,253
- Año 4: S/. 28,301,000 / (1.12)⁴ = S/. 17,985,940
- Año 5: S/. 28,301,000 / (1.12)⁵ = S/. 16,058,875

**Total VP Beneficios:** S/. 102,019,381

**Valor presente de costos:**
- Inversión inicial: S/. 48,723.40
- VP costos operativos: S/. 86,478 (5 años descontados)

**Total VP Costos:** S/. 135,201.40

**B/C = S/. 102,019,381 / S/. 135,201.40 = 754.5**

**Resultado:** B/C = 754.5 > 1, por lo tanto **SE ACEPTA EL PROYECTO**

##### 5.1.2.2. Valor Actual Neto (VAN)

**VAN = VP Beneficios - VP Costos**
**VAN = S/. 102,019,381 - S/. 135,201.40 = S/. 101,884,179.60**

**Resultado:** VAN = S/. 101,884,179.60 > 0, por lo tanto **SE ACEPTA EL PROYECTO**

##### 5.1.2.3. Tasa Interna de Retorno (TIR)

Dado que los beneficios netos anuales (S/. 28,301,000) son extremadamente superiores a la inversión inicial (S/. 48,723.40), la TIR es prácticamente infinita.

**Cálculo aproximado:**
TIR ≈ (Beneficio Neto Anual / Inversión Inicial) × 100
TIR ≈ (S/. 28,301,000 / S/. 48,723.40) × 100 ≈ 58,100%

**Resultado:** TIR ≈ 58,100% >> COK (12%), por lo tanto **SE ACEPTA EL PROYECTO**

**Resumen de Criterios de Inversión:**

| Criterio | Valor Calculado | Criterio de Aceptación | Decisión |
|----------|-----------------|------------------------|----------|
| **B/C** | 754.5 | > 1 | ✅ ACEPTA |
| **VAN** | S/. 101,884,179.60 | > 0 | ✅ ACEPTA |
| **TIR** | ~58,100% | > 12% (COK) | ✅ ACEPTA |

**Período de Recuperación:**
La inversión se recupera en menos de 1 día de operación, considerando los beneficios diarios estimados.

**Análisis de ingresos y gastos:**

El proyecto "BecasPerú Analytics Dashboard" se desarrolla inicialmente como un proyecto académico sin fines de lucro, pero con potencial de generar valor económico a largo plazo.

**Estructura de costos del proyecto:**

### Inversión inicial (Año 0)

| Concepto | Monto |
|----------|-------|
| **Desarrollo del sistema** | S/. 48,723.40 |
| **Equipamiento adicional** | S/. 2,500.00 |
| **Marketing inicial** | S/. 5,000.00 |
| **Capital de trabajo** | S/. 10,000.00 |
| **TOTAL INVERSIÓN INICIAL** | **S/. 66,223.40** |

### Costos operativos anuales

| Concepto | Año 1 | Año 2 | Año 3 |
|----------|-------|-------|-------|
| **Hosting y servidores** | S/. 3,960.00 | S/. 4,356.00 | S/. 4,791.60 |
| **Mantenimiento técnico** | S/. 12,000.00 | S/. 13,200.00 | S/. 14,520.00 |
| **Actualizaciones y mejoras** | S/. 8,000.00 | S/. 8,800.00 | S/. 9,680.00 |
| **Soporte al usuario** | S/. 6,000.00 | S/. 6,600.00 | S/. 7,260.00 |
| **Marketing y promoción** | S/. 4,000.00 | S/. 4,400.00 | S/. 4,840.00 |
| **Gastos administrativos** | S/. 3,000.00 | S/. 3,300.00 | S/. 3,630.00 |
| **TOTAL COSTOS ANUALES** | **S/. 36,960.00** | **S/. 40,656.00** | **S/. 44,721.60** |

### Proyección de beneficios

**Beneficios cuantificables:**

1. **Ahorro de tiempo para usuarios:**
   - 50,000 usuarios estimados en Año 1
   - 15 horas ahorradas por usuario/año
   - Valor hora: S/. 10.00
   - **Beneficio total:** S/. 7,500,000.00/año

2. **Reducción de costos institucionales:**
   - 100 instituciones educativas
   - Ahorro en personal de orientación: S/. 2,000/institución/año
   - **Beneficio total:** S/. 200,000.00/año

3. **Incremento en acceso a becas:**
   - 5% más estudiantes acceden a becas
   - 1,000 becas adicionales/año
   - Valor promedio beca: S/. 15,000
   - **Beneficio social:** S/. 15,000,000.00/año

### Análisis de viabilidad financiera

**Indicadores financieros (modelo de sostenibilidad):**

| Indicador | Valor |
|-----------|-------|
| **Inversión inicial** | S/. 66,223.40 |
| **Beneficio social anual** | S/. 22,700,000.00 |
| **ROI social** | 34,200% |
| **Payback period** | 1.1 días |
| **VAN social (5 años, 10%)** | S/. 85,890,847.00 |

**Modelo de sostenibilidad a largo plazo:**

**Fase 1 (Años 1-2): Proyecto académico**
- Financiamiento: Universidad y recursos propios
- Objetivo: Demostrar viabilidad y generar adopción

**Fase 2 (Años 3-4): Institucionalización**
- Financiamiento: Alianzas con instituciones educativas
- Objetivo: Escalamiento y mejora continua

**Fase 3 (Año 5+): Comercialización**
- Modelo freemium: Servicios básicos gratuitos, premium pagos
- Servicios premium: Análisis avanzados, alertas personalizadas
- Ingresos estimados: S/. 50,000-100,000/año

**Análisis de sensibilidad:**

| Escenario | Adopción | Beneficio Social | Viabilidad |
|-----------|----------|------------------|------------|
| **Pesimista** | 20,000 usuarios | S/. 9,080,000 | Alta |
| **Base** | 50,000 usuarios | S/. 22,700,000 | Muy Alta |
| **Optimista** | 100,000 usuarios | S/. 45,400,000 | Excelente |

**Conclusión financiera:** El proyecto presenta una viabilidad financiera excelente desde la perspectiva de beneficio social, con un retorno de inversión extraordinario y múltiples opciones de sostenibilidad a largo plazo.

---

## 6. CONCLUSIONES

Basado en el análisis integral de factibilidad realizado para el proyecto "BecasPerú Analytics Dashboard", se presentan las siguientes conclusiones:

### 6.1. Viabilidad General del Proyecto

El proyecto **"BecasPerú Analytics Dashboard"** es **COMPLETAMENTE VIABLE Y FACTIBLE** desde todas las perspectivas analizadas. Los resultados del estudio demuestran que la implementación del sistema no solo es técnica y económicamente posible, sino que también genera un impacto social significativo y un retorno de inversión excepcional.

### 6.2. Conclusiones por Área de Factibilidad

#### 6.2.1. Factibilidad Técnica: ✅ VIABLE

- **Tecnologías disponibles:** Todas las herramientas necesarias (Python, MySQL, Power BI, FastAPI) están disponibles y son maduras
- **Infraestructura:** La infraestructura requerida es accesible y escalable
- **Conocimiento técnico:** El equipo cuenta con las competencias necesarias
- **Riesgo técnico:** Bajo a medio, con estrategias de mitigación definidas

#### 6.2.2. Factibilidad Económica: ✅ ALTAMENTE VIABLE

- **Inversión inicial:** S/. 48,723.40 (moderada)
- **Relación B/C:** 754.5 (excepcional)
- **VAN:** S/. 101,884,179.60 (altamente positivo)
- **TIR:** ~58,100% (extraordinaria)
- **Período de recuperación:** Menos de 1 día

#### 6.2.3. Factibilidad Operativa: ✅ VIABLE

- **Beneficiarios directos:** 1.6 millones de estudiantes potenciales
- **Impacto social:** Democratización del acceso a información educativa
- **Capacidad de mantenimiento:** Garantizada por el equipo desarrollador
- **Aceptación esperada:** Alta, debido a la necesidad identificada

#### 6.2.4. Factibilidad Legal: ✅ VIABLE

- **Cumplimiento normativo:** Total adherencia a leyes de protección de datos
- **Uso de información pública:** Dentro del marco legal establecido
- **Propiedad intelectual:** Respeto completo a derechos de autor
- **Licenciamiento:** Uso de software libre y licencias educativas

#### 6.2.5. Factibilidad Social: ✅ ALTAMENTE VIABLE

- **Impacto positivo:** Reducción de la brecha de desigualdad educativa
- **Beneficio comunitario:** Acceso equitativo a oportunidades educativas
- **Sostenibilidad social:** Contribución al desarrollo del capital humano
- **Aceptación social:** Esperada alta aceptación por parte de todos los stakeholders

#### 6.2.6. Factibilidad Ambiental: ✅ VIABLE

- **Impacto ambiental:** Mínimo, principalmente digital
- **Sostenibilidad:** Reducción del uso de papel y desplazamientos
- **Eficiencia energética:** Uso de tecnologías cloud optimizadas
- **Huella de carbono:** Negativa debido a la digitalización de procesos

### 6.3. Indicadores Clave de Éxito

| Indicador | Meta | Justificación |
|-----------|------|---------------|
| **ROI** | 58,100% | Beneficios extraordinariamente superiores a la inversión |
| **Usuarios activos** | 10,000+ | Base conservadora para cálculo de beneficios |
| **Tiempo de implementación** | 6 meses | Cronograma realista y alcanzable |
| **Precisión de datos** | 95%+ | Estándar de calidad para sistemas de información |
| **Disponibilidad del sistema** | 99.5%+ | Garantía de servicio continuo |

### 6.4. Factores Críticos de Éxito

1. **Compromiso institucional:** Apoyo continuo de la Universidad Privada de Tacna
2. **Colaboración interinstitucional:** Establecimiento de alianzas con PRONABEC y otras entidades
3. **Mantenimiento técnico:** Actualización continua de scrapers y sistemas
4. **Adopción de usuarios:** Estrategias efectivas de difusión y capacitación
5. **Escalabilidad:** Capacidad de crecimiento según demanda

### 6.5. Recomendaciones Estratégicas

#### 6.5.1. Implementación Inmediata

**Se recomienda la implementación inmediata del proyecto** debido a:
- Viabilidad comprobada en todas las dimensiones
- Retorno de inversión excepcional
- Impacto social significativo
- Ventana de oportunidad en el mercado educativo

#### 6.5.2. Fases de Implementación

1. **Fase Piloto (Mes 1-2):** Implementación con 3 fuentes de datos
2. **Fase de Expansión (Mes 3-4):** Incorporación de todas las fuentes planificadas
3. **Fase de Optimización (Mes 5-6):** Mejoras basadas en feedback de usuarios
4. **Fase de Escalamiento (Mes 7+):** Expansión nacional y nuevas funcionalidades

#### 6.5.3. Gestión de Riesgos

- Implementar monitoreo continuo de cambios en sitios web
- Establecer acuerdos de colaboración con instituciones clave
- Desarrollar planes de contingencia para riesgos técnicos
- Mantener comunicación activa con stakeholders

### 6.6. Impacto Esperado

#### 6.6.1. Impacto Cuantitativo

- **28.3 millones de soles** en beneficios anuales tangibles
- **10,000+ estudiantes** beneficiados directamente
- **100+ instituciones** con procesos optimizados
- **25% de incremento** en acceso exitoso a becas

#### 6.6.2. Impacto Cualitativo

- Democratización del acceso a información educativa
- Reducción de la brecha de desigualdad en educación
- Modernización del sector educativo peruano
- Posicionamiento como referente en innovación educativa

### 6.7. Conclusión Final

El proyecto **"BecasPerú Analytics Dashboard"** representa una **oportunidad excepcional** para generar un impacto transformador en el sector educativo peruano. Con una inversión relativamente modesta de S/. 48,723.40, se pueden obtener beneficios anuales superiores a los S/. 28 millones, lo que resulta en uno de los proyectos con mayor retorno de inversión en el ámbito educativo.

**La recomendación final es PROCEDER INMEDIATAMENTE con la implementación del proyecto**, aprovechando la ventana de oportunidad actual y el potencial de impacto social positivo.

El éxito del proyecto no solo beneficiará a miles de estudiantes peruanos, sino que también posicionará a la Universidad Privada de Tacna como líder en innovación educativa y tecnología aplicada al desarrollo social.

**VEREDICTO FINAL: PROYECTO APROBADO PARA IMPLEMENTACIÓN INMEDIATA**

---

*Informe elaborado por:*
- **Angel Jose Vargas Gutierrez** - Líder de Proyecto
- **Andy Michael Calizaya Ladera** - Desarrollador Backend

*Bajo la supervisión de:*
- **Ing. Patrick Cuadros** - Docente del Curso de Inteligencia de Negocios

*Universidad Privada de Tacna*
*Facultad de Ingeniería*
*Escuela Profesional de Ingeniería de Sistemas*

*Fecha de elaboración: Diciembre 2024*

### Conclusiones por área de factibilidad

**1. Factibilidad Técnica: VIABLE**
- Todas las tecnologías requeridas están disponibles y son maduras
- El equipo cuenta con las competencias técnicas necesarias
- La infraestructura existente es suficiente para el desarrollo
- Los riesgos técnicos son manejables con las estrategias propuestas

**2. Factibilidad Económica: VIABLE**
- La inversión requerida (S/. 66,223.40) es razonable para el alcance del proyecto
- Los costos operativos son sostenibles a largo plazo
- El beneficio social supera ampliamente la inversión (ROI social: 34,200%)
- Existen múltiples modelos de sostenibilidad financiera

**3. Factibilidad Operativa: VIABLE**
- Los beneficios para usuarios y stakeholders están claramente identificados
- Existe capacidad técnica para mantener el sistema funcionando
- El impacto en usuarios es positivo y significativo
- Los stakeholders muestran interés y apoyo al proyecto

**4. Factibilidad Legal: VIABLE**
- No existen conflictos con la legislación peruana vigente
- El proyecto cumple con normativas de protección de datos
- Se respetan derechos de autor y términos de servicio
- Los riesgos legales son mínimos y manejables

**5. Factibilidad Social: VIABLE**
- El proyecto se alinea con valores culturales peruanos
- Contribuye significativamente a la reducción de desigualdades
- Tiene amplia aceptación social y apoyo institucional
- Los beneficios comunitarios son sustanciales

**6. Factibilidad Ambiental: VIABLE**
- El impacto ambiental neto es positivo
- Contribuye a la reducción de papel y transporte
- El consumo energético es mínimo y controlado
- Se implementan medidas de sostenibilidad ambiental

### Conclusión general

**El proyecto "BecasPerú Analytics Dashboard" es COMPLETAMENTE VIABLE** desde todas las perspectivas analizadas. Los beneficios sociales, económicos y educativos superan ampliamente los costos y riesgos asociados.

### Recomendaciones para la implementación

1. **Proceder con la implementación** siguiendo el cronograma propuesto
2. **Establecer alianzas estratégicas** con PRONABEC y universidades desde el inicio
3. **Implementar un sistema robusto de monitoreo** para mitigar riesgos técnicos
4. **Desarrollar un plan de comunicación** para maximizar la adopción
5. **Preparar estrategias de escalamiento** para manejar el crecimiento de usuarios
6. **Establecer métricas de éxito** para evaluar el impacto del proyecto

### Impacto esperado

El proyecto tiene el potencial de:
- **Democratizar el acceso** a información sobre becas educativas
- **Beneficiar directamente** a más de 50,000 estudiantes en el primer año
- **Generar ahorros sociales** superiores a S/. 22 millones anuales
- **Contribuir a la reducción** de la brecha educativa en el Perú
- **Establecer un modelo replicable** para otros países de la región

**El proyecto "BecasPerú Analytics Dashboard" no solo es viable, sino que representa una oportunidad excepcional para generar impacto social positivo en el sector educativo peruano.**
