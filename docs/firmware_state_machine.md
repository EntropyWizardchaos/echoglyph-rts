# Firmware State Machine (On‑Tag)

```
BOOT -> SELFTEST -> IDLE
IDLE -> LOGGING [if suction_ok and timer]
LOGGING:
  audio_on()
  imu_on()
  while mission_active:
      packetize_clicks()
      compute_features()
      low_power_save()
      duty_cycle()
      if release_time or remote_release or suction_lost: break
LOGGING -> RELEASE -> FLOAT
FLOAT:
  stop_audio(); stop_imu()
  beacon_on(); strobe_on()
  sleep_between_beacons()
```
- **Duty cycling:** audio continuous or bursty per profile; IMU 100–200 Hz; pressure 1–5 Hz.
- **Harvest manager:** route piezo → rectifier → supercap → system rail (through PMIC) to shave peak loads.
- **Timestamps:** TCXO + periodic sync markers.
