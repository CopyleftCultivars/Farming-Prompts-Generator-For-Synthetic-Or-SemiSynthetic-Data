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
FARM_TYPES = load_entities('farm_types.json')
CHALLENGES = load_entities('challenges.json')
GOALS = load_entities('goals.json')
TECHNIQUES = load_entities('techniques.json')
TIME_FRAMES = load_entities('time_frames.json')
SOIL_TYPES = load_entities('soil_types.json')
CLIMATE_ZONES = load_entities('climate_zones.json')
FARM_SIZES = load_entities('farm_sizes.json')
CERTIFICATIONS = load_entities('certifications.json')

# Enhanced first-person prompt templates
PROMPT_TEMPLATES = [
    "I'm a {farm_type} farmer in {location} with a {farm_size} farm. We're growing {crop1} and {crop2}, but we're facing {challenge}. How can I use {technique} and {entity} to {goal} {time_frame}?",
    "My family has been farming {crop1} in {location} for generations, but we're noticing changes due to {challenge}. I'm considering transitioning to {farm_type} farming. What steps should I take to implement {technique} and {entity} to {goal}?",
    "I'm part of a community-supported agriculture (CSA) project in {location}. We have a {farm_size} {farm_type} farm and want to diversify. How can we integrate {crop1}, {crop2}, and {entity} to {goal} while addressing {challenge}?",
    "As a {farm_type} farmer in {location}, I'm experimenting with {technique} for my {crop1} and {crop2} crops. What role can {entity} play in helping me {goal} and overcome {challenge}?",
    "I'm developing agri-tech solutions for {farm_type} {crop1} farms in {location}. How can we leverage {entity} and {technique} to help farmers {goal} and address {challenge} {time_frame}?",
    "Climate change is affecting my {crop1} yields here in {location}. As a {farm_type} farmer, how can I adapt using {entity}, {technique}, and possibly introducing {crop2} as a resilient alternative to {goal}?",
    "I manage a {farm_size} {farm_type} farm in {location} and want to implement a closed-loop system. How can I integrate {crop1}, {crop2}, and {entity} along with {technique} to {goal} and minimize waste?",
    "As an indigenous farmer in {location}, I'm blending our traditional {crop1} cultivation with modern {farm_type} practices. How can I use {entity} and {technique} to {goal} while preserving our cultural heritage?",
    "I'm a researcher studying the effects of {entity} on {crop1} and {crop2} in {farm_type} systems in {location}. What experimental design using {technique} could help us {goal} and address {challenge}?",
    "I'm an urban planner in {location} working on incorporating {farm_type} agriculture into our city development. How can we use {entity} and {technique} in {crop1} and {crop2} production to {goal} and tackle {challenge}?",
    "My {farm_size} {farm_type} {crop1} farm in {location} is struggling with {challenge}. What innovative applications of {entity} and {technique} could help me {goal} {time_frame}?",
    "I'm a regenerative {farm_type} farmer in {location} focusing on soil health. How can I use {entity} and {technique} in my {crop1} and {crop2} rotations to {goal} and address {challenge}?",
    "Our cooperative of small-scale {farm_type} farmers in {location} is pooling resources to implement {technique}. How can we incorporate {entity} in our {crop1} and {crop2} production to {goal}?",
    "I'm developing a curriculum on {farm_type} farming for agricultural students in {location}. How can I use {entity} and {technique} in practical exercises with {crop1} and {crop2} to teach students to {goal}?",
    "I manage a {farm_type} seed bank in {location} working to preserve heirloom varieties of {crop1} and {crop2}. How can we use {entity} and {technique} to {goal} and ensure genetic diversity?",
    "As a {farm_type} farmer in {location} with {soil_type} soil, I'm struggling with {challenge}. How can I use {entity} and {technique} to improve my {crop1} and {crop2} yields?",
    "I'm transitioning my {farm_size} farm in {location} to organic production. What strategies involving {entity} and {technique} can help me manage the transition period and {goal}?",
    "Our {farm_type} cooperative in {climate_zone} {location} is facing {challenge}. How can we implement {technique} and utilize {entity} to {goal} for our {crop1} and {crop2} crops?",
    "I'm a vertical farmer in urban {location} growing {crop1} and {crop2}. How can I incorporate {entity} and {technique} to {goal} and address {challenge} in our limited space?",
    "As a {farm_type} farmer in {location} pursuing {certification} certification, how can I use {entity} and {technique} to {goal} while meeting the stringent requirements?",
    "I'm researching climate-resilient farming practices for {crop1} in {climate_zone} {location}. How can {entity} and {technique} be combined to help farmers {goal} in the face of {challenge}?",
    "Our school in {location} is starting a {farm_type} garden to teach students about sustainable agriculture. How can we use {entity} and {technique} with our {crop1} and {crop2} plants to {goal}?",
    "I'm a {farm_type} beekeeper in {location} looking to expand into crop production. How can I integrate {crop1} and {crop2} with my beekeeping operation using {entity} and {technique} to {goal}?",
    "As a {farm_type} farmer in {location}, I'm interested in integrating livestock with my {crop1} and {crop2} production. How can I use {entity} and {technique} to {goal} in a mixed farming system?",
    "I'm part of a {farm_type} farming collective in {location} focusing on {crop1} and {crop2}. How can we use {entity} and {technique} to {goal} while promoting community engagement?"
]

def generate_prompt() -> str:
    """Generates a single, dynamic prompt using the templates and entities."""
    template = random.choice(PROMPT_TEMPLATES)
    return template.format(
        location=random.choice(LOCATIONS),
        farm_size=random.choice(FARM_SIZES),
        farm_type=random.choice(FARM_TYPES),
        crop1=random.choice(CROPS),
        crop2=random.choice(CROPS),
        entity=random.choice(ENTITIES),
        challenge=random.choice(CHALLENGES),
        goal=random.choice(GOALS),
        technique=random.choice(TECHNIQUES),
        time_frame=random.choice(TIME_FRAMES),
        soil_type=random.choice(SOIL_TYPES),
        climate_zone=random.choice(CLIMATE_ZONES),
        certification=random.choice(CERTIFICATIONS)
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
