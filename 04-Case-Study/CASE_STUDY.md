# Case Study: The Limits of Transaction Evidence

The banking system used per-account locks and ordered lock acquisition to protect balances during concurrent transactions. When I added transaction recording, however, I found that this protection did not extend to the evidence used to explain those balances. `RecordingAccount` appends a record only after updating the account, meaning that a failed append can leave completed activity absent from its history. This separation preserved the original class but left reporting and model review dependent on potentially incomplete records.

I investigated the weakness through the capstone workflow, comparing recorded attempts with the number scheduled alongside balance reconciliation. The additional check detected an unrecorded £25 deposit and withdrawal despite their effects cancelling, so the workflow withheld model advice.

That improvement depends on knowing the expected workload and cannot establish whether individual records are accurate. When both £25 transactions were recorded as £10, counts and net movement still agreed, allowing advisory output to proceed. An authoritative event record and failure recovery could offer stronger assurance, although their storage, synchronisation and performance costs remain untested.
