# Entregable 1 - 26 de octubre último commit - 5%

## Métricas de los requerimientos no funcionales

Documentar cada atributo no funcional con valores cuantitativos, parámetros técnicos y tecnologías a usar. Incluir ejemplos claros, abajo se documentan ejemplos de valores y tecnologías, pero ustedes deben diseñar y encontrar sus propios valores los cuales deben estar justificados por alguna teoría o práctica debidamente argumentada y analizada; realizando las extrapolaciones o cálculos que usted pueda diseñar bajo un algoritmo o método cuantitativo diseñado por el grupo mismo. 

Integrantes:
kskskss
ksksks
ksksksk


### Requerimientos No Funcionales (Utilizar estos para desarrollar el Entregable 1)

_Rendimiento_ 

* El tiempo promedio de respuesta del portal web no debe exceder **2.5 segundos** en operaciones estándar.
* Las consultas cacheadas mediante Redis deben entregar resultados en menos de **400 milisegundos**.
* Los procesos de generación automática de contenido o campañas deben ejecutarse en menos de **7 segundos** para solicitudes simples y menos de **20 segundos** para ejecuciones complejas con IA.

_Escalabilidad_

* La arquitectura debe soportar un incremento de **hasta 10 veces** la carga base sin degradación perceptible del rendimiento.
* Kubernetes debe permitir **autoescalado horizontal** basado en CPU, memoria y número de solicitudes concurrentes.
* El sistema debe manejar simultáneamente **más de 5000 campañas activas** y **más de 300 agentes o usuarios concurrentes** distribuidos entre las subempresas.
* Las API de cualquiera de las plataformas podría llegar a alcanzar en el primer año hasta 100000 operaciones de usuario por minuto que requieren acceso a la base de datos, en horario habitual de 7am hasta 7pm. Y hasta 300 procesos no supervisados por minuto ejecutándose en background fuera de horario de oficina. 

_Tolerancia a Fallos_

* Disponibilidad mínima del sistema de **99.9% mensual**.
* Los contenedores críticos deben reiniciarse automáticamente ante fallos o degradación de servicio.
* Redis y las bases de datos deben contar con **replicación en tiempo real** y **failover automático**.
* Implementación de **backups automáticos diarios** y retención mínima de **30 días**.

_Seguridad_

* Autenticación y autorización mediante **OAuth 2.0** para todos los usuarios y servicios.
* Cifrado de todas las comunicaciones entre servicios con **TLS 1.3**.
* Cifrado de datos en reposo con **AES-256** en bases de datos y almacenamiento persistente.
* Auditoría y logging centralizado con retención de **90 días**.
* Cumplimiento con estándares de protección de datos internacionales (**GDPR, CCPA**) y políticas de acceso mínimo necesario (principio de least privilege).

# Hay que diseñar estrategias para cumplir con los requerimientos no funcionales, como evidencia de que la estrategia diseñada cumple los requerimientos no funcionales hay que adjuntar algún benchmark hecho a esa tecnología. Los resultados de estos benchmarks hay que escalarlos a nuestra implementación.


### Performance

El equipo de desarrollo decidió utilizar las siguientes tecnologías Python + Django + Postgres.

1 operación de pedir todos los registros a una base de datos SQLite desde una API con Django dura 7.5ms según los benchmarks realizados por Bednarz y Miłosz en [Benchmarking the performance of Python web frameworks](/Benchmarking_the_performance_of_Python_web_framewo.pdf).

Los benchmarks se llevaron a cabo en una máquina con las siguientes especificaciones de hardware:

* CPU: Intel Core i7-8750H
* RAM: 16 GB DDR4
* Storage: 1 TB, Samsung SSD 970 EVO
* Operating System: Windows 10 Home 64-bit  

¿Cuánto tiempo duraría este server en hacer 100,000 transacciones?

7.5ms * 100,000 = 12,5min

Si 1 server dura 12.5min en realizar 100,000 transacciones, ¿Cuántos servers se necesitan para que las mismas 100,000 transacciones duren menos de 1min?

*Según la regla de 3* se necesitan más de 12 servers para cumplir con este requerimiento.

Para poder soportar la carga de 100,000 solicitudes por minuto por parte de los usuarios implementaremos 16 instancias de un server en AWS con las siguientes especificaciones:

