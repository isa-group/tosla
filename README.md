# TOSLA

Terms of Service Level Agreement (TOSLA) ODRL Profile is a vocabulary designed to incorporate the terminology necessary to semantically represent the terms defined in Service Level Agreements. It extends the W3C-recommended Open Digital Rights Language (ODRL) policy expression language standard.

With this model, based on a set of existing ontologies and domain-specific vocabularies, it is possible to formally and semantically interoperably represent the commitments undertaken by the provider to achieve defined levels of one or more Service Level Indicators (SLIs). In addition, the model enables the detailed description of:  

- The customer's obligations to monitor the fulfillment of such indicators and, where appropriate, to notify or submit claims in case of non-compliance.
- The provider's obligations to remedy and, optionally, to compensate when the established levels are not achieved.
- The conditions, metrics, and evaluation periods that determine the activation of these obligations.
- The exclusions of the provider's liability in cases of service unavailability due to certain circumstances beyond its control, which can also be formally defined as conditional clauses.  

## Profile diagram

![ontology_model](img/tosla_model_core_concepts.png)
---
![ontology_model_2](img/tosla_model_agreement_term_constraint_liability.png)

## Sample with TOSLA

Partial example of how the terms of an SLA would be modelled. In particular, it shows a guarantee clause, the consequences in case of non-compliance, the obligation to file a claim and an example of compensation.

```ttl
# Assets description
:instanceEcsService a tosl:Service ;
    dcterms:description "Alibaba Cloud Elastic Compute Service (ECS) instance offering covered by this SLA." ;
    dcterms:rightsHolder :alibaba .

:serviceCredit a odrl:Asset ;
    rdfs:label "Service Credit"@en ;
    dcterms:description "A monetary credit applied to the Customer’s account as compensation for non-compliance with the Service Level Agreement." .

# Properties 
:monthlyUptimePercentageInstanceUnavailable a odrl:LeftOperand ;
    rdfs:label "Monthly Uptime Percentage - Instance Unavailable"@en ;
    dcterms:description "Percentage availability per ECS instance in the month." ;
    usdl-agreement:hasMetric :monthlyUptimeMetric .

:monthlyUptimeMetric a usdl-agreement:Metric ;
    qudt:unit <http://qudt.org/vocab/unit#Percent> ;
    usdl-agreement:hasExpression "100 * ((?serviceCycleMinutes - ?downtimeMinutes) / ?serviceCycleMinutes)"^^xsd:string ;
    usdl-agreement:hasMeasuringInterval :monthlyInterval .

:monthlyInterval a time:Interval ;
    time:hasDurationDescription [
        a time:DurationDescription ;
        time:months "1"^^xsd:integer
    ] .

:serviceCreditPercentage a odrl:LeftOperand ;
    rdfs:label "Service Credit Percentage"@en ;
    dcterms:description "Percentage of the Monthly Service Fee to credit." .

# Uptime Commitment Instance
:uptimeCommitmentInstance a odrl:Duty ;
    dcterms:description "Alibaba must provide at least 99.975% uptime per instance." ;
    odrl:assignee :alibaba ;
    odrl:target :instanceEcsService ;
    odrl:action [
        a odrl:Action ;
        rdf:value tosla:guarantee;
        odrl:refinement [
            a odrl:Constraint;
            odrl:leftOperand :monthlyUptimePercentageInstanceUnavailable ;
            odrl:operator odrl:gteq ;
            odrl:rightOperand "99.975"^^xsd:decimal ;
            odrl:unit <http://qudt.org/vocab/unit#Percent>
        ] ;
        odrl:refinement [
            a odrl:Constraint;
            odrl:leftOperand odrl:timeInterval;
            odrl:operator odrl:eq ;
            odrl:rightOperand "P30D"^^xsd:duration
        ]; 
    ];
    tosl:liability [ 
        a tosl:Liability ;
        dcterms:description "The customer is responsible for monitoring, calculating the total downtime and compiling all information regarding service unavailability in order to claim compensation.";
        rdf:value tosla:conditionEvaluation, tosla:metricComputation ;
        tosl:liableParty :customer 
    ] ;
    odrl:consequence :customerClaimInstance ;
    odrl:consequence :compensationInstance10 .

:customerClaimInstance a odrl:Duty ;
    dcterms:description "Customer must submit the claim within the defined time window." ;
    odrl:assignee :customer ;
    odrl:target :instanceEcsService ;
    odrl:action [
        a odrl:Action ;
        rdf:value tosl:claim ;
        odrl:refinement [
            a odrl:Constraint;
            odrl:leftOperand odrl:timeInterval ;
            odrl:operator odrl:eq ;
            odrl:rightOperand :claimWindow
        ] ;
    ] ;
    odrl:constraint [
        odrl:leftOperand :monthlyUptimePercentageInstanceUnavailable ;
        odrl:operator odrl:lt ;
        odrl:rightOperand "99.975"^^xsd:decimal ;
        odrl:unit <http://qudt.org/vocab/unit#Percent>
    ] .    
    
:compensationInstance10 a odrl:Duty ;
    dcterms:description "10% credit if instance uptime <99.975% but ≥99%." ;
    odrl:compensatedParty :customer ;
    odrl:compensatingParty :alibaba ;
    odrl:assignee :alibaba ;
    odrl:target :instanceEcsService ;
    odrl:action [
        a odrl:Action ;
        rdf:value odrl:compensate;
        odrl:refinement [
            a odrl:Constraint ;
            odrl:leftOperand :serviceCreditPercentage ;
            odrl:operator odrl:eq ;
            odrl:rightOperand "10"^^xsd:decimal ;
            odrl:unit <http://qudt.org/vocab/unit#Percent>
        ] ;
    ];
    odrl:constraint [
        a odrl:LogicalConstraint ;
        odrl:and (
            [ 
                a odrl:Constraint ;
                odrl:leftOperand :monthlyUptimePercentageInstanceUnavailable ; 
                odrl:operator odrl:gteq ; 
                odrl:rightOperand "99.0"^^xsd:decimal ;
                odrl:unit <http://qudt.org/vocab/unit#Percent>
            ]
            [ 
                a odrl:Constraint ;
                odrl:leftOperand :monthlyUptimePercentageInstanceUnavailable ; 
                odrl:operator odrl:lt ; 
                odrl:rightOperand "99.975"^^xsd:decimal ;
                odrl:unit <http://qudt.org/vocab/unit#Percent>
            ]
        )
    ] .
```

## Repository Structure

`bin/`
Scripts for running SPARQL queries.TThe "competency_quetion_evaluation.ipynb" notebook executes all queries on the modelled SLAs.

`docs/` Contains the TOSLA Ontology Requirements Specification Document.

`examples/`
TOSLA representations of real agreements.

`img/` Contains the conceptual metamodel.

`sparql_queries/`
SPARQL queries for analysing SLA information, deontic modalities and identifying potentially abusive terms.

`validator/` SHACL rules for testing SLA representation conformance to the TOSLA structure.

`tosla.ttl`
Ontology file (TBox), defining structured concepts.

## Running a Query Using Jupiter Notebook

1. Clone the repository.
2. Open the file `bin/competency_questions_evaluation.ipynb`.
3. First part of the notebook is the TOSLA validator and later the Competency Questions, Potentially unfair terms and the obligations, permissions, and prohibitions of the parties.
4. Execute the code cell and modify the KG as needed.


```plaintext

````



