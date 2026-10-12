"""Compare concurrent transactions on shared and separate bank accounts."""

import csv
import threading
from decimal import Decimal
from statistics import median
from time import perf_counter

from bank_account import BankAccount

THREAD_COUNTS = (1, 2, 4, 8, 16, 32)
TOTAL_PAIRS = 600000
REPEATS = 5
STARTING_BALANCE = Decimal("100")
AMOUNT = Decimal("1")


def run_trial(thread_count, scenario):
    """Time a fixed workload and check the resulting account balances."""
    pairs_per_user = TOTAL_PAIRS // thread_count

    if scenario == "shared":
        accounts = [BankAccount("SHARED", STARTING_BALANCE)]
    else:
        accounts = [
            BankAccount(f"USER_{index}", STARTING_BALANCE)
            for index in range(thread_count)
        ]

    # Start workers together without including thread creation in the timing.
    starting_line = threading.Barrier(thread_count + 1)
    errors = [None] * thread_count

    def user_session(index):
        account = accounts[0] if scenario == "shared" else accounts[index]

        try:
            starting_line.wait()

            for _ in range(pairs_per_user):
                account.deposit(AMOUNT)

                if not account.withdraw(AMOUNT):
                    raise AssertionError("A funded withdrawal was rejected.")

        except Exception as exc:
            # Keep worker failures visible to the main testing thread.
            errors[index] = exc

    threads = [
        threading.Thread(target=user_session, args=(index,))
        for index in range(thread_count)
    ]

    for thread in threads:
        thread.start()

    start = perf_counter()
    starting_line.wait()

    for thread in threads:
        thread.join()

    elapsed = perf_counter() - start

    for error in errors:
        if error is not None:
            raise RuntimeError("A worker did not complete its transactions.") from error

    # Every deposit has a matching withdrawal.
    for account in accounts:
        if account.get_balance() != STARTING_BALANCE:
            raise AssertionError("An account ended with an unexpected balance.")

    return elapsed


def main():
    """Repeat each workload and save the measurements for evaluation."""
    if any(TOTAL_PAIRS % count for count in THREAD_COUNTS):
        raise ValueError("TOTAL_PAIRS must divide evenly across thread counts.")

    results = []
    total_operations = TOTAL_PAIRS * 2

    print("BankAccount contention experiment")
    print(f"Operations per trial  {total_operations:,}")
    print(f"Repetitions per setting  {REPEATS}")
    print()

    for thread_count in THREAD_COUNTS:
        for scenario in ("shared", "separate"):
            times = []

            for trial in range(1, REPEATS + 1):
                seconds = run_trial(thread_count, scenario)
                times.append(seconds)

                results.append(
                    {
                        "scenario": scenario,
                        "threads": thread_count,
                        "trial": trial,
                        "operations": total_operations,
                        "seconds": round(seconds, 6),
                        "operations_per_second": round(total_operations / seconds, 1),
                    }
                )

            middle_time = median(times)
            throughput = total_operations / middle_time

            print(
                f"{thread_count:>2} threads  {scenario:<8}  "
                f"median {middle_time:.4f} s  "
                f"{throughput:,.0f} ops/s"
            )

    with open(
        "contention_results_extended.csv", "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print("\nMeasurements saved to contention_results.csv")


if __name__ == "__main__":
    main()
