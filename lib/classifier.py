def classify_pitch(features: dict) -> str:
    """
    Rule-based pitch classifier operating in arm-side normalized frame.

    All inputs must be in the arm-side reference frame:
      pfx_x > 0  — arm-side movement (e.g., natural run for a fastball)
      pfx_x < 0  — glove-side movement (e.g., slider cut, cutter)
      pfx_z > 0  — rise above gravity (backspin lift)
      pfx_z < 0  — drop below gravity baseline

    Velocity in mph, pfx values in inches.
    Thresholds calibrated to 2024 MLB Statcast population averages.
    """
    velo = features['velocity']
    pfx_x = features['pfx_x']
    pfx_z = features['pfx_z']

    # 4-seam fastball: high velocity, arm-side run, backspin rise
    if velo >= 95.0 and pfx_x >= 5.0 and pfx_z >= 8.0:
        return '4-seam fastball'

    # Sinker / 2-seam: high velocity, arm-side run, heavy sink
    if velo >= 90.0 and pfx_x >= 3.0 and pfx_z < 6.0:
        return 'sinker'

    # Cutter: mid-high velocity, glove-side cut, moderate rise
    if velo >= 92.0 and pfx_x <= -2.0 and pfx_z >= 3.0:
        return 'cutter'

    # Slider: mid velocity, glove-side break, moderate-to-heavy drop
    if velo >= 78.0 and pfx_x <= -3.0 and pfx_z < 3.0:
        return 'slider'

    # Curveball: low velocity, large downward break
    if velo < 82.0 and pfx_z < -2.0:
        return 'curveball'

    # Changeup: mid velocity, arm-side fade, sinking action
    if velo < 90.0 and pfx_x >= 2.0 and pfx_z < 5.0:
        return 'changeup'

    return 'fastball'
