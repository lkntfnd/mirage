<!-- mirage:doc summary -->
# Executive summary

The one-page view of Hollow Lane Cycles, brought up to date on 2026-10-01.

<!-- mirage:section product -->
## What is being built

A phone app where customers book a repair slot at the shop, and a small API that also tells mechanics which parts are in stock. The detail is in the [PRD](prd.md).

<!-- mirage:section scope -->
## Scope and releases

v1.0 lets a customer book and cancel a slot. v1.1 adds a reminder the day before. The app takes no payments.

<!-- mirage:section decisions -->
## Decisions still open

Q-012 (which reminders to send) blocks the reminder story; the recommendation is one push reminder. Two delegated answers await the owner, and one input is missing.

<!-- mirage:section delivery -->
## Delivery status

Milestone M1 is under way: booking is done, cancelling is ready and part stock is in progress.

<!-- mirage:section next -->
## Next steps

1. The shop owner answers Q-012.
2. The shop owner provides the app store accounts (IN-002).
3. The mobile lane builds the cancel flow.
