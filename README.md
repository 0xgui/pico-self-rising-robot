# pico — self-righting robot

Pico is my build of a small, two-servo robot that tries to stand itself back up after being knocked over. An M5Stack ATOM Matrix senses its orientation and runs a neural-network policy that moves the two arms. Once flashed, the control loop runs on the robot; the MuJoCo simulation is used to train and inspect the policy.

This build starts from [HomeMadeGarbage's SelfRisingRobot](https://github.com/homemadegarbage/SelfRisingRobot). I have adapted the firmware to my wiring and servo directions and set up a PlatformIO workflow. The included 3D models, simulation, and pretrained policy come from that original project.

## How it works

1. The ATOM Matrix reads its IMU and estimates roll and pitch. If the robot stays tilted for about 300 ms, the firmware starts a getup attempt.
2. Every 20 ms during the attempt, the policy receives roll, pitch, and the two current servo targets. It outputs small changes to those targets, which the firmware converts to servo commands.
3. The attempt ends when the robot has stayed near upright for about 700 ms, or after a 14-second timeout. A local Wi-Fi page lets me adjust the servos and start or stop an attempt manually.

The pretrained policy was developed in MuJoCo with Stable-Baselines3 PPO and exported to a C header for the ESP32. The servo targets are part of the observation because these PWM servos do not report their actual joint angles. See [RL/README.md](RL/README.md) for the simulation files and training commands.

## This build

- GPIO 32 drives the lower servo and GPIO 26 drives the upper servo. Their directions are mapped to this assembly in the firmware.
- The firmware adjusts IMU roll initialization for the board's orientation, limits servo commands to 15–165 degrees, and reads an upper-joint home trim from device Preferences.
- [Arduino/README.md](Arduino/README.md) covers flashing and calibration. [improvements/](improvements/README.md) contains experiments I want to try next.

The code is configured for this hardware, but I have not documented a repeatable hardware getup success rate or results from my own training run yet.

## Parts used in this build

| Part | Spec | Qty | Approx Cost |
|------|------|-----|-------------|
| Microcontroller | M5Stack ATOM Matrix (ESP32 + MPU6886 IMU) | 1 | $10–15 |
| Servo | PTK 7465 MG (metal gear micro servo) | 2 | $5–8 each |
| Battery | 3.7V 220mAh LiPo (1S, E010 drone type) | 1 | $3–5 |
| Battery connector | JST-PH 2.0 pigtail | 1 | $0.50 |
| 3D Prints | foot, arm1, arm2, armhorn (PLA/PETG) | 1 set | ~$2 filament |

**Estimated base cost: ~$25–35**, excluding spares and tools. Prices are approximate.

See [`BOM.md`](BOM.md) for AliExpress links and ordering details.

## Try the simulation

```bash
cd RL

# Create venv
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Play the original pretrained policy in MuJoCo viewer
python play_robo1_policy.py

# Evaluate on all 4 fallen poses
python eval_robo1_policy.py
cd ..
```

Training and policy export commands are in [RL/README.md](RL/README.md). The firmware uses the original pretrained policy header until it is replaced with a new export.

## Flash the firmware

**Option A — PlatformIO (recommended, no Arduino IDE needed):**

```bash
cd Arduino/robo03
pio run              # builds, auto-installs libraries from platformio.ini
pio run -t upload    # flashes over USB
pio device monitor   # serial monitor, 115200 baud
```

**Option B — Arduino IDE:**

1. Install Arduino IDE + ESP32 board support
2. Install libraries: `M5Atom`, `Kalman Filter Library`, `ESP32Servo`, `FastLED`
3. Copy `robo03.ino` and `policy_network.h` from `Arduino/robo03/src/` into an Arduino sketch folder named `robo03`
4. Open that folder's `robo03.ino`
5. Select board: **M5Stack-ATOM**, upload

**Either way:**

6. Power on: the firmware creates Wi-Fi AP `robo1` (password: `password`)
7. Join that AP and open `http://192.168.42.1` to calibrate servos

## GPIO Wiring

| Signal | ATOM Matrix Pin | Servo Wire |
|--------|----------------|------------|
| Servo 1 (lower) | GPIO 32 | Signal (yellow/white) |
| Servo 2 (upper) | GPIO 26 | Signal (yellow/white) |
| Power (both servos) | 5V / GND | Red (+) / Brown (-) |
| Battery in this build | 5V / GND | 1S LiPo via JST-PH pigtail |

The direct 1S LiPo connection is part of this build, not a validated power recommendation. [M5Stack specifies a 5V input](https://docs.m5stack.com/en/core/Atom-Matrix_v1.1); a 1S cell is below that voltage for most of its discharge. Check the board and servo supply under load before relying on this arrangement.

## Project Structure

```
pico-self-rising-robot/
├── README.md           # This file
├── BOM.md              # Parts and alternatives for this build
├── 3Dmodel/            # Printable robot parts
├── Arduino/            # Firmware, PlatformIO project, and policy header
├── RL/                 # MuJoCo simulation, training code, and PPO model
└── improvements/       # Proposed experiments
```
