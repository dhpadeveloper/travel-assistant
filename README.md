Singapore Travel Planning Assistant
An AI-powered Singapore travel assistant leveraging Retrieval-Augmented Generation (RAG) for local travel knowledge and Model Context Protocol (MCP) for live currency conversion and current weather information.
Project Links
•	GitHub Repository:  https://github.com/dhpadeveloper/travel-assistant
•	Demo Video: https://nagarro-my.sharepoint.com/:v:/p/harsh_bhagwani/IQA7sEbzLGy0RphfjsTl661tAVBJvPpsutYeEOUIpyO3hIg?e=tTdnaR
________________________________________
Architecture & Workflow

 
________________________________________

Knowledge Base
The Knowledge Base contains information about Singapore used for destination-related factual questions.
The documents cover:
•	Singapore overview
•	Attractions
•	Neighborhoods
•	Transportation
•	Culture
•	Practical travel information
•	Food and local experiences
•	Itinerary information
•	Indoor and outdoor activities
Knowledge Base Sources
Singapore Basic Information
Source: Singapore - Wikivoyage Travel Guide
https://en.wikivoyage.org/wiki/Singapore
File: singapore_basic_info.txt
Singapore Travel / Itinerary Information
Source: Visit Singapore - Essential Travel Information
https://www.visitsingapore.com/travel-tips/travelling-to-singapore
File: singapore_itinerary.txt
Singapore Things To Do
Source: Visit Singapore - Things to Do
https://www.visitsingapore.com/things-to-do/top-things-to-do
File: singapore_things_to_do.txt
Source title and URL are stored as document metadata so that relevant source references can be provided in the response.
________________________________________
RAG Workflow
1.	Load Singapore travel documents into the Knowledge Base.
2.	Split documents into smaller chunks.
3.	Generate embeddings using the Gemini embedding model.
4.	Store embeddings and metadata in ChromaDB.
5.	User asks a destination-related question.
6.	search_singapore_knowledge retrieves relevant chunks.
7.	Retrieved information is passed to the LLM as grounded context.
8.	The LLM generates the response using the retrieved information.
9.	Source metadata is retained for source references.
10.	If sufficient information is unavailable, the assistant does not guess.
________________________________________
MCP Tools Workflow
Weather MCP
•	User asks about Singapore weather → agent calls the Weather MCP.
•	MCP server runs weather_mcp.py via STDIO.
•	Fetches forecast data from the Open-Meteo API.
•	Returns weather data to the agent.
•	Agent uses the data to provide the final response.
Currency MCP
•	User asks for currency conversion → agent calls the Currency MCP.
•	MCP server runs currency_mcp.py via STDIO.
•	Fetches the latest exchange rate from the Open Exchange Rates API.
•	Converts the requested amount.
•	Returns the conversion data to the agent.
•	Agent provides the final response.
________________________________________
Agent Design
•	The Travel Agent is built using LangChain and the Gemini LLM.
•	The agent connects the following tools:
o	search_singapore_knowledge → retrieves Singapore destination facts from the ChromaDB Knowledge Base.
o	get_singapore_weather → retrieves current/forecast weather through the Weather MCP server.
o	convert_currency → performs currency conversion through the Currency MCP server.
•	MCP tools are discovered using MultiServerMCPClient and added to the agent's tool list.
•	The agent uses the system prompt to decide which tool to call based on the user's question.
•	It combines RAG information, current MCP data, and user preferences to generate travel recommendations.
•	If required information is unavailable, the agent states that it cannot verify the information instead of guessing.
________________________________________
Prompt Strategy
A system prompt controls how the agent uses the different information sources.
The prompt establishes a clear separation between:
•	Knowledge Base → destination facts
•	MCP Tools → current information
•	LLM → recommendations and itinerary planning
1. Role / System Prompt
What it does: Sets the assistant's role as a Singapore travel planning assistant.
Why: Keeps responses professional, concise, structured, and travel-focused.
2. RAG Guardrails
What it does: Instructs the LLM to use retrieved Knowledge Base content for Singapore destination facts.
Why: If the Knowledge Base does not contain enough information, the assistant states that the information is unavailable instead of making up facts.
3. Smart Tool Routing
What it does: Instructs the assistant when to use the Knowledge Base versus MCP tools.
Why: Currency conversion and current weather information are obtained through MCP tools instead of relying on potentially outdated model knowledge.
4. User Context
What it does: Preserves relevant preferences from the conversation, such as trip duration, interests, budget, and preferred travel pace.
Why: Allows the assistant to provide context-aware recommendations without requiring the user to repeat their preferences.
________________________________________
Setup Instructions
Prerequisites
Install:
•	Python
•	uv
•	Google Gemini API key
The project uses:
•	Python
•	LangChain
•	Google Gemini
•	ChromaDB
•	MCP
•	Streamlit
•	uv
Step 1: Clone the Project
git clone <repository-url>
cd travel-assistant
Step 2: Install Dependencies
This project uses uv for environment and dependency management.
uv sync
If you are using an existing requirements.txt instead of pyproject.toml, install it with:
uv pip install -r requirements.txt
For the recommended project setup, use uv sync with dependencies declared in pyproject.toml.
Step 3: Configure Environment Variables
Create a .env file in the project root:
GOOGLE_API_KEY=your_google_api_key
The application loads environment variables using:
from dotenv import load_dotenv
load_dotenv()
Step 4: Build the Vector Database
Before running the assistant, create the Chroma vector database:
uv run python build_vector_db.py
This loads the Knowledge Base documents, creates embeddings, and stores them in ChromaDB.
Step 5: Run the Application
Start Streamlit:
uv run streamlit run app.py
Streamlit will display the application URL in the terminal.
Open the displayed URL in a browser.
________________________________________
Example Scenarios
Destination Information
Question: What are some top outdoor attractions to visit in Singapore?

