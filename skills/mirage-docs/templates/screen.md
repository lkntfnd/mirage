<!-- mirage:doc screen -->
# Screen or page spec: {{Screen name}}

{{One paragraph naming the screen's purpose, the component it belongs to, and the row in docs/ux.md's screen inventory this file fills in.}}

<!-- mirage:section purpose -->
## Purpose

{{State the one job this screen does for the user, and cite every requirement it satisfies as REQ-<AREA>-<NNN>. A screen with no requirement link has no reason to exist, so raise a question instead of inventing one.}}

<!-- mirage:section entry -->
## Entry points

{{List every way a user reaches this screen: navigation, a button on another screen, a deep link from docs/ux.md's links section, or a notification. Name the screen or event that precedes each entry.}}

<!-- mirage:section layout -->
## Layout and content

{{Describe the regions of the screen in reading order and the content each region shows. Point to the design file or wireframe named in docs/ux.md's design basis when one exists, instead of re-describing pixel positions here.}}

<!-- mirage:section states -->
## States

{{Cover every state the screen inventory marked yes for: loading, empty, error and offline, plus the normal populated state. State what the user sees and can do in each one, and how the screen recovers, such as a retry action on error.}}

<!-- mirage:section interactions -->
## Interactions

{{List every control on the screen, what happens when a user activates it, which state or screen it leads to, and the validation rules and error messages that apply.}}

<!-- mirage:section data -->
## Data

{{List the endpoints this screen calls, from docs/api.md's endpoint inventory, or the data source it reads when the project has no API, from docs/data-model.md. Name what each call returns and when it runs, such as on load or on a user action.}}

<!-- mirage:section events -->
## Analytics events

{{List the analytics events this screen fires, from docs/events.md's event catalog, and the user action or state change that triggers each one. State that analytics is out of scope here when the project has no analytics flag.}}

<!-- mirage:section strings -->
## Text and translations

{{List the strings this screen shows that are not obvious from the layout, such as button labels, error messages and empty-state copy. Name which locales from docs/i18n.md they must ship in, or state that the project ships one language only.}}

<!-- mirage:section accessibility -->
## Accessibility

{{State how this screen meets the accessibility standard named in docs/ux.md: reading order, labels for interactive elements, focus order and contrast for any custom color used only here.}}

<!-- mirage:section acceptance -->
## Acceptance criteria

- [ ] {{Every requirement cited in Purpose is testably satisfied.}}
- [ ] {{Every state listed above renders as described.}}
- [ ] {{Every analytics event listed above fires with the properties docs/events.md defines.}}
- [ ] {{The screen meets the accessibility criteria above.}}
