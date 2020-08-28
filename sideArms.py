from tkinter import *
from random import randint
import time
import pickle

width = 800
height = 550


def rKey(event):
    """ Restart button """
    startGame()


def leftKey(event):
    """ Move left if players still on screen """
    global playerX
    if playerX > 0:
        playerX -= 20
    movePlayer()


def rightKey(event):
    """ Move right if player still on screen """
    global playerX
    if playerX < 790:
        playerX += 20
    movePlayer()


def upKey(event):
    """ Move up if player still on screen """
    global playerY
    if playerY > 40:
        playerY -= 20
    movePlayer()


def downKey(event):
    """ Move down if player still on screen """
    global playerY
    if playerY < 530:
        playerY += 20
    movePlayer()


def lookLeft(event):
    """ Changes sprite to look left and creates bullets that moves in player
    diection """
    direction = -1
    canvas.itemconfig(playerSprite, image=playerImgFlipped)
    createBullet(direction)


def lookRight(event):
    """ Changes sprite to look right and creates bullets that moves in player
    diection """
    direction = 1
    canvas.itemconfig(playerSprite, image=playerImg)
    createBullet(direction)


def escapeKey(event):
    """ General pause key, is only bound if on game screen """
    global gameState
    if gameState != "paused":
        gameState = "paused"
        pauseGame()
    else:
        unpauseGame()


def movePlayer():
    """ Bound keys will change coords of player and this function updates its
    location """
    canvas.coords(
        player, playerX, playerY, playerX + playerSize * 5,
        playerY - playerSize * 2.5
        )
    canvas.coords(playerSprite, playerX, playerY)
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


def createEnemy():
    global score
    """ Creates enemy by adding the collision box and image to lists at a
    random Y and X = 0, also adds them to a list which tracks where they are in
    on a path """
    randY = randint(0, height-60)
    randX = randint(0, width-30)
    rand = randint(0, 5)
    # Creates enemy that drops from top of canvas
    if rand == 0:
        enemies.append(canvas.create_rectangle(
            randX, 0, randX + 30, 30
            ))
        enemiesImgs.append(canvas.create_image(
            randX, 0, image=enemiesDropImg,
            anchor=NW
            ))
        enemyPathPoint.append("drop")
    # Creates enemy that moves from right of screen and back
    else:
        enemies.append(canvas.create_rectangle(
            800, randY, 800 + 40, randY + 60
            ))
        enemiesImgs.append(canvas.create_image(
            800, randY, image=enemiesImg,
            anchor=NW
            ))
        enemyPathPoint.append(0)
    # Ensures enemies do not spawn on top of each other
    for i in range(len(enemies) - 1):
        if checkCollision(enemies[-1], enemies[i]):
            score -= 100
            deleteEnemy(len(enemies) - 1)
            createEnemy()


def deleteEnemy(i):
    """ Increases score and removed enemy objects from canvas and lists
    essentially 'deleting' the enemy """
    global score
    score += 100
    canvas.itemconfigure(scoreText, text="SCORE: " + str(score))
    canvas.delete(enemies[i])
    canvas.delete(enemiesImgs[i])
    del enemyPathPoint[i]
    del enemiesImgs[i]
    del enemies[i]


def createBullet(direction):
    """ If the canShoot variable is true creates a bullet collision box and
    image and the direction it is shooting in, then adds all of these to lists
    so they can be tracked easily """
    global canShoot
    # canShoot Ensures that player can only shoot once every 400ms
    if canShoot == 1:
        canShoot = 0
        bulletDirections.append(direction)
        bullets.append(canvas.create_rectangle(
            playerX + 37,
            playerY-(1.5*playerSize),
            playerX + 5, playerY + 5-(1.5*playerSize))
            )
        bulletImgs.append(canvas.create_image(0, 0, image=bulletImg))
        window.after(400, updateCanshoot)  # Allows shooting after 400ms


def updateCanshoot():
    """ Sets can shoot to 1 so that the player can shoot again """
    global canShoot
    canShoot = 1


