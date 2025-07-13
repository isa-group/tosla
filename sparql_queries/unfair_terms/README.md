# Identification of Unfair Clauses

This document provides a guide for identifying potentially unfair contractual clauses, based on the theoretical framework proposed by [**Lippi et al.**](https://link.springer.com/article/10.1007/s10506-019-09243-2) and the [**Directive 93/13/EEC**](https://eur-lex.europa.eu/eli/dir/1993/13/oj/eng) (UCTD 93/13). It also includes a SPARQL query applied to the TOSL model for automated detection.

<details>
<summary>Arbitration</summary>

### 1. Classification According to Lippi et al.

**Arbitration clauses** can be categorised into three types:

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `If fully optional`                  | Arbitration is offered as an option, and the consumer can choose to go to court instead. | ❌ Not unfair          |
| `In any other case than below or above` | Arbitration is mandatory but not extreme    | ⚠️ Potentially unfair  |
| `If in another country // not based on law but arbiter’s direction` | Arbitration takes place in another country or is governed by non-legal/arbitrary rules. | ✅ Unfair              |

---

### 2. Criteria According to Directive 93/13 (UCTD)

Directive 93/13/EEC establishes that:

> excluding or hindering the consumer's right to take legal action or exercise any other legal remedy, particularly by requiring the consumer to take disputes exclusively to arbitration not covered by legal provisions, unduly restricting the evidence available to him or imposing on him a burden of proof which, according to the applicable law, should lie with another party to the contract.

---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Is participation in arbitration fully optional for the consumer?  
- **CQ2**: Does the arbitration term make arbitration mandatory before any court action can be taken?  
- **CQ3**: Does the arbitration term require arbitration to take place in another country?  
- **CQ4**: Is the arbitration process based on established law, or is it solely at the arbitrator's discretion?

#### Evaluation

To detect such clauses automatically, a SPARQL query has been implemented over contracts modeled using the **TOSL ontology**.

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Is arbitration optional and litigation still available?                | ✅ Not unfair                        |
| Is arbitration required and replaces the right to litigation?         | ❌ Unfair                            |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT DISTINCT ?arbitration (COUNT(?litigation) AS ?litigationCount)
WHERE {

  ?arbitration a tosl:Arbitration .
  
  OPTIONAL {
    ?litigation a tosl:Litigation .
    ?litigation tosl:requires ?arbitration .
  }

}
GROUP BY ?arbitration
HAVING (SUM(IF(BOUND(?litigation), 1, 0)) = COUNT(?litigation))
```

---
</details>

<details>
<summary>Choice of Law</summary>

### 1. Classification According to Lippi et al.

**Choice of Law** define which country's legal system governs the contract. Their fairness depends on whether the chosen law protects the consumer appropriately.

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `When it’s consumer’s residence country’s law` | The contract is governed by the law of the country where the consumer resides. | ❌ Not unfair          |
| `In any other case`                  | The contract applies a different law that may not offer the same protection. | ⚠️ Potentially unfair  |
| `Not possible`                       | -                        | -           |

---

### 2. Automated Detection with SPARQL and TOSL

#### Competency Question

- **CQ1**: Is the governing law fixed (e.g., US federal law) and not the same as the consumer's country of residence?

#### Evaluation

To detect such clauses automatically, a SPARQL query has been implemented over contracts modeled using the **TOSL ontology**.

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Is the applicable law that of the consumer’s place of residence?      | ✅ Not unfair                        |
| Is another law applied that may limit consumer protection?            | ❌ Unfair                            |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT DISTINCT ?dispute ?litigation ?law
WHERE {
  ?dispute tosl:onDispute ?litigation .
  ?litigation a tosl:Litigation ;
              tosl:governedBy ?law .
  
  FILTER NOT EXISTS {
    ?litigation tosl:governedBy tosl:consumerPlaceLaw .
  }

  FILTER NOT EXISTS {
    ?litigation tosl:targetParty ?party .
    ?party a tosl:BusinessCustomer .
  }
}
```

</details>

<details>
<summary>Content Removal</summary>

### 1. Classification According to Lippi et al.

**Content Removal clauses** refer to the provider’s ability to delete, remove, or restrict access to user content. 

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `Not possible`                       | -       | - |
| `When reasons are specified`         | Content can be removed, but only for specified and valid reasons.        | ⚠️ Potentially unfair  |
| `If there’s no reasons needed // full discretion // no prior notice nor possibility to retrieve the content` | Content can be removed at the provider’s full discretion, without justification, notice, or recovery options. | ✅ Unfair              |

---

### 2. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Can the service provider remove the consumer's content?
- **CQ2**: Are specific reasons for content removal explicitly stated in the contract?
- **CQ3**: Does the service provider have full discretion to remove content without providing reasons?
- **CQ4**: Is prior notice required to be given to the user before content removal?
- **CQ5**: Can the consumer retrieve the content before removal?

#### Evaluation

To detect such clauses automatically, a SPARQL query has been implemented over contracts modeled using the **TOSL ontology**.

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Is content removal based on specific justification and prior notice?  | ✅ Not unfair                        |
| Is removal allowed without reason, notice, or possibility of recovery?| ❌ Unfair                            |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT ?permission ?action ?assignee ?target
WHERE {
    ?permission a odrl:Permission ;
        odrl:action ?action ;
        odrl:assignee ?assignee ;
        odrl:target ?target .
    
    ?assignee a tosl:Provider .

    FILTER (?action = tosl:remove)

    OPTIONAL {
        ?permission odrl:constraint ?constraint .
        ?constraint odrl:leftOperand tosl:justification
    }
    OPTIONAL {
        ?permission odrl:duty ?duty .
        ?duty odrl:action odrl:inform .
    }

    FILTER (!BOUND(?constraint) || !BOUND(?duty))
}
```

---
</details>

<details>
<summary>Contract by Using</summary>

### 1. Classification According to Lippi et al.

**Contract by Using clauses** bind the consumer to contractual terms simply through the use of a service or product, often without explicit consent.

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `Not possible`                       | -      | -    |
| `Always binding by use`              | The contract is deemed accepted just by using the service, regardless of explicit agreement or awareness. | ⚠️ Potentially unfair  |
| `Not possible`                       | -             | -         |


### 2. Criteria According to Directive 93/13 (UCTD)

Directive 93/13/EEC establishes that:

> irrevocably binding the consumer to terms with which he had no real opportunity of becoming acquainted before the conclusion of the contract;


---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: In what ways does the consumer provide consent to the terms of a contract?
- **CQ2**: Is the user legally bound by terms just by using the service?

#### Evaluation

To detect such clauses automatically, a SPARQL query has been implemented over contracts modeled using the **TOSL ontology**.

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Is the contract accepted through explicit and informed consent?        | ✅ Not unfair                        |
| Is the consumer considered to have accepted the contract by mere use or implied consent? | ⚠️ Potentially unfair              |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT ?duty ?action ?assignee ?target
WHERE {
    ?duty a odrl:Duty ;
          odrl:action ?action ;
          odrl:assignee ?assignee ;
          odrl:target ?target ;
          odrl:constraint ?constraint .

    ?assignee a tosl:Customer .
    ?constraint odrl:rightOperand tosl:implicitConsent .

    FILTER (?action = tosl:consent)
}
```

---
</details>

<details>
<summary>Jurisdiction</summary>

### 1. Classification According to Lippi et al.

**Jurisdiction clauses** determine the location or court where legal disputes must be resolved.

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `When it’s consumer’s place of residence` | Disputes are handled in the courts of the consumer’s place of residence. | ❌ Not unfair          |
| `Not possible`                       | -         | -
| `Takes a residence away`             | The clause requires disputes to be settled in a different city or country, limiting the consumer’s access to legal action. | ✅ Unfair              |

---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Does the contract specify jurisdiction for dispute resolution?
- **CQ2**: Does the jurisdiction term require dispute resolution in a different city, state, or country from the consumer's residence?

#### Evaluation

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Does the dispute take place in the courts of the consumer’s residence?| ✅ Not unfair                        |
| Is jurisdiction assigned to a different city or country?              | ❌ Unfair                            |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT DISTINCT ?dispute ?litigation ?place
WHERE {
  ?dispute tosl:onDispute ?litigation .
  ?litigation a tosl:Litigation ;
              tosl:takesPlaceIn ?place .

  FILTER NOT EXISTS {
    ?litigation tosl:takesPlaceIn tosl:consumerPlaceCourts .
  }

  FILTER NOT EXISTS {
    ?litigation tosl:targetParty ?party .
    ?party a tosl:BusinessCustomer .
  }
}
```

---
</details>

<details>
<summary>Limitation of Liability</summary>

### 1. Classification According to Lippi et al.

**Limitation of Liability clauses** attempt to restrict the provider’s responsibility for damages or harm. 

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `If stated that the provider is liable` | The provider accepts liability under certain conditions.                 | ❌ Not unfair          |
| `For any action taken by other people // for damages incurred by the computer because of malware // blanket disclaimers like “to the fullest extent permissible by law”` | Disclaims liability in overly broad or vague terms, including for third-party actions or common technical risks. | ⚠️ Potentially unfair  |
| `For physical injuries (health/life) // gross negligence // intentional damage` | Attempts to waive liability for serious harm or unlawful behavior.       | ✅ Unfair              |


### 2. Criteria According to Directive 93/13 (UCTD)

Directive 93/13/EEC establishes that:

> inappropriately excluding or limiting the legal rights of the consumer vis-à-vis the seller or supplier or another party in the event of total or partial non-performance or inadequate performance by the seller or supplier of any of the contractual obligations, including the option of offsetting a debt owed to the seller or supplier against any claim which the consumer may have against him;

---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Does the contract state that the provider is liable for any damages or losses?
- **CQ2**: Is the provider not liable for damages incurred by malware or harmful software, as stated in the contract?
- **CQ3**: Does the contract contain blanket phrases like "to the fullest extent permissible by law" to limit liability?
- **CQ4**: Are there provisions in the contract where the provider disclaims liability for physical injuries, health issues, or loss of life?
- **CQ5**: Does the contract attempt to exempt the provider from liability for gross negligence or intentional damage?

#### Evaluation

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Is liability accepted for key risks (e.g. physical harm, gross negligence)? | ✅ Not unfair                    |
| Is liability waived for physical injuries, malware damage, or through vague blanket disclaimers? | ❌ Unfair              |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT DISTINCT ?liability ?description ?limitationOn ?type ?liableParty
WHERE {
  ?liability a tosl:Liability ;
    dcterms:description ?description ;
    tosl:liableParty ?liableParty ;
    tosl:targetParty ?targetParty ;
    rdf:value ?type .

  ?targetParty a tosl:Customer .
  
  ?liableParty a tosl:Provider .
  
  {
    ?limitationOn tosl:limitationOfLiability ?liability .
  } UNION {
    ?limitationOn tosl:liability ?liability .
    ?liability odrl:limitation ?constraint .  
  }

  FILTER (?type IN (
    tosl:anyLiability,
    tosl:physicalInjuries,
    tosl:harmCausedByMalware,
    tosl:discontinuity,
    tosl:anyIndirectDamage,
    tosl:directDamage,
    tosl:anyLoss,
    tosl:thirdparty,
    tosl:serviceContent,
    tosl:breachOfContract,
    tosl:legalCompliance
  ))
}
```

---
</details>

<details>
<summary>Unilateral Change</summary>

### 1. Classification According to Lippi et al.

**Unilateral Change clauses** allow the provider to modify the contract terms after it has been accepted, often without the consumer’s consent.

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `Not possible`                       | -           | -      |
| `Any unilateral change`              | The provider reserves the right to change terms without needing consumer consent or valid reason. | ⚠️ Potentially unfair  |
| `Not possible`                       | -      | -   |


### 2. Criteria According to Directive 93/13 (UCTD)

Directive 93/13/EEC establishes that:

> enabling the seller or supplier to alter the terms of the contract unilaterally without a valid reason which is specified in the contract.

> enabling the seller or supplier to alter unilaterally without a valid reason any characteristics of the product or service to be provided

---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Is the provider allowed to modify the contract unilaterally?
- **CQ2**: Does the contract require the provider to give notice before making changes?
- **CQ3**: Can the consumer terminate the contract if they disagree with the changes made by the provider?

#### Evaluation

| Criterion                                                              | Evaluation                          |
|------------------------------------------------------------------------|--------------------------------------|
| Are changes justified and the consumer is informed in advance?        | ✅ Not unfair                        |
| Are changes made unilaterally without reason or prior notice?         | ⚠️ Potentially unfair                |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT ?permission ?action ?target
WHERE {
    ?permission a odrl:Permission ;
        odrl:action ?action ;
        odrl:target ?target .

    ?assignee a tosl:Provider .

    FILTER (?action = odrl:modify)

    OPTIONAL {
        ?permission odrl:constraint ?constraint .
        ?constraint odrl:leftOperand tosl:justification
    }
    OPTIONAL {
        ?permission odrl:duty ?duty .
        ?duty odrl:action odrl:inform .
    }

    FILTER (!BOUND(?constraint) || !BOUND(?duty))
}
```

---
</details>

<details>
<summary>Unilateral Termination</summary>

### 1. Classification According to Lippi et al.

**Unilateral termination** clauses can be categorized into three types:

| Clause Type                          | Description                                                              | Unfair?               |
|--------------------------------------|--------------------------------------------------------------------------|------------------------|
| `Not possible`                       | -         | -         |
| `If there are reasons specified`     | Allowed only if a specific reason is stated.                            | ⚠️ Potentially unfair  |
| `If for any reason / without notice` | Allowed without any reason or prior notice.                             | ✅ Unfair              |

---

### 2. Criteria According to Directive 93/13 (UCTD)

Directive 93/13/EEC establishes that:

> authorizing the seller or supplier to dissolve the contract on a discretionary basis where the same facility is not granted to the consumer, or permitting the seller or supplier to retain the sums paid for services not yet supplied by him where it is the seller or supplier himself who dissolves the contract.

> enabling the seller or supplier to terminate a contract of indeterminate duration without reasonable notice except where there are serious grounds for doing so.

---

### 3. Automated Detection with SPARQL and TOSL

#### Competency Questions

- **CQ1**: Can the provider terminate the contract unilaterally?
- **CQ2**: Does it specify specific causes, or termination is allowed without justified cause?
- **CQ3**: Is the provider required to give notice before terminating the contract?

#### Evaluation

| Criterion                                            | Evaluation                          |
|------------------------------------------------------|--------------------------------------|
| Is justification required and advance notice given?  | ✅ Not unfair if both are present     |
| Is either element missing?                           | ❌ Unfair                            |

#### SPARQL Query:

```sparql
PREFIX odrl: <http://www.w3.org/ns/odrl/2/>
PREFIX tosl: <https://w3id.org/tosl/>

SELECT ?permission ?action ?assignee ?target
WHERE {
    ?permission a odrl:Permission ;
               odrl:action ?action ;
               odrl:assignee ?assignee ;
               odrl:target ?target .

    ?assignee a tosl:Provider .

    FILTER (?action = tosl:terminate || ?action = tosl:suspend || ?action = tosl:disable)

    OPTIONAL {
        ?permission odrl:constraint ?constraint .
        ?constraint odrl:leftOperand tosl:justification
    }
    OPTIONAL {
        ?permission odrl:duty ?duty .
        ?duty odrl:action odrl:inform .
    }

    FILTER (!BOUND(?constraint) || !BOUND(?duty))
}
```

---
</details>
