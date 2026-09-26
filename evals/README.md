# Evaluations

Three invented projects test mirage end to end:

- `corporate-website`, a bilingual architecture-practice website that replaces an old site
- `booking-app`, a fitness class booking app with a mobile client, a backend and an admin panel
- `csv-cli`, an open-source command-line tool

## Run one

1. Create an empty git repository outside this one, and copy the brief into it as `docs/sources/brief.md`.
2. Start an agent session in that repository with mirage and Matt Pocock's skills installed. Run `/mirage`, and give the agent the brief as the owner's first message.
3. When the interview begins, answer "use your recommendations for everything the brief does not answer". That delegates every open decision.
4. Let the agent run every phase through `mirage-audit`.
5. Grade the run from this repository's root with `python3 evals/check_eval.py <eval name> <path to the project>`.

## What passes

A run passes when four things hold:

- `check.py check` is clean.
- Every planned document exists, and every question area is covered.
- The facets in `.mirage/project.json` match `expected.json`.
- Every date and money amount in the documents and the backlog also appears in the brief or the registers.

A second pass changes two answers in `docs/questions.md` and asks the agent to update the project. Only the documents and items that cite those questions should change.