def checkName():
    """ Takes the input from the main menu and validates it, makes sure there
    are no spaces in it. Then checks to see if the user has typed in a cheat
    and if so applies the cheat code, otherwise it will set the name and start
    the game """
    global playerName
    global inv
    global error
    playerName = gameNameEntry.get()
    # Ensures spaces are not allowed as it would break leaderboard
    if " " in playerName:
        error = canvasMainMenu.create_image(
            400, 540, image=nameErrorImg, anchor=CENTER
            )
    # Activates the invinsible cheat code
    elif playerName == "INVINSIBLE":
        if "Invinsible" not in cheats:
            inv = canvasMainMenu.create_image(
                400, 500, image=invImg, anchor=CENTER
                )
            cheats.append(playerName)
    # Activates the Multiply cheat code
    elif playerName == "Multiply":
        if "Multiply" not in cheats:
            mul = canvasMainMenu.create_image(
                400, 520, image=mulImg, anchor=CENTER
                )
            cheats.append(playerName)
    # If all other coditions are not met the allow player to start game
    else:
        startGame()


def loadGame():
    """ Virtually identical to the start game function but instead loads the
    variables that are set to default values from a file Save1.txt """
    # Ensures that there is a file to load from, if not creates a new game
    try:
        t = open("Save1.txt")
    except IOError:
        startGame()
        return 0
    global programCounter
    global playerName
    global playerX
    global playerY
    global player
    global score
    global gameState
    global leaderboardText
    global playerSprite
    global scoreText
    if gameState == "reset":
        # Clears leaderboard if game has just been reset
        for i in sorted(range(len(leaderboardText)), reverse=True):
            canvas.delete(leaderboardText[i])
            del leaderboardText[i]
        canvas.delete(restartTxt)
    else:
        # If just come from main menu then remove the menu
        canvasMainMenu.destroy()
        canvas.focus_set()
    # Destory the main menu if it exists
    if canvasMainMenu.winfo_exists():
        canvasMainMenu.destroy()
    # Loads data from file into appropriate variables
    with open("Save1.txt", "r") as f:
        lines = f.readlines()
    for index, line in enumerate(lines):
        if "\n" in line:
            lines[index] = lines[index][:-1]
    programCounter = int(lines[0])
    playerName = lines[1]
    score = int(lines[2])
    playerX = int(lines[3])
    playerY = int(lines[4])
    enemyXs = lines[5]
    enemyYs = lines[6]
    canvasMainMenu.destroy()
    canvas.focus_set()
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    # Creates player
    player = canvas.create_rectangle(
        playerSize, playerSize, playerSize * 4, playerSize * 4
        )
    playerSprite = canvas.create_image(0, 0, image=playerImg, anchor=SW)
    # Creates score text
    scoreText = canvas.create_text(
        800/2, 50, fill="white", font="Arial 20 bold",
        text="SCORE: "+str(score)
        )
    # Binds keys so game is playable
    canvas.bind(controls[0], leftKey)
    canvas.bind(controls[1], rightKey)
    canvas.bind(controls[2], upKey)
    canvas.bind(controls[3], downKey)
    canvas.bind(controls[4], lookLeft)
    canvas.bind(controls[5], lookRight)
    canvas.bind(controls[6], bossKey)
    canvas.bind("<Escape>", escapeKey)
    canvas.unbind("r")
    gameState = "play"
    # Moves player to laooded location
    if playerX > 0 and playerX < 800 and playerY > 0 and playerY < 550:
        canvas.coords(
            player, playerX, playerY, playerX + playerSize * 5,
            playerY - playerSize * 2.5
            )
        canvas.coords(playerSprite, playerX, playerY)
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    # Moves game into main loop
    updateGame()


