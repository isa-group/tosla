## TOSLA Validator

These diagrams represent the **validator shapes** for **TOSLA**. They visually define how **permissions**, **obligations**, **prohibitions**, **dispute resolution**, and **liability** statements are validated using **SHACL**, including validation of the predefined instances.

- **Solid arrows** represent **mandatory** elements in the model.
- **Dotted arrows** represent **optional** elements in the model.
- **Subroutine-shaped nodes** indicate that an **auxiliary validation subroutine** exists for that object (e.g., **Liability** and **Constraint**).

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Agreement Validator] --> B[Agreement]

    B --> C[Rule]
    B -. onDispute .-> D[[Dispute Resolution]]
    B -. liability / limitationOfLiability .-> E[[Liability]]

    C -. permission .-> F[[Permission]]
    C -. obligation .-> G[[Duty]]
    C -. prohibition .-> H[[Prohibition]]

```

#### Permission Rule Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Permission Validator] --> C[Exist a Rule]
    C -- permission --> D[Permission]
    D -- description --> P[Statement Description]

    D -- assignee --> G[Party]
    D -- action --> H[Action]
    D -- asset --> I[Asset]

    H -. refinement .-> J
    D -. constraint .-> J[[Constraint]]
    D -. logicalConstraint .-> R[Operand]
    R --> J

    I -. liability / limitationOfLiability .-> X[[Liability]]
    D -. liability / limitationOfLiability .-> X
    D -. duty .-> E[Duty]
    D -. trigger .-> E

    E -- description --> Q[Statement Description]
    E -- assignee --> L[Party]
    E -- action --> M[Action]
    E -- asset --> O[Asset]
    M -. refinement .-> N
    E -. constraint .-> N[[Constraint]]
    E -. logicalConstraint .-> S[Operand]
    S --> N
    O -. liability / limitationOfLiability .-> Y[[Liability]]
    E -. liability / limitationOfLiability .-> Y
    E -. consequence .-> E
```

#### Duty Rule Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Obligation Validator] --> C[Exist a Rule]
    C -- obligation --> D[Duty]
    D -- description --> P[Statement Description]

    D -- assignee --> G[Party]
    D -- action --> H[Action]
    D -- asset --> I[Asset]

    I -. liability / limitationOfLiability .-> X[[Liability]]

    H -. refinement .-> J
    D -. constraint .-> J[[Constraint]]
    D -. logicalConstraint .-> R[Operand]
    R --> J
    D -. liability / limitationOfLiability .-> X
    D -. consequence .-> D
```

#### Prohibition Rule Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Prohibition Validator] --> C[Exist a Rule]
    C -- prohibition --> D[Prohibition]
    D -- description --> P[Statement Description]

    D -- assignee --> G[Party]
    D -- action --> H[Action]
    D -- asset --> I[Asset]

    H -. refinement .-> J
    D -. constraint .-> J[[Constraint]]
    D -. logicalConstraint .-> R[Operand]
    R --> J

    I -. liability / limitationOfLiability .-> X[[Liability]]
    D -. liability / limitationOfLiability .-> X
    D -. remedy .-> E[Duty]
    
    E -- description --> Q[Statement Description]
    E -- assignee --> L[Party]
    E -- action --> M[Action]
    E -- asset --> O[Asset]
    O -. liability / limitationOfLiability .-> Y[[Liability]]
    M -. refinement .-> N
    E -. constraint .-> N[[Constraint]]
    E -. logicalConstraint .-> S[Operand]
    S --> N
    E -. liability / limitationOfLiability .-> Y
    E -. consequence .-> E
```

#### Dispute Resolution Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Dispute Resolution Validator] --> B[Litigation]
    A --> C[Arbitration]
    B -. requires .-> C

    B -- description --> G[Statement Description]
    B -- targetParty --> H[Party]
    B -- takePlaceIn --> D[Jurisdiction]
    B -- governedBy --> E[Law]
    B -. condition .-> F[[Constraint]]
    B -. logicalConstraint .-> R[Operand]
    R --> F


    C -. condition .-> M[[Constraint]]
    C -. logicalConstraint .-> P[Operand]
    P --> M

    C -- description --> I[Statement Description]
    C -- targetParty --> J[Party]
    C -- takePlaceIn --> K[Jurisdiction]
    C -- governedBy --> L[Law]
   
```

#### Liability  Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Liability Validator] -- liability / limitationOfLiability --> B[Liability]

    B -- description --> E[Statement Description]

    B -- liableParty --> C[Party]
    B -- targetParty --> C
    B -- rdf:value --> Value
    B -. limitation .-> D[[Constraint]]
    B -. logicalConstraint .-> R[Operand]
    R --> D
```

#### Constraint Validator Diagram

```mermaid 
%%{ init: { "theme": "neutral" } }%%
flowchart TD

    A[SHACL Constraint Validator] -- constraint --> B[Constraint]

    B -- leftOperand --> C[Left Operand]
    B -- operator --> D[Operator]
    B -- rightOperand -->  E[Right Operand]
    B -. unit .-> F[Unit]
```