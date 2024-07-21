import random
import ollama

def generate_base_prompt():
    seasons = ["spring", "summer", "fall", "winter"]
    crop_types = ["vegetables", "fruits", "grains", "herbs"]
    farming_activities = ["planting", "harvesting", "irrigation", "pest control", "soil management", "crop rotation"]
    challenges = ["drought", "heavy rainfall", "pest infestation", "market fluctuations", "labor shortage", "equipment failure"]
    farm_sizes = ["small family farm", "large commercial farm", "urban garden", "hydroponic setup"]
    farming_methods = ["organic", "conventional", "permaculture", "vertical farming", "aquaponics"]

    season = random.choice(seasons)
    crop = random.choice(crop_types)
    activity = random.choice(farming_activities)
    challenge = random.choice(challenges)
    farm_size = random.choice(farm_sizes)
    method = random.choice(farming_methods)

    prompt = f"You are a farmer managing a {farm_size} using {method} techniques. It's {season}, and you're focusing on {crop}. You're currently dealing with {activity}, but facing a challenge related to {challenge}. Describe the situation and ask for advice."

    return prompt

def generate_farming_prompt(base_prompt):
    try:
        response = ollama.generate(model="llama2", prompt=f"Based on the following scenario, generate a detailed and engaging farming-related prompt:\n\n{base_prompt}\n\nGenerated prompt:")
        return response['response'].strip()
    except Exception as e:
        print(f"Error generating prompt with Ollama: {e}")
        return base_prompt

def main():
    print("Dynamic Farming Prompts Generator")
    print("=================================")

    while True:
        base_prompt = generate_base_prompt()
        enhanced_prompt = generate_farming_prompt(base_prompt)

        print("\nGenerated Prompt:")
        print(enhanced_prompt)

        user_input = input("\nPress Enter to generate another prompt, or type 'q' to quit: ")
        if user_input.lower() == 'q':
            break

    print("Thank you for using the Dynamic Farming Prompts Generator!")

if __name__ == "__main__":
    main()