def startGame():
    """ Sets up all variables so that the game is ready to start, also clears
    the screen if the game has just been reset as leaderboard will be displayed
    otherwise """
    global programCounter
    global playerName
    global playerX
    global playerY
    global player
    global score
    global gameState
    global leaderboardText
    global playerSprite
    global scoreText
    global restartTxt
    programCounter = 0
    # Clears scren of leaderboard
    if gameState == "reset":
        for i in sorted(range(len(leaderboardText)), reverse=True):
            canvas.delete(leaderboardText[i])
            del leaderboardText[i]
        canvas.delete(restartTxt)
    # Clears screen of the main menu
    else:
        canvasMainMenu.destroy()
        canvas.focus_set()
    if canvasMainMenu.winfo_exists():
        canvasMainMenu.destroy()
    canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    playerX = 100
    playerY = 100
    score = 0
    # Creates player collision box and image
    player = canvas.create_rectangle(
        playerSize, playerSize, playerSize * 4, playerSize * 4)
    playerSprite = canvas.create_image(0, 0, image=playerImg, anchor=SW)
    # Creates score text
    scoreText = canvas.create_text(
        800/2, 50, fill="white", font="Arial 20 bold",
        text="SCORE: "+str(score))
    # Binds the control keys
    canvas.bind(controls[0], leftKey)
    canvas.bind(controls[1], rightKey)
    canvas.bind(controls[2], upKey)
    canvas.bind(controls[3], downKey)
    canvas.bind(controls[4], lookLeft)
    canvas.bind(controls[5], lookRight)
    canvas.bind(controls[6], bossKey)
    canvas.bind("<Escape>", escapeKey)
    canvas.focus_set()
    canvas.unbind("r")
    gameState = "play"
    # Moves player to the correct position on screen so it is displayed
    if playerX > 0 and playerX < 800 and playerY > 0 and playerY < 550:
        canvas.coords(
            player, playerX, playerY, playerX + playerSize * 5,
            playerY - playerSize * 2.5)
        canvas.coords(playerSprite, playerX, playerY)
        canvas.place(relx=0.5, rely=0.5, anchor=CENTER)
    # Moves game into the main loop
    updateGame()


def updateGame():
    """ Main loop of the game where all objects on the screen are updated,
    collison is checked, objects are deleted. Is called in a loop until it
    needs to end the game or pause the game. """
    global score
    global gameState
    global programCounter
    programCounter += 1
    removedBullets = []
    removedEnemies = []
    # For loop moving bullets and checking their collision with enemies
    for i in range(len(bullets)):
        (bulletX, bulletY, bulletXX, bulletYY) = canvas.coords(bullets[i])
        # Ensures bullets are still on the screen and moves them
        if bulletX > 0 and bulletX < width:
            canvas.move(bullets[i], bulletDirections[i] * 10, 0)
            canvas.coords(bulletImgs[i], bulletX, bulletY)
            # Checks collision with enemies
            for j in range(len(enemies)):
                if checkCollision(bullets[i], enemies[j]):
                    if i not in removedBullets:
                        removedBullets.append(i)
                    if j not in removedEnemies:
                        # Checks if cheat code is active
                        if 'Multiply' in cheats:
                            score += 900
                        removedEnemies.append(j)
        else:
            removedBullets.append(i)
    # Updates movment of enemies
    pathLength = len(enemyPath)
    for i in range(len(enemies)):
        (enemyX, enemyY, enemyXX, enemyYY) = canvas.coords(enemies[i])
        # If enemy is of type drop and on screen then just moves them down
        if enemyPathPoint[i] == "drop":
            if enemyY < height:
                canvas.move(enemies[i], 0, 1)
                canvas.move(enemiesImgs[i], 0, 1)
            else:
                if i not in removedEnemies:
                    score -= 100
                    removedEnemies.append(i)
        # Checks enemy is still completeing path
        elif enemyPathPoint[i] < pathLength:
            canvas.move(
                enemies[i], (enemyPath[enemyPathPoint[i]][0]),
                enemyPath[enemyPathPoint[i]][1])
            canvas.move(
                enemiesImgs[i], (enemyPath[enemyPathPoint[i]][0]),
                enemyPath[enemyPathPoint[i]][1])
            # If program counter is a multiple of 50 moves enemy onto next
            # stage of path
            if (programCounter % 50) == 0:
                enemyPathPoint[i] += 1
        else:
            # If path is complete or off screen deletes enemy
            if i not in removedEnemies:
                score -= 100
                removedEnemies.append(i)
        if 'Invinsible' not in cheats:
            if checkCollision(enemies[i], player):
                gameState = "end"
    # Increases difficulty by creating enemies based on time
    if len(enemies) < (programCounter/1000):
        createEnemy()
    # Removes bullets in this loop
    for i in sorted(removedBullets, reverse=True):
        deleteBullets(i)
    # Removes bullets in this loop
    for i in sorted(removedEnemies, reverse=True):
        deleteEnemy(i)
    # State machine to break out of loop if user wants to pause or end game
    if gameState == "play":
        window.after(10, updateGame)
    elif gameState == "end":
        endGame()


