"""
Probability of a sequence of states in a Markov chain.

Given
  - static (initial) probabilities, e.g. P(day 1 = Sunny) = 0.3
  - transition probabilities, e.g. P(Rainy tomorrow | Sunny today) = 0.1
find
  P(X1 = s1, X2 = s2, ..., Xn = sn)
    = P(s1) * P(s1 -> s2) * P(s2 -> s3) * ... * P(s(n-1) -> sn)

Usage:
  python markov_sequence_solver.py                      -> asks for the sequence
  python markov_sequence_solver.py Sunny Sunny Rainy    -> sequence on the command line
  python markov_sequence_solver.py --custom             -> also enter your own probabilities
"""

import sys

# ---------------- Data from the video (default) ----------------
STATES = ["Sunny", "Cloudy", "Rainy"]

INITIAL = {"Sunny": 0.3, "Cloudy": 0.5, "Rainy": 0.2}

TRANSITION = {
    "Sunny":  {"Sunny": 0.6, "Cloudy": 0.3, "Rainy": 0.1},
    "Cloudy": {"Sunny": 0.2, "Cloudy": 0.5, "Rainy": 0.3},
    "Rainy":  {"Sunny": 0.1, "Cloudy": 0.4, "Rainy": 0.5},
}


# ---------------- Core calculation ----------------
def sequence_probability(sequence, initial, transition, verbose=True):
    """Return P(sequence). If verbose, print the working step by step."""
    first = sequence[0]
    prob = initial[first]
    factors = [prob]

    if verbose:
        print(f"\nSequence: {' -> '.join(sequence)}\n")
        print(f"Step 1: P({first}) from the static probabilities = {prob}")

    for step, (a, b) in enumerate(zip(sequence[:-1], sequence[1:]), start=2):
        p = transition[a][b]
        prob *= p
        factors.append(p)
        if verbose:
            print(f"Step {step}: P({b} | {a}) = {p}")

    if verbose:
        working = " x ".join(str(f) for f in factors)
        print(f"\nP(sequence) = {working} = {prob:.6g}")
    return prob


# ---------------- Input helpers ----------------
def validate(states, initial, transition):
    if abs(sum(initial.values()) - 1) > 1e-9:
        raise ValueError("Initial probabilities must sum to 1.")
    for s in states:
        if abs(sum(transition[s].values()) - 1) > 1e-9:
            raise ValueError(f"Transition probabilities from {s} must sum to 1.")


def read_custom_data():
    states = [s.strip() for s in input("States (comma separated): ").split(",")]
    probs = [float(x) for x in input(f"Initial probabilities for {states}: ").replace(",", " ").split()]
    initial = dict(zip(states, probs))
    transition = {}
    print("Transition probabilities (to each state in the same order):")
    for s in states:
        row = [float(x) for x in input(f"  From {s}: ").replace(",", " ").split()]
        transition[s] = dict(zip(states, row))
    return states, initial, transition


def read_sequence(states, args):
    if args:
        seq = args
    else:
        print(f"Available states: {', '.join(states)}")
        seq = input("Enter the sequence (space separated), e.g. Sunny Sunny Rainy: ").split()

    # Case-insensitive match to the defined state names
    lookup = {s.lower(): s for s in states}
    cleaned = []
    for word in seq:
        key = word.strip(",->").lower()
        if key not in lookup:
            raise ValueError(f"Unknown state '{word}'. Choose from {states}.")
        cleaned.append(lookup[key])
    if not cleaned:
        raise ValueError("Sequence is empty.")
    return cleaned


def main():
    args = [a for a in sys.argv[1:] if a != "--custom"]

    if "--custom" in sys.argv:
        states, initial, transition = read_custom_data()
    else:
        states, initial, transition = STATES, INITIAL, TRANSITION

    validate(states, initial, transition)
    sequence = read_sequence(states, args)
    sequence_probability(sequence, initial, transition)


if __name__ == "__main__":
    main()
