import json
from math import ceil


def populate_dmg_sources(window, agent, weapon, balance_file):

    agent_data = {
        (item["row"], item["field"]): item["value"]
        for item in balance_file["overrides"]
        if item["row"].startswith(agent)
    }

    body_dmg = "DamageBehaviors[BehaviorName=Default].Damage"
    crit_dmg = "DamageBehaviors[BehaviorName=Default].CriticalDamageMultiplier"

    # To deal with Sasori's Weapons (W3 clones)
    if not weapon.endswith("SE"):
        bodyshot = agent_data.get((weapon, body_dmg))
        headshot = bodyshot * agent_data.get((weapon, crit_dmg))

    else:
        se_count = int(weapon[-3])
        se_mult = agent_data.get(("Sasori_Weapon_Mod2", "ThrowMod2MultiplierPerSE"))
        base_bs = agent_data.get((weapon[:-4], body_dmg))
        bodyshot = base_bs + se_count * se_mult * base_bs
        headshot = bodyshot * agent_data.get((weapon[:-4], crit_dmg))
        weapon = weapon[:-4]

    quick_melee = 15
    charged_melee = 30

    window.add_damage_tab("BS", ceil(bodyshot))
    window.add_damage_tab("HS", ceil(headshot))

    if agent == "Chavez":
        e2_dmg = 10  # This may be hard coded
        window.add_damage_tab("E2", e2_dmg, max_occ=1)

    elif agent == "Ace":
        charged_bs = bodyshot * 1.25
        charged_hs = headshot * 1.25
        window.add_damage_tab("Charged BS", ceil(charged_bs))
        window.add_damage_tab("Charged HS", ceil(charged_hs))

    elif agent == "Squire":
        pass  # Squire only has 2 sources of damage

    elif agent == "Larcin":
        toss_bs_dmg = agent_data.get((weapon, "DamageBehaviors[BehaviorName=Throw].Damage"))
        toss_hs_dmg = toss_bs_dmg * agent_data.get((weapon, "DamageBehaviors[BehaviorName=Throw].CriticalDamageMultiplier"))
        window.add_damage_tab("Throw BS", ceil(toss_bs_dmg), max_occ=1)
        window.add_damage_tab("Throw HS", ceil(toss_hs_dmg), max_occ=1)

    elif agent == "Cavaliere":
        if weapon != "Cavaliere_Weapon_Base":
            window.tab_list[-1].destroy()  # Gets rid of duplicate entry for bs
            window.tab_list[-2].destroy()  # Gets rid of duplicate entry for hs
            window.tab_list = window.tab_list[:-2]
            window.add_damage_tab("BS", 2*bodyshot)
            window.add_damage_tab("HS", 2*ceil(headshot))

    elif agent == "Madame Xiu":
        pass  # Xiu only has 2 sources of damage

    elif agent == "Hans":
        window.tab_list[-1].destroy()  # Gets rid of duplicate entry for hipfire
        window.tab_list = window.tab_list[:-1]

        if weapon == "Hans_Weapon_Base":
            ads_bs_dmg = agent_data.get(("Hans_Weapon_ADS_Base", body_dmg))
            ads_hs_dmg = ads_bs_dmg * agent_data.get(("Hans_Weapon_ADS_Base", crit_dmg))
            window.add_damage_tab("ADS BS", ads_bs_dmg)
            window.add_damage_tab("ADS HS", ceil(ads_hs_dmg))

        elif weapon == "Hans_Weapon_Mod1":
            ads_bs_dmg = agent_data.get(("Hans_Weapon_ADS_Mod1", body_dmg))
            ads_hs_dmg = ads_bs_dmg * agent_data.get(("Hans_Weapon_ADS_Mod1", crit_dmg))
            window.add_damage_tab("ADS BS", ads_bs_dmg)
            window.add_damage_tab("ADS HS", ceil(ads_hs_dmg))

        elif weapon == "Hans_Weapon_Mod2":
            ads_bs_dmg = agent_data.get(("Hans_Weapon_ADS_Mod2", body_dmg))
            ads_hs_dmg = ads_bs_dmg * agent_data.get(("Hans_Weapon_ADS_Mod2", crit_dmg))
            window.add_damage_tab("ADS BS", ads_bs_dmg)
            window.add_damage_tab("ADS HS", ceil(ads_hs_dmg))

    elif agent == "Yumi":
        charged_bs_dmg = agent_data.get((weapon, "DamageBehaviors[BehaviorName=Charged].Damage"))
        charged_hs_dmg = charged_bs_dmg * agent_data.get((weapon, "DamageBehaviors[BehaviorName=Charged].CriticalDamageMultiplier"))

        # There is an error in the balance json. Experimental Splitshot should be Mod1 but is listed as Mod2
        if weapon == "Yumi_Weapon_Mod2":
            window.tab_list[-1].destroy()  # Gets rid of duplicate entry for headshot
            window.tab_list = window.tab_list[:-1]
            window.add_damage_tab("CBS", ceil(charged_bs_dmg))
        else:
            window.add_damage_tab("CBS", ceil(charged_bs_dmg))
            window.add_damage_tab("CHS", ceil(charged_hs_dmg))

    elif agent == "Socialite":
        if weapon == "Socialite_Weapon_Mod2":
            window.tab_list[-1].destroy()  # Gets rid of duplicate entry for headshot
            window.tab_list = window.tab_list[:-1]

    elif agent == "Sasori":
        # Sasori's Sword damage cannot be changed in the balance file
        # P2's Multiplier can be changed, however
        # Sasori W3 is in all likelihood hard-coded as well, meaning that changes to it in the balance.json will not
        # be reflected during actual gameplay.
        if weapon == "Sasori_Weapon_Base":
            sword_dmg = 40
            sword_dmg_gat = sword_dmg * agent_data.get(("Sasori_Passive_Mod1", "Mod1DamageMultiplier"))
            window.add_damage_tab("Sword", sword_dmg, max_occ=1)
            window.add_damage_tab("Sword(P2)", ceil(sword_dmg_gat), max_occ=1)

        elif weapon == "Sasori_Weapon_Mod1":
            charged_bs = 5 * bodyshot
            charged_hs = 5 * headshot
            window.add_damage_tab("Charged BS", charged_bs)
            window.add_damage_tab("Charged HS", ceil(charged_hs))

            sword_dmg = 30
            sword_dmg_gat = sword_dmg * agent_data.get(("Sasori_Passive_Mod1", "Mod1DamageMultiplier"))
            charged_sword_dmg = 60
            charged_sword_dmg_gat = charged_sword_dmg * agent_data.get(("Sasori_Passive_Mod1", "Mod1DamageMultiplier"))
            window.add_damage_tab("Sword", sword_dmg, max_occ=1)
            window.add_damage_tab("Charged S'", charged_sword_dmg, max_occ=1)
            window.add_damage_tab("Sword(P2)", ceil(sword_dmg_gat), max_occ=1)
            window.add_damage_tab("Charged S'(P2)", ceil(charged_sword_dmg_gat), max_occ=1)

        elif weapon == "Sasori_Weapon_Mod2":
            sword_dmg = 15
            sword_dmg_gat = sword_dmg * agent_data.get(("Sasori_Passive_Mod1", "Mod1DamageMultiplier"))
            window.add_damage_tab("Sword", sword_dmg, max_occ=1)
            window.add_damage_tab("Sword(P2)", ceil(sword_dmg_gat), max_occ=1)

        poison_dmg = agent_data.get(("Sasori_Active_Mod2", "Mod2Damage"))
        window.add_damage_tab("E3", poison_dmg, max_occ=1)

    elif agent == "Octo":
        if weapon == "Octo_Weapon_Base":
            intel_shot_dmg = agent_data.get(("Octo_Weapon_ADS_Base", "DamageBehaviors[BehaviorName=Default].Damage"))
            window.add_damage_tab("Intel BS", intel_shot_dmg)

        elif weapon == "Octo_Weapon_Mod1":
            intel_c1_dmg = agent_data.get(("Octo_Weapon_ADS_Mod1", "DamageBehaviors[BehaviorName=Default].Damage"))
            intel_c2_dmg = intel_c1_dmg * 2
            intel_c3_dmg = intel_c1_dmg * 3
            intel_c4_dmg = intel_c1_dmg * 4
            intel_c5_dmg = intel_c1_dmg * 5
            window.add_damage_tab("10 Bomb", ceil(intel_c1_dmg))
            window.add_damage_tab("20 Bomb", ceil(intel_c2_dmg))
            window.add_damage_tab("30 Bomb", ceil(intel_c3_dmg))
            window.add_damage_tab("40 Bomb", ceil(intel_c4_dmg))
            window.add_damage_tab("50 Bomb", ceil(intel_c5_dmg))

        elif weapon == "Octo_Weapon_Mod2":
            intel_bs_dmg = agent_data.get(("Octo_Weapon_ADS_Mod2", "DamageBehaviors[BehaviorName=Default].Damage"))
            intel_hs_dmg = intel_bs_dmg * agent_data.get(("Octo_Weapon_ADS_Mod2", "DamageBehaviors[BehaviorName=Default].CriticalDamageMultiplier"))
            window.add_damage_tab("Intel BS", ceil(intel_bs_dmg))
            window.add_damage_tab("Intel HS", ceil(intel_hs_dmg))

    elif agent == "Vigil":
        # Expertise mag sizes seem hard-coded
        e1_dmg = agent_data.get(("Vigil_Weapon_Active_Base", "DamageBehaviors[BehaviorName=Default].Damage"))
        e2_dmg = agent_data.get(("Vigil_Weapon_Active_Mod1", "DamageBehaviors[BehaviorName=Default].Damage"))
        e3_dmg = agent_data.get(("Vigil_Weapon_Active_Mod2", "DamageBehaviors[BehaviorName=Default].Damage"))
        p2_dmg = agent_data.get(("Vigil_Passive_Mod1", "AoEDamage"))
        window.add_damage_tab("E1", ceil(e1_dmg), max_occ=3)
        window.add_damage_tab("E2", ceil(e2_dmg), max_occ=8)
        window.add_damage_tab("E3", ceil(e3_dmg), max_occ=1)
        window.add_damage_tab("P2", ceil(p2_dmg), max_occ=2)

    else:
        print(f'Invalid Agent... "{agent}"')

    window.add_damage_tab("QM", quick_melee, max_occ=1)
    window.add_damage_tab("CM", charged_melee, max_occ=1)
