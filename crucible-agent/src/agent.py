import json
import sys
import os
import urllib.request


def ask_ai(system_prompt, user_data, max_tokens=1000):
    base_url = os.environ["OPENAI_BASE_URL"].rstrip("/")
    api_key = os.environ["OPENAI_API_KEY"]
    model = os.environ["CRUCIBLE_AI_MODEL"]

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": json.dumps(user_data)
            }
        ],
        "max_tokens": max_tokens,
        "temperature": 0
    }

    req = urllib.request.Request(
        f"{base_url}/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=45) as response:
        result = json.loads(response.read().decode("utf-8"))

    content = result["choices"][0]["message"]["content"]
    return content


def choose_action(request):
    """
    Implement the game-specific strategy here.

    request contains:
      - decision: request ID, seat, and action kind
      - history: all observations visible to this seat
      - deadlineMs: time allowed for this decision

    Return the exact response object required by the game.
    """
    raise NotImplementedError("Game strategy has not been implemented")


def handle_request(request):
    request_type = request.get("type")

    if request_type == "init":
        print("Agent initialized", file=sys.stderr)
        return {}

    if request_type == "decision":
        return choose_action(request)

    raise ValueError(f"Unknown request type: {request_type}")


def main():
    for line in sys.stdin:
        if not line.strip():
            continue

        try:
            request = json.loads(line)
            response = handle_request(request)
        except Exception as exc:
            print(f"Agent error: {exc}", file=sys.stderr)
            # Do not fabricate a game action after an error.
            # The strategy must be implemented to handle decisions.
            continue

        sys.stdout.write(
            json.dumps(response, separators=(",", ":")) + "\n"
        )
        sys.stdout.flush()


if __name__ == "__main__":
    main()