Answer: 
Here are some of the top outdoor attractions to visit in Singapore, combining world-class gardens, wildlife reserves, and scenic nature spots:
•	Mandai Wildlife Reserve: A sprawling nature and wildlife hub that houses several renowned attractions, including the Singapore Zoo, Night Safari, River Wonders, the Mandai Boardwalk, and Bird Paradise (Asia's largest bird park, spanning 17 hectares with over 3,500 birds across eight thematic walk-through aviaries).
•	Gardens by the Bay: A futuristic waterfront garden in the Marina district showcasing cutting-edge architecture, iconic Supertrees, and lush botanical displays.
•	Singapore Botanic Gardens: Singapore’s first and only UNESCO World Heritage Site, offering gorgeous walking paths, beautiful lakes, and the world-famous National Orchid Garden.
•	Henderson Waves Bridge: The highest pedestrian bridge in Singapore, known for its unique wave-like architectural design and sweeping panoramic views of the surrounding greenery and city skyline.
•	Bukit Timah Nature Reserve: A rich primary rainforest reserve that contains a greater variety of plant species than the entire North American continent, also home to local wildlife like long-tailed macaques.
•	Pulau Ubin: Located just off Changi Village, this island gives visitors a nostalgic glimpse into rural Singapore ("kampong" life) of the past, with opportunities for island biking and mangrove kayaking.
(Sources: Singapore - Things To Do and Singapore - Wikivoyage Travel Guide)

Question : What is the weather like in Singapore today, and what is ₹20,000 INR in SGD?
Answer:  
•	Weather in Singapore Today:
o	Forecast: Thunderstorms/rain with a 100% probability of precipitation and expected rainfall around 3.2 mm [Retrieved via Weather/Currency MCP].
o	Temperature: High of around 29.5°C and low of 25.3°C [Retrieved via Weather/Currency MCP].
•	Currency Conversion:
o	₹20,000 INR is approximately $266.36 SGD (at an exchange rate of ~0.0133 SGD per INR) [Retrieved via Weather/Currency MCP].

Question: Plan a three-day trip to Singapore and adjust the activities based on the weather forecast
Answer:
Here is your weather-adjusted 3-day itinerary for Singapore. Looking at the forecast, all three days show a high probability of rain and thunderstorms (100%, 84%, and 99% rain probability respectively) [Retrieved via Weather/Currency MCP].
As per our guidelines, outdoor plans have been proactively swapped with world-class indoor alternatives to keep your trip dry and enjoyable!
Day 1: Iconic Architecture & Spectacular Indoor Conservatories
•	Weather: High of 29.5°C, Low of 25.3°C, 100% chance of thunderstorms [Retrieved via Weather/Currency MCP].
•	Morning (Indoor Rain-Proof Plan):
o	Start your morning at Gardens by the Bay by heading straight indoors to the Cloud Forest and Flower Dome. Walk through the mist-filled mountain dome and admire the massive indoor waterfall completely sheltered from the rain.
•	Afternoon:
o	Explore the Marina Bay Sands Shoppes—an expansive, luxury indoor mall connected to the gardens. You can even enjoy an indoor sampan boat ride along the canal.
•	Evening:
o	Head to the Helix Bridge and catch the stunning waterfront views (ducking under sheltered pathways if showers pass), and enjoy a hearty meal at a nearby indoor hawker center or restaurant.
Day 2: Immersive Wildlife & Indoor Marine Wonders
•	Weather: High of 32.2°C, Low of 24.6°C, 84% chance of rain [Retrieved via Weather/Currency MCP].
•	Morning (Weather-Adjusted):
o	While the Singapore Zoo and Mandai Wildlife Reserve feature outdoor trails, River Wonders is a great alternative because much of its main exhibits (including the giant pandas and the massive freshwater aquarium tunnel) are fully sheltered or indoor.
•	Afternoon:
o	If heavy rain persists, skip open-air walks and swap to an all-indoor hub like the ArtScience Museum at Marina Bay Sands or explore the sprawling indoor complexes around Orchard Road.
•	Evening:
o	Experience a fantastic indoor dining experience or a local food tour at an air-conditioned hawker hub like Lau Pa Sat (which features fully covered seating).
Day 3: Sentosa’s Top Indoor Entertainment
•	Weather: High of 30.5°C, Low of 24.8°C, 99% chance of thunderstorms [Retrieved via Weather/Currency MCP].
•	Morning & Afternoon (Weather-Adjusted):
o	Head over to Sentosa Island, but pivot away from the outdoor beaches. Spend your day at Universal Studios Singapore (which has plenty of indoor queue lines, shows, and covered rides) or go entirely indoors at the S.E.A. Aquarium (one of the world's largest aquariums) to marvel at marine life away from the rain.
•	Evening:
o	Wrap up your trip with dinner at VivoCity (Singapore's largest shopping mall, located right next to Sentosa) with extensive indoor dining choices and rooftop views.
Sources:
•	Visit Singapore - Itineraries
•	[Retrieved via Weather/Currency MCP]
