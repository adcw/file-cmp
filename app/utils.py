import colorsys

def similarity_to_color(value: float) -> str:
    r, g, b = colorsys.hsv_to_rgb((1 - value) * 0.4, 0.51, 0.98)
    return f"rgb({int(r * 255)}, {int(g * 255)}, {int(b * 255)})"
