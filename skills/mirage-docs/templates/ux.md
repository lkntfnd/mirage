<!-- mirage:doc ux -->
# User experience

{{One paragraph: which components have a user-facing surface, whether designs already exist, and that every screen in the inventory below gets its own spec under docs/specs/.}}

<!-- mirage:section basis -->
## Design basis

{{State whether wireframes, a design file or a live product already fixes the layout, and name the input (IN-nnn) that holds it when one exists. When nothing exists yet, state that this document and the screen specs are the design basis until a designer's file replaces them.}}

<!-- mirage:section inventory -->
## Screen inventory

{{List one row per screen or page in this release. Loading, Empty, Error and Offline mark whether that state needs its own design, yes or no. Link marks whether the screen opens from a deep link or a notification, yes or no. Spec is a Markdown link to the screen's file, relative to this document, so the validator reports a spec that is missing. Release names the release that ships it.}}

| ID | Screen | Entry points | Loading | Empty | Error | Offline | Link | Spec | Release |
|---|---|---|---|---|---|---|---|---|---|
| {{SCR-001}} | {{Screen name}} | {{How a user reaches it}} | {{yes/no}} | {{yes/no}} | {{yes/no}} | {{yes/no}} | {{yes/no}} | {{[Name](specs/<component id>/<Name>.md)}} | {{v1.0}} |

<!-- mirage:section flows -->
## Flows

{{Write one subsection per flow that matters most, named after the goal it completes. Number its steps, name the screen each step uses from the inventory above, note where the flow can fail or branch, and cite the requirement REQ-<AREA>-<NNN> each flow satisfies.}}

<!-- mirage:section navigation -->
## Navigation map

{{Describe the top-level navigation, such as a tab bar, a sidebar or a header menu, and what each entry leads to. State which screens sit outside the main navigation and how a user reaches them instead.}}

<!-- mirage:section links -->
## Links and deep links

{{List every screen that opens from an external link, a push notification or another app, the URL or scheme pattern for each, and what happens when the link points at content the user cannot access or that no longer exists.}}

<!-- mirage:section accessibility -->
## Accessibility

{{Name the accessibility standard this project targets, such as WCAG 2.2 AA, citing the question that settled it if the owner had to choose one. List the checks every screen spec's acceptance criteria must include, such as keyboard navigation, screen reader labels, color contrast and visible focus.}}

<!-- mirage:section responsive -->
## Responsive and platform rules

{{List the screen sizes, orientations and input methods that must work, and the breakpoints or size classes that separate layouts. Name any platform-specific rule, such as safe areas on notched devices or a minimum window size on desktop.}}
