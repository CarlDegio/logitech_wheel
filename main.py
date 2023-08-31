import time

import evdev
from evdev import ecodes, InputDevice, ff

# Find first EV_FF capable event device (that we have permissions to use).
for name in evdev.list_devices():
    dev = InputDevice(name)
    if ecodes.EV_FF in dev.capabilities():
        break

condition = ff.Condition(0x7fff, 0x7fff, 0x3000, 0x3000, 0x0010, 0x2000)
effect = ff.Effect(
  ecodes.FF_SPRING, -1, 0,
  ff.Trigger(0, 0),
  ff.Replay(0, 0),
  ff.EffectType(ff_condition_effect=(condition,condition))
)
effect_id1 = dev.upload_effect(effect)

condition = ff.Condition(0x7fff, 0x7fff, 0x3000, 0x3000, 0x0010, -0x2000)
effect = ff.Effect(
  ecodes.FF_SPRING, -1, 0,
  ff.Trigger(0, 0),
  ff.Replay(0, 0),
  ff.EffectType(ff_condition_effect=(condition,condition))
)
effect_id2 = dev.upload_effect(effect)

repeat_count = 5
try:
    for i in range(10):
        time.sleep(3)
        dev.write(ecodes.EV_FF, effect_id1, 0)
        dev.write(ecodes.EV_FF, effect_id2, 0)
        if i%2==0:
            dev.write(ecodes.EV_FF, effect_id1, repeat_count)
        else:
            dev.write(ecodes.EV_FF, effect_id2, repeat_count)
    # dev.erase_effect(effect_id)
    input("press enter when done")
finally:
    dev.erase_effect(effect_id1)# upload的逆操作
    dev.erase_effect(effect_id2)