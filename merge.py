import pyautogui
import time
from pynput import keyboard, mouse
import math
import sys

# List of image paths to find and move
images_to_find1 = [
    r"C:\PERSONAL\python\images\cow1.png",
    r"C:\PERSONAL\python\images\chicken1.png",
    r"C:\PERSONAL\python\images\goat1.png",
    r"C:\PERSONAL\python\images\pig1.png",
    r"C:\PERSONAL\python\images\weed1.png",
    r"C:\PERSONAL\python\images\eggplant1.png",
    r"C:\PERSONAL\python\images\carrot1.png",
    r"C:\PERSONAL\python\images\sugar1.png",
    r"C:\PERSONAL\python\images\sun1.png",
]

images_to_find2 = [
    r"C:\PERSONAL\python\images\cow2.png",
    r"C:\PERSONAL\python\images\chicken2.png",
    r"C:\PERSONAL\python\images\goat2.png",
    r"C:\PERSONAL\python\images\pig2.png",
    r"C:\PERSONAL\python\images\weed2.png",
    r"C:\PERSONAL\python\images\eggplant2.png",
    r"C:\PERSONAL\python\images\carrot2.png",
    r"C:\PERSONAL\python\images\sugar2.png",
    r"C:\PERSONAL\python\images\sun2.png",
]

images_to_find3 = [
    r"C:\PERSONAL\python\images\cow3.png",
    r"C:\PERSONAL\python\images\chicken3.png",
    r"C:\PERSONAL\python\images\goat3.png",
    r"C:\PERSONAL\python\images\pig3.png",
    r"C:\PERSONAL\python\images\weed3.png",
    r"C:\PERSONAL\python\images\eggplant3.png",
    r"C:\PERSONAL\python\images\carrot3.png",
    r"C:\PERSONAL\python\images\sugar3.png",
]

# Default target positions for the first 5 occurrences of each image
target_positions5 = [
    (1485, 663), #2
    (1448, 634), #3
    (1441, 679), #1
    (1403, 654), #4
    (1403, 654)  #4
]

target_positions3 = [
    (1441, 679), #1
    (1403, 654), #4
    (1403, 654)  #4
]

# Confidence level for image recognition
CONFIDENCE_LEVEL = 0.7  # Adjust if needed
MIN_DISTANCE = 30  # Minimum distance between detected images to be considered separate

# Global flag to indicate coordinate setup mode
setup_mode = False
click_positions = []

def find_and_drag(image_path, total):
    """Find up to 5 distinct occurrences of an image and move them to predefined locations"""
    try:
        all_locations = list(pyautogui.locateAllOnScreen(image_path, confidence=CONFIDENCE_LEVEL))

        detected_positions = []
        filtered_locations = []

        # Filter out duplicate or very close detections
        for loc in all_locations:
            x, y, largura, altura = loc
            center_x = x + largura // 2
            center_y = y + altura // 2
            
            if is_far_enough((center_x, center_y), detected_positions):
                detected_positions.append((center_x, center_y))
                filtered_locations.append(loc)

        print(f"Encontradas {len(filtered_locations)} ocorrências distintas de {image_path}.")

        if len(filtered_locations) < total:
            print("Menos de 5 imagens encontradas, não movendo.")
            return

        if(total == 5):
            for i, location in enumerate(filtered_locations[:5]):
                x, y, largura, altura = location
                center_x = x + largura // 2
                center_y = y + altura // 2
                target_x, target_y = target_positions5[i]  # Get the corresponding target position

                print(f"Movendo {image_path} ({i+1}) de ({center_x}, {center_y}) para ({target_x}, {target_y})")

                pyautogui.moveTo(center_x, center_y, duration=0.1)  # Move to image
                pyautogui.mouseDown()  # Click and hold
                time.sleep(0.1)  # Small pause before dragging
                pyautogui.moveTo(target_x, target_y, duration=0.1)  # Drag smoothly
                pyautogui.mouseUp()  # Release the click

        elif(total == 3):
            for i, location in enumerate(filtered_locations[:3]):
                x, y, largura, altura = location
                center_x = x + largura // 2
                center_y = y + altura // 2
                target_x, target_y = target_positions3[i]
                print(f"Movendo {image_path} ({i+1}) de ({center_x}, {center_y}) para ({target_x}, {target_y})")

                pyautogui.moveTo(center_x, center_y, duration=0.1)  # Move to image
                pyautogui.mouseDown()  # Click and hold
                time.sleep(0.1)  # Small pause before dragging
                pyautogui.moveTo(target_x, target_y, duration=0.1)  # Drag smoothly
                pyautogui.mouseUp()  # Release the click
            
    except Exception as e:
        print(f"Erro inesperado ao processar {image_path}: {e}")

