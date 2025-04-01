from dataclasses import dataclass

@dataclass(frozen=True)
class UIPrompts:
    """User interface prompts for the RAG Assistant."""
    welcome: str = "Hello! I'm your RAG Assistant. How can I help you learn about vitamins today?"
    kb_populated: str = "✅ Knowledge base populated!"
    error_prefix: str = "❌ Error:"

@dataclass(frozen=True)
class ActionLabels:
    """Labels and descriptions for UI actions."""
    populate_kb_label: str = "Populate Knowledge Base"
    populate_kb_desc: str = "Load or reload the vitamin knowledge base"