* CPU: Intel Core i7-8750H
* RAM: 16 GB DDR4
* Storage: 1 TB, Samsung SSD 970 EVO
* Operating System: Windows 10 Home 64-bit

### Scalability

* Debe soportar incremento de carga de hasta 10x sin degradación.
* Kubernetes configurado con autoescalado horizontal por CPU y memoria. Justificarlo con la configuracion de K8s.

Ya sabemos cuanto hardware ocupamos para cumplir con performance, entonces...

Ejemplo:
Se utilizara kubernetes para contenerización dinámica con un cluster de mínimo X servers con autoscale de tanto. Cada máquina tendrá XXX specs. Aquí está el link al archivo de configuración de kubernetes.

### Reliability

* Tasa de errores máxima permitida: 0.1% de transacciones por día.
* Monitoreo con pg_stat_statements y logs centralizados.
* Es importante determinar como se monitorea y como se notifican alertas. 

"Nivel de confianza en el sistema"

Para este punto ya debemos de saber en qué lo vamos a hacer.

¿En el cloud que escogí qué hay para monitorear alertas?

"Se va a usar el servicio XXX de XXX para el monitoreo de alertas críticas. Estas se van a comunicar por XXX, XXX, XXX otras por email. Se va a permitir un máximo de XXX (inventado) errores al día."

### Availability

* Disponibilidad mínima: 99.9% mensual. En el diseño de infraestructura debe lograr verse como se logra esto, podría ir en el diagrama de arquitectura, pero sería mejor uno de infraestructura. 
* Redis y bases de datos con failover y replicación.
* Considere load balancers. 

Esto se refiere al porcentaje del tiempo que el sistema debería de estar disponible. 98% o 99,7% etc. Existe un ejemplo de esto en el Excel. 

### Security

Se aplicará una autenticación basada en OpenID Connect. Esta será proporcionada por Okta.

Para cifrar los datos en la comunicación de REST se aplicará TLS. 

En las bases de datos Mongo y MySQL utilizaremos el cifrado AES-256.

### Maintainability

El código se desarrollará de manera modular siguiendo DDD y separación de dominios.

Durante el desarrollo se seguirá el siguiente GitFlow

El branch `main` se utilizará unicamente para llevar el control de versiones en producción, estas son versiones estables. `develop` se utilizará para la integración de nuevas funcionalidades en preparación para la próxima versión. Cuando una versión ya está preparada se hace merge a `main`.

También se definen las siguientes sub-branches de soporte:

`feature/*` → nuevas funcionalidades (creadas desde develop).

`release/*` → preparación de una versión antes del despliegue (desde develop, luego se fusiona en main y develop).

`hotfix/*` → correcciones urgentes en producción (creadas desde main y luego fusionadas de vuelta a develop).

Todo PR a `main` debe incluir una descripción detallada del cambio que se realizó. Se utilizarán herramientas automáticas (CI/CD) para verificar el formato, cálidad del código y pruebas unitarias. Solo tras la aprobación de los revisores el código se integra a la rama principal.

Esta es la estrategia que se seguirá para abordar hotfixes:

Primeramente se creará una rama desde main con el nombre `hotfix/*Info del bug*`, en esta rama se implementará y probará la corrección, una vez esta esté lista, se hará un PR hacia main (para despliegue inmediato). Seguidamente se fusionará el hotfix también hacia develop (para mantener sincronizadas las ramas). Por último se documentará el cambio.

Para el release de versiones se hará uso de la rama `release/*version*`. En esta se harán puebas QA para la validación funcional, de rendimiento y seguridad. En caso de que se necesiten correcciones menores estas se harán sobre la misma rama. Luego se hará un merge a `main` para desplegar en producción, y a `develop` para sincronización de cambios.

El proceso de soporte post-release será de la siguiente manera:

L0: Se creará y se brindará soporte a centros de ayuda como foros y videos tutoriales. También se brindarán a disposición chatbots con respuestas automáticas y flujos guiados.
Todo esto se complementará con documentación técnica y guías para desarrolladores.

L1: Se brindará soporte a solicitudes recibidas vía correo, chat, redes o tickets. También se tendrán a disposición scripts o flujos predefinidos para resolver problemas comunes.

L2: Este nivel busca abordar problemas complejos o no documentados que requieren un diagnóstico técnico más profundo. Estos son problemas que no se lograron solucionar en L1. Como estrategia se dispondrá de personal capacitado para brindar soporte al usuario hasta llegar a una solución temporal o definitiva. Este soporte será brindado a través de reunión virtual o presencial, dependiendo de la disponibilidad.

