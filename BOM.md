# Parts for my Self-Rising Robot build

My parts list for a build based on [HomeMadeGarbage's SelfRisingRobot](https://github.com/homemadegarbage/SelfRisingRobot). The original project supplies the printable parts and robot design; this list records parts and possible substitutes I considered. Prices in USD are rough snapshots, not current quotes.

---

## 1. M5Stack ATOM Matrix

I used the **MPU6886** IMU version (v1.0). The newer v1.1 has a BMI270; I have not tested this firmware on that version.

| Item | Link | Price |
|------|------|-------|
| M5Stack ATOM Matrix | [M5Stack Official Store](https://m5stack.aliexpress.com/store/1101665954) — search "ATOM Matrix" | ~$12–15 |

**Search terms:** "M5Stack ATOM Matrix ESP32" or "ATOM Matrix MPU6886"  
Buy from the official M5Stack AliExpress store to avoid clones.

**If you use v1.1 (BMI270):** check IMU library support and verify the roll and pitch readings before running the getup policy.

---

## 2. PTK 7465 MG Servo ×2

Micro metal-gear PWM servo. This is the model used in the original project and selected for this build.

| Item | Link | Price |
|------|------|-------|
| PTK 7465 MG | [AliExpress #3256807624827853](https://www.aliexpress.com/item/3256807624827853.html) | ~$5–8 each |

**Buy 3–4** — you want spares. These are small, precise servos and the self-righting motion puts load on the gears.

### Alternatives (if out of stock)

The PTK 7465 MG is ~6–8g, metal gear, digital. Rough equivalents:

| Alternative | Notes |
|-------------|-------|
| EMAX ES9251 II | 4.1g, metal gear, digital — lighter but may have enough torque |
| Feetech FT1117M | 6g, metal gear — cheap, widely available |
| Turnigy TGY-1551A | ~6g, metal gear — HobbyKing brand |
| Blue Bird BMS-303 | 6.4g, metal gear |

**Candidate specs to compare:** weight ≤9g, metal gears, ≥0.8 kg·cm torque at 4.8V, and 0.10–0.15 sec/60°. Check the chosen servo's voltage range and available torque at your actual supply voltage.

---

## 3. 3.7V 220mAh LiPo Battery (1S)

Small drone battery — the kind used in Eachine E010 / E011 mini quads.

| Item | Link | Price |
|------|------|-------|
| E010 220mAh LiPo ×5 pack | [AliExpress search: "E010 220mAh battery"](https://www.aliexpress.com/w/wholesale-e010-220mah-battery.html) | ~$8–12 for 5-pack |

**Get a multi-pack** — you'll want spare batteries, and they're cheap. Often sold as 5-pack with a USB charger.

**Connector type:** JST-PH 2.0 (2-pin). Verify the photos show the correct plug. If your battery comes with a different connector, you'll need to swap it or use an adapter.

---

## 4. JST-PH 2.0 Pigtail Connector

For the direct battery connection used in this build. The [README](README.md#gpio-wiring) explains why this is an experiment rather than a general power recommendation.

| Item | Link | Price |
|------|------|-------|
| JST-PH 2.0 male pigtail | [AliExpress search: "JST PH 2.0 male connector wire"](https://www.aliexpress.com/w/wholesale-jst-ph-2.0-male-connector.html) | ~$1 for 10-pack |

Match the pigtail to the battery connector and verify polarity before connecting it to the board.

---

## 5. 3D Printing Filament

You probably already have this.

| Part | STL File | Notes |
|------|----------|-------|
| Base (foot) | `3Dmodel/footP.stl` | The wide base that sits on the ground |
| Lower arm | `3Dmodel/arm1P.stl` | Connects to servo 1 (lower) |
| Upper arm | `3Dmodel/arm2P.stl` | Connects to servo 2 (upper) |
| Servo horn adapter | `3Dmodel/armhornP.stl` | Adapts between servo horn and arm |

Print in **PLA** or **PETG**. 20% infill is fine. No supports needed for any part.

---

## 6. Miscellaneous (local purchase or AliExpress)

| Item | Notes |
|------|-------|
| M2/M2.5 screws + nuts | For mounting servos to 3D-printed parts. Small assortment kit |
| Soldering iron + solder | To attach servo wires and battery pigtail to ATOM Matrix |
| USB-C cable | For programming the ATOM Matrix |
| Heat shrink tubing | Insulate solder joints |
| Double-sided tape or velcro | Mount battery to robot base |

---

## Total Estimated Cost

| Item | Cost |
|------|------|
| ATOM Matrix | $12 |
| PTK 7465 MG ×3 (incl spare) | $18 |
| LiPo battery 5-pack | $10 |
| JST-PH pigtails | $1 |
| Filament (~50g) | $2 |
| Misc (screws, tape) | $5 |
| **Total** | **~$48** |

The pure BOM (no spares, consumables) is ~$25–35.

---

## Quick Reference: Search Terms

Copy-paste these into AliExpress search:

- `M5Stack ATOM Matrix` — microcontroller
- `PTK7465MG` — servo
- `E010 220mAh battery` — LiPo
- `JST PH 2.0 male connector cable` — battery pigtail
- `micro servo metal gear 6g` — servo alternatives
