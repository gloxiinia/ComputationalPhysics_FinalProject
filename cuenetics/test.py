isRunning = True

while isRunning:

    
    clock.tick(FPS)
    space.step(1/FPS)

    #background filling
    screen.fill(BG)

    #check if game is paused
    if isGamePaused is True:
        pass
    else:
        continue

    #drawing the pool table
    screen.blit(tableImage, (0,0))

    #checking if any balls have been potted (went into the pockets)
    for i, ball in enumerate(balls):
        for pocket in pockets:
            xBallDist = abs(ball.body.position[0] - pocket[0])
            yBallDist = abs(ball.body.position[1] - pocket[1])
            ballDist = math.sqrt((xBallDist **2) + (yBallDist**2))
            if ballDist <= pocketDiam /2:
                #check if the potted ball was the cue ball
                if i == len(balls) - 1:
                    lives -= 1
                    isCueBallPotted = True
                    ball.body.position = (-200,-200)
                    ball.body.velocity = (0,0)
                else:
                    space.remove(ball.body)
                    balls.remove(ball)
                    pottedBalls.append(ballImages[i])
                    ballImages.pop(i)

    #drawing the pool balls
    for i, ball in enumerate(balls):
        screen.blit(ballImages[i], (ball.body.position[0] - ball.radius, ball.body.position[1] - ball.radius))

    #drawing the cue stick
    #checking if all pool balls have stopped moving
    isTakingShot = True
    for ball in balls:
        if int(ball.body.velocity[0]) != 0 or int(ball.body.velocity[1]) != 0: #checking for ball speed, int is used in cases where the velocity is a really low value close to 0
            isTakingShot = False
    
    #calculating the cue stick angle
    if isTakingShot is True and isGameRunning is True:
        if isCueBallPotted is True:
            #reposition cue ball
            balls[-1].body.position = (888, SCREEN_HEIGHT/2)
            isCueBallPotted = False

        mousePos = pygame.mouse.get_pos()

        cueStick.rect.center = balls[-1].body.position #making sure the cue stick follows the cue ball

        xDist = balls[-1].body.position[0] - mousePos[0]
        yDist = -(balls[-1].body.position[1] - mousePos[1]) #invert it back bc pygame y coordinates are flipped
        cueAngle = math.degrees(math.atan2(yDist, xDist))
        cueStick.update(cueAngle)
        cueStick.draw(screen)
    
    #powering up cue stick
    if isPoweringUp is True and isGameRunning is True:
        force += 100 * forceDir
        if force >= forceMax or force < 0:
            forceDir *= -1
        #draawing the power bar
        for bar in range(math.ceil(force /2000)):
            screen.blit(powerbar, (balls[-1].body.position[0] -30  + (bar*15), 
                                   balls[-1].body.position[1] + 30))

    elif isPoweringUp is False and isTakingShot is True:
        xImpulse = math.cos(math.radians(cueAngle))
        YImpulse = math.sin(math.radians(cueAngle))
        balls[-1].body.apply_impulse_at_local_point((force * -xImpulse, force * YImpulse), (0,0))
        force = 0 #resetting the force for the next power up
        forceDir = 1 #resetting the force direction to not get stuck in a loop
    
    #drawing the bottom section
    pygame.draw.rect(screen, BG, (0, SCREEN_HEIGHT, SCREEN_WIDTH, BOTTOM_PANEL))
    drawText("LIVES: " + str(lives), largeFont, WHITE, SCREEN_WIDTH - 200, SCREEN_HEIGHT + 10)
    
    #drawing the potted balls in the bottom section
    for i, ball in enumerate(pottedBalls):
        screen.blit(ball, ((10 + (i * 50)), (SCREEN_HEIGHT + 10)))

    #checking for game over
    if lives <= 0:
        drawText("GAME OVER", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
        isGameRunning = False
    
    #checking for win (all balls potted)
    if len(balls) == 1:
        drawText("YOU ARE WIN :D", largeFont, WHITE, SCREEN_WIDTH/2 - 160, SCREEN_HEIGHT /2 -100 )
        isGameRunning = False

    #event handling
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                isGamePaused = True
        if event.type == pygame.MOUSEBUTTONDOWN and isTakingShot is True:
            isPoweringUp = True
        if event.type == pygame.MOUSEBUTTONUP and isTakingShot is True:
            isPoweringUp = False
        if event.type == pygame.QUIT:
            isRunning = False
    
    # space.debug_draw(drawOptions)
    pygame.display.update()
