
import requests, base64

class gemma:

    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    stream = True

    with open("image.png", "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode()

    assert len(image_b64) < 180_000, \
    "To upload larger images, use the assets API (see docs)"
    

    headers = {
    "Authorization": "Bearer $API_KEY_REQUIRED_IF_EXECUTING_OUTSIDE_NGC",
    "Accept": "text/event-stream" if stream else "application/json"
    }

    payload = {
    "model": 'google/gemma-3-27b-it',
    "messages": [
        {
        "role": "user",
        "content": f'What is in this image? <img src="data:image/png;base64,{image_b64}" />'
        }
    ],
    "max_tokens": 512,
    "temperature": 0.20,
    "top_p": 0.70,
    "stream": stream
    }

    response = requests.post(invoke_url, headers=headers, json=payload)

    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    else:
        print(response.json())
