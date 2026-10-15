import requests
import re
import json


def generate(
    prompt: dict,
    system_prompt: str = "Be Helpful and Friendly",
    model: str = "Phind Instant",
    stream_chunk_size: int = 12,
    stream: bool = True,
) -> str:
    """
    Generates a response from the Phind Instant model based on the given prompt.

    Parameters:
    - prompt (dict): The input text to which the model will respond in a dictionary format.
    - system_prompt (str, optional): The system prompt to use for the model. Defaults to "Be Helpful and Friendly".
    - model (str, optional): The model to use for generating the response.
                                        Available Models:
                                            - "Phind-34B"
                                            - "Phind Instant"
    - stream_chunk_size (int, optional): The number of bytes to read from the response stream. Defaults to 64.
    - stream (bool, optional): Whether to stream the response. Defaults to True.

    Returns:
    - str: The generated text response from the model.

    This function initializes a session with the Phind Instant API, sets the necessary headers,
    and constructs the payload with the user's prompt. It then sends a POST request to the API
    endpoint and streams the response. The function collects the text content from the streamed
    response and returns it as a single string.
    """

    headers = {"User-Agent": "Mozilla/5.0"}
    if isinstance(prompt, str):
        message_history = [{"role": "user", "content": prompt}]
    else:
        message_history = list(prompt)
    message_history = [{"content": system_prompt, "role": "system"}] + message_history
    user_input = message_history[-1]["content"] if message_history else ""

    payload = {
        "additional_extension_context": "",
        "allow_magic_buttons": True,
        "is_vscode_extension": True,
        "message_history": message_history,
        "requested_model": model,
        "user_input": user_input,
    }

    # Send POST request and stream response
    chat_endpoint = "https://extension.phind.com/agent/"
    response = requests.post(
        chat_endpoint, headers=headers, json=payload, stream=True, timeout=30
    )

    # Collect streamed text content
    streaming_text = ""
    for value in response.iter_lines(decode_unicode=True, chunk_size=stream_chunk_size):
        if not value:
            continue
        line = value[5:].strip() if value.startswith("data:") else value.strip()
        if not line or line == "[DONE]":
            continue
        try:
            json_modified_value = json.loads(line)
            content = json_modified_value.get("choices", [{}])[0].get("delta", {}).get("content", "")
            if content:
                if stream:
                    print(content, end="", flush=True)
                streaming_text += content
        except Exception:
            continue

    return streaming_text


if __name__ == "__main__":
    # Predefined system prompt
    system_prompt = (
        "Be Helpful and Friendly. Keep your response straightforward, short and concise"
    )
    # system_prompt = "Be Helpful and Friendly. Keep your response straightforward, long and detailed"
    # system_prompt = "Talk like Shakespeare"

    # Predefined conversational history that includes providing a name and then asking the AI to recall it
    prompt = [
        {"role": "user", "content": "My name is Shreyas."},
        {"role": "assistant", "content": "Nice to meet you, Shreyas."},
        {"role": "user", "content": "What is my name?"},
    ]

    # Call the generate function with the predefined conversational history
    api_response = generate(
        prompt=prompt, system_prompt=system_prompt, model="Phind-34B", stream=True
    )
    # print("Response content:", api_response)
