# Digital Campus Library Reservation Gateway

Software Engineering Lab 1 - Requirements Engineering & UML Use-Case Modelling  
Problem Statement #08: Campus & Academic Operations

## Deliverables

- [`requirements_table.csv`](requirements_table.csv) - exactly 5 functional requirements and 2 non-functional requirements with measurable acceptance criteria and rationale.
- [`library_usecase_diagram_handdrawn.png`](library_usecase_diagram_handdrawn.png) - supplied hand-drawn UML use-case model with the Student Member, Head Librarian, and Notification Service actors; six use cases; one `<<include>>` and one `<<extend>>` relationship.
- [`use_case_diagram.svg`](use_case_diagram.svg) - editable vector source for the diagram; no rasterized or altered external artwork is used.
- [`use_case_flow.pdf`](use_case_flow.pdf) - one-page flow for UC-02 Place Hold on Loaned Book.
- [`Lab1_Submission_Report.pdf`](Lab1_Submission_Report.pdf) - consolidated report containing the requirements table, supplied UML diagram, and complete use-case flow.
- [`use_case_flow.md`](use_case_flow.md) - editable source for the flow document.

## Scope and Traceability

The model covers catalog search, FIFO holds for loaned books, availability notifications, librarian circulation operations, and overdue fine records. Requirements use the mandated `The system shall...` form and each acceptance criterion is written as an observable pass/fail check.

## UML Model

Actors: Student Member, Head Librarian, Notification Service.  
Primary use cases: Search ISBN Catalog, Place Hold, Validate Member Eligibility, Process Book Return, Send Availability Notification, Manage Circulation & Fines.  
Relationships: `Place Hold <<include>> Validate Member Eligibility`; `Send Availability Notification <<extend>> Process Book Return`.

## Source and Verification

The consolidated PDF report is generated from the editable Markdown/CSV sources and the supplied PNG. The hand-drawn diagram is preserved unchanged as the repository's authoritative diagram asset; no image editing or redraw was applied.
