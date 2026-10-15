# Case Study on Transaction Evidence and Reconciliation

The original banking tests established balance protection under the tested conditions, but the recording extension exposed a different failure. A forced `_append()` error left a completed £25 deposit unrecorded while reporting an exception to the caller. Retrying could duplicate the deposit, although no retry was performed.

Subsequent checks revealed further weaknesses. Reconciliation missed two unrecorded transactions whose effects cancelled. The capstone's record-count check detected those omissions, but accepted substituted amounts that preserved both the count and net movement. Each check improved detection without establishing whether individual transactions were accurately represented.

I would prioritise coordinated, durable recording and independent transaction-level verification before extending the review process. Their implementation and recovery behaviour remain untested. The [capstone evaluation](../05-Capstone-Project/CAPSTONE_EVALUATION.md) examines these limitations further.
