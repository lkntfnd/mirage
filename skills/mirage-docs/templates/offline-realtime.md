<!-- mirage:doc offline-realtime -->
# Offline and realtime

{{One paragraph: which parts of the product must keep working without a connection and which must update live.
Name what realtime means for this product, such as a live dashboard or a chat feed.
State that docs/questions.md holds every open decision about caching limits, conflict resolution or transport choice.}}

<!-- mirage:section connectivity -->
## Connectivity states

{{Name every connectivity state the product distinguishes, such as online, offline and reconnecting.
Cite the requirement (REQ-<AREA>-<NNN>) that sets what must keep working in each state.
State what the interface shows the user in each state, such as a banner or a disabled control.}}

<!-- mirage:section caching -->
## Caching

{{State what is cached on the device, and how long each cache entry stays valid.
State what happens when the device runs out of storage, such as evicting the oldest entry first.
Treat any cache size or expiry number as a hypothesis until a release has measured it.}}

<!-- mirage:section sync -->
## Synchronization and conflicts

{{State how a change made offline queues and later reaches the server once the connection returns.
State what happens when the same record changed on two devices while both were apart, and name the resolution rule, such as last write wins or a manual merge.
Cite the question (Q-nnn) if the resolution rule is not yet decided.}}

<!-- mirage:section realtime -->
## Realtime updates

{{Name what must update live without a page refresh, and cite the requirement that sets each live surface.
Name the transport that delivers it, such as WebSockets, server-sent events or polling.
State what the interface does when that transport is unavailable, such as falling back to polling or showing stale data with a notice.}}
