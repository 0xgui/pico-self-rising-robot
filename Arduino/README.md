# Firmware for my build

This firmware is adapted from [HomeMadeGarbage's SelfRisingRobot](https://github.com/homemadegarbage/SelfRisingRobot). Their Arduino sketch and exported policy are the starting point. I added PlatformIO setup and changed the servo mapping, joint directions, IMU roll initialization, command limits, and home trim for my assembly. The policy header still contains the original pretrained policy.

## Files

- `robo03/src/robo03.ino` - control sketch for the M5Atom
- `robo03/src/policy_network.h` - trained policy exported as a C header
- `robo03/platformio.ini` - PlatformIO project configuration

`policy_network.h` is included by `robo03.ino`, so it must stay in the same `src` folder.

## Required Libraries

When using PlatformIO, these are already listed in `lib_deps` in `platformio.ini` and are
fetched automatically when you run `pio run`.

- M5Atom
- Kalman Filter Library (TKJElectronics)
- ESP32Servo
- FastLED (internal dependency of M5Atom)

If using the Arduino IDE, install the same libraries manually via the Library Manager.

## Upload

**PlatformIO (recommended):**

```bash
cd Arduino/robo03
pio run              # build
pio run -t upload    # flash
pio device monitor   # serial monitor (115200 baud)
```

**Arduino IDE:**

Copy `robo03/src/robo03.ino` and `robo03/src/policy_network.h` into an Arduino sketch
folder named `robo03`. Open that folder's `robo03.ino`, build for M5Atom, and upload.

## Wi-Fi Control

On boot, the M5Atom creates a Wi-Fi access point.

- SSID: `robo1`
- Password: `password`
- URL: `http://192.168.42.1`

From a browser, you can manually adjust the servos, start/stop the getup motion, and turn
auto-getup on/off.

## Button

The M5Atom's built-in button can also start the getup motion.

Pressing the button during a getup attempt stops it and returns to manual mode.

## Notes

- This assembled robot uses GPIO 32 for the lower servo and GPIO 26 for the upper servo.
- The lower servo turns opposite to the upper servo. `lowerServoCommandDeg()` and
  `upperServoCommandDeg()` encode the two directions.
- The IMU roll initialization uses `atan2(accX, accZ)`. The original sketch's formula produced a
  180-degree offset on this ATOM orientation.
- Servo commands stay between 15 and 165 degrees to avoid the physical end stops.
- PC USB-C power caused brownouts when both servos moved in this build. The direct 1S LiPo
  connection used here is below the board's specified 5V input; see the [power note](../README.md#gpio-wiring).
- The upper-joint home trim is stored as `upperhome` in the ATOM Preferences. It is not part
  of the Git commit.
- Servo offset and pulse width can be adjusted from the web page and are saved to Preferences.
- `policy_network.h` is the original project's pre-generated policy network. Replace it only
  when you have exported and checked a different trained model.
