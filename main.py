import random
from json import dump

import gui
from validate import *


def generate_strike_pattern(seed, width, height):
    # Implemented according to map.rst, so should work.
    validated = False
    seed_plus = 0
    while not validated:
        random.seed(seed + seed_plus)
        astrd_list = []
        karb_possibilities = list(range(ASTEROID_KARB_MIN, ASTEROID_KARB_MAX + 1))
        round_possibilities = list(range(ASTEROID_ROUND_MIN, ASTEROID_ROUND_MAX + 1))
        x_possibilities = list(range(0, width))
        y_possibilities = list(range(0, height))
        rounds = 0
        while True:
            round_plus = random.choice(round_possibilities)
            rounds += round_plus
            if rounds >= ROUND_LIMIT:
                break
            karb = random.choice(karb_possibilities)
            x = random.choice(x_possibilities)
            y = random.choice(y_possibilities)
            astrd_list.append([rounds, karb, x, y])
        validated = validate_asteroid_pattern(astrd_list)
        if not validated:
            seed_plus += 1
    return astrd_list


def json_bot_list(bots, earth_height):
    bot_list = []
    for x, i in enumerate(bots):
        # bot_dict = {
        #                "id": x,
        #                "team": "Red" if i[2] == 0 else "Blue",
        #                "level": 0,
        #                "unit_type": "Worker",
        #                "location": {
        #                    "OnMap": {
        #                        "planet": "Earth",
        #                        "x": i[1],
        #                        "y": earth_height - i[0] - 1
        #                    }
        #                },
        #                "health": 100,
        #                "max_health": 100,
        #                "vision_range": 50,
        #                "damage": 0,
        #                "attack_range": 0,
        #                "movement_heat": 0,
        #                "attack_heat": 0,
        #                "movement_cooldown": 20,
        #                "attack_cooldown": 0,
        #                "is_ability_unlocked": True,
        #                "ability_heat": 0,
        #                "ability_cooldown": 500,
        #                "ability_range": 2,
        #                "has_worker_acted": False,
        #                "build_health": 5,
        #                "repair_health": 10,
        #                "harvest_amount": 3,
        #                "defense": 5,
        #                "cannot_attack_range": 10,
        #                "countdown": 0,
        #                "max_countdown": 5,
        #                "target_location": None,
        #                "self_heal_amount": 1,
        #                "is_built": False,
        #                "max_capacity": 8,
        #                "garrison": [
        #
        #                ],
        #                "factory_unit_type": None,
        #                "factory_rounds_left": None,
        #                "factory_max_rounds_left": 5,
        #                "is_used": False,
        #                "blast_damage": 50,
        #                "travel_time_decrease": 0
        #            },
        bot_dict = {
                "ability_cooldown": 500,
                "ability_heat": 0,
                "ability_range": 2,
                "attack_cooldown": 0,
                "attack_heat": 0,
                "attack_range": 0,
                "blast_damage": 50,
                "build_health": 5,
                "cannot_attack_range": 10,
                "countdown": 0,
                "damage": 0,
                "defense": 5,
                "factory_max_rounds_left": 5,
                "factory_rounds_left": None,
                "factory_unit_type": None,
                "garrison": [],
                "harvest_amount": 3,
                "has_worker_acted": False,
                "health": 100,
                "id": x,
                "is_ability_unlocked": True,
                "is_built": False,
                "is_used": False,
                "level": 0,
                "location": {
                    "OnMap": {
                        "planet": "Earth",
                        "x": i[1],
                        "y": earth_height - i[0] - 1
                    }
                },
                "max_capacity": 8,
                "max_countdown": 5,
                "max_health": 100,
                "movement_cooldown": 20,
                "movement_heat": 0,
                "repair_health": 10,
                "self_heal_amount": 1,
                "target_location": None,
                "team": "Red" if i[2] == 0 else "Blue",
                "travel_time_decrease": 0,
                "unit_type": "Worker",
                "vision_range": 50
            }
        bot_list.append(bot_dict)
    return bot_list


def json_random_asteroid_strikes(asteroid_list):
    asteroid_dict = {}
    for i in asteroid_list:
        asteroid_dict[i[0]] = {
            "karbonite": i[1],
            "location": {
                "planet": "Mars",
                "x": i[2],
                "y": i[3],
            }
        }
    return asteroid_dict


def json_orbit(amplitude, period, center):
    return {
        "amplitude": amplitude,
        "period": period,
        "center": center,
        "amplitude_s": amplitude,
        "period_s": period,
        "center_s": center
    }


