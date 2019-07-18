import numpy as np
from PIL import ImageGrab, Image
import cv2
import time
import math
import keyboard
from directKeys import click, queryMousePosition, PressKey, ReleaseKey, SPACE, moveMouseTo
from threading import Thread
import webbrowser
import livestreamer
from livestreamer.plugins import twitch
import livestreamer_cli
from livestreamer import Livestreamer


from_stream = True
client_id = ""
stream_url = ""
# Doesn't need to be set unless you want to read from local screen
game_coords = [283,235,1548,948]

def authenticate_twitch_oauth():
    # From livestream code - didn't feel like import it.
    """Opens a web browser to allow the user to grant Livestreamer
       access to their Twitch account."""

    client_id = "ewvlchtxgqq88ru9gmfp1gmyt6h2b93"
    redirect_uri = "http://livestreamer.tanuki.se/en/develop/twitch_oauth.html"
    url = ("https://api.twitch.tv/kraken/oauth2/authorize/"
           "?response_type=token&client_id={0}&redirect_uri="
           "{1}&scope=user_read+user_subscriptions").format(client_id, redirect_uri)

    try:
        if not webbrowser.open_new_tab(url):
            raise webbrowser.Error
    except webbrowser.Error:
        print("Unable to open a web browser, try accessing this URL "
                     "manually instead:\n{0}".format(url))

if from_stream:

    while client_id == "":
        authenticate_twitch_oauth()
        print("Opening browser, copy the client_id from the url and paste it in...")
        client_id = input("Client ID: ")
    while stream_url == "":
        stream_url = input("Streamer URL: ")

    session = Livestreamer()
    session.set_option("http-headers", {"client-id":client_id})
    session.set_option("hls-live-edge", 1)
    #streams = session.streams("https://www.twitch.tv/xyz")
    streams = session.streams(stream_url)

    if len(streams) == 0:
        print("No streams found on %s" % stream_url)
        exit()

    if "best" in streams:
        stream = streams["best"]
    else:
        for each in streams.keys():
            print(each)
        stream = input("Choose a stream from above: ")
        stream = streams[stream]

    print("Capturing Best Stream...")
    cap = cv2.VideoCapture(stream.url)
elif game_coords:
    pass


#
# print("Waiting for mouse over screen")
# while True:
#     #break
#     mouse_pos = queryMousePosition()
#     #print(mouse_pos.x, mouse_pos.y)
#     if mouse_pos.x < 1920:
#        break

def im_show(img, name, time, x=2000, y=100):
    cv2.namedWindow(name)
    cv2.moveWindow(name, x, y)
    cv2.imshow(name, img)
    cv2.waitKey(time)

def create_death_counter_image():
    global rips, start
    while True:

        # Create a black image
        img = np.zeros((55,350,3), np.uint8)

        # Write some Text
        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (10,30)
        fontScale              = 1
        fontColor              = (255,255,255)
        lineType               = 2

        cv2.putText(img,'Death Counter: %s' % rips,
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)


        font                   = cv2.FONT_HERSHEY_SIMPLEX
        bottomLeftCornerOfText = (80,50)
        fontScale              = .3
        fontColor              = (70,70,70)
        lineType               = 1

        cv2.putText(img,'SMM Death Counter v0.1 By Nebriv',
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            lineType)

        #Display the image
        im_show(img, "Death Counter", 1, x=100)

# def create_death_counter_image():
#     global rips, start
#     longest_time_since_death = None
#     while True:
#         time_since_last_death = round((time.time() - start),1)
#         if longest_time_since_death:
#             if time_since_last_death > longest_time_since_death:
#                 longest_time_since_death = time_since_last_death
#         else:
#             longest_time_since_death = time_since_last_death
#
#         if rips > 0:
#             longest_time_alive = longest_time_since_death
#         else:
#             longest_time_alive = "N/A"
#
#         # Create a black image
#         img = np.zeros((60,380,3), np.uint8)
#
#         # Write some Text
#         font                   = cv2.FONT_HERSHEY_SIMPLEX
#         bottomLeftCornerOfText = (10,20)
#         fontScale              = .8
#         fontColor              = (255,255,255)
#         lineType               = 2
#
#         cv2.putText(img,'Death Counter: %s' % rips,
#             bottomLeftCornerOfText,
#             font,
#             fontScale,
#             fontColor,
#             lineType)
#
#         # Write some Text
#         font                   = cv2.FONT_HERSHEY_SIMPLEX
#         bottomLeftCornerOfText = (10,40)
#         fontScale              = .5
#         fontColor              = (255,255,255)
#         lineType               = 1
#
#         cv2.putText(img,'Time since last death: %s seconds' % time_since_last_death,
#             bottomLeftCornerOfText,
#             font,
#             fontScale,
#             fontColor,
#             lineType)
#
#         # Write some Text
#         font                   = cv2.FONT_HERSHEY_SIMPLEX
#         bottomLeftCornerOfText = (12,55)
#         fontScale              = .5
#         fontColor              = (255,255,255)
#         lineType               = 1
#
#         cv2.putText(img,'   Longest time alive: %s seconds' % longest_time_alive,
#             bottomLeftCornerOfText,
#             font,
#             fontScale,
#             fontColor,
#             lineType)
#
#         #Display the image
#         im_show(img, "Death Counter", 1, x=100)

