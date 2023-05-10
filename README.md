## Experiments with LangChain and LLMs to read, summarize, Q&A, take suggestions from our Podcast interview transcripts so that we are able to:

1. Let LLMs summarize our interviews
2. Generate tweets and posts for posting our interviews on social media platforms
3. Ask suggestions about the interview contents
4. Document our interviews, and ask anything straight to the point in a very efficient manner

chain_io.py specified the functions for interacting with LangChain and utilizing vectordb, chains, and LLMs

user_inferface.py is a simple UI built with PyQt5 that you can enter your OpenAI API key, upload any PDF document from your local directory, and start asking anything you want about the content in the document. There is also another section that you can ask for a summarization based on the whole content in the document (This is achieved with LangChain map_reduce). 

You can git clone the code in your local directory, and following the requirement.txt to install required packages and initiate the UI on your local machine. 

### Check out our Podcast (The Craft Podcast): https://www.youtube.com/channel/UCnkFrokyriTDDi-Dw1NXsxA