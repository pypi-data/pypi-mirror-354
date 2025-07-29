"""Diff parser for extracting individual hunks from git diff output."""

import re
import subprocess
from dataclasses import dataclass
from typing import List, Optional, Tuple


@dataclass
class Hunk:
    """Represents an individual hunk (change block) from a git diff."""
    
    id: str  # Unique identifier like "file.py:123-145"
    file_path: str  # Path to the file
    start_line: int  # Starting line number in original file
    end_line: int  # Ending line number in original file  
    content: str  # The actual diff content for this hunk
    context: str  # Surrounding code context for better AI understanding
    hunk_header: str  # The @@ line for this hunk
    
    def __str__(self) -> str:
        """String representation for debugging."""
        return f"Hunk({self.id}): {self.file_path}:{self.start_line}-{self.end_line}"


def parse_diff(diff_output: str) -> List[Hunk]:
    """Parse git diff output into individual hunks.
    
    Args:
        diff_output: Raw git diff output
        
    Returns:
        List of Hunk objects representing individual change blocks
    """
    hunks = []
    
    # Split diff into individual file sections
    file_sections = _split_diff_by_files(diff_output)
    
    for file_path, file_diff in file_sections:
        # Parse hunks within this file
        file_hunks = _parse_file_hunks(file_path, file_diff)
        hunks.extend(file_hunks)
    
    return hunks


def _split_diff_by_files(diff_output: str) -> List[Tuple[str, str]]:
    """Split diff output into sections for each file.
    
    Returns:
        List of (file_path, file_diff_content) tuples
    """
    file_sections = []
    lines = diff_output.split('\n')
    current_file = None
    current_diff = []
    
    for line in lines:
        # Match file headers like "diff --git a/file.py b/file.py"
        if line.startswith('diff --git'):
            # Save previous file if exists
            if current_file and current_diff:
                file_sections.append((current_file, '\n'.join(current_diff)))
            
            # Extract file path from diff header
            # Handle various formats: a/file.py b/file.py, "a/file with spaces.py" etc.
            match = re.search(r'diff --git a/(.+?) b/(.+?)$', line)
            if match:
                # Use the 'b/' version (after changes) as the canonical path
                current_file = match.group(2)
                # Remove quotes if present
                if current_file.startswith('"') and current_file.endswith('"'):
                    current_file = current_file[1:-1]
            else:
                current_file = "unknown"
            
            current_diff = [line]
        else:
            if current_diff is not None:
                current_diff.append(line)
    
    # Don't forget the last file
    if current_file and current_diff:
        file_sections.append((current_file, '\n'.join(current_diff)))
    
    return file_sections


def _parse_file_hunks(file_path: str, file_diff: str) -> List[Hunk]:
    """Parse hunks within a single file's diff.
    
    Args:
        file_path: Path to the file
        file_diff: Diff content for this file
        
    Returns:
        List of Hunk objects for this file
    """
    hunks = []
    lines = file_diff.split('\n')
    current_hunk_lines = []
    current_hunk_header = None
    hunk_start_line = None
    hunk_count = 0
    
    for i, line in enumerate(lines):
        # Match hunk headers like "@@ -123,10 +123,15 @@ class MyClass:"
        if line.startswith('@@'):
            # Save previous hunk if exists
            if current_hunk_header and current_hunk_lines:
                hunk = _create_hunk_from_lines(
                    file_path, current_hunk_header, current_hunk_lines, 
                    hunk_start_line, hunk_count
                )
                if hunk:
                    hunks.append(hunk)
            
            # Start new hunk
            current_hunk_header = line
            current_hunk_lines = [line]
            hunk_start_line = _extract_line_number(line)
            hunk_count += 1
            
        elif current_hunk_header:
            # We're inside a hunk, collect lines
            current_hunk_lines.append(line)
    
    # Don't forget the last hunk
    if current_hunk_header and current_hunk_lines:
        hunk = _create_hunk_from_lines(
            file_path, current_hunk_header, current_hunk_lines,
            hunk_start_line, hunk_count
        )
        if hunk:
            hunks.append(hunk)
    
    return hunks


def _extract_line_number(hunk_header: str) -> int:
    """Extract starting line number from hunk header.
    
    Args:
        hunk_header: Line like "@@ -123,10 +123,15 @@ class MyClass:"
        
    Returns:
        Starting line number in original file
    """
    # Parse "@@ -old_start,old_count +new_start,new_count @@"
    match = re.search(r'@@ -(\d+)(?:,\d+)? \+(\d+)(?:,\d+)? @@', hunk_header)
    if match:
        # Use the original file line number (before changes)
        return int(match.group(1))
    return 1


