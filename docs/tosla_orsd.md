
### 1. Purpose

Enable semantic representation of Service Level Agreements (SLAs) to analyse the consistency of terms and clauses, facilitate information retrieval, improve interoperability between services and support automation and reasoning.

Formally represent the structural, technical and legal components of an SLA for subsequent consultation, validation and monitoring.

---

### 2. Scope

Machine-readable SLAs between SaaS service provider and consumer that define:

1.- Representation of actions that the provider and the consumer can, must or are not allowed to perform.

2.- Representation of QoS metrics.

3.- Definition of measurable objectives (SLOs), their thresholds and conditions.

4.- Penalties, monitoring, dates and violations

5.- Exclusions and limitations of liability

---

### 3. Implementation Language

RDF, RDFS

---

### 4. Intended End-Users

The ontology is primarily conceived as a technical data model for researchers,practitioners and developers, enabling automated analysis and serving as a basis for building tools and powering applications to support non-technical stakeholders such as service providers, customers and government agencies.

- **SaaS Providers**  
Although they are not direct users of the ontology, they could benefit from tools built on it to define and formalise the terms of SLAs, monitor compliance, automate SLA reporting and provide transparent assurances to customers.

- **SaaS Customers**  
Even if they are not direct users of the ontology, they could use ontology-based tools to query and understand the guarantees offered, track compliance with SLAs, request redress and compare providers based on the terms of the SLAs.

- **Researchers / Practitioners / Developers**  
Researchers, practitioners and developers can use the ontology to study SLA models, analyse service performance and create methods to automate and improve SLAs. They can apply it to manage services, ensure contract compliance and monitor performance. They can also create SLA-aware tools, automate SLA checks and connect SLA data to service management platforms.

- **Government Agencies** 
Government agencies can use real-world SLAs modelled with the ontology to regulate service provision, verify compliance with legal requirements and audit service providers for regulatory compliance.

---

### 5. Intended Uses / Use Cases

CU1: Ensure interoperability, consistency and traceability of SLAs in service chains.

CU2: Monitor compliance with the commitments defined in the SLA at runtime.

CU3: Query obligations, permissions, prohibitions and restrictions defined in a particular SLA

CU4: Automatically detect internal inconsistencies in the terms of the SLA (contradictory metrics, redundant exclusion clauses)

CU5: Verify whether the terms of an SLA are aligned with regulations or standards (compliance)

CU6: Enable automated verification of whether actions performed by the provider or consumer are permitted, required or prohibited under the SLA when they are attempted (enforcement).

---

### 6. Ontology Requirements

#### a. Non-Functional Requirements

- **NFR 1:** The ontology shall be published online with standard documentation

#### b. Functional Requirements:

**Competency Questions**
- CQ1. Which services are governed by the SLA?
- CQ2. Which quality of service levels does a service deliver? (has commitment, SLO?)
- CQ3. Which particular properties of a service are guaranteed to have certain values? (which SLIs?)
- CQ4. Which compensations are offered if the guaranteed value of a property is not honored?
- CQ5. Who is the responsible party for enforcing the guaranteed service level values?
- CQ6. Who is the responsible party for monitoring and computing the guaranteed values?
- CQ7. During which period of time a guarantee is offered?
- CQ8. How are current values of a service property computed? 


### 7. Pre-Glossary of Terms

### a. Terms from Competency Questions + Frequency

| Term              | Frequency |
|-------------------|-----------|
| Service           | 2         |
| Provider          | 2         |
| SLA               | 1         |
| QoS               | 1         |
| Commitment        | 1         |
| SLI               | 1         |
| Service Property  | 2         |
| Compensation      | 1         |
| Penalties         | 1         |
| Obligation        | 1         |
| Liability         | 1         |
| Computation       | 2         |
| Evaluation        | 1         |
| Period Interval   | 1         |
| Metric Expression | 1         |

---
### 8. Non-Ontological Resources

- [NIST-500-307](https://www.nist.gov/publications/cloud-computing-service-metrics-description)
- [ISO-IEC-19086](https://www.iso.org/standard/67545.html)
- [Garcia_et_al](https://ieeexplore.ieee.org/document/7519020)
- [Ganapathy_et_al](https://ieeexplore.ieee.org/document/9678067)

---
### 9. Ontological Resources

- [odrl-model](https://www.w3.org/TR/odrl-model/)
- [odrl-vocab](https://www.w3.org/TR/odrl-vocab/)
- [tosl](https://github.com/isa-group/tosl)
- [linked-usdl-agreement](https://github.com/linked-usdl/usdl-agreement) 
- [qudt](https://qudt.org/) 
- [time](https://www.w3.org/TR/owl-time/)

---

**Label:** `tab:ORSD`
