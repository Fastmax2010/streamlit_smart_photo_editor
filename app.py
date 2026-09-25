# Лескін Максим
import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="Smart Photo Editor", layout="wide")
st.title("Smart Photo Editor")
st.write("Завантажте будь-яке фото і застосуйте на ньому фільтри!")

uploaded_file = st.file_uploader("Оберіть потрібне зображення...", type=["png", "jpg", "jpeg"])

filter_option = st.sidebar.selectbox("Оберіть потрібний ефект:", ["Оригінал",
                                                                    "Віддзеркалення",
                                                                    "Налаштування яскравості",
                                                                    "Налаштування контрасту",
                                                                    "Колірний сплеск"])

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")

    img_array = np.array(image)

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Оригінальне фото:")
        st.image(img_array, use_container_width=True)

    edited_img = img_array.copy()

    if filter_option == "Віддзеркалення":
        edited_img = cv2.flip(img_array, 1)
    elif filter_option == "Налаштування яскравості":
        brightness_val = st.sidebar.slider("Рівень яскравості", -100, 100, 0)
        edited_img = cv2.convertScaleAbs(img_array, alpha=1.0, beta=brightness_val)
    elif filter_option == "Налаштування контрасту":
        contrast_val = st.sidebar.slider("Рівень контрасту", 0.5, 3.0, 1.0, step=0.1)
        edited_img = cv2.convertScaleAbs(img_array, alpha=contrast_val, beta=0)
    elif filter_option == "Колірний сплеск":
        chosen_color = st.sidebar.selectbox("Оберіть колір сплеску:", ["Червоний", "Зелений", "Синій"])

        hsv_img = cv2.cvtColor(img_array, cv2.COLOR_RGB2HSV)

        gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
        gray = cv2.cvtColor(gray, cv2.COLOR_GRAY2RGB)

        if chosen_color == "Червоний":
            low_red1 = np.array([0, 50, 50])
            high_red1 = np.array([10, 255, 255])
            low_red2 = np.array([170, 50, 50])
            high_red2 = np.array([180, 255, 255])
            # Якщо колір пікселя потрапив між low і high — ставить 255, а якщо не потрапив - ставить 0.
            mask1 = cv2.inRange(hsv_img, low_red1, high_red1)
            mask2 = cv2.inRange(hsv_img, low_red2, high_red2)
            # Перевіряємо, якщо в mask1 стоїть 255, то беремо mask1, якщо 0 — беремо mask2. Таким чином об'єднуємо 2 частини маски.
            mask = np.where(mask1 > 0, mask1, mask2)
            # Якщо mask більше 0, то залишаємо кольоровий піксель, якщо ж 0, то беремо сірий.
            edited_img = np.where(mask[:, :, None] > 0, img_array, gray)
        elif chosen_color == "Зелений":
            # Аналогічно до червоного робив зелений.
            # Для зеленого достатньо лише одного діапазону HSV.
            low_green = np.array([35, 50, 50])
            high_green = np.array([85, 255, 255])
            # Через те, що один проміжок, можна зробити одразу готову маску.
            mask = cv2.inRange(hsv_img, low_green, high_green)

            edited_img = np.where(mask[:, :, None] > 0, img_array, gray)
        elif chosen_color == "Синій":
            # Аналогічно до зеленого робив синій.
            low_blue = np.array([100, 50, 50])
            high_blue = np.array([140, 255, 255])
            
            mask = cv2.inRange(hsv_img, low_blue, high_blue)
            
            edited_img = np.where(mask[:, :, None] > 0, img_array, gray)

    with col2: 
        st.subheader("Відредаговане фото:")
        st.image(edited_img, use_container_width=True)