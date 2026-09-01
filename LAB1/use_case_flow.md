# Use-Case Flow: Place Hold on Loaned Book

**Use-case ID:** UC-02  
**Primary actor:** Student Member  
**Supporting actor:** Head Librarian (via inventory status), Notification Service  
**Goal:** Join the FIFO queue for a book that is currently loaned.

## Preconditions

- The student member is authenticated and has an active library account.
- The requested ISBN exists in the catalog and all copies are currently loaned.
- The student has not reached the configured active-hold limit and has no duplicate active hold for the ISBN.

## Postconditions

- A hold record is stored with the student, ISBN, queue position, creation time, and status `WAITING`.
- The member sees the assigned queue position and the request appears in the librarian queue view.
- No copy is checked out or removed from another member's loan.

## Main Success Scenario

1. Student searches the catalog by title, author, or ISBN.
2. System validates the query and displays the matching title with `Loaned` availability.
3. Student selects the title and chooses **Place hold**.
4. System verifies authentication, account standing, active-hold limit, and duplicate-hold rules.
5. System locks the title queue, calculates the next FIFO position, and creates the hold record.
6. System releases the queue lock and schedules a future availability notification.
7. System displays confirmation with the queue position and estimated notification conditions.
8. Use case ends successfully.

## Alternate Flow: Member Not Eligible (4a)

4a1. If the member has reached the active-hold limit, has an existing active hold, or has a blocked account, the system does not create a hold.  
4a2. The system displays the specific reason and the action needed (for example, return an overdue item or cancel an existing hold).  
4a3. The student may return to search; the use case ends without changing the queue.

## Related Relationships

- `Place Hold` **includes** `Validate Member Eligibility` because every hold requires the same checks.
- `Send Availability Notification` **extends** `Process Book Return` when a waiting queue exists and a copy becomes available.
