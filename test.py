
import evdev
from evdev import ecodes, InputDevice, ff

# Find first EV_FF capable event device (that we have permissions to use).
for name in evdev.list_devices():
    dev = InputDevice(name)
    if ecodes.EV_FF in dev.capabilities():
        break

envelope = ff.Envelope(0, 0, 0, 0)
force = -0.3
constant = ff.Constant(int(force * (65535 / 2)), envelope)
# effect = ff.Effect(
#   ecodes.FF_CONSTANT, -1, 16384,
#   ff.Trigger(0, 0),
#   ff.Replay(0, 0),
#   ff.EffectType(ff_constant_effect=constant)
# )
effect_type = ff.EffectType(ff_rumble_effect=rumble)
repeat_count = 1
effect_id = dev.upload_effect(effect)
try:
        dev.write(ecodes.EV_FF, effect_id, repeat_count)
        input("press enter when done")
finally:
        dev.erase_effect(effect_id)