import mediapipe as mp #one person detection
import cv2
import tensorflow as tf
import tensorflow_hub as hub
from matplotlib import pyplot as plt
import numpy as np




def recognise_one_person():
    mp_draw = mp.solutions.drawing_utils  # drawing utilities
    mp_holistic = mp.solutions.holistic  # our holistic module
    webcam = cv2.VideoCapture(0)
    with mp_holistic.Holistic(min_detection_confidence=0.6, min_tracking_confidence=0.6) as holistic:
        while webcam.isOpened:
            ret, frame = webcam.read()

            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            result = holistic.process(img)

            img = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            mp_draw.draw_landmarks(img, result.pose_landmarks, mp_holistic.POSE_CONNECTIONS) #allbody
            #print(mp_holistic.POSE_CONNECTIONS)

            cv2.imshow('Webcam Window', img)

            if cv2.waitKey(1) and 0xFF == ord('q'):
                break

    webcam.release()
    cv2.destroyWindow('Webcam Window')

# Function to loop through each person detected and render
def loop_through_people(frame, keypoints_with_scores, edges, confidence_threshold):
    for person in keypoints_with_scores:
        draw_connections(frame, person, edges, confidence_threshold)
        draw_keypoints(frame, person, confidence_threshold)

def defense_move1(person):
    #6: right shoulder, 8: right elbow, 10: right wrist && 0= y, 1 = x
    if person[6][0]<person[8][0] and person[8][0]>person[10][0]:
        if person[6][1]< person[8][1] and person[8][1]<person[10][1]:
            return True
    return False


def recognise_mult_people(): #https://github.com/nicknochnack/MultiPoseMovenetLightning/blob/main/MultiPose%20MoveNet%20Tutorial.ipynb
    model = hub.load('https://tfhub.dev/google/movenet/multipose/lightning/1')
    movenet = model.signatures['serving_default']

    webcam = cv2.VideoCapture(0)
    while webcam.isOpened():
        ret, frame = webcam.read()
        image = frame.copy()
        image = tf.expand_dims(image, axis=0)
        # Resize and pad the image to keep the aspect ratio and fit the expected size.
        image = tf.cast(tf.image.resize_with_pad(image, 192, 192), dtype=tf.int32)
        results = movenet(image)
        keypoints_with_scores = results['output_0'].numpy()[:, :, :51].reshape((6, 17, 3))
        #keypoints_with_scores[Ø] would be first person 1-> would be second person etc
        #loop_through_people(frame, keypoints_with_scores, EDGES, 0.1)#not needed just draws
        cv2.imshow('Multi-person pose', frame)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
    webcam.release()
    cv2.destroyAllWindows()


def draw_keypoints(frame, keypoints, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

    for kp in shaped:
        ky, kx, kp_conf = kp
        if kp_conf > confidence_threshold:
            cv2.circle(frame, (int(kx), int(ky)), 6, (0, 255, 0), -1)


EDGES = {
    (0, 1): 'm',
    (0, 2): 'c',
    (1, 3): 'm',
    (2, 4): 'c',
    (0, 5): 'm',
    (0, 6): 'c',
    (5, 7): 'm',
    (7, 9): 'm',
    (6, 8): 'c',
    (8, 10): 'c',
    (5, 6): 'y',
    (5, 11): 'm',
    (6, 12): 'c',
    (11, 12): 'y',
    (11, 13): 'm',
    (13, 15): 'm',
    (12, 14): 'c',
    (14, 16): 'c'
}


def draw_connections(frame, keypoints, edges, confidence_threshold):
    y, x, c = frame.shape
    shaped = np.squeeze(np.multiply(keypoints, [y, x, 1]))

    for edge, color in edges.items():
        p1, p2 = edge
        y1, x1, c1 = shaped[p1]
        y2, x2, c2 = shaped[p2]

        if (c1 > confidence_threshold) & (c2 > confidence_threshold):
            cv2.line(frame, (int(x1), int(y1)), (int(x2), int(y2)), (0, 0, 255), 4)



if __name__ == "__main__":
    recognise_mult_people()