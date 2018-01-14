import pygame

TILE_SIZE = 20


def get_grid_coords_from_mouse(x, y, height, width):
    grid_col = int((x / (width * TILE_SIZE)) * width)
    grid_row = int((y / (height * TILE_SIZE)) * height)
    return grid_row, grid_col


def draw_bots(screen, bot_list):
    for i in bot_list:
        if i[2] == 0:  # red
            color = [255, 0, 0]
        else:  # blue
            color = [0, 255, 255]
        pygame.draw.circle(screen, color, [int(i[1] * TILE_SIZE + (TILE_SIZE / 2)),
                                           int(i[0] * TILE_SIZE + (TILE_SIZE / 2))],
                           int(TILE_SIZE / 4))
    pygame.display.flip()


def draw_lines(screen, height, width):
    for i in range(0, height):
        pygame.draw.line(screen, [255, 255, 255], [0, i * TILE_SIZE], [width * TILE_SIZE, i * TILE_SIZE], 1)
    for i in range(0, width):
        pygame.draw.line(screen, [255, 255, 255], [i * TILE_SIZE, 0], [i * TILE_SIZE, height * TILE_SIZE], 1)
    pygame.display.flip()

def create_pygame_earth_editor(height, width):
    terrain = [[True for _ in range(width)] for _ in range(height)]
    robot_positions = []
    karbonite = [[0 for _ in range(width)] for _ in range(height)]
    pygame.init()
    screen = pygame.display.set_mode([width * TILE_SIZE, height * TILE_SIZE])
    screen.fill([0, 200, 0])
    draw_lines(screen, height, width)
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise StopIteration
                elif 1 in pygame.mouse.get_pressed():
                    try: # try-catch necessary for off-screen mouse holds
                        event_pos = event.pos
                        event_button = event.button
                    except:
                        try:
                            event_button = list(event.buttons).index(1)+1
                        except:
                            continue
                    if event_button == 1:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        if list(coords) not in [x[:2] for x in robot_positions]:

                            terrain[coords[0]][coords[1]] = False
                            karbonite[coords[0]][coords[1]] = 0
                            pygame.draw.rect(screen, [0, 0, 255],
                                             pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                         TILE_SIZE), 0)
                            draw_bots(screen, robot_positions)
                            draw_lines(screen, height, width)
                    elif event_button == 3:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        terrain[coords[0]][coords[1]] = True
                        karbonite[coords[0]][coords[1]] = 0
                        if list(coords) in [x[:2] for x in robot_positions]:
                            idx = [x[:2] for x in robot_positions].index(list(coords))
                            robot_positions.pop(idx)
                        pygame.draw.rect(screen, [0, 200, 0],
                                         pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                     TILE_SIZE), 0)
                        draw_bots(screen, robot_positions)
                        draw_lines(screen, height, width)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 4:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        terrain[coords[0]][coords[1]] = True
                        if karbonite[coords[0]][coords[1]] < 45:
                            karbonite[coords[0]][coords[1]] += 5
                        pygame.draw.rect(screen, [0, 200 - karbonite[coords[0]][coords[1]] * 4, 0],
                                         pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                     TILE_SIZE), 0)
                        draw_bots(screen, robot_positions)
                        draw_lines(screen, height, width)
                    elif event.button == 5:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        terrain[coords[0]][coords[1]] = True
                        if karbonite[coords[0]][coords[1]] >= 5:
                            karbonite[coords[0]][coords[1]] -= 5
                        pygame.draw.rect(screen, [0, 200 - karbonite[coords[0]][coords[1]] * 5, 0],
                                         pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                     TILE_SIZE), 0)
                        draw_bots(screen, robot_positions)
                        draw_lines(screen, height, width)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        pos = pygame.mouse.get_pos()
                        coords = get_grid_coords_from_mouse(pos[0], pos[1], height, width)
                        if [*coords, 1] not in robot_positions and [*coords, 0] not in robot_positions:
                            terrain[coords[0]][coords[1]] = True
                            pygame.draw.rect(screen, [0, 200 - karbonite[coords[0]][coords[1]] * 5, 0],
                                             pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                         TILE_SIZE), 0)
                            robot_positions.append([*coords, 0])
                            draw_bots(screen, robot_positions)
                            draw_lines(screen, height, width)
                    elif event.key == pygame.K_b:
                        pos = pygame.mouse.get_pos()
                        coords = get_grid_coords_from_mouse(pos[0], pos[1], height, width)
                        if [*coords, 1] not in robot_positions and [*coords, 0] not in robot_positions:
                            terrain[coords[0]][coords[1]] = True
                            pygame.draw.rect(screen, [0, 200 - karbonite[coords[0]][coords[1]] * 5, 0],
                                             pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                         TILE_SIZE), 0)
                            robot_positions.append([*coords, 1])
                            draw_bots(screen, robot_positions)
                            draw_lines(screen, height, width)


    except StopIteration:
        pygame.quit()
        return terrain, karbonite, robot_positions


def create_pygame_mars_editor(height, width):
    terrain = [[True for _ in range(width)] for _ in range(height)]
    karbonite_tiles = [[0 for _ in range(width)] for _ in range(height)]
    pygame.init()
    screen = pygame.display.set_mode([width * TILE_SIZE, height * TILE_SIZE])
    screen.fill([231, 125, 17])
    draw_lines(screen, height, width)
    try:
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    raise StopIteration
                elif 1 in pygame.mouse.get_pressed():
                    try: # try-catch necessary for off-screen mouse holds
                        event_pos = event.pos
                        event_button = event.button
                    except:
                        try:
                            event_button = list(event.buttons).index(1)+1
                        except:
                            continue
                    if event_button == 1:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        terrain[coords[0]][coords[1]] = False
                        karbonite_tiles[coords[0]][coords[1]] = 0
                        pygame.draw.rect(screen, [230, 24, 4],
                                         pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                     TILE_SIZE), 0)
                        draw_lines(screen, height, width)
                    elif event_button == 3:
                        coords = get_grid_coords_from_mouse(event.pos[0], event.pos[1], height, width)
                        terrain[coords[0]][coords[1]] = True
                        karbonite_tiles[coords[0]][coords[1]] = 0
                        pygame.draw.rect(screen, [231, 125, 17],
                                         pygame.Rect(coords[1] * TILE_SIZE, coords[0] * TILE_SIZE, TILE_SIZE,
                                                     TILE_SIZE), 0)
                        draw_lines(screen, height, width)
    except StopIteration:
        pygame.quit()
        return terrain, karbonite_tiles