def is_far_enough(new_pos, detected_positions):
    """Check if a detected position is far enough from already stored positions"""
    for pos in detected_positions:
        distance = math.dist(new_pos, pos)  # Euclidean distance
        if distance < MIN_DISTANCE:
            return False  # Too close to another detected position
    return True

def on_click3(x, y, button, pressed):
    """Capture mouse clicks for setting new target positions"""
    global setup_mode, click_positions, target_positions3

    if setup_mode and pressed:
        click_positions.append((x, y))
        print(f"Nova posição capturada: ({x}, {y})")

        # If 5 positions are captured, update target_positions3 and exit setup mode
        if len(click_positions) == 3:
            target_positions3 = click_positions[:3]  # Update global target positions
            setup_mode = False
            print(f"Novas posições de destino definidas: {target_positions3}")
            return False  # Stop mouse listener

def on_click5(x, y, button, pressed):
    """Capture mouse clicks for setting new target positions"""
    global setup_mode, click_positions, target_positions5

    if setup_mode and pressed:
        click_positions.append((x, y))
        print(f"Nova posição capturada: ({x}, {y})")

        # If 5 positions are captured, update target_positions5 and exit setup mode
        if len(click_positions) == 5:
            target_positions5 = click_positions[:5]  # Update global target positions
            setup_mode = False
            print(f"Novas posições de destino definidas: {target_positions5}")
            return False  # Stop mouse listener

def print_menu():
    """Print the menu options"""
    print("\nPressione a tecla correspondente para executar a ação:")
    print("1 - Mover 3 de nível 1")
    print("2 - Mover 5 de nível 1")
    print("3 - Mover 3 de nível 2")
    print("4 - Mover 5 de nível 2")
    print("5 - Mover 5 de nível 3")
    print("6 - Mover 5 de nível 1 e 2")
    print("a - Configurar nova posição para mover 3 imagens")
    print("s - Configurar nova posição para mover 5 imagens")
    print("p - Sair")  # Clarify exit key

def on_press(key):
    """Handle key presses and execute actions"""
    if hasattr(key, 'char'):
        if key.char:
            key_lower = key.char.lower()

            if key_lower == '1':
                print("Merging 3 of level 1...")
                for image in images_to_find1:
                    find_and_drag(image, 3)

            elif key_lower == '2':
                print("Merging 5 of level 1...")
                for image in images_to_find1:
                    find_and_drag(image, 5)

            elif key_lower == '3':
                print("Merging 3 of level 2...")
                for image in images_to_find2:
                    find_and_drag(image, 3)

            elif key_lower == '4':
                print("Merging 5 of level 2...")
                for image in images_to_find2:
                    find_and_drag(image, 5)

            elif key_lower == '5':
                print("Merging 5 of level 3...")
                for image in images_to_find3:
                    find_and_drag(image, 5)

            elif key_lower == '6':
                print("Merging 5 of level 1...")
                for image in images_to_find1:
                    find_and_drag(image, 5)
                print("Merging 5 of level 2...")
                for image in images_to_find2:
                    find_and_drag(image, 5)

            elif key_lower == 'a':
                print("Merge 3 config, click 3 spots.")
                setup_mode = True
                click_positions = []
                with mouse.Listener(on_click=on_click3) as mouse_listener:
                    mouse_listener.join()

            elif key_lower == 's':
                print("Merge 5 config, click 5 spots.")
                setup_mode = True
                click_positions = []
                with mouse.Listener(on_click=on_click5) as mouse_listener:
                    mouse_listener.join()

            elif key_lower == 'p':  # Exit option
                print("Exiting...")
                return False  # Return False to stop the listener and exit the loop

    return True  # Continue listening for other key presses

# Main loop
def main():
    print_menu()
    with keyboard.Listener(on_press=on_press) as listener:
        listener.join()  # Block until listener is stopped

if __name__ == "__main__":
    main()