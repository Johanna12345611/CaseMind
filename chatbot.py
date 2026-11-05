import json
import random

from nlp_processor import (
    classify_intent,
    extract_entities
)


def load_cases():
    with open("cases.json", "r", encoding="utf-8") as file:
        data = json.load(file)

    return data["cases"]


def get_response(user_input, case, discovered_clues):

    text = user_input.lower().strip()

    if not text:
        return "Detective, please enter a question."

    intent = classify_intent(text)

    entities = extract_entities(text, case)

    # Greeting
    if intent == "greeting":
        return (
            "Welcome, Detective! The investigation is waiting. "
            "Ask me about suspects, clues or the crime scene."
        )

    # Suspects
    if intent == "suspects":
        names = [
            suspect["name"]
            for suspect in case["suspects"]
        ]

        return (
            "The people under investigation are: "
            + ", ".join(names)
            + ". You can ask me about their statements and motives."
        )

    # Suspect details
    for suspect in case["suspects"]:

        if suspect["name"].lower() in text:

            if any(word in text for word in
                   ["motive", "reason", "why"]):

                return (
                    f"{suspect['name']} is a "
                    f"{suspect['role']}. "
                    f"Possible motive: {suspect['motive']}"
                )

            if any(word in text for word in
                   ["alibi", "where", "location"]):

                return (
                    f"{suspect['name']}'s alibi: "
                    f"{suspect['alibi']}"
                )

            return (
                f"{suspect['name']} is a "
                f"{suspect['role']}. "
                f"Their statement is: "
                f"{suspect['statement']}"
            )

    # Clue discovery
    for index, clue in enumerate(case["clues"]):

        if any(keyword in text for keyword in clue["keywords"]):

            discovered_clues.add(index)

            return (
                f"🔍 Evidence discovered: {clue['name']}\n\n"
                f"{clue['description']}"
            )

    # Show discovered clues
    if intent == "clues":

        if not discovered_clues:
            return (
                "No evidence has been collected yet. "
                "Ask questions about the investigation "
                "to discover clues."
            )

        names = [
            case["clues"][i]["name"]
            for i in sorted(discovered_clues)
        ]

        return "Evidence collected: " + ", ".join(names)

    # Location
    if intent == "location":
        return (
            f"The incident took place at "
            f"{case['location']}."
        )

    # Time
    if intent == "time":
        return (
            f"The incident was reported at "
            f"{case['time']}."
        )

    # Victim
    if intent == "victim":
        return (
            f"The victim is {case['victim']}."
        )

    # Help
    if intent == "help":
        return (
            "You can ask me:\n\n"
            "• Who are the suspects?\n"
            "• What is their motive?\n"
            "• Where did the incident happen?\n"
            "• When did it happen?\n"
            "• What clues are available?\n"
            "• What was a suspect's alibi?"
        )

    # Hint
    if intent == "hint":
        remaining = [
            clue for i, clue in enumerate(case["clues"])
            if i not in discovered_clues
        ]

        if remaining:
            return (
                "Here's a hint: Pay attention to "
                + remaining[0]["name"]
                + ". Think about how it connects "
                  "to the suspects."
            )

        return (
            "You've discovered all the evidence! "
            "Review the suspects' statements carefully."
        )

    # Entity recognition response
    if entities:
        return (
            "I recognized: "
            + ", ".join(entities)
            + ". Ask me about the person's statement, "
              "motive or alibi."
        )

    return (
        "I'm not sure I understood that, Detective. "
        "Try asking about suspects, motives, evidence, "
        "the location or the time of the incident."
    )