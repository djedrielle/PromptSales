### Desarrollado por
* Djedrielle Alexander
* Sebastian Muñoz
* Isaac Gamboa

## Métricas de los requerimientos no funcionales

### Performance

El equipo de desarrollo decidió utilizar las siguientes tecnologías Python + Django + Postgres.

1 request de pedir todos los registros a una base de datos SQLite desde una API con Django dura 75ms según los benchmarks realizados por Bednarz y Miłosz en [Benchmarking the performance of Python web frameworks](/Benchmarking_the_performance_of_Python_web_framewo.pdf).

Los benchmarks se llevaron a cabo en una máquina con las siguientes especificaciones de hardware:

* CPU: Intel Core i7-8750H
* RAM: 16 GB DDR4
* Storage: 1 TB, Samsung SSD 970 EVO
* Operating System: Windows 10 Home 64-bit  

¿Cuántas request por segundo es capaz de realizar una máquina de estas según los benchmarks observados (asumiendo que solo tiene 1 worker)?

1/0.075 = 13,33 req/s

¿Cuántas req/s ocupamos alcanzar según el requerimiento no funcional?

100,000/60 = 1667 req/s

Si 1 worker puede realizar 13,33 req/s, ¿Cuántos se necesitan para llegar a las 1667 req/s?

*Según la regla de 3* ~ 125

Utilizaremos 16 instancias de la máquina `r7i.2xlarge` (cada una tiene 8 workers) esta nos permite cumplir con los requerimientos no funcionales relacionados a Performance y también los relacionados a Scalability.

### Scalability

* REST + Django + MySQL

