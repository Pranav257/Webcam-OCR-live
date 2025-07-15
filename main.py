import cv2
import pygame
import numpy as np
from PIL import Image, ImageDraw
import os
from pix2text import Pix2Text


def initialize_camera():
    for i in range(5):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            print(f"Webcam {i} opened successfully.")
            return cap
    print("Error: Could not open any webcam.")
    return None


def save_frame(image, folder, frame_number):
    if not os.path.exists(folder):
        os.makedirs(folder)
    file_path = os.path.join(folder, f"frame_{frame_number}.png")
    image.save(file_path)


def main():
    pygame.init()
    screen = pygame.display.set_mode((640, 480))
    pygame.display.set_caption("Webcam Live Feed with Text Extraction")
    cap = initialize_camera()
    if not cap:
        return

    p2t = Pix2Text.from_config()
    frame_counter = 0

    save_folder_path = r'C:\Users\prana\Desktop\TechnoGems\Ocr\pix\Frames'

    running = True
    while running:
        ret, frame = cap.read()
        if not ret:
            print("Error: Could not read frame.")
            break

        frame = cv2.flip(frame, 1)
        img_pil = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        recognition_output = p2t.recognize(img_pil, file_type='text_formula', return_text=True, return_boxes=True)
        print("Recognition Output:", recognition_output)

        if isinstance(recognition_output, tuple) and len(recognition_output) == 2:
            text_output, boxes = recognition_output
            if boxes:
                draw = ImageDraw.Draw(img_pil)
                for box in boxes:
                    if isinstance(box, dict) and all(key in box for key in ['left', 'top', 'right', 'bottom']):
                        draw.rectangle([box['left'], box['top'], box['right'], box['bottom']], outline="red")
                    else:
                        print("Box format is incorrect:", box)
        else:
            print("Unexpected format of recognition output.")

        save_frame(img_pil, save_folder_path, frame_counter)
        frame_counter += 1

        frame_rgb = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
        frame_rgb = np.rot90(frame_rgb)
        surface = pygame.surfarray.make_surface(frame_rgb)
        screen.blit(surface, (0, 0))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                running = False

    cap.release()
    pygame.quit()
    print("Webcam released and Pygame closed.")


if __name__ == "__main__":
    main()
