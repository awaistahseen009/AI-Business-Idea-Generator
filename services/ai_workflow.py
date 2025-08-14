from langgraph.graph import StateGraph, END
from langchain_openai import ChatOpenAI
from typing import TypedDict, List, Dict, Any, Optional
import os
import json
from services.web_search import WebSearchService
from pydantic import BaseModel, Field

class BusinessIdeaModel(BaseModel):
    name: str = Field(description="The startup name")
    pitch: str = Field(description="A one-paragraph pitch for the startup")
    audience: str = Field(description="The target audience")
    revenue_model: str = Field(description="The suggested revenue model")

class BusinessIdeasResponse(BaseModel):
    ideas: List[BusinessIdeaModel] = Field(description="List of exactly 3 business ideas")

class WorkflowState(TypedDict):
    niche: str
    web_search_enabled: bool
    web_search_results: Optional[str]
    generated_ideas: Optional[List[Dict[str, Any]]]
    error: Optional[str]

class BusinessIdeaWorkflow:
    def __init__(self):
        # Configure OpenAI model; API key is read from OPENAI_API_KEY env var
        model_name = os.getenv('OPENAI_MODEL', 'gpt-4o-mini')
        self.llm = ChatOpenAI(
            model=model_name,
            temperature=0.7
        )
        self.web_search_service = WebSearchService()
        self.workflow = self._create_workflow()
    
    def _create_workflow(self) -> StateGraph:
        """Create the LangGraph workflow"""
        workflow = StateGraph(WorkflowState)
        
        # Add nodes
        workflow.add_node("start", self._start_node)
        workflow.add_node("web_search", self._web_search_node)
        workflow.add_node("generate_ideas", self._generate_ideas_node)
        workflow.add_node("format_output", self._format_output_node)
        
        # Add edges
        workflow.set_entry_point("start")
        workflow.add_conditional_edges(
            "start",
            self._should_web_search,
            {
                "search": "web_search",
                "generate": "generate_ideas"
            }
        )
        workflow.add_edge("web_search", "generate_ideas")
        workflow.add_edge("generate_ideas", "format_output")
        workflow.add_edge("format_output", END)
        
        return workflow.compile()
    
    def _start_node(self, state: WorkflowState) -> WorkflowState:
        """Start node - initialize the workflow"""
        return state
    
    def _should_web_search(self, state: WorkflowState) -> str:
        """Conditional edge to determine if web search should be performed"""
        return "search" if state["web_search_enabled"] else "generate"
    
    def _web_search_node(self, state: WorkflowState) -> WorkflowState:
        """Web search node - perform web search if enabled"""
        try:
            niche = state["niche"]
            search_query = f"startup ideas trends opportunities {niche} market analysis 2024"
            
            search_results = self.web_search_service.search(search_query)
            # Expecting dict with keys: text, sources
            if isinstance(search_results, dict):
                state["web_search_results"] = search_results.get("text", "")
                state["web_search_sources"] = search_results.get("sources", [])
            else:
                # Backward compatibility if a plain string is returned
                state["web_search_results"] = search_results or ""
                state["web_search_sources"] = []
            
        except Exception as e:
            print(f"Web search error: {e}")
            state["web_search_results"] = None
            state["error"] = f"Web search failed: {str(e)}"
        
        return state
    
    def _generate_ideas_node(self, state: WorkflowState) -> WorkflowState:
        """Generate business ideas using the LLM"""
        try:
            niche = state["niche"]
            web_data = state.get("web_search_results", "")
            
            # Create the prompt
            prompt = self._create_prompt(niche, web_data)
            
            # Use structured output with Pydantic
            structured_llm = self.llm.with_structured_output(BusinessIdeasResponse)
            
            # Generate ideas
            response = structured_llm.invoke(prompt)
            
            # Convert to dictionary format
            ideas_list = []
            for idea in response.ideas:
                ideas_list.append({
                    "name": idea.name,
                    "pitch": idea.pitch,
                    "audience": idea.audience,
                    "revenue_model": idea.revenue_model
                })
            
            state["generated_ideas"] = ideas_list
            
        except Exception as e:
            print(f"Idea generation error: {e}")
            state["error"] = f"Failed to generate ideas: {str(e)}"
            state["generated_ideas"] = None
        
        return state
    
    def _format_output_node(self, state: WorkflowState) -> WorkflowState:
        """Format the final output"""
        if state.get("generated_ideas"):
            # Ideas are already in the correct format
            pass
        elif state.get("error"):
            # Error handling is already done
            pass
        else:
            state["error"] = "No ideas were generated"
        
        return state
    
    def _create_prompt(self, niche: str, web_data: str = "") -> str:
        """Create the prompt for the LLM"""
        base_prompt = f"""You are a professional startup ideation assistant with expertise in market analysis and business development.

Given the following niche: "{niche}"
"""
        
        if web_data:
            base_prompt += f"""
Recent market research and trends:
{web_data[:2000]}  # Limit web data to avoid token limits
"""
        
        base_prompt += """
Generate EXACTLY 3 innovative and viable startup ideas for this niche.

For each idea, provide:
- A compelling startup name
- A one-paragraph pitch that clearly explains the value proposition
- The specific target audience
- A realistic revenue model

Focus on:
- Market gaps and opportunities
- Scalable business models
- Current technology trends
- Practical implementation

Ensure each idea is unique, feasible, and addresses real market needs."""
        
        return base_prompt
    
    def run_workflow(self, niche: str, web_search_enabled: bool = False) -> Dict[str, Any]:
        """Run the complete workflow"""
        try:
            initial_state = {
                "niche": niche,
                "web_search_enabled": web_search_enabled,
                "web_search_results": None,
                "generated_ideas": None,
                "error": None
            }
            
            # Execute the workflow
            final_state = self.workflow.invoke(initial_state)
            
            if final_state.get("error"):
                return {"error": final_state["error"]}
            
            if final_state.get("generated_ideas"):
                return {
                    "ideas": final_state["generated_ideas"],
                    "web_search_used": web_search_enabled,
                    "niche": niche,
                    "sources": final_state.get("web_search_sources", [])
                }
            else:
                return {"error": "No ideas were generated"}
                
        except Exception as e:
            print(f"Workflow execution error: {e}")
            return {"error": f"Workflow failed: {str(e)}"}
