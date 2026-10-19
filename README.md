# Advanced Object-Oriented Design and Programming e-Portfolio

This portfolio documents my progression from a thread-safe banking system to design-pattern implementations, testing investigations and an AI-facing review prototype. The supporting code, tests and evaluations show both what I implemented and the limitations identified through further investigation.

## Assessment Tasks

### 1. Learning Outcomes

[**Task 1 – Learning Outcomes**](01-Module-Reflection/LEARNING_OUTCOMES.md)

Examines my development across the five learning outcomes, including secure coding, object-oriented programming, design patterns, architecture and AI-aware design. It connects lecturer feedback and independent study with tested artefacts and areas requiring further work.

### 2. Practical Artefacts and Testing

The practical evidence is organised into four connected sections.

1. **[Banking System and Design Patterns](02-Coding-Exercises/BankAccount/README.md)**

   The original thread-safe banking implementation, twelve unit tests, requirements traceability, contention benchmarking and investigations of Strategy, Decorator, Visitor and Abstract Factory.

2. **[SOLID Checkout Exercise](02-Coding-Exercises/SOLID-Checkout/README.md)**

   Refactoring payment responsibilities, using mock testing and correcting a monetary rounding error identified through an additional boundary test.

3. **[Testing and AI-Aware Review](03-Testing/README.md)**

   Nine mocked model-review tests examining incomplete transaction evidence, failure handling and the limitations of automated decisions.

4. **[Capstone Project](05-Capstone-Project/README.md)**

   Integrates the four design patterns into a transaction-verification workflow. Seven integration tests examine what the additional record-count check detects and what it still misses.

### 3. Academic and Employability Skills

[**Task 3 – Academic and Employability Skills**](07-Professional-Development/SKILLS_DEVELOPMENT.md)

Reflects on independent study, responding to feedback, critical evaluation, problem-solving, technical communication and the limits of working without independent code review.

### 4. Professional Development Plan

[**Task 4 – Professional Development Plan**](07-Professional-Development/PROFESSIONAL_DEVELOPMENT_PLAN.md)

Identifies current strengths, development gaps and measurable actions towards application security and software assurance. Proposed work on durable transactions, recovery testing and external review is distinguished from completed evidence.

## Finding the Supporting Evidence

The numbered tasks above provide the assessment reading order. The repository folders retain their original project organisation.

Each section links to its supporting Python implementations, unit tests and critical evaluations. The contention investigation also includes recorded benchmark data. The AI-related tests use mocked dependencies rather than a live deployed model.
