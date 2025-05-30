def evaluate_resume(text, lang="en"):
    score = 100
    suggestions = []

    # Define must-have sections
    required_sections = {
        "en": ["education", "experience", "skills", "contact"],
        "fr": ["formation", "expérience", "compétences", "contact"]
    }

    penalties = {
        "missing_section": 10,
        "too_short": 15,
        "no_email": 5
    }

    lowered = text.lower()

    # Check for required sections
    for section in required_sections[lang]:
        if section not in lowered:
            score -= penalties["missing_section"]
            suggestions.append(
                f"❌ Missing section: {section.capitalize()}"
                if lang == "en"
                else f"❌ Section manquante : {section.capitalize()}"
            )

    # Check length
    if len(text.split()) < 150:
        score -= penalties["too_short"]
        suggestions.append(
            "❗ Your résumé is very short — add more content."
            if lang == "en"
            else "❗ Votre CV est très court — ajoutez plus de contenu."
        )

    # Check for email
    if "@" not in text:
        score -= penalties["no_email"]
        suggestions.append(
            "📧 No email detected — include your contact info."
            if lang == "en"
            else "📧 Aucune adresse e-mail détectée — ajoutez vos coordonnées."
        )

    # Ensure score doesn't go below 0
    score = max(score, 0)

    return score, suggestions

