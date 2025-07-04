
### 1. Purpose

Permitir la representación semántica de los Acuerdos de Nivel de Servicio para analizar la consistencia de los términos/cláusulas, facilitar la búsqueda de información, mejorar la interoperabilidad entre servicios, permitir la automatización y razonamiento. 

Representar formalmente los componentes estructurales, técnicos y jurídicos de un SLA para su posterior consulta, valizdación y monitoreo. 
---

### 2. Scope

SLAs machine-readable entre proveedor y consumidor de servicios SaaS que definan: 

1.- Representación de acciones que el proveedor y el consumidor pueden, deben o no tienen permitido realizar

2.- Representación de métricas de QoS

3.- Definición de objetivos cuantificables (SLOs), sus umbrales y condiciones

4.- Penalizaciones, monitoreo, fechas y violaciones

5.- Exclusiones y limitaciones de responsabilidad 

---

### 3. Implementation Language

RDF, RDFS

---

### 4. Intended End-Users

---

### 5. Intended Uses / Use Cases

CU1: Garantizar la interoperabilidad, consistencia y trazabilidad de los SLAs en las cadenas de servicios 

CU2: Monitorear el cumplimiento de los compromisos definidos en el SLA en tiempo de ejecución

CU3: Consultar las obligaciones, permisos, prohibiciones y restricciones definidas en un SLA concreto

CU4: Detectar automáticamente inconsistencias internas en los términos del SLA (métricas contradictorias, cláusulas de exclusión redundantes)

CU5: Verificar si los términos de un SLA están alineados con normativas o estándares (compliance)

CU6: Permitir la verificación automatizada de si las acciones realizadas por el proveedor o el consumidor están permitidas, obligadas o prohibidas según el SLA cuando se están intentando ejecutar (enforcement)

---

### 6. Ontology Requirements

#### a. Non-Functional Requirements

- **NFR 1:** 

#### b. Functional Requirements:

**CQ**
<!-- - CQ1. ¿Qué servicio se están ofreciendo y quién lo provee? Which services are governed by the SLA?
- CQ2. Which quality of service levels does a service deliver? (has commitment, SLO? en odrl sería una constraint)
- CQ3. Which particular properties of a service are guaranteed to have certain values? (which SLIs?)
- CQ4. Which compensations are offered if the guaranteed value of a property is not honored?
- CQ5. Who is the responsible party for enforcing the guaranteed service level values?
- CQ6. Who is the responsible party for monitoring and computing the guaranteed values?
- CQ7. During which period of time a guarantee is offered?
- CQ8. How are current values of a service property computed? -->

¿Qué **servicios** están gobernados por el SLA?

¿Qué **niveles de calidad** entrega un servicio? (SLOs, constraints)

¿Qué **propiedades del servicio** están garantizadas con ciertos valores? (SLIs)

¿Qué **compensaciones** se ofrecen si no se cumplen los valores garantizados?

¿Quién es **responsable** de hacer cumplir los valores garantizados?

¿Quién es **responsable de monitorear** y calcular los valores garantizados?

¿Durante qué **período de tiempo** se ofrece la garantía?

¿Cómo se **calculan** los valores actuales de una propiedad del servicio?

---

Natolana: ¿Qué compensaciones tiene como obligación el proveedor en caso de incumplimiento de un SLA?

Natolana: ¿Qué compensaciones están definidas para proveedores cuando la disponibilidad del servicio alcanza o supera un determinado umbral (eg. gteq 95%)? 

¿Qué proveedor tiene un SLA que satisface un umbral dado para una métrica de calidad como latencia, disponibilidad o throughput?

¿Ha habido alguna violación del SLA?

¿Cuál fue la causa y la fecha de la última violación?

---

| Proveedor             | Enlace al SLA                                                                                            | Métricas comunes                                                                                     |
| --------------------- | -------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| **Amazon AWS**        | [aws.amazon.com/legal/service-level-agreements/](https://aws.amazon.com/legal/service-level-agreements/) | Uptime (Availability %), Response Time (solo en servicios específicos), Monthly Uptime %, Error rate |
| **Microsoft Azure**   | [azure.microsoft.com/support/legal/sla/](https://azure.microsoft.com/support/legal/sla/)                 | Availability (%), Recovery Time Objective (RTO), Recovery Point Objective (RPO)                      |
| **Google Cloud**      | [cloud.google.com/terms/sla](https://cloud.google.com/terms/sla)                                         | Monthly Uptime %, Error Budget, Latency (a veces), Throughput                                        |
| **IBM Cloud**         | [cloud.ibm.com/docs/overview?topic=overview-sla](https://cloud.ibm.com/docs/overview?topic=overview-sla) | Availability %, MTTR (Mean Time to Repair)                                                           |
| **Salesforce (SaaS)** | [trust.salesforce.com](https://trust.salesforce.com) (reporte operativos, SLAs por contrato)             | Uptime %, Data Retention, Transaction latency                                                        |

---

### 7. Pre-Glossary of Terms

#### a. Terms from Competency Questions + Frequency

| Term               | Frequency |
|--------------------|-----------|
|  |  |

---

### 8. Non-Ontological Resources

---
### 9. Ontological Resources

- [odrl-model](https://www.w3.org/TR/odrl-model/)
- [odrl-vocab](https://www.w3.org/TR/odrl-vocab/)

---

**Label:** `tab:ORSD`
