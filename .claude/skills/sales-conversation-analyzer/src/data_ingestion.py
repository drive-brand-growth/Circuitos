"""
Data Ingestion - Import conversation data from various sources
Supports: Plain text, CSV, TSV, JSON, and database connections
"""

import csv
import json
import os
from typing import Dict, List, Any, Optional, Iterator
from pathlib import Path


class DataIngestion:
    """
    Handles data ingestion from multiple sources
    """

    def __init__(self):
        """Initialize data ingestion"""
        self.supported_formats = ['txt', 'csv', 'tsv', 'json', 'jsonl']

    def ingest_file(self, file_path: str, format: str = None) -> List[Dict[str, Any]]:
        """
        Ingest conversations from a file

        Args:
            file_path: Path to the file
            format: File format (auto-detected if None)

        Returns:
            List of conversation dictionaries
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        # Auto-detect format
        if format is None:
            format = self._detect_format(file_path)

        # Ingest based on format
        if format == 'txt':
            return self._ingest_text(file_path)
        elif format == 'csv':
            return self._ingest_csv(file_path)
        elif format == 'tsv':
            return self._ingest_csv(file_path, delimiter='\t')
        elif format == 'json':
            return self._ingest_json(file_path)
        elif format == 'jsonl':
            return self._ingest_jsonl(file_path)
        else:
            raise ValueError(f"Unsupported format: {format}")

    def ingest_directory(
        self,
        directory_path: str,
        format: str = None,
        recursive: bool = False
    ) -> List[Dict[str, Any]]:
        """
        Ingest all conversation files from a directory

        Args:
            directory_path: Path to directory
            format: File format (processes all if None)
            recursive: Search subdirectories

        Returns:
            List of conversation dictionaries
        """
        if not os.path.isdir(directory_path):
            raise NotADirectoryError(f"Not a directory: {directory_path}")

        conversations = []

        # Get file pattern
        if recursive:
            pattern = '**/*'
        else:
            pattern = '*'

        # Find files
        path_obj = Path(directory_path)

        if format:
            files = path_obj.glob(f"{pattern}.{format}")
        else:
            files = [f for f in path_obj.glob(pattern) if f.is_file()]

        # Ingest each file
        for file_path in files:
            try:
                file_conversations = self.ingest_file(str(file_path), format)
                conversations.extend(file_conversations)
                print(f"✓ Ingested {len(file_conversations)} conversations from {file_path.name}")
            except Exception as e:
                print(f"✗ Error ingesting {file_path.name}: {e}")

        return conversations

    def ingest_database(
        self,
        connection_string: str,
        query: str,
        db_type: str = 'sqlite'
    ) -> List[Dict[str, Any]]:
        """
        Ingest conversations from database

        Args:
            connection_string: Database connection string
            query: SQL query to fetch conversations
            db_type: Database type (sqlite, postgres, mysql)

        Returns:
            List of conversation dictionaries
        """
        if db_type == 'sqlite':
            return self._ingest_sqlite(connection_string, query)
        elif db_type == 'postgres':
            return self._ingest_postgres(connection_string, query)
        elif db_type == 'mysql':
            return self._ingest_mysql(connection_string, query)
        else:
            raise ValueError(f"Unsupported database type: {db_type}")

    def stream_conversations(
        self,
        file_path: str,
        format: str = None,
        batch_size: int = 100
    ) -> Iterator[List[Dict[str, Any]]]:
        """
        Stream conversations in batches (for large files)

        Args:
            file_path: Path to file
            format: File format
            batch_size: Number of conversations per batch

        Yields:
            Batches of conversation dictionaries
        """
        if format is None:
            format = self._detect_format(file_path)

        if format == 'csv':
            yield from self._stream_csv(file_path, batch_size)
        elif format == 'jsonl':
            yield from self._stream_jsonl(file_path, batch_size)
        else:
            # For small formats, just return all at once
            conversations = self.ingest_file(file_path, format)
            yield conversations

    # Format-specific ingestion methods

    def _ingest_text(self, file_path: str) -> List[Dict[str, Any]]:
        """Ingest plain text file"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # Try to split on common delimiters
        conversations = []

        # Check for conversation markers
        if '---' in content or '===' in content:
            # Split on markers
            parts = content.split('---') if '---' in content else content.split('===')
            for i, part in enumerate(parts):
                if part.strip():
                    conversations.append({
                        'conversation_id': f"{Path(file_path).stem}_{i+1}",
                        'transcript': part.strip(),
                        'source': str(file_path),
                        'format': 'text'
                    })
        else:
            # Treat whole file as one conversation
            conversations.append({
                'conversation_id': Path(file_path).stem,
                'transcript': content.strip(),
                'source': str(file_path),
                'format': 'text'
            })

        return conversations

    def _ingest_csv(self, file_path: str, delimiter: str = ',') -> List[Dict[str, Any]]:
        """
        Ingest CSV file

        Expected columns:
        - conversation_id (optional)
        - transcript (required)
        - outcome (optional)
        - industry (optional)
        - deal_value (optional)
        - Other metadata columns
        """
        conversations = []

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter=delimiter)

            for i, row in enumerate(reader):
                # Extract transcript (try multiple column names)
                transcript = (
                    row.get('transcript') or
                    row.get('conversation') or
                    row.get('text') or
                    row.get('content') or
                    ''
                )

                if not transcript:
                    print(f"Warning: Row {i+1} missing transcript, skipping")
                    continue

                # Build conversation dict
                conversation = {
                    'conversation_id': row.get('conversation_id') or row.get('id') or f"{Path(file_path).stem}_{i+1}",
                    'transcript': transcript,
                    'source': str(file_path),
                    'format': 'csv'
                }

                # Add metadata
                metadata_fields = [
                    'outcome', 'industry', 'deal_value', 'duration',
                    'contact_id', 'agent_id', 'buyer_persona', 'company',
                    'date', 'timestamp'
                ]

                for field in metadata_fields:
                    if field in row and row[field]:
                        # Convert deal_value and duration to numbers
                        if field in ['deal_value', 'duration']:
                            try:
                                conversation[field] = float(row[field])
                            except:
                                conversation[field] = row[field]
                        else:
                            conversation[field] = row[field]

                # Add any extra columns as metadata
                extra_fields = set(row.keys()) - set(['transcript', 'conversation', 'text', 'content'] + metadata_fields)
                if extra_fields:
                    conversation['extra_metadata'] = {field: row[field] for field in extra_fields if row[field]}

                conversations.append(conversation)

        return conversations

    def _ingest_json(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Ingest JSON file

        Supports both single conversation and array of conversations
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        conversations = []

        # Check if data is array or single object
        if isinstance(data, list):
            # Array of conversations
            for i, conv in enumerate(data):
                if isinstance(conv, dict):
                    conversations.append(self._normalize_conversation(conv, file_path, i))
        elif isinstance(data, dict):
            # Single conversation or object with conversations
            if 'conversations' in data:
                # Object with conversations array
                for i, conv in enumerate(data['conversations']):
                    conversations.append(self._normalize_conversation(conv, file_path, i))
            else:
                # Single conversation
                conversations.append(self._normalize_conversation(data, file_path, 0))

        return conversations

    def _ingest_jsonl(self, file_path: str) -> List[Dict[str, Any]]:
        """Ingest JSON Lines file"""
        conversations = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if line.strip():
                    try:
                        conv = json.loads(line)
                        conversations.append(self._normalize_conversation(conv, file_path, i))
                    except json.JSONDecodeError as e:
                        print(f"Warning: Error parsing line {i+1}: {e}")

        return conversations

    def _ingest_sqlite(self, db_path: str, query: str) -> List[Dict[str, Any]]:
        """Ingest from SQLite database"""
        try:
            import sqlite3
        except ImportError:
            raise ImportError("sqlite3 is required for SQLite ingestion")

        conversations = []

        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Enable column access by name
        cursor = conn.cursor()

        cursor.execute(query)
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            conv = dict(row)
            conversations.append(self._normalize_conversation(conv, db_path, i))

        conn.close()

        return conversations

    def _ingest_postgres(self, connection_string: str, query: str) -> List[Dict[str, Any]]:
        """Ingest from PostgreSQL database"""
        try:
            import psycopg2
            from psycopg2.extras import RealDictCursor
        except ImportError:
            raise ImportError("psycopg2 is required for PostgreSQL ingestion. Install with: pip install psycopg2-binary")

        conversations = []

        conn = psycopg2.connect(connection_string)
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        cursor.execute(query)
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            conv = dict(row)
            conversations.append(self._normalize_conversation(conv, "postgres", i))

        cursor.close()
        conn.close()

        return conversations

    def _ingest_mysql(self, connection_string: str, query: str) -> List[Dict[str, Any]]:
        """Ingest from MySQL database"""
        try:
            import mysql.connector
        except ImportError:
            raise ImportError("mysql-connector-python is required for MySQL ingestion. Install with: pip install mysql-connector-python")

        conversations = []

        # Parse connection string
        conn = mysql.connector.connect(**self._parse_connection_string(connection_string))
        cursor = conn.cursor(dictionary=True)

        cursor.execute(query)
        rows = cursor.fetchall()

        for i, row in enumerate(rows):
            conversations.append(self._normalize_conversation(row, "mysql", i))

        cursor.close()
        conn.close()

        return conversations

    # Streaming methods

    def _stream_csv(self, file_path: str, batch_size: int) -> Iterator[List[Dict[str, Any]]]:
        """Stream CSV in batches"""
        batch = []

        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for i, row in enumerate(reader):
                transcript = row.get('transcript') or row.get('conversation') or ''
                if transcript:
                    conversation = {
                        'conversation_id': row.get('conversation_id') or f"{Path(file_path).stem}_{i+1}",
                        'transcript': transcript,
                        'source': str(file_path),
                        **{k: v for k, v in row.items() if k not in ['transcript', 'conversation']}
                    }
                    batch.append(conversation)

                    if len(batch) >= batch_size:
                        yield batch
                        batch = []

            # Yield remaining
            if batch:
                yield batch

    def _stream_jsonl(self, file_path: str, batch_size: int) -> Iterator[List[Dict[str, Any]]]:
        """Stream JSONL in batches"""
        batch = []

        with open(file_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if line.strip():
                    try:
                        conv = json.loads(line)
                        batch.append(self._normalize_conversation(conv, file_path, i))

                        if len(batch) >= batch_size:
                            yield batch
                            batch = []
                    except json.JSONDecodeError:
                        pass

            # Yield remaining
            if batch:
                yield batch

    # Helper methods

    def _detect_format(self, file_path: str) -> str:
        """Auto-detect file format from extension"""
        ext = Path(file_path).suffix.lower().lstrip('.')

        if ext in self.supported_formats:
            return ext
        elif ext in ['text']:
            return 'txt'
        else:
            raise ValueError(f"Cannot detect format for extension: {ext}")

    def _normalize_conversation(
        self,
        conv: Dict,
        source: str,
        index: int
    ) -> Dict[str, Any]:
        """
        Normalize conversation dictionary to standard format
        """
        # Extract transcript
        transcript = (
            conv.get('transcript') or
            conv.get('conversation') or
            conv.get('text') or
            conv.get('content') or
            conv.get('message') or
            ''
        )

        # Build normalized conversation
        normalized = {
            'conversation_id': conv.get('conversation_id') or conv.get('id') or f"{Path(source).stem}_{index+1}",
            'transcript': transcript,
            'source': str(source),
            'format': 'database' if source in ['postgres', 'mysql'] else 'json'
        }

        # Add standard metadata fields
        metadata_fields = [
            'outcome', 'industry', 'deal_value', 'duration',
            'contact_id', 'agent_id', 'buyer_persona', 'company'
        ]

        for field in metadata_fields:
            if field in conv and conv[field]:
                normalized[field] = conv[field]

        # Add any extra fields
        extra_fields = set(conv.keys()) - set(['transcript', 'conversation', 'text', 'content'] + metadata_fields)
        if extra_fields:
            normalized['extra_metadata'] = {field: conv[field] for field in extra_fields if conv.get(field)}

        return normalized

    def _parse_connection_string(self, conn_str: str) -> Dict:
        """Parse MySQL connection string"""
        # Simple parser for format: host:port/database?user=x&password=y
        # Or dict format: host=x,port=y,database=z,user=a,password=b

        if '=' in conn_str and ',' in conn_str:
            # Dict format
            parts = conn_str.split(',')
            config = {}
            for part in parts:
                key, value = part.split('=')
                config[key.strip()] = value.strip()
            return config
        else:
            # URL format (simplified)
            raise ValueError("Use dict format: host=x,port=y,database=z,user=a,password=b")

    def validate_conversation(self, conv: Dict) -> Tuple[bool, List[str]]:
        """
        Validate conversation has required fields

        Returns: (is_valid, error_messages)
        """
        errors = []

        # Required fields
        if not conv.get('transcript'):
            errors.append("Missing required field: transcript")

        if not conv.get('conversation_id'):
            errors.append("Missing required field: conversation_id")

        # Warnings
        if not conv.get('outcome'):
            errors.append("Warning: outcome not specified")

        is_valid = len([e for e in errors if not e.startswith('Warning')]) == 0

        return is_valid, errors
