# Plan: LED matrix status indicator

## Goal

Use the ATOM Matrix's built-in 5x5 RGB LED grid to show the robot's current state
directly on its body, so you don't need to open the calibration web page
(`http://192.168.42.1`) just to see what mode it's in.

## Why

`M5.begin(true, false, true)` in `Arduino/robo03/src/robo03.ino` already enables the
display (third argument), but nothing in the sketch ever writes to it — the LED
grid is fully unused today. The planned change only needs to display the current
mode, but its effect on timing and getup behavior still needs hardware testing.

## Hardware API (M5Atom library, already a project dependency)

- `M5.dis.fillpix(CRGB color)` — set the whole 5x5 grid to one color.
- `M5.dis.drawpix(index, color)` — set a single LED (index 0–24), for animations
  like a "spinner" during the getup attempt.
- Note: the M5Atom library has had color-order bugs/fixes between versions (RGB
  vs GRB) — pick a color, check it looks right on real hardware, don't assume
  the hex value maps the way you'd expect on a normal display.

## Proposed state → color mapping

`robotMode` already exists as an enum in the sketch (`MODE_MANUAL`, `MODE_GETUP`,
`MODE_GETUP_DONE`, `MODE_GETUP_ABORT`). Map it to color:

| `robotMode` | Color | Notes |
|---|---|---|
| `MODE_MANUAL` | Blue | Idle / manual control mode |
| `MODE_GETUP` | Yellow, or a simple spinning single-pixel animation | Actively attempting to get up |
| `MODE_GETUP_DONE` | Green | Succeeded, upright |
| `MODE_GETUP_ABORT` | Red | Timed out without righting itself (see `GETUP_TIMEOUT_MS`) |

## Implementation steps

1. Add a `updateStatusLed()` function to `robo03.ino` that reads `robotMode` and
   calls `M5.dis.fillpix(...)` with the mapped color.
2. Call it once wherever `robotMode` changes (`startGetupMode()`,
   `stopGetupMode()`) rather than every loop iteration — it's state feedback,
   not something that needs 50Hz updates.
3. Optional stretch: during `MODE_GETUP`, animate a single lit pixel moving
   around the ring via `drawpix()` on a slower timer (e.g. every 100ms) instead
   of a static fill, so it's visually obvious the robot is actively working
   versus stuck.
4. Test on real hardware across all four states: manual idle, mid-getup,
   successful getup, and a forced timeout/abort (e.g. hold it in a position the
   policy can't solve within `GETUP_TIMEOUT_MS`).

## Acceptance criteria

- [ ] LED color matches `robotMode` within one loop iteration of a mode change.
- [ ] No change in getup success rate or timing versus the current build (this
      should be a no-op on the control logic).
- [ ] Colors are visually distinguishable at a glance (verify on real hardware,
      not just in code — GRB/RGB mixups are easy to miss until you see it lit up).

## Out of scope

- Does not affect the RL policy, `export_policy_header.py`, or the training
  pipeline — fully independent of the `pufferlib-migration.md` plan.
