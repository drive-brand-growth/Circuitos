"""
Advanced File Chunking Strategies for RAG
Handles: Documents, Audio transcripts, Websites, Code, Structured data
"""

from typing import List, Dict, Any
import re
from pathlib import Path
from dataclasses import dataclass
from enum import Enum


class ChunkStrategy(Enum):
    """Different chunking strategies for different content types"""
    FIXED_SIZE = "fixed_size"
    SEMANTIC = "semantic"
    RECURSIVE = "recursive"
    MARKDOWN = "markdown"
    CODE = "code"
    AUDIO_TRANSCRIPT = "audio_transcript"
    STRUCTURED = "structured"


@dataclass
class Chunk:
    """Represents a chunk of text with metadata"""
    text: str
    metadata: Dict[str, Any]
    chunk_id: str
    source: str
    strategy: ChunkStrategy


class FileChunker:
    """Main chunking orchestrator"""

    def __init__(self, chunk_size: int = 1000, chunk_overlap: int = 200):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk_text(self, text: str, metadata: Dict[str, Any],
                   strategy: ChunkStrategy = ChunkStrategy.RECURSIVE) -> List[Chunk]:
        """Route to appropriate chunking strategy"""

        strategies = {
            ChunkStrategy.FIXED_SIZE: self._chunk_fixed_size,
            ChunkStrategy.SEMANTIC: self._chunk_semantic,
            ChunkStrategy.RECURSIVE: self._chunk_recursive,
            ChunkStrategy.MARKDOWN: self._chunk_markdown,
            ChunkStrategy.CODE: self._chunk_code,
            ChunkStrategy.AUDIO_TRANSCRIPT: self._chunk_audio_transcript,
            ChunkStrategy.STRUCTURED: self._chunk_structured
        }

        return strategies[strategy](text, metadata)

    # ========================================
    # Strategy 1: Fixed Size (Simple)
    # ========================================

    def _chunk_fixed_size(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Simple fixed-size chunking with overlap
        Good for: General text, simple documents
        """
        chunks = []
        start = 0
        chunk_num = 0

        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end]

            chunks.append(Chunk(
                text=chunk_text,
                metadata={**metadata, "chunk_num": chunk_num},
                chunk_id=f"{metadata.get('source', 'unknown')}_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.FIXED_SIZE
            ))

            start += self.chunk_size - self.chunk_overlap
            chunk_num += 1

        return chunks

    # ========================================
    # Strategy 2: Semantic (Smart Boundaries)
    # ========================================

    def _chunk_semantic(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Chunk at semantic boundaries (paragraphs, sentences)
        Good for: Articles, blog posts, documentation
        """
        # Split into paragraphs first
        paragraphs = text.split('\n\n')
        chunks = []
        current_chunk = ""
        chunk_num = 0

        for para in paragraphs:
            # If adding this paragraph exceeds chunk size, save current chunk
            if len(current_chunk) + len(para) > self.chunk_size and current_chunk:
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    metadata={**metadata, "chunk_num": chunk_num, "type": "paragraph"},
                    chunk_id=f"{metadata.get('source', 'unknown')}_semantic_{chunk_num}",
                    source=metadata.get('source', 'unknown'),
                    strategy=ChunkStrategy.SEMANTIC
                ))
                current_chunk = para
                chunk_num += 1
            else:
                current_chunk += "\n\n" + para if current_chunk else para

        # Add final chunk
        if current_chunk:
            chunks.append(Chunk(
                text=current_chunk.strip(),
                metadata={**metadata, "chunk_num": chunk_num, "type": "paragraph"},
                chunk_id=f"{metadata.get('source', 'unknown')}_semantic_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.SEMANTIC
            ))

        return chunks

    # ========================================
    # Strategy 3: Recursive (Hierarchical)
    # ========================================

    def _chunk_recursive(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Recursive chunking with hierarchy preservation
        Good for: Long documents, technical content
        Try to split by: \n\n, then \n, then sentences, then words
        """
        separators = ["\n\n\n", "\n\n", "\n", ". ", " "]
        return self._recursive_split(text, separators, metadata)

    def _recursive_split(self, text: str, separators: List[str],
                        metadata: Dict, chunk_num: int = 0) -> List[Chunk]:
        """Recursively split text using separator hierarchy"""
        chunks = []

        if not separators or len(text) <= self.chunk_size:
            # Base case: no more separators or text is small enough
            return [Chunk(
                text=text,
                metadata={**metadata, "chunk_num": chunk_num},
                chunk_id=f"{metadata.get('source', 'unknown')}_recursive_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.RECURSIVE
            )]

        separator = separators[0]
        splits = text.split(separator)
        current_chunk = ""

        for split in splits:
            if len(current_chunk) + len(split) <= self.chunk_size:
                current_chunk += separator + split if current_chunk else split
            else:
                if current_chunk:
                    chunks.append(Chunk(
                        text=current_chunk,
                        metadata={**metadata, "chunk_num": len(chunks)},
                        chunk_id=f"{metadata.get('source', 'unknown')}_recursive_{len(chunks)}",
                        source=metadata.get('source', 'unknown'),
                        strategy=ChunkStrategy.RECURSIVE
                    ))

                # If single split is too large, use next separator
                if len(split) > self.chunk_size:
                    sub_chunks = self._recursive_split(split, separators[1:], metadata, len(chunks))
                    chunks.extend(sub_chunks)
                    current_chunk = ""
                else:
                    current_chunk = split

        if current_chunk:
            chunks.append(Chunk(
                text=current_chunk,
                metadata={**metadata, "chunk_num": len(chunks)},
                chunk_id=f"{metadata.get('source', 'unknown')}_recursive_{len(chunks)}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.RECURSIVE
            ))

        return chunks

    # ========================================
    # Strategy 4: Markdown (Structure-Aware)
    # ========================================

    def _chunk_markdown(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Chunk markdown preserving structure (headers, code blocks, lists)
        Good for: Documentation, README files, technical guides
        """
        chunks = []
        current_chunk = ""
        current_header = ""
        chunk_num = 0

        lines = text.split('\n')

        for line in lines:
            # Detect headers
            if line.startswith('#'):
                # Save previous chunk if it exists
                if current_chunk:
                    chunks.append(Chunk(
                        text=current_chunk.strip(),
                        metadata={
                            **metadata,
                            "chunk_num": chunk_num,
                            "header": current_header,
                            "type": "markdown_section"
                        },
                        chunk_id=f"{metadata.get('source', 'unknown')}_md_{chunk_num}",
                        source=metadata.get('source', 'unknown'),
                        strategy=ChunkStrategy.MARKDOWN
                    ))
                    chunk_num += 1

                # Start new chunk with header
                current_header = line.strip('# ')
                current_chunk = line + '\n'

            # Add line to current chunk
            else:
                if len(current_chunk) + len(line) > self.chunk_size and current_chunk:
                    # Save chunk
                    chunks.append(Chunk(
                        text=current_chunk.strip(),
                        metadata={
                            **metadata,
                            "chunk_num": chunk_num,
                            "header": current_header,
                            "type": "markdown_section"
                        },
                        chunk_id=f"{metadata.get('source', 'unknown')}_md_{chunk_num}",
                        source=metadata.get('source', 'unknown'),
                        strategy=ChunkStrategy.MARKDOWN
                    ))
                    chunk_num += 1
                    current_chunk = line + '\n'
                else:
                    current_chunk += line + '\n'

        # Add final chunk
        if current_chunk:
            chunks.append(Chunk(
                text=current_chunk.strip(),
                metadata={
                    **metadata,
                    "chunk_num": chunk_num,
                    "header": current_header,
                    "type": "markdown_section"
                },
                chunk_id=f"{metadata.get('source', 'unknown')}_md_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.MARKDOWN
            ))

        return chunks

    # ========================================
    # Strategy 5: Code (Syntax-Aware)
    # ========================================

    def _chunk_code(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Chunk code preserving function/class boundaries
        Good for: Python, JavaScript, etc.
        """
        chunks = []

        # Detect functions and classes
        function_pattern = r'(def |class |function |const |let |var )'

        splits = re.split(f'({function_pattern})', text)
        current_chunk = ""
        chunk_num = 0

        for i in range(0, len(splits), 2):
            section = splits[i]
            if i + 1 < len(splits):
                section += splits[i + 1]

            if len(current_chunk) + len(section) > self.chunk_size and current_chunk:
                chunks.append(Chunk(
                    text=current_chunk.strip(),
                    metadata={**metadata, "chunk_num": chunk_num, "type": "code"},
                    chunk_id=f"{metadata.get('source', 'unknown')}_code_{chunk_num}",
                    source=metadata.get('source', 'unknown'),
                    strategy=ChunkStrategy.CODE
                ))
                chunk_num += 1
                current_chunk = section
            else:
                current_chunk += section

        if current_chunk:
            chunks.append(Chunk(
                text=current_chunk.strip(),
                metadata={**metadata, "chunk_num": chunk_num, "type": "code"},
                chunk_id=f"{metadata.get('source', 'unknown')}_code_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.CODE
            ))

        return chunks

    # ========================================
    # Strategy 6: Audio Transcript (Time-Aware)
    # ========================================

    def _chunk_audio_transcript(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Chunk audio transcripts preserving timestamps and speaker info
        Good for: Your 50+ MB audio training files!

        Expected format:
        [00:00:15] Speaker 1: Training module introduction...
        [00:02:30] Speaker 2: Now let's discuss...
        """
        chunks = []

        # Split by timestamps
        timestamp_pattern = r'\[(\d{2}:\d{2}:\d{2})\]'
        splits = re.split(f'({timestamp_pattern})', text)

        current_chunk = ""
        current_timestamp = "00:00:00"
        chunk_num = 0

        i = 0
        while i < len(splits):
            # Check if this is a timestamp
            if re.match(timestamp_pattern, splits[i]):
                timestamp = splits[i].strip('[]')

                # Get the text after this timestamp
                if i + 1 < len(splits):
                    segment = splits[i] + splits[i + 1]

                    if len(current_chunk) + len(segment) > self.chunk_size and current_chunk:
                        # Save current chunk
                        chunks.append(Chunk(
                            text=current_chunk.strip(),
                            metadata={
                                **metadata,
                                "chunk_num": chunk_num,
                                "start_time": current_timestamp,
                                "type": "audio_transcript"
                            },
                            chunk_id=f"{metadata.get('source', 'unknown')}_audio_{chunk_num}",
                            source=metadata.get('source', 'unknown'),
                            strategy=ChunkStrategy.AUDIO_TRANSCRIPT
                        ))
                        chunk_num += 1
                        current_chunk = segment
                        current_timestamp = timestamp
                    else:
                        if not current_chunk:
                            current_timestamp = timestamp
                        current_chunk += segment

                    i += 2
                else:
                    i += 1
            else:
                i += 1

        # Add final chunk
        if current_chunk:
            chunks.append(Chunk(
                text=current_chunk.strip(),
                metadata={
                    **metadata,
                    "chunk_num": chunk_num,
                    "start_time": current_timestamp,
                    "type": "audio_transcript"
                },
                chunk_id=f"{metadata.get('source', 'unknown')}_audio_{chunk_num}",
                source=metadata.get('source', 'unknown'),
                strategy=ChunkStrategy.AUDIO_TRANSCRIPT
            ))

        return chunks

    # ========================================
    # Strategy 7: Structured (JSON/CSV)
    # ========================================

    def _chunk_structured(self, text: str, metadata: Dict) -> List[Chunk]:
        """
        Chunk structured data (JSON, CSV, tables)
        Good for: Database exports, API responses, spreadsheets
        """
        import json

        chunks = []

        try:
            # Try to parse as JSON
            data = json.loads(text)

            # If it's a list, chunk by items
            if isinstance(data, list):
                for i, item in enumerate(data):
                    chunks.append(Chunk(
                        text=json.dumps(item, indent=2),
                        metadata={
                            **metadata,
                            "chunk_num": i,
                            "item_index": i,
                            "type": "json_item"
                        },
                        chunk_id=f"{metadata.get('source', 'unknown')}_json_{i}",
                        source=metadata.get('source', 'unknown'),
                        strategy=ChunkStrategy.STRUCTURED
                    ))

            # If it's a dict, chunk by keys
            elif isinstance(data, dict):
                for i, (key, value) in enumerate(data.items()):
                    chunks.append(Chunk(
                        text=json.dumps({key: value}, indent=2),
                        metadata={
                            **metadata,
                            "chunk_num": i,
                            "key": key,
                            "type": "json_key"
                        },
                        chunk_id=f"{metadata.get('source', 'unknown')}_json_{i}",
                        source=metadata.get('source', 'unknown'),
                        strategy=ChunkStrategy.STRUCTURED
                    ))

        except json.JSONDecodeError:
            # Fall back to fixed size if not valid JSON
            return self._chunk_fixed_size(text, metadata)

        return chunks


# ========================================
# Usage Examples
# ========================================

if __name__ == "__main__":
    chunker = FileChunker(chunk_size=1000, chunk_overlap=200)

    # Example 1: Chunk a markdown file
    markdown_text = """
# Training Module 1: Introduction

Welcome to the first module...

## Section 1.1: Getting Started

Here's how to begin...

## Section 1.2: Core Concepts

Let's explore the fundamentals...
"""

    md_chunks = chunker.chunk_text(
        markdown_text,
        metadata={"source": "training_module_1.md", "type": "training"},
        strategy=ChunkStrategy.MARKDOWN
    )

    print(f"Created {len(md_chunks)} markdown chunks")

    # Example 2: Chunk audio transcript
    audio_text = """
[00:00:15] Instructor: Welcome to this training session on bodybuilding nutrition.
[00:02:30] Instructor: Let's start with protein requirements...
[00:05:45] Instructor: Now, carbohydrates are crucial for energy...
"""

    audio_chunks = chunker.chunk_text(
        audio_text,
        metadata={"source": "nutrition_training.mp3", "duration": "30:00"},
        strategy=ChunkStrategy.AUDIO_TRANSCRIPT
    )

    print(f"Created {len(audio_chunks)} audio transcript chunks")

    # Example 3: Chunk Python code
    code_text = """
def calculate_macros(weight, goal):
    protein = weight * 1.2
    return protein

class Athlete:
    def __init__(self, name):
        self.name = name
"""

    code_chunks = chunker.chunk_text(
        code_text,
        metadata={"source": "nutrition_calculator.py"},
        strategy=ChunkStrategy.CODE
    )

    print(f"Created {len(code_chunks)} code chunks")
