import random
import numpy as np

def generate_random_profile():
    """
    Generates a psychological profile with gender, IQ, Big Five traits, MBTI type, and income.
    """
    # Gender distribution: 50/50 male and female
    gender = random.choice(["Male", "Female"])

    # IQ: Normal distribution (mean=100, std=15), rounded and constrained between 55 and 145
    iq = max(55, min(145, int(np.random.normal(100, 15))))

    # Big Five Personality Traits: Gender-specific adjustments for realism
    def bounded_normal(mean, std, lower=0, upper=100):
        """Generates values bounded between lower and upper limits."""
        return max(lower, min(upper, int(np.random.normal(mean, std))))

    if gender == "Male":
        openness = bounded_normal(55, 15)
        conscientiousness = bounded_normal(50, 10)
        extraversion = bounded_normal(55, 15)
        agreeableness = bounded_normal(45, 15)
        neuroticism = bounded_normal(45, 15)
    else:
        openness = bounded_normal(50, 15)
        conscientiousness = bounded_normal(55, 10)
        extraversion = bounded_normal(60, 15)
        agreeableness = bounded_normal(60, 15)
        neuroticism = bounded_normal(60, 15)

    # MBTI: Base probabilities for each gender
    mbti_types = {
        "Male": {
            "ISTJ": 16.4, "ISFJ": 8.1, "INFJ": 2.3, "INTJ": 3.3,
            "ISTP": 8.5, "ISFP": 5.9, "INFP": 4.1, "INTP": 4.8,
            "ESTP": 5.6, "ESFP": 4.5, "ENFP": 6.4, "ENTP": 4.5,
            "ESTJ": 11.2, "ESFJ": 7.5, "ENFJ": 2.8, "ENTJ": 3.0
        },
        "Female": {
            "ISTJ": 6.9, "ISFJ": 19.4, "INFJ": 3.6, "INTJ": 0.9,
            "ISTP": 2.4, "ISFP": 9.9, "INFP": 4.6, "INTP": 1.7,
            "ESTP": 3.0, "ESFP": 10.1, "ENFP": 9.7, "ENTP": 2.4,
            "ESTJ": 6.3, "ESFJ": 16.9, "ENFJ": 3.3, "ENTJ": 0.9
        }
    }

    def adjust_mbti_probabilities(base_probs, openness, conscientiousness, extraversion, agreeableness, neuroticism):
        """
        Adjusts MBTI probabilities based on Big Five personality correlations.
        """
        adjusted_probs = {}
        for mbti, prob in base_probs.items():
            # Correlation-based scaling
            if "N" in mbti:  # Intuition correlates with Openness
                prob *= 1 + (openness - 50) / 100
            if "F" in mbti:  # Feeling correlates with Agreeableness
                prob *= 1 + (agreeableness - 50) / 100
            if "J" in mbti:  # Judging correlates with Conscientiousness
                prob *= 1 + (conscientiousness - 50) / 100
            if "E" in mbti:  # Extraversion correlates with Extraversion
                prob *= 1 + (extraversion - 50) / 100
            adjusted_probs[mbti] = prob

        # Normalize probabilities to sum to 100%
        total = sum(adjusted_probs.values())
        for mbti in adjusted_probs:
            adjusted_probs[mbti] = (adjusted_probs[mbti] / total) * 100

        return adjusted_probs

    # Adjust probabilities based on gender and Big Five traits
    base_probs = mbti_types[gender]
    adjusted_probs = adjust_mbti_probabilities(base_probs, openness, conscientiousness, extraversion, agreeableness, neuroticism)

    # Randomly select MBTI type based on adjusted probabilities
    mbti = random.choices(list(adjusted_probs.keys()), weights=adjusted_probs.values())[0]

    # Income: Bell curve distribution in the US (mean=70k, std=20k)
    income = int(np.random.normal(70000, 20000))

    # Adjust income based on IQ, Conscientiousness, and Openness
    # Each standard deviation above the mean adds an upward income adjustment
    iq_adjustment = (iq - 100) / 15 * 10000  # $10k per SD
    conscientiousness_adjustment = (conscientiousness - 50) / 10 * 5000  # $5k per SD
    openness_adjustment = (openness - 50) / 10 * 3000  # $3k per SD

    # Final income calculation with adjustments
    income += iq_adjustment + conscientiousness_adjustment + openness_adjustment
    income = max(15000, min(200000, int(income)))  # Clamp to realistic bounds

    # Compile the psychological profile
    profile = {
        "Gender": gender,
        "IQ": iq,
        "Big Five": {
            "Openness": openness,
            "Conscientiousness": conscientiousness,
            "Extraversion": extraversion,
            "Agreeableness": agreeableness,
            "Neuroticism": neuroticism,
        },
        "MBTI": mbti,
        "Income": income,
    }

    return profile

# Generate and display a random profile
if __name__ == "__main__":
    random_profile = generate_random_profile()
    for key, value in random_profile.items():
        if key == "Big Five":
            print(f"{key}:")
            for trait, score in value.items():
                print(f"  {trait}: {score}")
        else:
            print(f"{key}: {value}")
