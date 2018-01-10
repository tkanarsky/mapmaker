import random
from json import dump
import gui


def create_bot_list(bots, earth_height):
    bot_list = []
    for x, i in enumerate(bots):
        bot_dict = {
                       "id": x,
                       "team": "Red" if i[2] == 0 else "Blue",
                       "level": 0,
                       "unit_type": "Worker",
                       "location": {
                           "OnMap": {
                               "planet": "Earth",
                               "x": i[1],
                               "y": earth_height - i[0] - 1
                           }
                       },
                       "health": 100,
                       "max_health": 100,
                       "vision_range": 50,
                       "damage": 0,
                       "attack_range": 0,
                       "movement_heat": 0,
                       "attack_heat": 0,
                       "movement_cooldown": 20,
                       "attack_cooldown": 0,
                       "is_ability_unlocked": True,
                       "ability_heat": 0,
                       "ability_cooldown": 500,
                       "ability_range": 2,
                       "has_worker_acted": False,
                       "build_health": 5,
                       "repair_health": 10,
                       "harvest_amount": 3,
                       "defense": 5,
                       "cannot_attack_range": 10,
                       "countdown": 0,
                       "max_countdown": 5,
                       "target_location": None,
                       "self_heal_amount": 1,
                       "is_built": False,
                       "max_capacity": 8,
                       "garrison": [

                       ],
                       "factory_unit_type": None,
                       "factory_rounds_left": None,
                       "factory_max_rounds_left": 5,
                       "is_used": False,
                       "blast_damage": 50,
                       "travel_time_decrease": 0
                   },
        bot_list.append(bot_dict)
    return bot_list


def random_asteroid_strikes(number, height, width, karbonite_range):
    asteroid_dict = {}
    for _ in range(number):
        time = random.randint(1, 1001)
        x = random.randint(0, width)
        y = random.randint(0, height)
        karbonite = random.randint(*karbonite_range)
        asteroid_dict[str(time)] = {
            "karbonite": karbonite,
            "location": {
                "planet": "Mars",
                "x": x,
                "y": y,
            }
        }
    return asteroid_dict


def orbit(amplitude, period, center):
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
            "is_passable_terrain": earth_terrain,
            "initial_karbonite": earth_karb,
        },
        "mars_map": {
            "planet": "Mars",
            "height": mars_height,
            "width": mars_width,
            "initial_units": [],
            "is_passable_terrain": mars_terrain,
            "initial_karbonite": mars_karb
        },
        "asteroids": {
            "pattern": asteroids
        },
        "orbit": orbit
    }


if __name__ == "__main__":
    try:
        seed = int(input(
            "\nWelcome to the barebones map creation wizard! Please enter a seed for the map (some random integer): "))
        earth_width, earth_height, *_ = [int(i) for i in
                                         input("Enter Earth map width and height, e.g: 20 20: ").strip().split(" ")]
        input("\nDefine Earth's geography, karbonite deposits, and initial worker placement.\n"
              "Left mouse button to place a water tile, right mouse button to clear tile.\n"
              "Scroll up/down to adjust karbonite on a particular tile, in increments of 5.\n"
              "Press R or B while hovering over a tile to place a red or blue worker, respectively.\n"
              "When finished, close the gui to proceed.\n"
              "Press ENTER to continue.")
        earth_terrain, earth_karbonite, robot_pos = gui.create_pygame_earth_editor(earth_height, earth_width)
        mars_width, mars_height, *_ = [int(i) for i in
                                       input("Enter Mars map width and height, e.g: 20 20: ").strip().split(" ")]
        input(
            "Next, define Mars's geography and initial karbonite deposits (even though technically there shouldn't be any).\n"
            "Left mouse button to place an impassable cliff, right mouse button to clear tile.\n"
            "Scroll up/down to adjust karbonite on a particular tile, in increments of 5.\n"
            "When finished, close the gui to proceed.\n"
            "Press ENTER to continue.")
        mars_terrain, mars_karbonite = gui.create_pygame_mars_editor(mars_height, mars_width)
        num_strikes = int(input(
            "Next, define the Mars asteroid strike pattern. Currently, this editor only supports random asteroid strikes.\n"
            "How many asteroid strikes do you want over the course of the game? e.g: 50: "))
        karbonite_range = [int(i) for i in input(
            "Enter low and high bounds for amount of karbonite per asteroid, e.g: 5 20: ").strip().split(" ")]
        amplitude = int(input("Enter an amplitude for the Earth-Mars transfer orbit, e.g: 1: "))
        period = int(input("Enter a period for the Earth-Mars transfer orbit, e.g: 218: "))
        center = int(input("Enter the center of the Earth-Mars transfer orbit, e.g: 67: "))
        bots = create_bot_list(robot_pos, earth_height)
        orbit_params = orbit(amplitude, period, center)
        asteroids = random_asteroid_strikes(num_strikes, mars_height, mars_width, karbonite_range)

        filename = input("Almost done! Give your map a name: ")
        filename += ".bc18"
        print("Creating json...")
        json_struct = create_json(seed, earth_height, earth_width, earth_terrain, earth_karbonite, bots, mars_width,
                                  mars_height, mars_terrain, mars_karbonite, asteroids, orbit_params)
        print("Created json!")
        dump(json_struct, open(filename, "w"))

    except KeyboardInterrupt:
        print("Exiting. File will not be created.")
