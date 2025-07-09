# business_graph.py

import json
import pandas as pd
from langgraph.graph import StateGraph, END
from Utils import AgentState, BusinessRecord
import OpenAI_LLM


llm = OpenAI_LLM()

# Input Node
def input_node(state: dict) -> dict:
    raw = input("Paste your JSON data:\n")
    parsed = AgentState.parse_raw(raw)
    return parsed.dict()

# Metric Calculation Node
def compute_metrics(state: dict) -> dict:
    agent = AgentState(**state)
    df = pd.DataFrame([r.dict() for r in agent.data])

    agent.profit = float(df["revenue"].sum() - df["cost"].sum())
    if df["customers_acquired"].sum() > 0:
        agent.cac = float(df["customer_acquisition_cost"].sum() / df["customers_acquired"].sum())
    else:
        agent.cac = None

    print(f"\n📊 Profit: {agent.profit}")
    print(f"📈 CAC: {agent.cac}")
    return agent.dict()

# Recommendation Node
def recommend_node(state: dict) -> dict:
    agent = AgentState(**state)
    prompt = (
        f"You are a business advisor.\n"
        f"Based on the following metrics:\n"
        f"Profit: {agent.profit}\n"
        f"CAC: {agent.cac}\n"
        f"Provide a short recommendation to improve business performance."
    )
    recommendation = llm.ask(prompt)
    agent.recommendation = recommendation
    print(f"\n💡 Recommendation: {recommendation}")
    return agent.dict()

def create_graph()->StateGraph:
    builder = StateGraph(dict)
    builder.add_node("input", input_node)
    builder.add_node("metrics", compute_metrics)
    builder.add_node("recommend", recommend_node)

    builder.set_entry_point("input")
    builder.add_edge("input", "metrics")
    builder.add_edge("metrics", "recommend")
    builder.add_edge("recommend", END) 
    graph = builder.compile()
    return graph  