template = cv2.imread("death.png", cv2.IMREAD_GRAYSCALE)
w, h = template.shape[::-1]

template2 = cv2.imread("death2.png", cv2.IMREAD_GRAYSCALE)
w2, h2 = template.shape[::-1]

def detect_death(frame):
    detection = False
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    res = cv2.matchTemplate(gray_frame, template, cv2.TM_CCOEFF_NORMED)
    res2 = cv2.matchTemplate(gray_frame, template2, cv2.TM_CCOEFF_NORMED)


    threshold = 0.9

    loc = np.where(res >= threshold)
    loc2 = np.where(res2 >= threshold)
    for pt in zip(*loc[::-1]):
        detection = True
        cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)

    if len(loc[0]) > 0 and len(loc2[0] > 0):
        for pt in zip(*loc[::-1]):
            detection = True
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
    elif len(loc[0] > 0):
        for pt in zip(*loc[::-1]):
            detection = True
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)
    elif len(loc2[0] > 0):
        for pt in zip(*loc2[::-1]):
            detection = True
            cv2.rectangle(frame, pt, (pt[0] + w, pt[1] + h), (0, 255, 0), 3)

    im_show(frame, "Death Detector", 1, x=2500)
    if detection:
        return True
    else:
        return False

start = time.time()
rips = 0
thread = Thread(target=create_death_counter_image, args=())
thread.setDaemon(True)
thread.start()

counter = 0
restart = 3000


# Read Stream
while True:
    succ, frame = cap.read()
    if succ:
        counter += 1
        if counter < 60:
            #im_show(frame, "Test", 1)
            # Detect deaths
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            death = detect_death(frame)

            if death:
                start = time.time()
                rips += 1
                print("RIPs: %s" % rips)
                black = False
                print("waiting for black screen")
                while not black:
                    success, frame = cap.read()
                    if success:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        if np.any(frame[100, 100] == 0) and np.any(frame[50, 50] == 0) and np.any(frame[50, 150] == 0):
                            black = True
                    else:
                        break


                    # if color == 0:
                    #     black = True

                print("Waiting for game screen")
                while black:
                    success, frame = cap.read()
                    if success:
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

                        if np.any(frame[100, 100] != 0) and np.any(frame[50, 50] != 0) and np.any(frame[50, 150] != 0):
                            black = False
                    else:
                        break
                print("Continuing")
        else:
            print("Catching up")
            counter = 0
            cap.read()


    break
cap.release()


# Read image from screen
while True:

    mouse_pos = queryMousePosition()

    # Make sure the screen position is Left Screen (less than x = 1920)
    if mouse_pos.x < 1920:

        # Capture Screen Grab
        img = ImageGrab.grab(bbox=game_coords)
        screen = np.array(img)
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        death = detect_death(screen)

        if death:
            start = time.time()
            rips += 1
            print("RIPs: %s" % rips)
            black = False
            time.sleep(.1)
            print("waiting for black screen")
            while not black:
                img = ImageGrab.grab(bbox=game_coords)
                color = img.getpixel((50,50))
                color2 = img.getpixel((100,100))
                color3 = img.getpixel((150,150))
                if color == (0,0,0) and color2 == (0,0,0) and color3 == (0,0,0):
                    black = True

            print("Waiting for game screen")
            while black:
                img = ImageGrab.grab(bbox=game_coords)
                color = img.getpixel((50,50))
                color2 = img.getpixel((100,100))
                color3 = img.getpixel((150,150))
                if color != (0,0,0) and color2 != (0,0,0) and color3 != (0,0,0):
                    black = False
            print("Continuing")
            time.sleep(.2)