# Synthetic Data Generator for Matching Algorithms

## Overview
This project is an **AI-powered system** that synthesizes user responses to **over 130 relationship-centric questions**. It generates realistic, nuanced personality profiles and corresponding survey responses to aid in the development and testing of **matching algorithms** for romantic or friendship connections.

## Features
- **Automated Personality Generation:** Creates detailed psychological profiles using AI, incorporating factors like **IQ**, **Big Five traits**, **MBTI types**, and **income**.
- **Survey Simulation:** Generates responses to a comprehensive set of **relationship-centric questions**, covering topics like *core values*, *communication*, *lifestyle*, *intimacy*, and more.
- **Customizable Data Generation:** Allows for multiple iterations of profile and response generation with configurable parameters.
- **Data Storage:** Saves generated responses in **JSON format** for easy integration with matching algorithms.

## File Structure
```plaintext
├── looped_personality_answering.py   # Main script to generate and store simulated survey responses
├── personality_creator.py           # Generates detailed narrative profiles based on psychological traits
├── rand_personality_gen.py          # Randomly generates psychological attributes like IQ, Big Five traits, MBTI, and income
├── prompts.py                       # Contains the set of over 130 relationship-centric questions
├── questions.txt                    # Full list of relationship-centric questions
└── response.json                    # Stores the generated responses in JSON format
```

## Setup Instructions
1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/synthetic-data-generator-for-matching-algorithm.git
   cd synthetic-data-generator-for-matching-algorithm
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**
   Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```

## Running the Program
To generate simulated survey responses, run the following command:
```bash
python looped_personality_answering.py
```
This will generate **200 profiles** starting from **ID 10000** and store them in `response.json`.

## Customization
You can modify the number of profiles generated and the starting ID in `looped_personality_answering.py`:
```python
START_ID = 10000
NUM_ITERATIONS = 200
```

## Sample Output
The generated data in `response.json` includes structured responses across multiple categories:
```json
{
  "10000": {
    "Core Values": [5, 4, 4, 3, 3, 2, 2, 2, 2, 3],
    "Communication and Conflict Resolution": [5, 4, 5, 5, 5, 4, 4, 3, 3, 5],
    "Lifestyle and Habits": [4, 3, 4, 5, 5, 4, 3, 3, 2, 3]
    // ... additional categories
  }
}
```

## Question Categories
The system generates responses across a wide range of relationship dimensions, including:

- **Core Values**
- **Communication and Conflict Resolution**
- **Lifestyle and Habits**
- **Emotional and Physical Intimacy**
- **Commitment and Future Goals**
- **Trust and Security**
- **Social and Family Life**
- **Personal Growth and Self-Development**
- **Fun and Adventure**
- **Flexibility and Adaptability**
- **Giving and Receiving**
- **Social Life and Friendships**
- **Personal Habits and Preferences**

For the full list of questions, refer to [`questions.txt`](questions.txt).

## Contributing
Contributions are welcome! Please **fork** the repository and submit a **pull request** for review.

## License
This project is licensed under the **MIT License**.

## Contact
For any questions or feedback, please contact [your email or GitHub profile].