def _create_hunk_from_lines(file_path: str, hunk_header: str, hunk_lines: List[str], 
                           start_line: int, hunk_count: int) -> Optional[Hunk]:
    """Create a Hunk object from parsed lines.
    
    Args:
        file_path: Path to the file
        hunk_header: The @@ header line
        hunk_lines: All lines in this hunk including header
        start_line: Starting line number
        hunk_count: Sequential hunk number within file
        
    Returns:
        Hunk object or None if invalid
    """
    if not hunk_lines or len(hunk_lines) < 2:
        return None
    
    # Calculate end line by counting context and removed lines
    end_line = start_line
    for line in hunk_lines[1:]:  # Skip header
        if line.startswith(' ') or line.startswith('-'):
            end_line += 1
        # Don't count added lines for original file range
    
    # Create unique ID
    hunk_id = f"{file_path}:{start_line}-{end_line}"
    if hunk_count > 1:
        hunk_id += f"#{hunk_count}"
    
    # Join hunk content
    content = '\n'.join(hunk_lines)
    
    # Get context for this hunk
    context = get_hunk_context(file_path, start_line, end_line)
    
    return Hunk(
        id=hunk_id,
        file_path=file_path,
        start_line=start_line,
        end_line=end_line,
        content=content,
        context=context,
        hunk_header=hunk_header
    )


def get_hunk_context(file_path: str, start_line: int, end_line: int, 
                     context_lines: int = 3) -> str:
    """Extract surrounding code context for a hunk to help AI understand it.
    
    Args:
        file_path: Path to the file
        start_line: Starting line number
        end_line: Ending line number
        context_lines: Number of context lines to include before/after
        
    Returns:
        String containing surrounding code context
    """
    try:
        # Try to read the file from the working directory
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        # Calculate context range
        context_start = max(0, start_line - context_lines - 1)  # -1 for 0-based indexing
        context_end = min(len(lines), end_line + context_lines)
        
        # Extract context lines
        context_lines_list = lines[context_start:context_end]
        
        # Add line numbers for readability
        context_with_numbers = []
        for i, line in enumerate(context_lines_list):
            line_num = context_start + i + 1  # +1 for 1-based line numbers
            marker = ">" if start_line <= line_num <= end_line else " "
            context_with_numbers.append(f"{marker}{line_num:4d}: {line.rstrip()}")
        
        return '\n'.join(context_with_numbers)
        
    except (FileNotFoundError, IOError, UnicodeDecodeError):
        # If we can't read the file, try to get context from git
        return _get_git_context(file_path, start_line, context_lines)


def _get_git_context(file_path: str, start_line: int, context_lines: int) -> str:
    """Get file context from git when file is not readable.
    
    Args:
        file_path: Path to the file
        start_line: Starting line number
        context_lines: Number of context lines
        
    Returns:
        String containing context from git, or empty string if unavailable
    """
    try:
        # Try to get file content from git HEAD
        result = subprocess.run(
            ['git', 'show', f'HEAD:{file_path}'],
            capture_output=True, text=True, check=True
        )
        
        lines = result.stdout.split('\n')
        context_start = max(0, start_line - context_lines - 1)
        context_end = min(len(lines), start_line + context_lines)
        
        context_lines_list = lines[context_start:context_end]
        
        # Add line numbers
        context_with_numbers = []
        for i, line in enumerate(context_lines_list):
            line_num = context_start + i + 1
            context_with_numbers.append(f" {line_num:4d}: {line}")
        
        return '\n'.join(context_with_numbers)
        
    except (subprocess.CalledProcessError, UnicodeDecodeError):
        return f"Context unavailable for {file_path} around line {start_line}"


def validate_hunk_combination(hunks: List[Hunk]) -> bool:
    """Validate that a combination of hunks can be applied together.
    
    Args:
        hunks: List of hunks to validate
        
    Returns:
        True if hunks can be safely applied together
    """
    if not hunks:
        return True
    
    # Group hunks by file
    files_hunks = {}
    for hunk in hunks:
        if hunk.file_path not in files_hunks:
            files_hunks[hunk.file_path] = []
        files_hunks[hunk.file_path].append(hunk)
    
    # Check for overlapping hunks within each file
    for file_path, file_hunks in files_hunks.items():
        if len(file_hunks) < 2:
            continue
            
        # Sort hunks by start line
        sorted_hunks = sorted(file_hunks, key=lambda h: h.start_line)
        
        # Check for overlaps
        for i in range(len(sorted_hunks) - 1):
            current = sorted_hunks[i]
            next_hunk = sorted_hunks[i + 1]
            
            # If current hunk ends after next hunk starts, they overlap
            if current.end_line >= next_hunk.start_line:
                return False
    
    return True