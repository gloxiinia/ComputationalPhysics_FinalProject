    #     g.clock.tick(g.FPS)
    #     g.space.step(1/g.FPS)
    #     rows = 5

    #     g.display.fill(g.BG)

    #     #pool balls
    #     #creating balls
    #     for column in range(5):
    #         for row in range (rows):
    #             pos = (250 + (column * (g.diam + 1)), 270 + (row * (g.diam + 1)) + (column * g.diam/2)) #x coordinate, y coordinate
    #             newBall = g.create_ball(g.diam/2, pos)
    #             g.balls.append(newBall)
    #         rows -= 1
        
    #     #creating ball images
    #     g.adding_ball_images()
    #     print(g.balls)
        
    #     #cue ball
    #     pos = (888, g.DISPLAY_H/2)
    #     cue_ball = g.create_ball(g.diam/2, pos)
    #     g.balls.append(cue_ball)

    #     #pool cushions
    #     for c in g.cushions:
    #         g.create_cushion(c)

    #     #cue stick setup
    #     cue_stick = Cue(g.balls[-1].body.position)

    #     #power bar setup and creation
    #     powerbar = pygame.Surface((10, 20))
    #     powerbar.fill(g.RED)

    #     #drawing the pool table
    #     g.display.blit(g.table_image, (0,0))

    #     #checking if any balls have been potted (went into the pockets)
    #     for i, ball in enumerate(g.balls):
    #         for pocket in g.pockets:
    #             xBallDist = abs(ball.body.position[0] - pocket[0])
    #             yBallDist = abs(ball.body.position[1] - pocket[1])
    #             ballDist = math.sqrt((xBallDist **2) + (yBallDist**2))
    #             if ballDist <= g.pocketDiam /2:
    #                 #check if the potted ball was the cue ball
    #                 if i == len(g.balls) - 1:
    #                     g.lives -= 1
    #                     g.cue_ball_potted = True
    #                     ball.body.position = (-200,-200)
    #                     ball.body.velocity = (0,0)
    #                 else:
    #                     g.space.remove(ball.body)
    #                     g.balls.remove(ball)
    #                     g.potted_balls.append(g.ball_images[i])
    #                     g.ball_images.pop(i)

    #     #drawing the pool balls
    #     for i, ball in enumerate(g.balls):
    #         g.display.blit(g.ball_images[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    #     #drawing the cue stick
    #     #checking if all pool balls have stopped moving
    #     g.taking_shot = True
    #     for ball in g.balls:
    #         if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0: #checking for ball speed, int is used in cases where the velocity is a really low value close to 0
    #             g.taking_shot = False
        
    #     #calculating the cue stick angle
    #     if g.taking_shot is True and g.running is True:
    #         if g.cue_ball_potted is True:
    #             #reposition cue ball
    #             g.balls[-1].body.position = (888, g.DISPLAY_H/2)
    #             g.cue_ball_potted = False

    #         mousePos = pygame.mouse.get_pos()

    #         cue_stick.rect.center = g.balls[-1].body.position #making sure the cue stick follows the cue ball

    #         xDist = g.balls[-1].body.position[0] - mousePos[0]
    #         yDist = -(g.balls[-1].body.position[1] - mousePos[1]) #invert it back bc pygame y coordinates are flipped
    #         cueAngle = math.degrees(math.atan2(yDist, xDist))
    #         cue_stick.update(cueAngle)
    #         cue_stick.draw(g.display)
        
    #     #powering up cue stick
    #     if g.powering_up is True and g.running is True:
    #         g.force += 100 * g.forceDir
    #         if g.force >= g.forceMax or g.force < 0:
    #             g.forceDir *= -1
    #         #draawing the power bar
    #         for bar in range(math.ceil(g.force /2000)):
    #             g.display.blit(powerbar, (g.balls[-1].body.position[0] -30  + (bar*15), 
    #                                 g.balls[-1].body.position[1] + 30))

    #     elif g.powering_up is False and g.taking_shot is True:
    #         xImpulse = math.cos(math.radians(cueAngle))
    #         YImpulse = math.sin(math.radians(cueAngle))
    #         g.balls[-1].body.apply_impulse_at_local_point((g.force * -xImpulse, g.force * YImpulse), (0,0))
    #         g.force = 0 #resetting the force for the next power up
    #         g.forceDir = 1 #resetting the force direction to not get stuck in a loop
        
    #     #drawing the bottom section
    #     pygame.draw.rect(g.display, g.BG, (0, g.DISPLAY_H, g.DISPLAY_W, g.BOTTOM_PANEL))
    #     g.draw_text(("LIVES: " + str(g.lives)), g.WHITE, 60, g.DISPLAY_W - 200, g.DISPLAY_H + 10)
        
    #     #drawing the potted balls in the bottom section
    #     for i, ball in enumerate(g.potted_balls):
    #         g.display.blit(ball, ((10 + (i * 50)), (g.DISPLAY_H + 10)))

    #     #checking for game over
    #     if g.lives <= 0:
    #         g.draw_text("GAME OVER", g.WHITE, 60, g.DISPLAY_W/2 - 160, g.DISPLAY_H /2 -100 )
    #         g.running = False
        
    #     #checking for win (all balls potted)
    #     if len(g.balls) == 1:
    #         g.draw_text("YOU ARE WIN :D", g.WHITE, 60, g.DISPLAY_W/2 - 160, g.DISPLAY_H /2 -100 )
    #         g.running = False

    # #background filling