import re
import time
from math import ceil, prod


def apply_blueprint_dumb(costs, time_left,
                         ore=0, clay=0, obs=0,
                         ore_bot=1, clay_bot=0, obs_bot=0):
    if time_left <= 0:
        return 0
    if time_left < 6 and obs_bot == 0:
        return 0
    # print(time_left, ore, clay, obs, ore_bot, clay_bot, obs_bot)
    new_ore = ore + ore_bot
    new_clay = clay + clay_bot
    new_obs = obs + obs_bot
    time_left -= 1
    most_geodes = 0
    # no building
    profit = apply_blueprint_dumb(costs, time_left,
                                  new_ore, new_clay, new_obs,
                                  ore_bot, clay_bot, obs_bot)
    if profit > most_geodes:
        most_geodes = profit
    # build ore_bot
    if ore >= costs[0]["ore"]:
        profit = apply_blueprint_dumb(costs, time_left,
                                      new_ore - costs[0]["ore"],
                                      new_clay, new_obs,
                                      ore_bot + 1, clay_bot, obs_bot)
        if profit > most_geodes:
            most_geodes = profit
    # build clay_bot
    if ore >= costs[1]["ore"]:
        profit = apply_blueprint_dumb(costs, time_left,
                                      new_ore - costs[1]["ore"],
                                      new_clay, new_obs,
                                      ore_bot, clay_bot + 1, obs_bot)
        if profit > most_geodes:
            most_geodes = profit
    # build obs_bot
    if ore >= costs[2]["ore"] and clay >= costs[2]["clay"]:
        profit = apply_blueprint_dumb(costs, time_left,
                                      new_ore - costs[2]["ore"],
                                      new_clay - costs[2]["clay"],
                                      new_obs,
                                      ore_bot, clay_bot, obs_bot + 1)
        if profit > most_geodes:
            most_geodes = profit
    # build geode_bot
    if ore >= costs[3]["ore"] and obs >= costs[3]["obsidian"]:
        profit = (
                time_left
                + apply_blueprint_dumb(costs, time_left,
                                       new_ore - costs[3]["ore"],
                                       new_clay,
                                       new_obs - costs[3]["obsidian"],
                                       ore_bot, clay_bot, obs_bot)
        )
        if profit > most_geodes:
            most_geodes = profit

    return most_geodes


def apply_blueprint(costs, time_left,
                    ore=0, clay=0, obs=0,
                    ore_bot=1, clay_bot=0, obs_bot=0):
    if time_left <= 0:
        return 0
    # print(f"T: {time_left}, OCO {ore, clay, obs}, Bots {ore_bot, clay_bot, obs_bot}")
    most_geodes = 0
    # next ore-bot
    if costs[0]["ore"] <= ore:
        time_to = 1
    else:
        time_to = ceil((costs[0]["ore"] - ore) / ore_bot) + 1
    if 0 < time_to < time_left:
        profit = apply_blueprint(costs, time_left - time_to,
                                 ore + time_to * ore_bot - costs[0]["ore"],
                                 clay + time_to * clay_bot,
                                 obs + time_to * obs_bot,
                                 ore_bot + 1, clay_bot, obs_bot)
        if profit > most_geodes:
            most_geodes = profit
    # next clay-bot
    time_to = ceil((costs[1]["ore"] - ore) / ore_bot) + 1
    if 0 < time_to < time_left:
        profit = apply_blueprint(costs, time_left - time_to,
                                 ore + time_to * ore_bot - costs[1]["ore"],
                                 clay + time_to * clay_bot,
                                 obs + time_to * obs_bot,
                                 ore_bot, clay_bot + 1, obs_bot)
        if profit > most_geodes:
            most_geodes = profit
    # next obs-bot
    if clay_bot > 0:
        time_to = max(
            ceil((costs[2]["ore"] - ore) / ore_bot),
            ceil((costs[2]["clay"] - clay) / clay_bot)
        ) + 1
        if 0 < time_to < time_left:
            profit = apply_blueprint(costs, time_left - time_to,
                                     ore + time_to * ore_bot - costs[2]["ore"],
                                     clay + time_to * clay_bot - costs[2]["clay"],
                                     obs + time_to * obs_bot,
                                     ore_bot, clay_bot, obs_bot + 1)
            if profit > most_geodes:
                most_geodes = profit
    # next geode-bot
    if obs_bot > 0:
        time_to = max(
            ceil((costs[3]["ore"] - ore) / ore_bot),
            ceil((costs[3]["obsidian"] - obs) / obs_bot)
        ) + 1
        if 0 < time_to < time_left:
            profit = (apply_blueprint(costs, time_left - time_to,
                                      ore + time_to * ore_bot - costs[3]["ore"],
                                      clay + time_to * clay_bot,
                                      obs + time_to * obs_bot - costs[3]["obsidian"],
                                      ore_bot, clay_bot, obs_bot)
                      + time_left - time_to)
            # print(f"left: {time_left}, next: {time_to}, geodes: {time_left - time_to}"
            #       f"   ore: {ore}, obs: {obs}")
            if profit > most_geodes:
                most_geodes = profit
    return most_geodes

blueprints = []
with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        rob_list = []
        for robot in line.split(":")[1].split(".")[:-1]:
            match = re.findall("([0-9]+) ([a-z]+)", robot)
            rob_dict = {}
            for group in match:
                rob_dict[group[1]] = int(group[0])
            rob_list.append(rob_dict)
        blueprints.append(rob_list)

start_time = time.time()
quality_levels = []
for i, blue in enumerate(blueprints):
    quality_levels.append(
        apply_blueprint(blue, 24) * (i+1)
    )
print("--- First part: ---")
print(f"Quality levels: {quality_levels}")
print(f"Sum of quality levels: {sum(quality_levels)}")
print(f"{time.time() - start_time}s")

start_time = time.time()
geodes_opened = []
for i, blue in enumerate(blueprints[:3]):
    geodes_opened.append(
        apply_blueprint(blue, 32)
    )
    print(f"Number {i+1} done after {time.time() - start_time}s")
print("--- Second part: ---")
print(f"Geodes opened: {geodes_opened}")
print(f"Product of opened Geodes: {prod(geodes_opened)}")
# 79560 too high [26, 102, 30]
#                 26,  51, 10
# 13260 too low