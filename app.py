import streamlit as st
from llm.client import generate_response
from utils.images import encode_image
import os
import datetime

st.set_page_config(page_title="QA Test Case Generator", layout="centered")

# --- Заголовок ---
st.title("Генератор тест-кейсов из скриншотов")

# --- Индикатор режима ---
st.markdown(
    "<div style='padding:8px;border-radius:8px;background-color:#d4edda;color:#155724;'>🟢 OpenAI режим</div>",
    unsafe_allow_html=True
)

# --- Загрузка файлов ---
uploaded_files = st.file_uploader(
    "Загрузи скриншоты (в порядке шагов)",
    accept_multiple_files=True,
    type=["png", "jpg", "jpeg"]
)

# --- Описание ---
description = st.text_area("Опиши шаги и ожидаемый результат")

# --- Кнопка ---
if st.button("Сгенерировать тест-кейс"):

    if not uploaded_files or not description:
        st.warning("Добавь скриншоты и описание")
    else:
        images = []

        for file in uploaded_files:
            base64_img = encode_image(file)
            images.append(base64_img)

        with st.spinner("Генерация..."):
            response = generate_response(description, images)

        # --- Вывод результата ---
        st.markdown("### 📄 Результат")
        st.markdown(response)

        # --- Имя файла ---
        filename = f"test_case_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"

        # --- Скачать файл (ВАЖНО для Streamlit Cloud) ---
        st.download_button(
            label="📥 Скачать тест-кейс",
            data=response,
            file_name=filename,
            mime="text/plain"
        )

        # --- (опционально) сохранить локально ---
        try:
            with open(filename, "w", encoding="utf-8") as f:
                f.write(response)
        except:
            pass