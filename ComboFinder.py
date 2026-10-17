import math


def find_combos(dmg_values, dmg_dealt=0, combos=None, previous_setup="", base_health=100):
    if combos is None:
        combos = []
    if not dmg_values:
        return combos

    dmg_instance = dmg_values[0]

    shot_dmg = dmg_instance[0]
    shot_name = dmg_instance[1]
    dmg_diff = base_health - dmg_dealt
    shots_needed = math.ceil(dmg_diff/shot_dmg)

    # Check if there is a limit on how often an instance of damage can be applied
    if len(dmg_instance) > 2:
        max_shots = dmg_instance[2]
        max_shot_count = min(shots_needed, max_shots)
    else:
        max_shot_count = shots_needed

    for shot_count in range(max_shot_count, -1, -1):
        damage = dmg_dealt + shot_count * shot_dmg

        current_combo = previous_setup
        if shot_count > 0:
            current_combo += f"{shot_count} {shot_name}"

        if damage >= base_health:
            combos.append((damage, current_combo))
        else:
            if current_combo and shot_count > 0:
                current_combo += " + "
            combos = find_combos(dmg_values[1:], damage, combos, current_combo, base_health)
    return combos
