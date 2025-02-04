import json
import os
from openai import OpenAI
from personality_creator import generate_personality_profile
from rand_personality_gen import generate_random_profile
from dotenv import load_dotenv
from prompts import questions

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OpenAI API key not found. Please set it in the .env file.")

client = OpenAI(api_key=api_key)

def load_existing_responses(filename):
    """Load existing responses from JSON file"""
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}
    return {}

def save_responses(filename, data):
    """Save responses to JSON file"""
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)

def generate_single_response(current_id):
    """Generate a single response for a given ID"""
    random_profile = generate_random_profile()
    personality_info = {
        "Gender": random_profile["Gender"],
        "IQ": random_profile["IQ"],
        "Big Five Personality Traits": {
            "Openness": random_profile["Big Five"]["Openness"],
            "Conscientiousness": random_profile["Big Five"]["Conscientiousness"],
            "Extraversion": random_profile["Big Five"]["Extraversion"],
            "Agreeableness": random_profile["Big Five"]["Agreeableness"],
            "Neuroticism": random_profile["Big Five"]["Neuroticism"]
        },
        "MBTI Type": random_profile["MBTI"],
        "Income": f"${random_profile['Income']:,}/year"
    }
    
    personality_profile = generate_personality_profile(json.dumps(personality_info, indent=4))
    
    system_message = """
    Act as the individual described in the personality profile provided. Answer questions based on the personality traits, 
    habits, values, and preferences outlined in the narrative. Assume the identity and mindset of this individual, 
    considering how they would think, feel, and act in various situations. Answer in json format.
    """
    
    user_message = {
        "Personality Profile": personality_profile,
        "Questions": questions
    }
    
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": json.dumps(user_message, indent=4)}
            ],
            temperature=0.7,
            tools=[{
                "type": "function",
                "function": {
                    "name": "format_personality_response",
                    "description": "Format the personality assessment responses",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "Core Values": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Communication and Conflict Resolution": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Lifestyle and Habits": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Emotional and Physical Intimacy": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Commitment and Future Goals": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Trust and Security": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Social and Family Life": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Personal Growth and Self-Development": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Fun and Adventure": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Flexibility and Adaptability": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Giving and Receiving": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Social Life and Friendships": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}},
                            "Personal Habits and Preferences": {"type": "array", "items": {"type": "integer", "minimum": 1, "maximum": 5}}
                        },
                        "required": [
                            "Core Values", "Communication and Conflict Resolution", "Lifestyle and Habits",
                            "Emotional and Physical Intimacy", "Commitment and Future Goals", "Trust and Security",
                            "Social and Family Life", "Personal Growth and Self-Development", "Fun and Adventure",
                            "Flexibility and Adaptability", "Giving and Receiving", "Social Life and Friendships",
                            "Personal Habits and Preferences"
                        ]
                    }
                }
            }],
            tool_choice={"type": "function", "function": {"name": "format_personality_response"}}
        )
        
        response_args = json.loads(response.choices[0].message.tool_calls[0].function.arguments)
        return response_args
    except Exception as e:
        print(f"API Error for ID {current_id}: {str(e)}")
        return None

def process_responses(start_id, num_iterations, filename="response.json"):
    """Process responses one at a time with progress saving"""
    existing_data = load_existing_responses(filename)
    processed_count = 0
    
    for i in range(num_iterations):
        current_id = start_id + i
        if str(current_id) in existing_data:
            print(f"Skipping already processed ID: {current_id}")
            continue
            
        print(f"Processing ID: {current_id}")
        response = generate_single_response(current_id)
        
        if response:
            existing_data[str(current_id)] = response
            save_responses(filename, existing_data)
            processed_count += 1
            print(f"Successfully processed ID: {current_id}")
        else:
            print(f"Failed to process ID: {current_id}")
    
    print(f"Processing complete. Total new responses: {processed_count}")
    return existing_data

if __name__ == "__main__":
    START_ID = 10000
    NUM_ITERATIONS = 200
    OUTPUT_FILE = "response.json"
    
    final_data = process_responses(START_ID, NUM_ITERATIONS, OUTPUT_FILE)
    print(f"Total responses in file: {len(final_data)}")