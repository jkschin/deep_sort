import cv2
import os
import numpy as np

confidences = [3, 5, 8, 9]
videos_dir = "/home/jkschin/code/deep_sort/output"
mot_dir = "/home/jkschin/code/deep_sort/MOT16/test"
for sequence in os.listdir(mot_dir):
    caps = []
    for confidence in confidences:
        video_file = "%s_%d.avi" %(sequence, confidence)
        print (videos_dir, video_file)
        cap = cv2.VideoCapture(os.path.join(videos_dir, video_file))
        caps.append(cap)
    w = int(caps[0].get(3))
    h = int(caps[0].get(4))
    fps = caps[0].get(5)
    output_shape = (int(w*2), int(h*2))
    fourcc_string = "MJPG"
    fourcc = cv2.VideoWriter_fourcc(*fourcc_string)
    output_filename = "%s.avi" %(sequence)
    video_writer = cv2.VideoWriter(
        output_filename, fourcc, fps, output_shape)
    output_image = np.zeros((output_shape[1], output_shape[0], 3))
    print ("Width: %d, Height: %d, FPS:%d" %(w, h, fps))
    print ("Output Shape: ", output_shape)
    while True:
        c = 0
        for i in range(0, w+1, w):
            for j in range(0, h+1, h):
                ret, img = caps[c].read()
                img = cv2.putText(img, "Confidence: 0.%d" %(confidences[c]),
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 4)
                # print(img.shape)
                # print(j, j+h, i, i+w)
                if ret == False:
                    break
                output_image[j:j+h, i:i+w, :] = img
                c += 1
        if ret == False:
            break
        video_writer.write(np.uint8(output_image))
    video_writer.release()
    for cap in caps:
        cap.release()