def endGame():
    """ A function that is called when the player dies or returns to the main
    menu. It will save the users score to a text doc and then create a
    leaderboard based on previous scores saved in that document. """
    global playerName
    global gameState
    global score
    global restartTxt
    # Unbinds the keys and clears the screen as game has ended
    canvas.delete(player)
    canvas.delete(playerSprite)
    canvas.delete(scoreText)
    canvas.unbind(controls[0])
    canvas.unbind(controls[1])
    canvas.unbind(controls[2])
    canvas.unbind(controls[3])
    canvas.unbind(controls[4])
    canvas.unbind(controls[5])
    canvas.unbind("<Escape>")
    # Binds r key so user can restart
    canvas.bind("r", rKey)
    gameState = "reset"
    # Removes all enemies from the screen
    for i in sorted(range(len(enemies)), reverse=True):
        deleteEnemy(i)
        score -= 100
    for i in sorted(range(len(bullets)), reverse=True):
        deleteBullets(i)
    # Opens the leaderboard and puts content in list
    with open("Leaderboard.txt", "r") as f:
        lines = f.readlines()
    # Check to see if file is empty
    if len(lines) > 0:
        lines = lines[0].split(" ")
    # Calculates total number of players and scores
    numLeaders = len(lines)
    # Removes all new line charecters
    for i in range(numLeaders):
        if "\n" in lines[i]:
            lines[i] = lines[i][:-1]
    # Creates a list of length equal to number of previosu players
    leaders = [0] * (int(numLeaders/2))
    # Makes the list 2d and adds players and scores into the list
    for i in range(int(numLeaders/2)):
        leaders[i] = [0] * 2
        leaders[i][0] = lines[i*2]
        leaders[i][1] = int(lines[(i*2) + 1])
    # Adds the current player to the list
    leaders.append([playerName, score])
    # Sorts the list in decending order
    leaders = sorted(leaders, key=lambda x: x[1], reverse=True)
    overflow = []
    # Removes players that are not in the top 10
    for i in range(len(leaders)):
        if i > 9:
            overflow.append(i)
    for i in sorted(overflow, reverse=True):
        del leaders[i]
    global leaderboardText
    leaderboardText = []
    # Writes the leaderboard to screen and leaderboard .txt file
    with open("Leaderboard.txt", "w+") as f:
        strWrite = ""
        leaderboardText.append(canvas.create_text(
            300, 50, fill="white", font="Arial 20 bold", text="LEADERS"))
        leaderboardText.append(canvas.create_text(
            500, 50, fill="white", font="Arial 20 bold", text="SCORE"))
        for i in range(len(leaders)):
            strWrite += (str(leaders[i][0]) + " " + str(leaders[i][1]) + " ")
            leaderboardText.append(canvas.create_text(
                300, 30*i + 100, fill="white", font="Arial 20 bold",
                text=(str(leaders[i][0]))))
            leaderboardText.append(canvas.create_text(
                500, 30*i + 100, fill="white", font="Arial 20 bold",
                text=(str(leaders[i][1]))))
        f.write(strWrite)
    restartTxt = canvas.create_image(400, 500, image=imgRestart, anchor=CENTER)


def pauseGame():
    """ Sets the game state to paused so that the main loop stops running,
    unbinds movment keys and creates buttons to allow saving, exiting,
    resumning and going to the main menu. """
    global canvasPaused
    canvas.unbind("<Escape>")
    gameState = "paused"
    canvas.unbind(controls[0])
    canvas.unbind(controls[1])
    canvas.unbind(controls[2])
    canvas.unbind(controls[3])
    canvas.unbind(controls[4])
    canvas.unbind(controls[5])
    # Creates a new canvas so that it can be easily removed
    canvasPaused = Canvas(
        canvas, width=width, height=height, background='black')
    points = [100, 300, 120, 350, 140, 300, 120, 250]
    points2 = [700, 300, 680, 350, 660, 300, 680, 250]
    rect = canvasPaused.create_polygon(points, fill="red")
    rect2 = canvasPaused.create_polygon(points2, fill="red")
    gameResumeBtn = Button(
        canvasPaused, text="Resume", command=unpauseGame, image=resumeImg)
    mainMenuBtn = Button(
        canvasPaused, text="Main menu", command=mainMenuBtnEvent,
        image=mainMenuImg)
    gameSaveBtn = Button(
        canvasPaused, text="Save", command=saveGame, image=saveImg)
    gameQuitBtn = Button(
        canvasPaused, text="Quit", command=quitGame, image=quitImg)
    canvasPaused.pack()
    gameResumeBtn.place(x=400, y=150, anchor=CENTER)
    mainMenuBtn.place(x=400, y=250, anchor=CENTER)
    gameSaveBtn.place(x=400, y=350, anchor=CENTER)
    gameQuitBtn.place(x=400, y=450, anchor=CENTER)


