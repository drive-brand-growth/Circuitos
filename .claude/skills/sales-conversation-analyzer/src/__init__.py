"""
Sales Conversation Analyzer Package
"""

from .analyzer import SalesConversationAnalyzer, RealTimeAssistant, ConversationAnalysis
from .pattern_detector import PatternDetector
from .buyer_signal_detector import BuyerSignalDetector
from .flow_analyzer import FlowAnalyzer
from .gap_analyzer import GapAnalyzer
from .vector_store import VectorStore

__all__ = [
    "SalesConversationAnalyzer",
    "RealTimeAssistant",
    "ConversationAnalysis",
    "PatternDetector",
    "BuyerSignalDetector",
    "FlowAnalyzer",
    "GapAnalyzer",
    "VectorStore"
]

__version__ = "1.0.0"
