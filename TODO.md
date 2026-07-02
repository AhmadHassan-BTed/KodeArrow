# Refactor TODO — Proper Architecture (Clean/Hexagonal)

## Phase 0 — Baseline understanding
- [x] Scan existing services and GUI adapters used by `StandardApp` / `REditionApp`.
- [x] Identify current ports we need (keyboard, tray, dialogs, premium validation, telemetry upload).

## Phase 1 — Create Architecture Skeleton
- [x] Create `kode_arrow/domain/ports/` with interfaces for: keyboard, keypress, tray, dialogs, premium, telemetry.
- [x] Create `kode_arrow/application/use_cases/`:
  - [x] navigation action use-case
  - [x] unlock premium use-case
  - [x] telemetry collector use-case
  - [x] telemetry upload use-case
- [x] Create adapter layer scaffolding under `kode_arrow/infrastructure/`:
  - [x] keyboard adapter (wrap `keyboard`)
  - [x] tray adapter (wrap `pystray`)
  - [x] dialog adapter (wrap `tkinter` + existing `UIWindowManager`)

## Phase 2 — Refactor StandardApp
- [x] Replace inline hotkey wiring with use-case handler wiring.
- [x] Replace inline tray menu callbacks with tray adapter callbacks.
- [x] Replace inline unlock logic with `unlock_premium` use-case.
- [x] Ensure `StandardApp` becomes a thin composition root.

## Phase 3 — Refactor REditionApp
- [x] Move telemetry counters + batching into telemetry use-cases.
- [x] Hook keyboard press tracking via keyboard adapter to collector use-case.
- [x] Replace tray research info + unlock logic using adapters/use-cases.
- [x] Ensure `REditionApp` becomes a thin composition root.

## Phase 4 — Deduplication & Cleanup
- [x] Remove duplicated unlock dialog code.
- [x] Reduce edition-specific logic to configuration/edition config.
- [ ] Add new controllers/composition builders so app files stop containing wiring/lambdas.

## Phase 5 — Verification
- [ ] Import checks for both editions.
- [ ] Manual smoke tests: tray, hotkeys, unlock flow, telemetry batching.

## Phase 6 — Release (To Be Done by User)
- [ ] Run & manually verify selection / word actions (`Ctrl+Alt`, `Alt+Ctrl` and both Alts + Ctrl).
- [ ] Build the application to executable (`python infrastructure/build/build.py`).
- [ ] Deploy the new build executable to the release channel.


## v2.5.1 Completed
- [x] Fix Firestore timeout killing the app
- [x] Add missing handle_selection_combination method
- [x] Fix WNDCLASSW Python 3.13 compatibility
- [x] Silence non-critical telemetry warnings