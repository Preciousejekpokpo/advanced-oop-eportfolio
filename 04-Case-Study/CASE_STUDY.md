# Case Study on Transaction Evidence and Reconciliation

The original banking tests established balance protection under the tested conditions, but the recording extension exposed a different failure. A forced `_append()` error left a completed £25 deposit unrecorded while reporting an exception to the caller. Retrying could duplicate the deposit, although no retry was performed.

Subsequent checks revealed further weaknesses. Reconciliation missed two unrecorded movements that cancelled, while the capstone's count check accepted substituted amounts. Both could report agreement without establishing whether individual transactions were accurately recorded, since the evidence itself remained unreliable.

I would prioritise atomic, durable balance-and-record updates and failure-recovery testing before introducing further review layers. These remain proposals rather than implemented safeguards. The [capstone evaluation](../05-Capstone-Project/CAPSTONE_EVALUATION.md) examines the checks in detail.
