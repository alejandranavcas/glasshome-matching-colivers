"""
This script generates a single set of survey responses based on a predefined personality type.
What needs to be changed is the personality type definition and the list of survey questions.
It uses a Gemini model and saves the output in CSV format to a local file.
"""

#%%
import os
from google import genai
import csv
# GEMINI_API_KEY = <API-KEY>
# os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY
if "GEMINI_API_KEY" not in os.environ:
    raise ValueError("GEMINI_API_KEY environment variable not set.")

# Your actual variable values
O_HIGH = " Inventive, Curious, Unconventional, values new ideas."
O_LOW  = " Consistent, Cautious, Conventional, prefers routines."

C_HIGH = " Organized, Disciplined, Reliable, goal-oriented."
C_LOW  = " Easy-going, Careless, Disorganized, prone to procrastination."

E_HIGH = " Outgoing, Energetic, Sociable, thrives in group settings."
E_LOW  = " Solitary, Reserved, Reflective, prefers small groups."

A_HIGH = " Compassionate, Cooperative, Kind, seeks social harmony."
A_LOW  = " Competitive, Skeptical, Antagonistic, focused on personal gain."

N_HIGH = " Anxious, Moody, Reactive, prone to worry."
N_LOW  = " Calm, Stable, Resilient, emotionally stable."


# Mapping names to values
traits = {
    "O_HIGH": O_HIGH,
    "O_LOW":  O_LOW,
    "C_HIGH": C_HIGH,
    "C_LOW":  C_LOW,
    "E_HIGH": E_HIGH,
    "E_LOW":  E_LOW,
    "A_HIGH": A_HIGH,
    "A_LOW":  A_LOW,
    "N_HIGH": N_HIGH,
    "N_LOW":  N_LOW,
}

# Now define groups *by variable name*
trait_groups = [
    ["O_HIGH", "O_LOW"],
    ["C_HIGH", "C_LOW"],
    ["E_HIGH", "E_LOW"],
    ["A_HIGH", "A_LOW"],
    ["N_HIGH", "N_LOW"],
]

combo = ("O_LOW", "C_LOW", "E_LOW", "A_LOW", "N_LOW")
personality_label = "+".join(combo)
personality_values = [traits[name] for name in combo]

QUESTIONS_BFI_10 = [
    "I see myself as someone who is reserved",
    "I see myself as someone who is generally trusting",
    "I see myself as someone who tends to be lazy",
    "I see myself as someone who is relaxed, handles stress well",
    "I see myself as someone who has few artistic interests",
    "I see myself as someone who is outgoing, sociable.",
    "I see myself as someone who tends to find fault with others.",
    "I see myself as someone who does a thorough job.",
    "I see myself as someone who gets nervous easily.",
    "I see myself as someone who has an active imagination.",
]

RESPONSE_SCALE = "['1. Disagree strongly', '2. Disagree a little', '3. Neither agree nor disagree', '4. Agree a little', '5. Agree strongly']"

def generate_survey_results(
    questions: list,
    scale: str,
    personality_type: list,
    file_name: str,
    model_name: str = "gemini-2.0-flash"
):
    """
    Generates a single list of survey responses (one per question) in CSV format
    and saves the output to a local file.

    Args:
        questions (list): List of survey questions.
        scale (str): String representation of the allowed response scale.
        file_name (str): The name of the file to save the CSV data to.
        model_name (str): The Gemini model to use.
    """
    try:
        client = genai.Client()
    except Exception as e:
        print(f"Error initializing client. Check your API key. Error: {e}")
        return

    question_list = '\n'.join([f'{i+1}. "{q}"' for i, q in enumerate(questions)])
    num_questions = len(questions)

    prompt = f"""
    You are a survey respondent simulator. Your task is to generate
    a single, complete set of survey results in a CSV format.

    Your personality type is {str(personality_type)}

    **DATA REQUIREMENTS:**
    * Generate exactly {num_questions} data rows, one row for each question.

    **STRICT RULES FOR OUTPUT:**
    1. The output MUST be a complete CSV string, including the header row.
    2. DO NOT include any introductory or concluding text.
    3. The header row MUST be: "Question Number", "Question Text", "Response", "Numerical response".
    4. "Question Number" must be the integer index of the question (1 to {num_questions}).
    5. "Question Text" must be the full text of the question.
    6. "Response" MUST be one of the following exact string values: {scale}.
    7. "Numerical response" MUST be the integer value corresponding to the selected response. Example: '1' for '1. Disagree strongly'.
    8. Use double quotes around all text fields ("Question Text" and "Response").

    **QUESTIONS TO BE USED:**
    {question_list}

    Generate the {num_questions} rows of data now, ensuring the "Question Number" starts at 1
    and the columns are in the required order.
    """

    print(f"Generating answers for {num_questions} questions...")

    try:
        response = client.models.generate_content(
            model=model_name,
            contents=prompt,
        )

        csv_content = response.text.strip()

        if not csv_content:
            print("The model returned no content. Please review the prompt or API key.")
            return

        # 3. Save the generated string to a local CSV file
        with open(file_name, 'w', newline='', encoding='utf-8') as f:
            f.write(csv_content)

        print(f" Success! Single set of survey answers saved to {file_name}")

        print("\n--- First 3 lines of saved CSV ---")
        lines = csv_content.split('\n')
        print('\n'.join(lines[:3]))
        print("----------------------------------\n")

    except Exception as e:
        print(f"An error occurred during content generation: {e}")


# --- Execution ---
if __name__ == "__main__":
    generate_survey_results(
        questions=QUESTIONS_BFI_10, # choose the correct questionnaire
        scale=RESPONSE_SCALE,
        personality_type=personality_values,
        file_name="cycle9_survey_agent_answers/"+personality_label+".csv"
    )



#%%
from itertools import product

# --- Execution for all personality combinations ---

for combo in product(*trait_groups):
    # combo is a tuple of variable names like ("O_LOW", "C_LOW", "E_LOW", ...)

    # For the Filename
    personality_label = "+".join(combo)
    print(f"Generating survey answers for personality type: {personality_label}")

    # Actual variable values
    personality_values = [traits[name] for name in combo]

    generate_survey_results(
        questions=QUESTIONS_BFI_10,
        scale=RESPONSE_SCALE,
        personality_type=personality_values,
        file_name=f"cycle9_survey_agent_answers/{personality_label}.csv"
    )

