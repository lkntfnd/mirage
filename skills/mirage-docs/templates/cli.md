<!-- mirage:doc cli -->
# Command-line interface

{{One paragraph: what this tool is for, who runs it, and what this document fixes. Say an unsettled command name, flag or exit code becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section commands -->
## Commands

{{List every command and subcommand the first release ships, one sentence each naming what it does and which requirement it satisfies as REQ-<AREA>-NNN. Group subcommands under their parent command in the order a user would discover them.}}

<!-- mirage:section options -->
## Options

{{List the flags and arguments each command accepts, which are required, which repeat, and their default values. State the precedence when the same setting comes from a flag, a config file and an environment variable.}}

<!-- mirage:section exit-codes -->
## Exit codes

{{List every exit code the tool returns and the condition that produces it, since scripts branch on these values. Reserve 0 for success and give every distinct failure its own code rather than a generic nonzero.}}

<!-- mirage:section output -->
## Output formats

{{State which output formats exist, such as a human-readable format for a terminal and a machine-readable format such as JSON for scripts, and which flag selects each. State what goes to standard output and what goes to standard error.}}

<!-- mirage:section configuration -->
## Configuration and environment

{{List the configuration file locations, the environment variables the tool reads, and the order in which flags, files and environment variables override each other. Name any variable that must never be logged or printed.}}

<!-- mirage:section distribution -->
## Distribution

{{State how the tool is installed, such as a package registry, Homebrew or a signed binary, and which operating systems and architectures the first release supports. Name who publishes a new version and what triggers a release.}}
