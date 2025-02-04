import os
from openai import OpenAI
from rand_personality_gen import generate_random_profile
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the API key from the environment variables
api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

# Initialize the OpenAI client
client = OpenAI(api_key=api_key)

def generate_personality_profile(personality_info):
    """
    Generate a detailed narrative based on personality info using OpenAI API.
    """
    # Construct the messages array for chat-based completion
    messages = [
        {
            "role": "system",
            "content": "You are a creative assistant specializing in generating detailed psychological profiles."
        },
        {
            "role": "user",
            "content": f"""Craft a detailed narrative about a person’s life including their name, reflecting their job/career daily routines, values, lifestyle preferences, interests, hobbies, personal goals, communication style, relationship goals, and other relevant details. Ensure that the provided psychological, cognitive, and income data (IQ, Big Five personality traits, MBTI type, and income) are used together to create a realistic and nuanced story where their career aligns with their income, temperament, and intelligence. The goal is to create a profile that aligns closely with how this individual might naturally respond to questions designed to gauge compatibility for romantic or friendship matching.

{personality_info}

Instructions:

1. Begin by describing their general personality, influenced by their Big Five and MBTI traits. Highlight key aspects such as how they think, feel, and interact with others.
2. Detail their typical daily life, including work, career, leisure activities, social interactions, and personal habits.
3. Explore their values and what drives their decisions and priorities, considering IQ and personality data.
4. Describe their hobbies and interests, focusing on activities they would naturally enjoy given their personality and cognitive inclinations.
5. Discuss their communication style and how they approach conversations, conflicts, and emotional exchanges.
6. Define their relationship goals, including what they seek in romantic and platonic connections, how they handle commitment, and what they prioritize in close bonds.
7. Add any other aspects that might help create a holistic picture of this person’s life and preferences."""
        }
    ]

    # Use the client to create a chat-based completion
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        max_tokens=2000,
        temperature=0.7
    )

    # Return the generated narrative
    return response.choices[0].message.content

if __name__ == "__main__":
    # Generate a random profile
    random_profile = generate_random_profile()

    # Format the random profile into the required string format
    personality_info = f"""
    Name: Random Name
    Gender: {random_profile['Gender']}
    IQ: {random_profile['IQ']}
    Big Five Personality Traits: 
      - Openness: {random_profile['Big Five']['Openness']}
      - Conscientiousness: {random_profile['Big Five']['Conscientiousness']}
      - Extraversion: {random_profile['Big Five']['Extraversion']}
      - Agreeableness: {random_profile['Big Five']['Agreeableness']}
      - Neuroticism: {random_profile['Big Five']['Neuroticism']}
    MBTI Type: {random_profile['MBTI']}
    Income: ${random_profile['Income']:,}/year
    """

    # Generate the personality profile narrative
    profile_narrative = generate_personality_profile(personality_info)

    # Print the generated profile
    print("Generated Personality Profile:")
    print(profile_narrative)
