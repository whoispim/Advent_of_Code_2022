import re
import time
from math import ceil, prod
import functools


@functools.cache
def apply_blueprint(costs, time_left,
                    ore=0, clay=0, obs=0,
                    ore_bot=1, clay_bot=0, obs_bot=0):
    if time_left <= 0:
        return 0
    most_geodes = 0
    # next ore-bot
    # check if max feasible amount hasn't been reached yet
    if ore_bot < costs[4]:
        if costs[0] <= ore:
            time_to = 1
        else:
            time_to = ceil((costs[0] - ore) / ore_bot) + 1
        if 0 < time_to < time_left:
            profit = apply_blueprint(costs, time_left - time_to,
                                     ore + time_to * ore_bot - costs[0],
                                     clay + time_to * clay_bot,
                                     obs + time_to * obs_bot,
                                     ore_bot + 1, clay_bot, obs_bot)
            if profit > most_geodes:
                most_geodes = profit
    # next clay-bot
    # check if max feasible amount hasn't been reached yet
    if clay_bot < costs[2][1]:
        if costs[1] <= ore:
            time_to = 1
        else:
            time_to = ceil((costs[1] - ore) / ore_bot) + 1
        if 0 < time_to < time_left:
            profit = apply_blueprint(costs, time_left - time_to,
                                     ore + time_to * ore_bot - costs[1],
                                     clay + time_to * clay_bot,
                                     obs + time_to * obs_bot,
                                     ore_bot, clay_bot + 1, obs_bot)
            if profit > most_geodes:
                most_geodes = profit
    # next obs-bot
    # check if base resource can be produced and if max feasible
    # amount hasn't been reached yet
    if clay_bot > 0 and obs_bot < costs[3][1]:
        if costs[2][0] <= ore and costs[2][1] <= clay:
            time_to = 1
        else:
            time_to = max(
                ceil((costs[2][0] - ore) / ore_bot),
                ceil((costs[2][1] - clay) / clay_bot)
            ) + 1
        if 0 < time_to < time_left:
            profit = apply_blueprint(costs, time_left - time_to,
                                     ore + time_to * ore_bot - costs[2][0],
                                     clay + time_to * clay_bot - costs[2][1],
                                     obs + time_to * obs_bot,
                                     ore_bot, clay_bot, obs_bot + 1)
            if profit > most_geodes:
                most_geodes = profit
    # next geode-bot
    if obs_bot > 0:
        if costs[3][0] <= ore and costs[3][1] <= obs:
            time_to = 1
        else:
            time_to = max(
                ceil((costs[3][0] - ore) / ore_bot),
                ceil((costs[3][1] - obs) / obs_bot)
            ) + 1
        if 0 < time_to < time_left:
            profit = (apply_blueprint(costs, time_left - time_to,
                                      ore + time_to * ore_bot - costs[3][0],
                                      clay + time_to * clay_bot,
                                      obs + time_to * obs_bot - costs[3][1],
                                      ore_bot, clay_bot, obs_bot)
                      + time_left - time_to)
            if profit > most_geodes:
                most_geodes = profit
    return most_geodes


blueprints = []
with open("input", "r") as f:
    for line in f.read().strip().split("\n"):
        rob_list = []
        for robot in line.split(":")[1].split(".")[:-1]:
            match = re.findall("([0-9]+) ([a-z]+)", robot)
            rob_tup = []
            for group in match:
                rob_tup.append(int(group[0]))
            if len(rob_tup) == 1:
                rob_list.append(rob_tup[0])
            else:
                rob_list.append(tuple(rob_tup))
        # add max clay need to end
        rob_list.append(max(rob_list[0], rob_list[1], rob_list[2][0]))
        blueprints.append(tuple(rob_list))

start_time = time.time()
quality_levels = []
for i, blue in enumerate(blueprints):
    apply_blueprint.cache_clear()
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
    apply_blueprint.cache_clear()
    geodes_opened.append(
        apply_blueprint(blue, 32)
    )
    print(f"Number {i+1} done after {time.time() - start_time}s")
print("--- Second part: ---")
print(f"Geodes opened: {geodes_opened}")
print(f"Product of opened Geodes: {prod(geodes_opened)}")

