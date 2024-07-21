import csv
import logging
import random
import pandas as pd
import json
from typing import List, Dict
from datetime import datetime, timedelta

# Path to the CSV file for storing prompts and responses
DATA_FILE = "prompts_and_responses.csv"

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load entities from JSON files
def load_entities(file_path: str) -> List[str]:
    with open(file_path, 'r') as f:
        return json.load(f)

LOCATIONS = load_entities('locations.json')
CROPS = load_entities('crops.json')
ENTITIES = load_entities('entities.json')

# Additional dictionaries for more diverse prompts
FARM_TYPES = ["organic", "conventional", "biodynamic", "permaculture", "hydroponic", "aquaponic", "vertical", "urban", "rooftop", "greenhouse", "open-field", "no-till", "conservation agriculture"]
CHALLENGES = ["pest infestation", "soil erosion", "water scarcity", "climate change", "market fluctuations", "labor shortage", "increasing input costs", "crop diseases", "biodiversity loss", "soil degradation"]
GOALS = ["increase yield", "improve soil health", "reduce water usage", "enhance biodiversity", "minimize chemical inputs", "optimize resource efficiency", "expand market reach", "implement sustainable practices", "reduce carbon footprint", "improve crop resilience"]
TECHNIQUES = ["crop rotation", "companion planting", "integrated pest management", "cover cropping", "mulching", "composting", "precision agriculture", "agroforestry", "intercropping", "conservation tillage"]
TIME_FRAMES = ["this growing season", "over the next five years", "in the long term", "year-round", "during the transition period", "in the off-season", "throughout the crop cycle"]

# Enhanced prompt templates
PROMPT_TEMPLATES = [
    "A {farm_size} acre {farm_type} farm in {location} growing {crop1} and {crop2} is facing {challenge}. How can they use {technique} and {entity} to {goal} {time_frame}?",
    "In {location}, a farmer wants to transition their {farm_size} acre {crop1} farm from {farm_type} to a more sustainable model. What steps should they take to implement {technique} and {entity} to {goal}?",
    "A community-supported agriculture (CSA) project in {location} is diversifying their {farm_size} acre {farm_type} farm. How can they integrate {crop1}, {crop2}, and {entity} to {goal} while addressing {challenge}?",
    "{farm_type} farmers in {location} are experimenting with {technique} for their {crop1} and {crop2} crops. What role can {entity} play in helping them {goal} and overcome {challenge}?",
    "An agri-tech startup in {location} is developing solutions for {farm_type} {crop1} farms. How can they leverage {entity} and {technique} to help farmers {goal} and address {challenge} {time_frame}?",
    "Climate change is affecting {crop1} yields in {location}. How can {farm_type} farmers adapt using {entity}, {technique}, and possibly introducing {crop2} as a resilient alternative to {goal}?",
    "A {farm_size} acre {farm_type} farm in {location} wants to implement a closed-loop system. How can they integrate {crop1}, {crop2}, and {entity} along with {technique} to {goal} and minimize waste?",
    "Indigenous farmers in {location} are blending traditional {crop1} cultivation with modern {farm_type} practices. How can they use {entity} and {technique} to {goal} while preserving cultural heritage?",
    "A research institute in {location} is studying the effects of {entity} on {crop1} and {crop2} in {farm_type} systems. What experimental design using {technique} could help them {goal} and address {challenge}?",
    "Urban planners in {location} are incorporating {farm_type} agriculture into city development. How can they use {entity} and {technique} in {crop1} and {crop2} production to {goal} and tackle {challenge}?",
    "A {farm_size} acre {farm_type} {crop1} farm in {location} is struggling with {challenge}. What innovative applications of {entity} and {technique} could help them {goal} {time_frame}?",
    "Regenerative {farm_type} farmers in {location} are focusing on soil health. How can they use {entity} and {technique} in their {crop1} and {crop2} rotations to {goal} and address {challenge}?",
    "A cooperative of small-scale {farm_type} farmers in {location} is pooling resources to implement {technique}. How can they incorporate {entity} in their {crop1} and {crop2} production to {goal}?",
    "Agricultural educators in {location} are developing a curriculum on {farm_type} farming. How can they use {entity} and {technique} in practical exercises with {crop1} and {crop2} to teach students to {goal}?",
    "A {farm_type} seed bank in {location} is working to preserve heirloom varieties of {crop1} and {crop2}. How can they use {entity} and {technique} to {goal} and ensure genetic diversity?",
]

def generate_prompt() -> str:
    """Generates a single, dynamic prompt using the templates and entities."""
    template = random.choice(PROMPT_TEMPLATES)
    return template.format(
        location=random.choice(LOCATIONS),
        farm_size=str(random.randint(1, 1000)),
        farm_type=random.choice(FARM_TYPES),
        crop1=random.choice(CROPS),
        crop2=random.choice(CROPS),
        entity=random.choice(ENTITIES),
        challenge=random.choice(CHALLENGES),
        goal=random.choice(GOALS),
        technique=random.choice(TECHNIQUES),
        time_frame=random.choice(TIME_FRAMES)
    )

def generate_fake_response(prompt: str) -> str:
    """Generates a fake response based on keywords in the prompt."""
    words = prompt.lower().split()
    response_parts = []

    if "organic" in words:
        response_parts.append("Consider implementing organic pest control methods and natural fertilizers.")
    if "climate change" in prompt.lower():
        response_parts.append("Adapt crop varieties and planting schedules to changing climate patterns.")
    if "water scarcity" in prompt.lower():
        response_parts.append("Implement water-efficient irrigation systems like drip irrigation or rainwater harvesting.")
    if "soil health" in prompt.lower():
        response_parts.append("Focus on building organic matter through cover cropping and minimal tillage.")
    if "biodiversity" in prompt.lower():
        response_parts.append("Integrate polyculture systems and create habitat corridors for beneficial insects and wildlife.")

    if not response_parts:
        response_parts.append("Implement sustainable farming practices tailored to your specific crop and location.")
        response_parts.append("Consult with local agricultural extension services for region-specific advice.")

    return " ".join(response_parts)

def generate_data(num_prompts: int) -> None:
    """Generates synthetic data by creating prompts and fake responses."""
    with open(DATA_FILE, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Prompt", "Response", "Generation Date"])

        for _ in range(num_prompts):
            prompt = generate_prompt()
            response = generate_fake_response(prompt)
            generation_date = (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d")
            writer.writerow([prompt, response, generation_date])
            logging.info(f"Prompt: {prompt}\nResponse: {response}\nGeneration Date: {generation_date}\n")

def analyze_data(data: pd.DataFrame) -> Dict[str, int]:
    """Analyzes the generated data and returns some basic statistics."""
    stats = {
        "total_prompts": len(data),
        "unique_crops": len(data['Prompt'].str.extractall(r'growing (\w+)')[0].unique()),
        "unique_locations": len(data['Prompt'].str.extractall(r'in (\w+)')[0].unique()),
        "challenges_mentioned": sum(data['Prompt'].str.contains('|'.join(CHALLENGES), case=False)),
        "techniques_mentioned": sum(data['Prompt'].str.contains('|'.join(TECHNIQUES), case=False))
    }
    return stats

def main():
    num_prompts = 1000
    generate_data(num_prompts)

    # Read the CSV file
    data = pd.read_csv(DATA_FILE)

    # Analyze the data
    stats = analyze_data(data)
    logging.info("Data Analysis Results:")
    for key, value in stats.items():
        logging.info(f"{key}: {value}")

    logging.info(f"Data for {num_prompts} prompts saved to {DATA_FILE}")

if __name__ == "__main__":
    main()
