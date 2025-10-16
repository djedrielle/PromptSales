# Entregable 1 - 26 de octubre último commit - 5%

## Métricas de los requerimientos no funcionales

Documentar cada atributo no funcional con valores cuantitativos, parámetros técnicos y tecnologías a usar. Incluir ejemplos claros, abajo se documentan ejemplos de valores y tecnologías, pero ustedes deben diseñar y encontrar sus propios valores los cuales deben estar justificados por alguna teoría o práctica debidamente argumentada y analizada; realizando las extrapolaciones o cálculos que usted pueda diseñar bajo un algoritmo o método cuantitativo diseñado por el grupo mismo. 


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


### Performance

* Tiempo máximo permitido para una consulta estándar: 1.5 segundos.
* Tiempo máximo para resultados cacheados: 200 ms usando Redis.
* Tecnología: PostgreSQL, Redis; aquí pueden ser métricas por las técnologías clave por separado. 

### Scalability

* Debe soportar incremento de carga de hasta 10x sin degradación.
* Kubernetes configurado con autoescalado horizontal por CPU y memoria. Justificarlo con la configuracion de K8s.

### Reliability

* Tasa de errores máxima permitida: 0.1% de transacciones por día.
* Monitoreo con pg_stat_statements y logs centralizados.
* Es importante determinar como se monitorea y como se notifican alertas. 

### Availability

* Disponibilidad mínima: 99.9% mensual. En el diseño de infraestructura debe lograr verse como se logra esto, podría ir en el diagrama de arquitectura, pero sería mejor uno de infraestructura. 
* Redis y bases de datos con failover y replicación.
* Considere load balancers. 

### Security

* Autenticación: OAuth 2.0 y/o OpenID Connect.
* Cifrado TLS 1.3 en comunicación y AES-256 en reposo.

### Maintainability

* Código modular siguiendo DDD y separación de dominios.
* Documentación en readme.md y comentarios claros en código.

### Interoperability

* Integración de APIs REST y MCP servers entre subempresas y servicios externos.

### Compliance

* Cumplimiento de GDPR en gestión de datos sensibles.

### Extensibility

* Arquitectura modular, permite agregar nuevas subempresas o módulos sin alterar sistemas existentes.

## Domain driven design

Para esto proceda en esta sección a: 

* Identificar todos los dominios principales por subempresa y dominios globales.
* Definir contratos entre dominios mediante interfaces o APIs.
* Crear facades para simplificar la interacción entre subempresas y dominios.
* Diseñar pruebas unitarias y de integración por dominio.
* Diagrama de dominios que muestre dependencias, límites de contexto y flujos de datos.
* Asegurar independencia entre dominios internos y globales.
* Esta documentación debe estar debidamente vinculada y guiada por código en el repositorio. 