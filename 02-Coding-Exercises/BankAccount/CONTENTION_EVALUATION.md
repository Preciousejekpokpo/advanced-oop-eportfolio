# Examining Lock Contention and Performance

![Figure 2. Shared and separate account execution times across sixty benchmark trials](contention_graph.png)

Figure 2 examines the assumption that separate account locks would reduce contention and improve performance when transactions operate on unrelated accounts. The benchmark compared 1.2 million operations per trial across shared and separate accounts, using one to thirty-two threads and five repetitions per configuration. However, fluctuating median times and overlapping trial ranges reveal no consistent advantage for either arrangement. Although separate locks reduce competition for account-level resources, this was not reflected in sustained performance gains.

All trials preserved the expected balances, supporting the correctness of concurrent updates under these conditions. However, this offers limited evidence of scalability, as increasing thread counts produced no consistent throughput improvement. Kalibera and Jones (2013) emphasise measurement variability, particularly relevant given the five repetitions and sub-second execution times. The fixed workload also limits conclusions about growing transaction volumes. The GIL-enabled CPython interpreter may have constrained parallel execution, although its influence cannot be isolated. Using Python 3.15.0a6, an alpha release, further limits generalisability.

The findings support retaining per-account locking for balance protection without assuming a performance advantage. Repeating the experiment on stable Python, with more trials, comparison against free-threaded execution and closer examination of timing variation, would provide stronger evidence of its suitability under heavier workloads.

## Evidence

- [Benchmark implementation](benchmark_contention.py)
- [Extended dataset with 60 trials](contention_results_extended.csv)
- [Earlier dataset](contention_results.csv)

## References

Kalibera, T. and Jones, R.E. (2013) ‘Rigorous benchmarking in reasonable time’, *Proceedings of the ACM SIGPLAN International Symposium on Memory Management*. Available at https://doi.org/10.1145/2464157.2464160 (Accessed 14 October 2026).
