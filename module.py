import cv2
import mediapipe as mp
import time


class searchHands():
    def __init__(self, mode=False, max=1, minConf=0.6, minTrack=0.7):
        self.mode = mode
        self.max = max
        self.minConf = minConf
        self.minTrack = minTrack

        self.hand = mp.solutions.hands
        self.hands = self.hand.Hands(self.mode, self.max,
                                     self.minConf, self.minTrack)
        self.draw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        imgRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.result = self.hands.process(imgRGB)

        if self.result.multi_hand_landmarks:
            for Lms in self.result.multi_hand_landmarks:
                if draw:
                    self.draw.draw_landmarks(frame, Lms, self.hand.HAND_CONNECTIONS)
        return frame

    def pos(self, frame, handNum=0, draw=True):

        lmList = []
        if self.result.multi_hand_landmarks:
            hand = self.result.multi_hand_landmarks[handNum]

            for id, lm in enumerate(hand.landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append([cx, cy])
                if draw:
                    cv2.circle(frame, (cx, cy), 3, (255, 0, 255), cv2.FILLED)
        return lmList


def main():
    vid = cv2.VideoCapture(0)
    detect = searchHands()
    while True:
        ret, frame = vid.read()
        detect.findHands(frame)
        lmList = detect.pos(frame)
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("Exiting.")
            break

    vid.release()
    # Destroy all the windows
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
