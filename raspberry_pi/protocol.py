VALID_DIRECTIONS = {"LEFT", "CENTER", "RIGHT"}
VALID_RISKS = {"SAFE", "CAUTION", "DANGER"}


def encode_hazard(hazard):
    direction = hazard["direction"]
    risk = hazard["risk"]

    if direction not in VALID_DIRECTIONS:
        raise ValueError(f"잘못된 direction 값: {direction}")

    if risk not in VALID_RISKS:
        raise ValueError(f"잘못된 risk 값: {risk}")

    return (
        f"{hazard['object']},"
        f"{direction},"
        f"{risk},"
        f"{hazard['ttc']}"
    )