# Brief: tallyho

tallyho is an invented open-source command-line tool. The maintainer writes:

tallyho reads CSV exports from several banks, normalises them into one format, and reconciles them against a ledger file so freelancers can see which invoices were paid. It runs on macOS, Linux and Windows. Output should be readable in a terminal and also available as JSON for scripts.

Each bank exports a different CSV layout, so tallyho needs a way to describe a layout without code changes. Matching payments to invoices uses the amount, the date within a few days, and a reference string when one exists. Users must be able to see why a payment matched or did not.

The tool is distributed through Homebrew and as a standalone binary. There is no server and no account. Contributors are volunteers.