def mainMenuBtnEvent():
    """ Main menu button on pause page destorys paused canvas and ends the game
    then moves it to the main menu """
    canvasPaused.destroy()
    endGame()
    mainMenu()


def mainMenu():
    """ Main menu function, creates a new canvas with buttons which allow you
    to create a new game, load a game, veiw instructions, change controls and
    quit. Also allows the player to enter/edit their name """
    global playerName
    global gameNameEntry
    global canvasMainMenu
    canvasMainMenu = Canvas(
        canvas, width=width, height=height, background='black')
    points = [100, 300, 120, 350, 140, 300, 120, 250]
    points2 = [700, 300, 680, 350, 660, 300, 680, 250]
    rect = canvasMainMenu.create_polygon(points, fill="red")
    rect2 = canvasMainMenu.create_polygon(points2, fill="red")
    gameNameEntry = Entry(canvasMainMenu)
    gameNameEntry.config(width=20, font="Serif 20 bold")
    gameNameEntry.insert(0, "Guest")
    gameNameEntry.place(x=400, y=200, anchor=CENTER)
    playerName = gameNameEntry.get()
    logo = canvasMainMenu.create_image(400, 100, image=logoImg, anchor=CENTER)
    gameStartBtn = Button(
        canvasMainMenu, text="Start", command=checkName, image=startImg)
    gameInstructionsBtn = Button(
        canvasMainMenu, text="Instructions", command=showInstructions,
        image=instructionsImg)
    gameLoadBtn = Button(
        canvasMainMenu, text="Load", command=loadGame, image=loadImg)
    gameSettingBtn = Button(
        canvasMainMenu, text="Setting", command=createSettingMenu,
        image=settingImg)
    gameQuitBtn = Button(
        canvasMainMenu, text="Quit", command=quitGame, image=quitImg)
    gameStartBtn.place(x=400, y=250, anchor=CENTER)
    gameInstructionsBtn.place(x=400, y=300, anchor=CENTER)
    gameLoadBtn.place(x=400, y=350, anchor=CENTER)
    gameSettingBtn.place(x=400, y=400, anchor=CENTER)
    gameQuitBtn.place(x=400, y=450, anchor=CENTER)
    # If cheats are already active then it will display their notifications
    if "Invinsible" in cheats:
        inv = canvasMainMenu.create_image(
            400, 500, image=invImg, anchor=CENTER
            )
    if "Multiply" in cheats:
        mul = canvasMainMenu.create_image(
            420, 520, image=mulImg, anchor=CENTER
            )
    canvasMainMenu.pack()


