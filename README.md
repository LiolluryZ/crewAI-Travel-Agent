# CrewAI Travel Agents

This project explain step by step the concept of AI Agents applied to travel planning.

## Step 1: Write a forst set of agents

- **Macro Planning Agent**: This agent is responsible for creating a high-level travel itinerary based on user preferences, budget, and time constraints. It identifies key destinations, travel dates, and major activities.
- **Activity Planner Agent**: This agent focuses on detailing the activities and experiences at each destination. It suggests tours, cultural experiences, dining options, and local attractions.
- **Food Planner Agent**: This agent specializes in curating dining experiences, recommending restaurants, local cuisines, and food tours based on user preferences and dietary restrictions.
- **Accommodation Planner Agent**: This agent finds and suggests accommodations that fit the user's budget, preferences, and location needs. It considers factors like proximity to attractions, amenities, and user reviews.

This a "dumb" implementation, there are no customization for user preferences, but it is a good start to understand how to use agents to create a travel plan.

## Step 2 : Force data output

To ensure that each agent outputs data in a structured format, we can define a common schema for the output. Each agent will return its results in a JSON format, which can be easily parsed and integrated into a final travel plan.

## Step 3 : Add tools

To enhance the capabilities of each agent, we can integrate various tools and APIs. For example:
- Serper API for web search to gather up-to-date information on destinations, activities, and accommodations.
- Scrapper tools to extract data from travel websites and review platforms.

More specific tools can be added for each agent to improve their performance and the quality of their recommendations, but this is paid feature.

## Step 4 : Add custom tools

Custom tools can be developed to address specific needs or challenges in travel planning. For example:
- An optical passport reader tool to help users quickly input their passport information.
- A user input tool to add capabilities for AI to ask questions to the user to refine their preferences and requirements.

## Step 5 : Workflow

To create a seamless travel planning experience, we can design a workflow that orchestrates the interactions between the different agents. The workflow will ensure that each agent receives the necessary input from the previous agent and passes its output to the next agent in the sequence.

## How to start 

Fill the `.env` file with your API keys.

different steps can be start with the following commands:

```bash
poetry run step1
poetry run step2
poetry run step3
poetry run step4
poetry run step5
```