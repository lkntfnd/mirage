<!-- mirage:doc platform:{{kind}} -->
# Platform: {{Platform name}}

{{One paragraph: this file is written once per component kind the project ships, such as a mobile app, a desktop app, a browser extension or an embedded target. A kind that ships on several operating systems, such as iOS and Android, covers each one under its own sub-heading in every section. Name which component this instance documents and what this document fixes. Say an unsettled target version, store account or permission becomes a question in docs/questions.md rather than an invented one.}}

<!-- mirage:section targets -->
## Supported platforms and versions

{{Name the exact platform and the minimum and target operating system versions the first release supports, and why that floor was chosen, such as device share or a required system API. Cite the requirement as REQ-<AREA>-NNN.}}

<!-- mirage:section distribution -->
## Distribution and review

{{Name the store or channel that distributes this platform's build, such as an app store or a direct download, and whose account publishes it. Describe the review process and its typical turnaround, marking any duration as a hypothesis until the first submission confirms it.}}

<!-- mirage:section permissions -->
## Permissions

{{List every device permission the app requests, such as camera, location or notifications, the requirement that needs it as REQ-<AREA>-NNN, and the moment the app asks for it. State what the app does when a user declines.}}

<!-- mirage:section updates -->
## Updates

{{State how an update reaches an installed copy, whether the channel pushes it automatically or the user must act, and whether the app can force a user on an old version to update. Name the mechanism, such as a minimum-version check against the API.}}

<!-- mirage:section signing -->
## Signing and credentials

{{Name who holds the signing keys or certificates for this platform, where they are stored, and who can rotate them. Cite the input that supplies access to those credentials as (IN-nnn).}}

<!-- mirage:section crashes -->
## Crash reporting

{{Name the crash reporting tool this platform sends reports to, what triggers a triage, and who is notified. State which symbol or debug information must ship with each build so a crash report can be decoded.}}