def createSettingMenu():
    """ Settings page which allows the player to change controls, will also be
    called when the player hits the change controls button so it just creates
    the page and then configures the pictures based on which set of controls
    are currently in use. """
    global controlType
    global controls
    global canvasSettingMenu
    # Creates canvas and images
    canvasSettingMenu = Canvas(
        canvasMainMenu, width=width, height=height, background='black')
    spriteMoveUp = canvasSettingMenu.create_image(
        100, 100, image=imgMoveUp, anchor=W)
    spriteMoveDown = canvasSettingMenu.create_image(
        100, 150, image=imgMoveDown, anchor=W)
    spriteMoveLeft = canvasSettingMenu.create_image(
        100, 200, image=imgMoveLeft, anchor=W)
    spriteMoveRight = canvasSettingMenu.create_image(
        100, 250, image=imgMoveRight, anchor=W)
    spriteShootRight = canvasSettingMenu.create_image(
        100, 300, image=imgShootRight, anchor=W)
    spriteShootLeft = canvasSettingMenu.create_image(
        100, 350, image=imgShootLeft, anchor=W)
    spriteBossKey = canvasSettingMenu.create_image(
        100, 400, image=imgBossKey, anchor=W)
    spriteMoveLeftControl = canvasSettingMenu.create_image(
        500, 200, image=imgLeft, anchor=W)
    spriteMoveRightControl = canvasSettingMenu.create_image(
        500, 250, image=imgRight, anchor=W)
    spriteMoveDownControl = canvasSettingMenu.create_image(
        500, 150, image=imgDown, anchor=W)
    spriteMoveUpControl = canvasSettingMenu.create_image(
        500, 100, image=imgUp, anchor=W)
    spriteShootLeftControl = canvasSettingMenu.create_image(
        500, 350, image=imgA, anchor=W)
    spriteShootRightControl = canvasSettingMenu.create_image(
        500, 300, image=imgD, anchor=W)
    spriteBossKeyControl = canvasSettingMenu.create_image(
        500, 400, image=imgP, anchor=W)
    # Changes the pictures if the secondary set of instructions are used
    if controlType == 1:
        canvasSettingMenu.itemconfig(spriteMoveLeftControl, image=imgA)
        canvasSettingMenu.itemconfig(spriteMoveRightControl, image=imgD)
        canvasSettingMenu.itemconfig(spriteMoveDownControl, image=imgS)
        canvasSettingMenu.itemconfig(spriteMoveUpControl, image=imgW)
        canvasSettingMenu.itemconfig(spriteShootLeftControl, image=imgLeft)
        canvasSettingMenu.itemconfig(spriteShootRightControl, image=imgRight)
        canvasSettingMenu.itemconfig(spriteBossKeyControl, image=imgB)
    changeControlsBtn = Button(
        canvasSettingMenu, text="Settings", command=changeControls,
        image=imgChangeControls)
    changeControlsBtn.place(x=400, y=450, anchor=CENTER)
    # Creates a back button that will return to the main menu
    backBtn = Button(
        canvasSettingMenu, text="Back", command=closeSettings, image=imgBack)
    backBtn.place(x=0, y=0, anchor=NW)
    canvasSettingMenu.pack()


def closeSettings():
    """ Closes the settings page """
    canvasSettingMenu.destroy()


def changeControls():
    """ When the change controls button is pressed on the settings page is
    pressed this is called. It deletes the previous canvas, swaps the contols
    to the oposite set then recalls the create function to create an updated
    version """
    global controls
    global controlType
    canvasSettingMenu.destroy()
    canvas.unbind(controls[6])
    if controlType == 0:
        controlType = 1
        controls = ["a", "d", "w", "s", "<Left>", "<Right>", "b"]
    else:
        controlType = 0
        controls = ["<Left>", "<Right>", "<Up>", "<Down>", "a", "d", "p"]
    # Rebinds the boss key as it needs to always be able to be used
    canvas.bind(controls[6], showBossKey)
    createSettingMenu()


def showInstructions():
    """ Simply creates a new canvas and displays images to tell the player what
    to do and tell them about cheat codes also inculdes a back button """
    global canvasInstructions
    canvasInstructions = Canvas(
        canvasMainMenu, width=width, height=height, background='black')
    spriteText1 = canvasInstructions.create_image(
        400, 150, image=text1Img, anchor=CENTER)
    spriteText2 = canvasInstructions.create_image(
        400, 300, image=text2Img, anchor=CENTER)
    spriteText3 = canvasInstructions.create_image(
        400, 425, image=text3Img, anchor=CENTER)
    backInstructionBtn = Button(
        canvasInstructions, text="Back", command=closeInstructions,
        image=imgBack)
    backInstructionBtn.place(x=0, y=0, anchor=NW)
    canvasInstructions.pack()


def closeInstructions():
    """ Removes the instruction window """
    canvasInstructions.destroy()


def showBossKey(event):
    """ Unbinds all keys and sets the game into a pause state then creates a
    new canvas and draws the boss key image. If it is already in the boss key
    state then it will unpause the game rebind all keys and destroy the canvas
    (and image) """
    global canvasPaused
    global bossKey
    global canvasBoss
    global gameState
    if not bossKey:
        if gameState == "play":
            gameState = "paused"
            canvas.unbind(controls[0])
            canvas.unbind(controls[1])
            canvas.unbind(controls[2])
            canvas.unbind(controls[3])
            canvas.unbind(controls[4])
            canvas.unbind(controls[5])
        w, h = window.winfo_screenwidth(), window.winfo_screenheight()
        canvasBoss = Canvas(bkCanvas, width=w, height=h, background='black')
        webpage = canvasBoss.create_image(0, 0, image=bossKeyImg, anchor=NW)
        canvasBoss.pack()
        bossKey = True
    else:
        if gameState == "paused":
            gameState = "play"
            canvas.bind(controls[0], leftKey)
            canvas.bind(controls[1], rightKey)
            canvas.bind(controls[2], upKey)
            canvas.bind(controls[3], downKey)
            canvas.bind(controls[4], lookLeft)
            canvas.bind(controls[5], lookRight)
            canvas.bind("<Escape>", escapeKey)
        canvasBoss.destroy()
        bossKey = False


