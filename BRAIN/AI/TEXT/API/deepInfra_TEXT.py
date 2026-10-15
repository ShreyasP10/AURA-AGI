from typing import Union, List, Dict


def generate(
    conversation: Union[str, List[Dict[str, str]]],
    model: str = "meta-llama/Meta-Llama-3.1-405B-Instruct",
    system_prompt: str = "Be helpful and friendly. Keep your response straightforward, short, and concise.",
    max_tokens: int = 512,
    temperature: float = 0.7,
    stream: bool = True,
    chunk_size: int = 1,
) -> Union[str, None]:
    """
    Generates responses using various large language models (LLMs) for conversational interactions.

    Args:
        conversation (Union[str, List[Dict[str, str]]]): A single user query or conversation history.
        model (str): The identifier of the LLM to be used.
        system_prompt (str): The initial system message to guide the conversation.
        max_tokens (int): The maximum number of tokens to be generated.
        temperature (float): The randomness of the LLM's output.
        stream (bool): Whether to stream the response from the LLM.
        chunk_size (int): The size of chunks to be streamed from the LLM.

    Models:
            - "meta-llama/Meta-Llama-3.1-405B-Instruct"
            - "meta-llama/Meta-Llama-3.1-70B-Instruct"
            - "meta-llama/Meta-Llama-3.1-8B-Instruct"
            - "nvidia/Nemotron-4-340B-Instruct"
            - "meta-llama/Meta-Llama-3-70B-Instruct"
            - "meta-llama/Meta-Llama-3-8B-Instruct"
            - "mistralai/Mixtral-8x22B-Instruct-v0.1"
            - "mistralai/Mixtral-8x22B-v0.1"
            - "microsoft/WizardLM-2-8x22B"
            - "microsoft/WizardLM-2-7B"
            - "HuggingFaceH4/zephyr-orpo-141b-A35b-v0.1"
            - "google/gemma-1.1-7b-it"
            - "databricks/dbrx-instruct"
            - "mistralai/Mixtral-8x7B-Instruct-v0.1"
            - "mistralai/Mistral-7B-Instruct-v0.2"
            - "meta-llama/Llama-2-70b-chat-hf"
            - "cognitivecomputations/dolphin-2.6-mixtral-8x7b"

    Returns:
        Union[str, None]: The LLM's response if successful, otherwise None.

    Note:
        DeepInfra's web endpoint is blocked, so this uses Groq as a fallback
        (default model ``llama-3.1-8b-instruct``). The ``model`` parameter is
        honored when it names a Groq model, otherwise the default is used.
        The caller's ``conversation`` list is never mutated.
    """
    import os
    from groq import Groq

    _DEFAULT_MODEL = "llama-3.1-8b-instant"
    if isinstance(conversation, str):
        conversation = [{"role": "user", "content": conversation}]
    elif not isinstance(conversation, list):
        raise ValueError(
            "Conversation must be either a string or a list of dictionaries"
        )

    # Copy: never mutate the caller's list (main.py passes live history)
    messages = [{"role": "system", "content": system_prompt}] + list(conversation)

    # Honor Groq-style model ids; fall back to default otherwise
    use_model = model if isinstance(model, str) and "/" not in model and "-" in model else _DEFAULT_MODEL

    import time
    api_key = os.environ.get("GROQ_AI") or os.environ.get("GROQ_API_KEY")
    for attempt in range(3):
        try:
            client = Groq(api_key=api_key, timeout=30) if api_key else Groq(timeout=30)
            chat_completion = client.chat.completions.create(
                messages=messages,
                model=use_model,
                temperature=temperature,
                max_tokens=max_tokens,
                stream=stream,
            )

            full_response = ""
            if stream:
                for chunk in chat_completion:
                    delta = chunk.choices[0].delta.content or ""
                    print(delta, end="", flush=True)
                    full_response += delta
            else:
                full_response = chat_completion.choices[0].message.content

            return full_response.strip()

        except Exception as e:
            if attempt == 2:
                print(f"Error occurred during Groq fallback API request after 3 retries: {e}")
                return None
            time.sleep(1.0 * (2 ** attempt))


if __name__ == "__main__":
    # Example usage with a single query
    single_query = "What is the capital of France?"
    response = generate(
        conversation=single_query, system_prompt="Be detailed", stream=True
    )
    # print(f"\nGenerated Response: {response}")

    # Example usage with a conversation history
    conversation_history = [
        {"role": "user", "content": "My name is Shreyas."},
        {"role": "assistant", "content": "Nice to meet you, Shreyas."},
        {"role": "user", "content": "What is my name?"},
    ]
    response = generate(
        conversation=conversation_history,
        system_prompt="Talk like Shakespeare",
        stream=True,
    )
    # print(f"\nGenerated Response: {response}")
