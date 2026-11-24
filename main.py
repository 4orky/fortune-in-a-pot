# Fortune in a Pot — make.fun bounty
# u-golden-heron-44-fortune-in-a-pot-ded981e9
#
# The program writes one kind, funny fortune for a houseplant
# (a single line of at most 120 characters) to /output/entry.txt.
# Candidates were drafted against the judge's brief, in order of weight:
#   1. a fortune for a houseplant, about the plant's own future —
#      the windowsill, the pot, the watering, the leaves
#   2. funny in a way a plant lover would laugh at, a small joke
#      that lands rather than a pun groaned at
#   3. kind and warm, no doom, no withering, no mockery
#   4. sounds like a fortune, the cadence of a prediction,
#      not a slogan, a caption or a care instruction
#   5. one crisp line that reads cleanly aloud, no padding
# Each candidate carries a hand-scored craft score (0-10 per criterion,
# summed below); selection is deterministic: highest score wins, ties go
# to the shorter text. The output is byte-identical on every run.

CANDIDATES = [
    # score: plant-fortune 10, funny 9, kind 10, fortune-voice 10,
    #   crisp 9 = 48. Fortune-slip opening ("A tall stranger will..."),
    #   turned on the plant's own life: regular watering, and the
    #   forgiving of the last drought — by the leaves, and by the
    #   plant itself. Kind, specific to a potted windowsill plant,
    #   and the punch lands on the last four words.
    ("A tall stranger will water you twice a week and mean it \u2014 "
     "your leaves will forgive the last drought, and so will you.",
     48),
    # score: plant-fortune 10, funny 8, kind 9, fortune-voice 9,
    #   crisp 9 = 45. Warm and visual — the pot turned toward the
    #   sun, leaves leaning in like they heard good news — but the
    #   joke is gentler and the turn less sharp than the winner.
    ("Soon a hand you trust will turn your pot toward the sun, and "
     "every leaf you own will lean in like it heard good news.",
     45),
    # score: plant-fortune 9, funny 8, kind 9, fortune-voice 9,
    #   crisp 8 = 43. Bright and warm with a good outgrowing-the-pot
    #   beat, but "your future is bright" is a stock fortune opening
    #   and the line leans slightly toward a care list.
    ("Your future is bright: a sunny sill, a faithful waterer, and "
     "one glorious afternoon when you finally outgrow your pot.",
     43),
    # score: plant-fortune 9, funny 8, kind 9, fortune-voice 9,
    #   crisp 8 = 42. The keeper talking to the plant "as if you can
    #   hear" is a lovely plant-lover joke, but "chosen by the sun"
    #   is vaguer than the winner's watering promise.
    ("The sun has already chosen you: expect a fresh leaf by spring, "
     "and a keeper who talks to you as if you can hear.",
     42),
    # score: plant-fortune 9, funny 8, kind 8, fortune-voice 8,
    #   crisp 8 = 41. The windowsill as "the best seat in the house"
    #   is charming, but it reads more like a caption about the plant
    #   than a fortune told to it.
    ("A visitor will admire your leaves, ask your name, and leave "
     "convinced the windowsill is the best seat in the house.",
     41),
    # score: plant-fortune 9, funny 7, kind 9, fortune-voice 9,
    #   crisp 8 = 42. Gentle and true — news growing slowly, a new
    #   leaf, a keeper taking credit — but the humour is quieter
    #   than the winner's and the prediction softer.
    ("Good news grows slowly: by spring a new leaf will unfurl, and "
     "your keeper will act like they planned it all along.",
     42),
]

# The gate requires 1-120 characters of non-whitespace UTF-8 text.
MAX_CHARS = 120


def pick(candidates):
    best = None
    for text, score in candidates:
        assert 1 <= len(text) <= MAX_CHARS, \
            f"candidate over gate: {len(text)} chars"
        assert text.strip(), "candidate is blank"
        assert "\n" not in text, "candidate must be a single line"
        key = (score, -len(text))  # highest score, then shortest
        if best is None or key > best[0]:
            best = (key, text)
    return best[1]


def main():
    import hashlib
    import os
    import sys

    fortune = pick(CANDIDATES)
    os.makedirs("/output", exist_ok=True)
    with open("/output/entry.txt", "w", encoding="utf-8") as f:
        f.write(fortune)
    os.chmod("/output/entry.txt", 0o644)
    # Verify the written output: read it back byte-for-byte and re-check
    # the gate (1-120 characters, single line, non-blank). A truncated or
    # altered file must fail loudly instead of shipping a bad entry.
    with open("/output/entry.txt", "rb") as f:
        raw = f.read()
    written = raw.decode("utf-8")
    if written != fortune:
        print("error: /output/entry.txt does not match selected fortune",
              file=sys.stderr)
        sys.exit(1)
    if not (1 <= len(written) <= MAX_CHARS and written.strip()
            and "\n" not in written):
        print("error: /output/entry.txt fails gate: "
              f"{len(written)} chars", file=sys.stderr)
        sys.exit(1)
    digest = hashlib.sha256(raw).hexdigest()
    print(fortune)
    print(f"chars={len(written)} sha256={digest}")


if __name__ == "__main__":
    main()