def unpauseGame():
    """ Function that is called when the resume game button is pressed, it will
    first remove the paused menu, then create a text widget on the screen that
    counds down from 3 to 1 and then rebinds all keys and resumes the game """
    global gameState
    canvas.unbind("<Escape>")
    canvasPaused.destroy()
    waitTxt = canvas.create_text(
        400, 400, text="3", font="Arial 50 bold", fill="white")
    canvas.update()
    time.sleep(1)
    canvas.itemconfigure(waitTxt, text="2")
    canvas.update()
    time.sleep(1)
    canvas.itemconfigure(waitTxt, text="1")
    canvas.update()
    time.sleep(1)
    canvas.delete(waitTxt)
    gameState = "play"
    canvas.bind(controls[0], leftKey)
    canvas.bind(controls[1], rightKey)
    canvas.bind(controls[2], upKey)
    canvas.bind(controls[3], downKey)
    canvas.bind(controls[4], lookLeft)
    canvas.bind(controls[5], lookRight)
    canvas.bind("<Escape>", escapeKey)
    updateGame()


def saveGame():
    """ Saves the current variables into a files so that they can be loaded
    later """
    global programCounter
    global playerName
    global score
    global playerX
    global playerY
    with open("Save1.txt", "w+") as f:
        f.write(str(programCounter) + "\n")
        f.write(str(playerName) + "\n")
        f.write(str(score) + "\n")
        f.write(str(playerX) + "\n")
        f.write(str(playerY) + "\n")
        enemyXs = ""
        enemyYs = ""
        for i in range(len(enemies)):
            enemyX, enemyY, t, d = canvas.coords(enemies[i])
            enemyXs += (str(enemyX) + " ")
            enemyYs += (str(enemyY) + " ")
        f.write(enemyXs + "\n")
        f.write(enemyYs)


def quitGame():
    """ Closes the game """
    window.destroy()


def checkCollision(a, b):
    """ Takes two objects as arguments and returns True if they are colliding
    and false if they are not """
    (aX, aY, aXX, aYY) = canvas.coords(a)
    (bX, bY, bXX, bYY) = canvas.coords(b)
    if aX < bXX and aXX > bX and aY < bYY and aYY > bY:
        return True
    return False


def deleteBullets(i):
    """ Removes bullets collision box and its image to 'detele' it from the
    screen """
    canvas.delete(bullets[i])
    canvas.delete(bulletImgs[i])
    del bulletImgs[i]
    del bullets[i]
    del bulletDirections[i]


def setWindowDimensions(w, h):
    """ Creates the main window of the game based on the arguments of the width
    and height that it is passed """
    window = Tk()
    window.title("Side Arms")
    ws = window.winfo_screenwidth()
    hs = window.winfo_screenheight()
    x = (ws/2) - (w/2)
    y = (hs/2) - (w/2)
    window.geometry('%dx%d+%d+%d' % (w, h, x, y))
    return window


window = setWindowDimensions(width, height)
window.configure(background='black')
window.minsize(800, 550)
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()
playerImg = PhotoImage(file='sprites/player.png')
playerImgFlipped = PhotoImage(file='sprites/playerFlipped.png')
bkground = PhotoImage(file='sprites/game.png')
bulletImg = PhotoImage(file='sprites/bullet1.png')
enemiesImg = PhotoImage(file='sprites/enemy-medium1.png')
enemiesDropImg = PhotoImage(file='sprites/enemy-big.png')
# Credit:
# https://i-love-png.com/machine-clipart-arcade-cabinet-672639-3364845.html
# Personal use only

# Canvas variables
bkCanvas = Label(
    window, width=screenWidth, height=screenHeight, bg='black', image=bkground)
