import json
import sys
from games.connect_four import strategy as connect_four_strategy

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
