**RepliSense**

**🧠 AI-Powered Customer Review Analyzer (LangGraph + LangChain)**
This project demonstrates how to build a multi-step, LLM-powered workflow for analyzing customer reviews using LangGraph and LangChain.
The system detects sentiment, performs a diagnosis of negative reviews, and generates empathetic automated responses.

**🚀 Features**
	Sentiment Analysis → Classifies reviews as positive or negative.
	Diagnosis of Negative Reviews → Identifies:
	Issue Type (UX, Performance, Bug, Support, Other)
	Tone (angry, frustrated, disappointed, calm)
	Urgency (low, medium, high)

**Automated Responses →**
	Thank-you notes for positive reviews.
	Empathetic, helpful replies for negative reviews.

**Workflow Orchestration → Powered by LangGraph with conditional logic and state management.**

**🛠️ Tech Stack**
	LangChain – for LLM integration and structured outputs
 
	LangGraph – for workflow orchestration
	OpenAI – GPT-4o-mini model
	Pydantic – for schema validation
	Python Dotenv – for environment variable management

**📂 Project Structure**
. ├── review_analyzer.py # Main code (workflow definition + test run) ├── .env # Environment variables (contains API keys) ├── requirements.txt # Python dependencies └── README.md # Project documentation

**▶️ Usage**

**Run the workflow with a sample review:** python replisense.py 

**Example input:**

initial_state = { 'review': 'I am trying to play this game for a long time, its hanging every now and then, its frustrating' }

**Example output**

{ "review": "I am trying to play this game for a long time, its hanging every now and then, its frustrating", "sentiments": "negative", "diagnosis": { "issue_type": "Performance", "tone": "frustrated", "urgency": "high" }, "response": "We’re really sorry you had this experience. It sounds frustrating dealing with repeated performance issues. Our team is actively working on improving stability, and your feedback helps us prioritize this. Thank you for your patience." }

**🧩 Workflow Design The workflow is built as a LangGraph StateGraph: START → find_sentiments → [positive_response | run_diagonis → negative_response] → END**

Positive Review → Directly generates a warm thank-you note. Negative Review → Runs a detailed diagnosis, then generates an empathetic resolution message.
