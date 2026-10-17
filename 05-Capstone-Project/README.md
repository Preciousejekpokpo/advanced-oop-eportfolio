# Capstone Project: Transaction Verification and AI-Aware Review

This capstone brings together the banking exercises to investigate whether recorded transaction evidence is sufficient for model review. The integration adds a record-count check to the existing reconciliation process and tests both its usefulness and its limitations.

## Project evidence

- [Capstone evaluation](CAPSTONE_EVALUATION.md)
- [Workflow implementation](../02-Coding-Exercises/BankAccount/capstone_workflow.py)
- [Integration tests](../02-Coding-Exercises/BankAccount/test_capstone_workflow.py)



## Architecture and verification flow

The diagram shows how the existing banking components support the capstone's verification process. Model advice is only requested after the available transaction evidence passes the preliminary checks.

```mermaid
flowchart TD
    A["RecordedScenarioFactory<br/>(Abstract Factory)"]
    B["BankingScenario"]
    C["StrategySimulator<br/>(Strategy)"]
    D["RecordingAccount<br/>(Decorator)"]
    E["BankAccount<br/>(Thread-safe balances)"]
    F["Transaction records"]
    G["RecordedMovementCheck<br/>(CashFlowVisitor)"]
    H{"Balance movement agrees?"}
    I{"Record count matches<br/>scheduled attempts?"}
    J["ModelReviewService<br/>(Reconciliation and Visitors)"]
    K["ReviewModel<br/>(Mocked in tests)"]
    L["Manual review"]
    M["Advisory only"]

    A --> B
    B --> C
    C --> D
    D --> E
    D --> F
    B --> G
    F --> G
    G --> H
    H -- No --> L
    H -- Yes --> I
    C -. "Expected count" .-> I
    F --> I
    I -- No --> L
    I -- Yes --> J
    F --> J
    J -- "Evidence mismatch or model failure" --> L
    J -- "Checks pass" --> K
    K -- "Valid suggestion" --> M
    K -- "Invalid response" --> L
```

