# gaim-bot-v2
## http://ec2-3-87-212-100.compute-1.amazonaws.com/ or https://gaimbotv2.streamlit.app/
This project serves as the front end repository of the Gaim-bot chatbot.
This frontend is a streamlit project that creates a chat interface for querying an AWS Lambda RAG microservice. 
The front end allows users to ask natural languge queries about the videogame Eldin Ring for hints, explanations and more. The chat also provides images of relevant game locations, weapons, armor etc.
The front and backend are also designed to be agnostic to what kind of information you would like the chatbot to answer. Provided you have a vector database of documents relevant to your topic, this RAG chat interface can be used for any topic

## Architecture
See https://github.com/HDWilliams/gaim-bot-backend for more information on the project architecture. 

## Set Up and Running
1. git clone git@github.com:HDWilliams/gaim-bot-v2.git
2. streamlit uses a secrets.toml folder in a '~/.streamlit/secrets.toml' see https://docs.streamlit.io/develop/concepts/connections/secrets-management for proper formatting
3. Include secrets for

   LAMBDA_API_KEY= { API KEY FOR LAMBDA API GATEWAY }

   LAMBDA_GPT_URL= { URL FOR AWS API GATEWAY CONNECTED TO LAMBDA FUNCTION }

   INDEX_NAME= { NAME OF PINECONE INDEX }

   INSTRUCTIONS={ INITIAL MODEL PROMPT }

   INITIAL_MESSAGE= { WELCOME USER MESSAGE ON APP START }
  
6. Set up and connect backend service, see https://github.com/HDWilliams/gaim-bot-backend
7. Run locally with 'streamlit run app.py'
8. Alternatively you can deploy it to streamlit cloud by creating an account and connecting a github account

 
