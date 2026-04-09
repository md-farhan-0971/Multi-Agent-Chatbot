from langchain_groq import ChatGroq
from agency.state import AgencyState
import os
from dotenv import load_dotenv

load_dotenv()

# Initialize the Free Groq LLM (Using Meta's Llama 3 8B model)
llm = ChatGroq(temperature=0.5, model_name="llama-3.1-8b-instant")

def researcher_node(state: AgencyState):
    print("--- RESEARCHER WORKING ---")
    topic = state["topic"]
    prompt = f"You are a senior researcher. Gather 3 key factual bullet points about: {topic}"
    response = llm.invoke(prompt)
    
    return {"research_notes": response.content}

def writer_node(state: AgencyState):
    print("--- WRITER WORKING ---")
    topic = state["topic"]
    notes = state.get("research_notes", "")
    feedback = state.get("feedback", "")
    
    prompt = f"""You are an expert copywriter. Write a short, engaging article on {topic}.
    Use these facts: {notes}.
    If there is feedback from the editor, apply it: {feedback}"""
    
    response = llm.invoke(prompt)
    current_count = state.get("revision_count", 0)
    
    return {"draft": response.content, "revision_count": current_count + 1}

def editor_node(state: AgencyState):
    print("--- EDITOR WORKING ---")
    draft = state["draft"]
    
    prompt = f"""You are a strict editor. Review this draft:
    {draft}
    If it is good, reply with exactly 'APPROVED'. 
    If it needs work, provide 1 short sentence of feedback."""
    
    response = llm.invoke(prompt)
    return {"feedback": response.content}