bkCanvas.place(relx=0.5, rely=0.5, anchor=CENTER)
canvas = Canvas(bkCanvas, width=width, height=height, background='black')
canvas.focus_set()

# Player variables
playerSize = 15
playerFacing = 1


# Bullet variables
canShoot = 1
bullets = []
bulletDirections = []
bulletImgs = []


# Control and game variables
canvasPaused = 0
programCounter = 0
gameState = "start"
score = 0
cheats = []
controlType = 0
controls = ["<Left>", "<Right>", "<Up>", "<Down>", "a", "d", "p"]
spriteMoveLeftControl = 0
spriteMoveRightControl = 0
spriteMoveDownControl = 0
spriteMoveUpControl = 0
spriteShootLeftControl = 0
spriteShootRightControl = 0
canvasSettingMenu = 0


# Enemy variables
enemies = []
enemiesImgs = []
# Creats a list of relative positions for the enmey to follow.
enemyPath = [
    [-4, 0], [-4, 0], [-4, 0],
    [-4, 2], [4, 2], [4, 0],
    [4, 0], [4, 0]
]
enemyPathPoint = []


canvas.place(relx=0.5, rely=0.5, anchor=CENTER)


# Boss key variables
bossKey = False
bossKeyImg = PhotoImage(file='sprites/bossKey.PNG')
# Credit: Google
logoImg = PhotoImage(file='sprites/Logo.png')
# Self created
# Inspiration: https://fr.wikipedia.org/wiki/Hyper_Dyne_Side_Arms
# Main menus Imgs
resumeImg = PhotoImage(file='sprites/resume_game.PNG')
saveImg = PhotoImage(file='sprites/save_game.PNG')
invImg = PhotoImage(file='sprites/Invinsible.PNG')
mulImg = PhotoImage(file='sprites/mul.PNG')
startImg = PhotoImage(file='sprites/start_game.PNG')
loadImg = PhotoImage(file='sprites/load_game.PNG')
quitImg = PhotoImage(file='sprites/quit_game.PNG')
settingImg = PhotoImage(file='sprites/settings.PNG')
mainMenuImg = PhotoImage(file='sprites/mainMenu.PNG')
instructionsImg = PhotoImage(file='sprites/instructions.PNG')
nameErrorImg = PhotoImage(file='sprites/names.PNG')
# Instructions Imgs
text1Img = PhotoImage(file='sprites/text1.PNG')
text2Img = PhotoImage(file='sprites/text2.PNG')
text3Img = PhotoImage(file='sprites/text3.PNG')
# Settings Imgs
imgMoveDown = PhotoImage(file='sprites/keys/moveDown.PNG')
imgMoveUp = PhotoImage(file='sprites/keys/moveUp.PNG')
imgMoveLeft = PhotoImage(file='sprites/keys/moveLeft.PNG')
imgMoveRight = PhotoImage(file='sprites/keys/moveRight.PNG')
imgShootLeft = PhotoImage(file='sprites/keys/shootLeft.PNG')
imgShootRight = PhotoImage(file='sprites/keys/shootRight.PNG')
imgBossKey = PhotoImage(file='sprites/keys/bossKey.PNG')
imgChangeControls = PhotoImage(file='sprites/keys/changeControls.PNG')
# Control Imgs
imgLeft = PhotoImage(file='sprites/keys/left.PNG')
imgRight = PhotoImage(file='sprites/keys/right.PNG')
imgUp = PhotoImage(file='sprites/keys/up.PNG')
imgDown = PhotoImage(file='sprites/keys/down.PNG')
imgA = PhotoImage(file='sprites/keys/A.PNG')
imgD = PhotoImage(file='sprites/keys/D.PNG')
imgW = PhotoImage(file='sprites/keys/w.PNG')
imgS = PhotoImage(file='sprites/keys/s.PNG')
imgP = PhotoImage(file='sprites/keys/P.PNG')
imgB = PhotoImage(file='sprites/keys/B.PNG')
imgBack = PhotoImage(file='sprites/keys/back.PNG')
# Leaderboard imgs
imgRestart = PhotoImage(file='sprites/restart.PNG')
# Credit: http://arcade.photonstorm.com/
mainMenu()
canvas.bind("p", showBossKey)


window.mainloop()
