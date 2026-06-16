from datetime import date, datetime

VENDOR_CHANGE_DATE = date(2025, 4, 15)


def normalize_pitch_features(pitch_hand: str, velocity: float, pfx_x: float,
                               pfx_z: float, spin_rate: int, game_date) -> dict:
    """
    Normalize pitch tracking features to arm-side reference frame.

    Vendor coordinate conventions:
      Pre-2025-04-15  — pfx_x in catcher's frame: positive = toward first base.
                        Left-handed pitchers: arm-side movement is NEGATIVE pfx_x.
                        Flip needed: multiply LHP pfx_x by -1 to normalize.
      2025-04-15 +    — pfx_x already in arm-side frame: positive = arm-side for
                        both handedness groups. No flip needed for LHP.

    Returns features with pfx_x normalized so positive always = arm-side movement.
    """
    if isinstance(game_date, str):
        game_date = datetime.strptime(game_date, '%Y-%m-%d').date()

    is_new_vendor = game_date >= VENDOR_CHANGE_DATE

    # Bug 1 (MAIN): flip is applied regardless of vendor convention.
    # For new vendor data (is_new_vendor=True), LHP pfx_x is already arm-side
    # normalized; flipping again reverses the sign, swapping fastball <-> slider.
    # Fix: add `and not is_new_vendor` to the condition.
    if pitch_hand == 'L':
        pfx_x = -pfx_x

    return {
        'velocity': velocity,
        'pfx_x': pfx_x,
        'pfx_z': pfx_z,
        'spin_rate': spin_rate,
        'pitch_hand': pitch_hand,
    }
