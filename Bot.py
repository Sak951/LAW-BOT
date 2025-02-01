import json
from difflib import get_close_matches
from typing import Optional, Dict, List


def load_Knowlegebase(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            data: Dict = json.load(file)
            return data
    except FileNotFoundError:
        print("Knowledgebase file not found. Starting with an empty knowledge base.")
        return {"questions": []}
    except json.JSONDecodeError:
        print("Error decoding JSON. Starting with an empty knowledge base.")
        return {"questions": []}

def save_Knowlegebase(file_path: str, data: Dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches: List[str] = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None

def get_answer_for_question(question: str, knowledge_base: Dict) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]
    return None

def chat_bot():
    Knowledgebase: Dict = load_Knowlegebase('Knowledgebase.json')
    while True:
        user_input: str = input("You: ")
        if user_input.lower() == 'quit':
            break
        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in Knowledgebase["questions"]])
         
        if best_match:
            answer: Optional[str] = get_answer_for_question(best_match, Knowledgebase)
            print(f'Bot: {answer}')
        else:
            print('Bot: I don\'t know the answer. Can you teach me?')
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                Knowledgebase["questions"].append({"question": user_input, "answer": new_answer})
                save_Knowlegebase('Knowledgebase.json', Knowledgebase)
                print('Bot: Thank you! I learned a new response!')

if __name__ == '__main__':
    chat_bot()