L3: En caso de no encontrar solución definitiva a un problema en L2, el usuario será referido a uno de los integrantes del equipo de desarrollo de la plataforma. Este integrante le brindará soporte al usuario y en caso de que darle solución implique realizar algún cambio en la estructura de la aplicación, este proceso se llevará a cabo.

### Interoperability

En cuanto a la comunicación entre dominios, esta se reserva a que se haga únicamente mediante entes llamados Facades (fachadas).

Se agregó un dominio encargado de proporcionar integración a servicios externos a los demás dominios. Este se llama
`Integration for Extern Services Domain`.

### Compliance

Todo pago o transferencia se hace con servicio de terceros. En nuestro PayPal será nuestro provedor.

A la hora de realizar las pruebas automáticas de Owasp se aceptarán un máximo de dos pruebas críticas, siempre y cuándo ninguna de estas se encuentren en la lista de `OWASP Top 10 - 2021`. Se aceptará toda alerta leve relacionada a algún elemente de UI.

### Extensibility

En futuras versiones el alcance de esta arquitectura se puede extender conectando REST APIs, creando nuevos MCP Servers o incluso acoplando nuevos dominios.

## Domain driven design

### AI and Content Generation Domain
Este dominio se encarga de la creación de contenido textual, audiovisual e imágenes. También opera y ofrece servicios de IA a otros dominios como `Campaign Management and Analitics` y `Crm`.

- Text Generation
- Image Generation
- Video Generation
- AI services provider for other domains

### Campaign Management and Analitics Domain
Este dominio se encarga del diseño, segmentación y publicación de campañas publicitarias en redes sociales, email marketing, SMS, LinkedIn e influencers. También se encarga del análisis en tiempo real del rendimiento de estas campañas. Las campañas son generadas de manera automática a partir de datos de públicos meta y objetivos de venta.

- Campaign Planning: Encargado de diseñar la campaña publicitaria a partir del objetivo definido por el cliente. Define los KPIs, canales, formatos y duración de la campaña.

- Targeting: Selecciona el público objetivo al que se mostrará la campaña, segmentando por datos demográficos, comportamiento, intereses y otras variables.

- Bidding and Budgeting: Establece las reglas de puja y presupuesto. Define cuánto se invertirá por canal o audiencia y cómo se distribuirá la oferta en cada plataforma.

- Activation Manager: Se encarga de activar y publicar la campaña en las plataformas externas (Google Ads, Meta Ads, TikTok, etc.) utilizando listas de control de acceso (ACL) y herramientas de integración.

- Insights: Recopila y presenta métricas clave de desempeño como clics, impresiones, CTR, tasa de conversión y otros indicadores de efectividad en tiempo real.

- Attribution: Asigna crédito de conversión a los distintos canales o interacciones que contribuyeron al cierre de una venta, permitiendo mejorar futuras campañas.

- Experimentation: Permite probar variaciones de campañas, audiencias o mensajes mediante pruebas A/B u otros métodos para optimizar resultados.

- Compliance: Supervisa el cumplimiento de regulaciones locales e internas. Aplica reglas por país o cliente, impone límites de gasto y registra cambios con trazabilidad (quién, qué, cuándo).

### Crm Domain
Este dominio se encarga principalmente del monitoreo de leads. Estos se registran y clasifican automáticamente con sus respectivos datos de proveniencia. Para la interacción con el usuario el dominio ofrece chatbots, voicebots y flujos automatizados de atención. Todo esto es proporcionado por la implementación de IA.

### Business Domain
Este dominio se encarga de validar qué funcionalidades de la plataforma el usuario es capaz de utilizar, esto va a depender del plan al que este se haya suscrito. También se encarga de gestionar todo lo relacionado con pagos por parte del usuario.

### Integration for Extern Services Domain
Este dominio le permite la integración de aplicaciones o servicios externos a los demás dominios.

Plataformas como HubSpot, Salesforce, Zendesk, WhatsApp Business API, Google Ads, Meta Ads, TikTok for Business, Mailchimp, Canva, Adobe, Meta Business Suite y OpenAI API, etc...

Así como servicios de pago como PayPal, o de seguridad como Owasp.

A continuación se muestra un diagrama de los dominios de PromptSales.

![DDD diagram](/diagramDDD.png)