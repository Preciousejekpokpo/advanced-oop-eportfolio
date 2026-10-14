# Testing and AI-Aware Review

This folder follows a problem that emerged as I extended the original banking system. `RecordingAccount` updates an account balance before saving its transaction record. If recording fails, money can move without a corresponding history entry. The earlier tests examined whether transactions produced the expected balances, but those results could not establish whether every completed operation had been recorded.

I investigated this weakness through `ModelReviewService`, using `unittest.mock` to isolate the model dependency. Nine tests examined invalid responses, dependency failures, the conditions under which model advice is requested, and whether review alters account state. The full banking suite subsequently passed 65 tests locally, although these results cannot establish the reliability of a live AI model.

The most revealing test involved a £25 deposit and £25 withdrawal whose records both failed. The balance returned to £100, leaving an empty history that still satisfied reconciliation. The service therefore returned the mock's `no_flag` suggestion as advisory output. The test passed, but its result showed how two missing transactions could become indistinguishable from no activity.

This finding shifts my priority towards dependable transaction recording and independent verification before introducing a real model.

## Evidence

- [Critical testing evaluation](MOCKING_AND_AI_TESTING.md)
- [Model review implementation](../02-Coding-Exercises/BankAccount/model_review.py)
- [Nine unit tests](../02-Coding-Exercises/BankAccount/test_model_review.py)
