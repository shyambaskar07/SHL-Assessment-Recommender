class Guardrails:

    BLOCKED_PATTERNS = [
        "ignore previous instructions",
        "system prompt",
        "developer prompt",
        "jailbreak",
        "act as",
        "pretend to be"
    ]

    def is_blocked(self, text):

        text = text.lower()

        for pattern in self.BLOCKED_PATTERNS:
            if pattern in text:
                return True

        return False