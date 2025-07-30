import requests


def query_ollama(prompt: str, model: str = "mistral", port: int = 11434) -> str:
    response = requests.post(
        f"http://localhost:{port}/api/generate",
        json={
            "model": model,
            "prompt": prompt,
            "stream": False
        },
        timeout=60
    )
    response.raise_for_status()
    return response.json()["response"].strip()


if __name__ == "__main__":
    print(query_ollama("List users with EC2 and Lambda access"))
