from langgraph.graph import StateGraph,START,END
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from typing import TypedDict , Literal
from pydantic import BaseModel ,Field


# Load environment variables
load_dotenv()

#LLM
model = ChatOpenAI(model='gpt-4o-mini')

# Structured output schema 1 - Diagnosis
class DiagnosisSchema(BaseModel):
    issue_type: Literal["UX", "Performance", "Bug", "Support", "Other"] = Field(description='The category of issue mentioned in the review')
    tone: Literal["angry", "frustrated", "disappointed", "calm"] = Field(description='The emotional tone expressed by the user')
    urgency: Literal["low", "medium", "high"] = Field(description='How urgent or critical the issue appears to be')
structured_model_diagnosis = model.with_structured_output(DiagnosisSchema)

# Structured output schema 2 - Sentiment
class SentimentSchema(BaseModel):
    sentiments : Literal['positive','negative'] = Field(description = " This shows sentiments of the reviewer")
structured_model_sentiments = model.with_structured_output(SentimentSchema)



## Define State
class ReviewState(TypedDict):
    review : str
    sentiments : Literal["positive", "negative"]
    diagnosis  : dict
    response : str


# Define nodes
def find_sentiments(state: ReviewState):
    prompt = f"What is the sentiments of this review {state['review']}"
    sentiments = structured_model_sentiments.invoke(prompt).sentiments
    return {"sentiments": sentiments}


def check_sentiments(state:ReviewState) -> Literal ["positive_response" , "run_diagonis"]:
    if state['sentiments'] == "positive":
        return "positive_response"
    else:
        return "run_diagonis"
    
def positive_response(state: ReviewState):
    prompt ="Write a warn thankful message in the response  of the review "
    result = model.invoke(prompt).content
    return {"response": result}

def run_diagonis(state :ReviewState):
    prompt=f""" You are a helpful assistance find out negative response in the review : \n {state['review']} \n "
    "Return  issue_type ,tone, urgency """
    result = structured_model_diagnosis.invoke(prompt)
    return { "diagnosis" : result.model_dump()}


def negative_response(state: ReviewState):   
    diagnosis = state['diagnosis']
    prompt = f""" You are an intelligent support assistance , the user has expressed 
   '{diagnosis['issue_type']}' had sound '{diagnosis['tone']}' and raised urgency '{diagnosis['urgency']}'
    write an empathic and helpful resolution."""
    result = model.invoke(prompt).content
    return  {"response" : result}




# Create Graph
graph = StateGraph(ReviewState)

graph.add_node('find_sentiments',find_sentiments)
graph.add_node('positive_response',positive_response)
graph.add_node('negative_response',negative_response)
graph.add_node('run_diagonis',run_diagonis)

graph.add_edge(START,'find_sentiments')
graph.add_conditional_edges('find_sentiments',check_sentiments)
graph.add_edge('positive_response',END)
graph.add_edge('run_diagonis','negative_response')
graph.add_edge('negative_response',END)

workflow = graph.compile()

# Test
initial_state= {'review' : 'I am trying to  play this game for a long time , its hanging every now and then , its frustating '}
final_state = workflow.invoke(initial_state)

#Final output
print(final_state)




