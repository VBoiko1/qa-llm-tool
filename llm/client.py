import os
from dotenv import load_dotenv
from openai import OpenAI
from utils.images import encode_image, get_image_mime_type

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def build_prompt(description: str) -> str:
    return f"""
Ты опытный QA инженер (Middle+).

На основе сценария и скриншотов:

ТРЕБОВАНИЯ:
- Пиши на русском языке
- Используй профессиональный QA стиль (Jira/TestRail)
- НЕ повторяй входной сценарий — расширяй его
- Добавляй проверки валидации

ФОРМАТ:

Test Case ID: TC-XXX
Title: ...

Preconditions:
- ...

Steps:
1. ...
2. ...

Expected Result:
- ...

Postconditions:
- ...

Test Data:
- ...

Priority: High / Medium / Low

---

Описание:
{description}
"""


def generate_response(description, images=None):

    prompt = build_prompt(description)

    content = [
        {
            "type": "input_text",
            "text": prompt
        }
    ]

    if images:
        for file in images:
            base64_img = encode_image(file)
            mime = get_image_mime_type(file)

            content.append({
                "type": "input_image",
                "image_url": f"data:{mime};base64,{base64_img}"
            })

    response = client.responses.create(
        model="gpt-4.1",
        input=[{
            "role": "user",
            "content": content
        }]
    )

    return response.output_text