<!-- mirage:doc performance -->
# Performance

<!-- mirage:section budgets -->
## Budgets

The app starts in under two seconds; the API answers in under 300 ms at p95 (Q-008).

<!-- mirage:section measurement -->
## Measurement

Start time is measured on a mid-range phone; latency in the API's metrics.

<!-- mirage:section techniques -->
## Techniques

The slot list is cached for one minute on the device.

<!-- mirage:section monitoring -->
## Monitoring

An alert fires when p95 latency passes 300 ms for ten minutes.