* utilizando una máquina Microsoft Windows con una CPU Intel Xeon E3-1230 (4 núcleos físicos, 8 hiperprocesos) y 24 GB de memoria, usando 4 CPUs se obtienen 691,66 req/s como lo podemos ver en el [benchmark](https://www.augmentedmind.de/2024/07/14/go-vs-python-performance-benchmark/#:~:text=This%20article%20benchmarks%20the%20performance,than%20for%20both%20Python%20frameworks)

* Transaccion: Ejecuta 200 solicitudes GET paralelas al backend REST durante un minuto.

* Requerimiento: 16,666 req/s (~1,000,000 req/min)

* Eligiendo la instancia "r7i.2xlarge" en AWS la cual posee 8 vCPUs, 4 CPU cores, si reservamos 10-15% se tiene que:

- Capacidad efectiva por pod usando 4 CPUs: 691.66 × 0.85 ≈ 588 req/s.
- Pods necesarios: 16,667 ÷ 588 ≈ 29 pods.

- Como la capacidad de la instancia solo alcanza para 1 pod que usa 4 CPUs, entonces vamos a necesitar ~29 pods de "r7i.2xlarge" configurados en el archivo de k8s.

- Se utilizará Kubernetes (EKS) para contenerización y autoescalado. Inicialmente se desplegarán ~4 pods (cada pod 4 vCPU / 8 GiB, rendimiento de referencia ~691 req/s por benchmark), sobre nodos r7i.2xlarge (8 vCPU, 64 GiB). El autoescalado horizontal (HPA) se activará por CPU (70 %), memoria (70 %) y solicitudes concurrentes por pod (métrica http_requests_inflight vía Prometheus Adapter), pudiendo crecer hasta 30 réplicas (~x10) según demanda. [Archivo Config K8s](/deploy/k8s/base/promptSales-api.yaml)

### Reliability

Se va a usar el servicio [Amazon CloudWatch](https://aws.amazon.com/es/cloudwatch/?nc2=type_a) de AWS para el monitoreo de alertas del sistema.
CloudWatch se encargará de recolectar métricas, logs y trazas, además de activar [CloudWatch Alarms](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html) cuando se superen los umbrales definidos.

Las alertas críticas se enviarán mediante [Amazon SNS](https://aws.amazon.com/es/sns/), el cual notificará por SMS, correo electrónico y WhatsApp usando un webhook externo conectado al grupo de soporte técnico.

Tasa de error permitidos 1% transacciones diarias.


### Availability

**Downtime permitido**:
A partir del requerimiento de disponibilidad mínima del 99.9 %, se calculó el tiempo máximo de inactividad permitido en un año.
Un año tiene 525 600 minutos, por lo que:

`525 600 x 0.999 = 525074.4 `

Al restar este resultado del total anual se obtiene el tiempo de inactividad permitido:
- 43.8 min mensuales
- 525.6 min anuales

**Balanceador de Carga**

Se va a usar el servicio [ALB](https://aws.amazon.com/es/elasticloadbalancing/application-load-balancer/) de AWS como balanceador de carga.
- Health checks: `interval: 10s`, `unhealthyThreshold: 3`, `timeout: 5s`.
- SLA AWS: [99.99%](https://d1.awsstatic.com/legal/AmazonElasticLoadBalancing/Amazon_Elastic_Load_Balancing_Service_Level_Agreement_2022-07-25_ES-ES.pdf)

**Kubernetes/EC2**

Se usa el servicio [EKS](https://docs.aws.amazon.com/es_es/eks/latest/userguide/what-is-eks.html) de AWS para kubernetes y [EC2](https://aws.amazon.com/es/ec2/) para computación.
- SLA EKS: [99.95%](https://d1.awsstatic.com/legal/amazon-eks-sla/Amazon%20EKS%20Service%20Level%20Agreement_Spanish_2022-05-04.pdf)
- SLA EC2: [99.99%](https://d1.awsstatic.com/legal/AmazonComputeServiceLevelAgreement/Amazon_Compute_Service_Level_Agreement_Spanish_2022-05-25.pdf)

**Bases de datos**

Para las bases de datos PostgreSQL y MySQL se utilizará [Amazon Aurora](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/CHAP_AuroraOverview.html)
- Aurora Multi-AZ (writer + reader)
- RPO objetivo: ≈ 0 s
- RTO objetivo (failover): ≤ 60 s (conmutación automática a réplica).
- SLA: [99.99%](https://aws.amazon.com/es/rds/aurora/sla/)

Para MongoDB se va a usar [MongoDB Atlas](https://aws.amazon.com/es/partners/mongodb/)
- Atlas Replica Set (3 nodos, 2+ AZ)
- RPO objetivo: ≈ 0 s
- RTO objetivo (election/failover): ≈ 10–60 s.
- SLA: [99.995%](https://www.mongodb.com/legal/sla/cloud/atlas-database)

**Backups**

Se configurarán backups automáticos diarios en Amazon Aurora y MongoDB Atlas,
con una retención mínima de 30 días según las políticas de cada servicio administrado.

**Cache**

Para el cache se va a usar el servicio [Amazon ElastiCache for Redis](https://aws.amazon.com/es/documentation-overview/redis/) en Multi-AZ con Auto-Failover
- SLA: [99.99%](https://d1.awsstatic.com/legal/elasticache-sla/Amazon%20Elasticache%20Service%20Level%20Agreement_2023-11-27-es_la-R-C.pdf)

**Uptime**

La disponibilidad sería 99.905%, cumpliendo así el requerimiento.

### Security

Se aplicará una autenticación basada en OpenID Connect. Esta será proporcionada por Okta.

Para cifrar los datos en la comunicación de REST se utilizará TLS. 

En las bases de datos Mongo, Postgres y MySQL utilizaremos el cifrado AES-256.

### Maintainability

El código se desarrollará de manera modular siguiendo DDD y separación de dominios.

Durante el desarrollo se seguirá el siguiente GitFlow

El branch `main` se utilizará únicamente para llevar el control de versiones en producción, estas son versiones finales de la plataforma. `develop` se utilizará para la integración de nuevas funcionalidades en preparación para la próxima versión final.

También se definen las siguientes sub-branches de soporte:

`feature/*` → nuevas funcionalidades (creadas desde develop).

`release/*` → preparación de una versión antes del despliegue (desde develop, luego se fusiona en main y develop).

`hotfix/*` → correcciones urgentes en producción (creadas desde main y luego fusionadas de vuelta a develop).

Todo PR a `main` debe incluir una descripción detallada del cambio que se realizó. Se utilizarán herramientas automáticas (CI/CD) para verificar el formato, calidad del código y pruebas unitarias. Solo tras la aprobación de los revisores el código se integra a la rama principal.

Esta es la estrategia que se seguirá para abordar hotfixes:

Primeramente se creará una rama desde main con el nombre `hotfix/*Info del bug*`, en esta rama se implementará y probará la corrección, una vez esta esté lista, se hará un PR hacia main (para despliegue inmediato). Seguidamente se fusionará el hotfix también hacia develop (para mantener sincronizadas las ramas). Por último se documentará el cambio.

Para el release de versiones se hará uso de la rama `release/*version*`. En esta se harán puebas QA para la validación funcional, de rendimiento y seguridad. En caso de que se necesiten correcciones menores estas se harán sobre la misma rama. Luego se hará un merge a `main` para desplegar en producción, y a `develop` para sincronización de cambios.

La estrategia de soporte post-release es la siguiente:

L0: Se creará y brindará soporte a centros de ayuda como foros y videos tutoriales. También se dispondrán chatbots con respuestas automáticas y flujos guiados.
Todo esto se complementará con documentación técnica y guías para desarrolladores.

L1: Se brindará soporte a solicitudes recibidas vía correo, chat o redes. También se tendrán a disposición scripts o flujos predefinidos para resolver problemas comunes.

L2: Para abordar los problemas no solucionados en L1 se dispondrá de personal capacitado para brindar soporte al usuario hasta llegar a una solución temporal o definitiva. Este soporte será brindado a través de reunión virtual o presencial, dependiendo de la disponibilidad.

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

## Domain Driven Design

### PromptContent

**Dominios principales**

- Creative Briefing: Encargado de recopilar los objetivos, públicos meta, tono y lineamientos del cliente para generar el brief creativo que guía toda la producción de contenido.

- Text Generation: Genera textos publicitarios, descripciones o copys basados en el brief aprobado. Aplica control de tono, idioma y longitud del mensaje según el canal.

- Image Generation: Produce imágenes, banners o ilustraciones usando modelos de IA y plantillas predefinidas, respetando los lineamientos del brief.

- Video Generation: Crea videos o animaciones a partir del contenido textual y visual generado. Gestiona duración, formato y metadatos por plataforma destino.

- Campaign Generation: Combina texto, imágenes y videos en piezas completas de campaña. Define variantes por canal, idioma y formato, y prepara entregables finales.

- Culture Campaign Generation: Adapta el contenido generado a contextos culturales e idiomáticos, asegurando coherencia local y evitando sesgos o errores culturales.

- SEO & Adaptation: Optimiza el contenido generado para motores de búsqueda y asistentes IA, ajustando keywords, títulos y metadatos según mercado y canal.

- External Publishing: Gestiona la publicación del contenido en plataformas externas (redes sociales, CMS, blogs o herramientas publicitarias) y controla su trazabilidad.

- Cloud: Proporciona almacenamiento centralizado, versionado y recuperación de recursos multimedia, además de controlar permisos de acceso entre dominios.

**Diagrama DDD PromptContent**

![DDD diagram](/diagrams/Promptcontent.png)

### PromptAds Domains

**Lista de dominios principales**

- Campaign Planning: Encargado de diseñar la campaña publicitaria a partir del objetivo definido por el cliente. Define los KPIs, canales, formatos y duración de la campaña.

- Targeting: Selecciona el público objetivo al que se mostrará la campaña, segmentando por datos demográficos, comportamiento, intereses y otras variables.

- Bidding and Budgeting: Establece las reglas de puja y presupuesto. Define cuánto se invertirá por canal o audiencia y cómo se distribuirá la oferta en cada plataforma.

- Activation Manager: Se encarga de activar y publicar la campaña en las plataformas externas (Google Ads, Meta Ads, TikTok, etc.) utilizando listas de control de acceso (ACL) y herramientas de integración.

- Insights: Recopila y presenta métricas clave de desempeño como clics, impresiones, CTR, tasa de conversión y otros indicadores de efectividad en tiempo real.

- Attribution: Asigna crédito de conversión a los distintos canales o interacciones que contribuyeron al cierre de una venta, permitiendo mejorar futuras campañas.

- Experimentation: Permite probar variaciones de campañas, audiencias o mensajes mediante pruebas A/B u otros métodos para optimizar resultados.

- Compliance: Supervisa el cumplimiento de regulaciones locales e internas. Aplica reglas por país o cliente, impone límites de gasto y registra cambios con trazabilidad (quién, qué, cuándo).

**Diagrama DDD PromptAds**

![DDD diagram](/diagrams/DiagramaDDDCorregido.drawio%20(1).png)

Se pueden observar la estructura de carpetas basada en este Domain Driven Design para PromptAds, asi como tambien plantillas de codigo de alguno elementos importantes como facades, contracts, use_cases y tests en la siguiente ruta -> [Organizacion y Plantillas](/PromptAds/)

Siempre que crees un nuevo dominio, agrega:

- `core/domain/<dominio>/...`
- `core/application/dto|interfaces|use_cases|facades`
- `core/infrastructure/db/models|repositories y adapters externos si aplica`
- `endpoints en api/v1/<dominio>/...`

### PromptCrm Domains
Este dominio se encarga principalmente del monitoreo de leads. Estos se registran y clasifican automáticamente con sus respectivos datos de proveniencia. Para la interacción con el usuario el dominio ofrece chatbots, voicebots y flujos automatizados de atención. Todo esto es proporcionado por la implementación de IA.

- Contacts Management Domain: registro de clientes, leads, cuentas, y organizaciones.

- Leads Segmentation Domain: clasificación por tipo, industria, potencial de compra, región, etc.

- Overall Leads Info Domain: consolidación de toda la información e historial en una sola interfaz.

**Diagrama DDD PromptCrm**

![DDD diagram](/diagrams/promptCrmDDDdiagram.png)

### Business Domain (Global)
Este dominio se encarga de validar qué funcionalidades de la plataforma el usuario es capaz de utilizar, esto va a depender del plan al que este se haya suscrito. También se encarga de gestionar todo lo relacionado con pagos por parte del usuario.

**Diagrama DDD PromptSales**
![DDD diagram](/diagrams/promptSalesDDDdiagram.png)

### Tecnologías
- Python: Lenguaje base del backend para todos los dominios.
- Django + DRF: Framework usado para exponer las REST APIs de cada dominio siguiendo DDD (viewsets, facades y clients).
- Aurora PostgreSQL / MySQL
    - PostgreSQL: datos de PromptAds y PromptCrm.
    - MySQL: datos de Global Domains (suscripciones, planes, billing).
- MongoDB Atlas: Base del dominio PromptContent para briefs, configuraciones y metadatos creativos.
- Redis (ElastiCache): Cache compartido para respuestas rápidas, tokens temporales y soporte a rate limiting / eventos.
- EKS + EC2 r7i.2xlarge: Clúster donde corren los pods.
- Application Load Balancer (ALB): Balancea tráfico HTTPS hacia EKS y aplica health checks.
- CloudWatch + Alarms + SNS: Monitoreo centralizado y alertas automáticas para cualquier dominio (logs, métricas y notificaciones).
- Okta: Identity Provider externo para SSO y emisión de tokens OIDC.
- TLS (ACM): Certificados administrados por AWS para cifrado HTTPS.
- Prometheus Adapter: Expone métricas al HPA para autoescalado (CPU, memoria, requests en vuelo).
- GitHub + GitHub Actions: Control de versiones, CI/CD y despliegue automatizado al clúster EKS.
- Cognito: Gestión del acceso en el API Gateway valida tokens y pasa claims a los dominios sin acoplar la lógica de autenticación.
- Vercel: Plataforma de despliegue para el portal web.
### Versionamiento 
El versionamiento se hace a nivel de API y deployment, no solo de ramas.

<<<<<<< HEAD
=======
Cada dominio expone endpoints versionados por ruta, por ejemplo:
- src/core/api/v1/brief/
  
Si se necesita una nueva versión:

Se duplica la carpeta v1, crea v2, ahí modifica sin romper a nadie.
- src/core/api/v2/brief/

Cada versión se despliega como un servicio independiente:

`promptcontent-api-v1`

`promptcontent-api-v2`

Se crea un nuevo deployment YAML: 
```yaml
metadata:
  name: promptcontent-api-v2
spec:
  containers:
    - image: promptsales/promptcontent:v2
```

El dev crea una nueva stage o base path mapping:

- /api/promptcontent/v1 - promptcontent-api-v1
- /api/promptcontent/v2 - promptcontent-api-v2

el gateway enruta el tráfico a la versión correcta y ambas conviven.

GitFlow se usa solo para el ciclo de desarrollo (feature/, release/, hotfix/, main), pero la compatibilidad entre versiones se garantiza en la capa de API Gateway + EKS manteniendo deployments separados por versión.


### Diagrama de arquitectura

>>>>>>> b4d3d9f94117e6782e32b884b61cc49f3130ddd9
## Big Pic
![DDD diagram](/diagrams/Captura%20de%20pantalla%202025-11-13%20235717.png)



## Otros Services relacionados al pub/sub model
![DDD diagram](/diagrams/Captura%20de%20pantalla%202025-11-13%20184323.png)

## Link a Miro 
https://miro.com/welcomeonboard/R1Z6NkY1clBwRHQ1allYbWRWMStuKyt4L3BGRFVyaFJ5WEd0aEdSdVhrdFkvZXAxR0REMExaODVLMlk4eHBJc0FzZWZFU3o3cUJGU0ppbGprdmNaeGNWSlE0U09TUnRlN0V4Wml6cmJzRnRnMUkyVmw2OHo2Vlc5SncrYldYd2p3VHhHVHd5UWtSM1BidUtUYmxycDRnPT0hdjE=?share_link_id=516617271561