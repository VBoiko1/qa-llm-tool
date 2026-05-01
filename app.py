import streamlit as st
from llm.client import client
from utils.images import encode_image

st.title("Генератор тест-кейсов из скриншотов")

uploaded_files = st.file_uploader(
    "Загрузи скриншоты (в порядке шагов)",
    accept_multiple_files=True
)

description = st.text_area("Опиши шаги и ожидаемый результат")

if st.button("Сгенерировать тест-кейсы"):

    if not uploaded_files or not description:
        st.warning("Добавь данные")
    else:
        content = []

        content.append({
            "type": "input_text",
            "text": f"""
Ты QA инженер.
Сгенерируй тест-кейс:

{description}
"""
        })

        for file in uploaded_files:
            content.append({
                "type": "input_image",
                "image_base64": encode_image(file)
            })

        with st.spinner("Генерация..."):
            response = client.responses.create(
                model="gpt-4.1",
                input=[{
                    "role": "user",
                    "content": content
                }]
            )

        st.markdown(response.output_text)