def create_json(seed, earth_height, earth_width, earth_terrain, earth_karb, bots, mars_width, mars_height, mars_terrain,
                mars_karb, asteroids, orbit):
    return {
        "seed": seed,
        "earth_map": {
            "planet": "Earth",
            "height": earth_height,
            "width": earth_width,
            "initial_units": bots,
            "is_passable_terrain": [list(i)[::-1] for i in zip(*earth_terrain)], # I love python (transposing array)!
            "initial_karbonite": [list(i)[::-1] for i in zip(*earth_karb)],
        },
        "mars_map": {
            "planet": "Mars",
            "height": mars_height,
            "width": mars_width,
            "initial_units": [],
            "is_passable_terrain": [list(i)[::-1] for i in zip(*mars_terrain)],
            "initial_karbonite": [list(i)[::-1] for i in zip(*mars_karb)]
        },
        "asteroids": {
            "pattern": asteroids
        },
        "orbit": orbit
    }

if __name__ == "__main__":
    try:
        seed = int(input(
            "\nWelcome to the barebones map creation wizard! Now complying with the Battlecode specs.\n"
            "Please enter a seed for the RNG (some random integer): "))
        valid = False
        while not valid:
            earth_width, earth_height, *_ = [int(i) for i in
                                             input(
                                                 "Enter Earth map width and height. Minimum is 20x20, maximum is 50x50. e.g 25 25: ").strip().split(
                                                 " ")]
            valid = validate_map_dims(earth_height, earth_width)
            if not valid:
                print(
                    "Sorry, that was not a valid dimension. This would be rejected by the Battlecode engine. Try again.")

        input("\nDefine Earth's geography, karbonite deposits, and initial worker placement.\n"
              "Left mouse button to place a water tile, right mouse button to clear tile.\n"
              "Scroll up/down to adjust karbonite on a particular tile, in increments of 5.\n"
              "Press R or B while hovering over a tile to place a red or blue worker, respectively.\n"
              "When finished, close the gui to proceed.\n\n"
              "IMPORTANT: THERE MUST BE AN EVEN TOTAL NUMBER OF WORKERS, 0 < x <= 6. FAILURE TO DO SO WILL RESULT IN LOSS OF MAP.\n"
              "ALSO IMPORTANT: MAP MUST BE SYMMETRICAL. FAILURE TO DO SO WILL RESULT IN LOSS OF MAP.\n\n"
              "Press ENTER to continue.")
        valid = False
        while not valid:
            earth_terrain, earth_karbonite, robot_pos = gui.create_pygame_earth_editor(earth_height, earth_width)
            valid = validate_num_bots(robot_pos)
            if not valid:
                input(
                    "Sorry, that map wouldn't've passed Battlecode's checks. Please try again. Read the 'IMPORTANT'. Press ENTER to continue.")
        valid = False
        while not valid:
            mars_width, mars_height, *_ = [int(i) for i in
                                           input(
                                               "Enter Mars map width and height. Minimum is 20x20, maximum is 50x50. e.g 25 25: ").strip().split(
                                               " ")]
            valid = validate_map_dims(mars_height, mars_width)
            if not valid:
                print(
                    "Sorry, that was not a valid dimension. This would be rejected by the Battlecode engine. Try again.")

        input(
            "Next, define Mars's geography and initial karbonite deposits (even though technically there shouldn't be any).\n"
            "Left mouse button to place an impassable cliff, right mouse button to clear tile.\n"
            "When finished, close the gui to proceed.\n"
            "Press ENTER to continue.")

        mars_terrain, mars_karbonite = gui.create_pygame_mars_editor(mars_height, mars_width)
        print("Generating asteroid pattern...")
        asteroid_list = generate_strike_pattern(seed, mars_height, mars_width)

        valid = False
        while not valid:
            print(
                "PLEASE NOTE THAT THE MAXIMUM ALLOWED TRAVEL TIME IS 200 RDS AND MINIMUM ALLOWED TRAVEL TIME IS 50 RDS. KEEP THIS IN MIND.")
            amplitude = int(input(
                "Enter an amplitude for the Earth-Mars transfer orbit. This is by how much from the centerline the travel time varies, e.g: 50: "))
            period = int(input(
                "Enter a period for the Earth-Mars transfer orbit. This is how often an orbit cycle repeats, in rounds e.g: 200: "))
            center = int(input(
                "Enter the center of the Earth-Mars transfer orbit. This is the centerline travel time. e.g: 125: "))

            valid = validate_orbital_pattern(amplitude, period, center)
            if not valid:
                print("Sorry, the orbital parameters are outside the allowed values. Please try again.")

        bots = json_bot_list(robot_pos, earth_height)
        orbit_params = json_orbit(amplitude, period, center)
        asteroids = json_random_asteroid_strikes(asteroid_list)

        filename = input("Almost done! Give your map a name: ")
        filename += ".bc18map"
        print("Creating json...")
        json_struct = create_json(seed, earth_height, earth_width, earth_terrain, earth_karbonite, bots, mars_width,
                                  mars_height, mars_terrain, mars_karbonite, asteroids, orbit_params)
        print("Created json!")
        dump(json_struct, open(filename, "w"))

    except KeyboardInterrupt:
        print("Exiting. File will not be created.")
