"""
Diff parser module for extracting individual hunks from git diff output.
"""

import re
import subprocess
from dataclasses import dataclass, field
from typing import List, Optional, Tuple, Set, Dict


@dataclass
class Hunk:
    """Represents an individual hunk (change block) from a git diff."""
    id: str
    file_path: str
    start_line: int
    end_line: int
    content: str
    context: str
    dependencies: Set[str] = field(default_factory=set)  # Hunk IDs this depends on
    dependents: Set[str] = field(default_factory=set)    # Hunk IDs that depend on this
    change_type: str = field(default="modification")     # addition, deletion, modification, import, export


def parse_diff(diff_output: str, context_lines: int = 3) -> List[Hunk]:
    """
    Parse git diff output into individual hunks.
    
    Args:
        diff_output: Raw git diff output string
        
    Returns:
        List of Hunk objects representing individual change blocks
    """
    hunks = []
    current_file = None
    
    lines = diff_output.split('\n')
    i = 0
    
    while i < len(lines):
        line = lines[i]
        
        # Check for file header
        if line.startswith('diff --git'):
            # Extract file path from the diff header
            # Format: diff --git a/path/to/file b/path/to/file
            match = re.match(r'diff --git a/(.*) b/(.*)', line)
            if match:
                current_file = match.group(2)  # Use the 'b/' path (after changes)
        
        # Check for hunk header
        elif line.startswith('@@') and current_file:
            hunk_match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', line)
            if hunk_match:
                old_start = int(hunk_match.group(1))
                old_count = int(hunk_match.group(2)) if hunk_match.group(2) else 1
                new_start = int(hunk_match.group(3))
                new_count = int(hunk_match.group(4)) if hunk_match.group(4) else 1
                
                # Collect hunk content
                hunk_content_lines = [line]  # Include the @@ line
                i += 1
                
                # Read until next file header, hunk header, or end
                while i < len(lines):
                    next_line = lines[i]
                    if (next_line.startswith('diff --git') or 
                        next_line.startswith('@@') or
                        (next_line.startswith('\\') and 'No newline' in next_line)):
                        # Handle "\ No newline at end of file"
                        if next_line.startswith('\\'):
                            hunk_content_lines.append(next_line)
                            i += 1
                        break
                    hunk_content_lines.append(next_line)
                    i += 1
                
                # Create hunk
                hunk_content = '\n'.join(hunk_content_lines)
                
                # Calculate line range for the hunk ID
                # Use the new file line numbers for the range
                end_line = new_start + max(0, new_count - 1)
                
                hunk_id = f"{current_file}:{new_start}-{end_line}"
                
                # Get context around the hunk
                context = get_hunk_context(current_file, new_start, end_line, context_lines)
                
                # Analyze change type
                change_type = analyze_hunk_change_type(hunk_content, current_file)
                
                hunk = Hunk(
                    id=hunk_id,
                    file_path=current_file,
                    start_line=new_start,
                    end_line=end_line,
                    content=hunk_content,
                    context=context,
                    change_type=change_type
                )
                
                hunks.append(hunk)
                continue  # Don't increment i, we already did it in the while loop
        
        i += 1
    
    # Analyze dependencies between hunks
    analyze_hunk_dependencies(hunks)
    
    return hunks


def get_hunk_context(file_path: str, start_line: int, end_line: int, context_lines: int = 3) -> str:
    """
    Extract surrounding code context for better AI understanding.
    
    Args:
        file_path: Path to the file
        start_line: Starting line number of the hunk
        end_line: Ending line number of the hunk
        context_lines: Number of lines before and after to include
        
    Returns:
        String containing the context around the hunk
    """
    try:
        # Read the current file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            file_lines = f.readlines()
        
        # Calculate context boundaries
        context_start = max(0, start_line - context_lines - 1)  # -1 for 0-based indexing
        context_end = min(len(file_lines), end_line + context_lines)
        
        # Extract context lines
        context_lines_list = file_lines[context_start:context_end]
        
        # Add line numbers for clarity
        numbered_lines = []
        for i, line in enumerate(context_lines_list, start=context_start + 1):
            prefix = ">>> " if start_line <= i <= end_line else "    "
            numbered_lines.append(f"{prefix}{i:4d}: {line.rstrip()}")
        
        return '\n'.join(numbered_lines)
        
    except (FileNotFoundError, IOError):
        # If we can't read the file, return minimal context
        return f"File: {file_path} (lines {start_line}-{end_line})"


def create_hunk_patch(hunks: List[Hunk], base_diff: str) -> str:
    """
    Create a patch file containing only the specified hunks.
    
    Args:
        hunks: List of hunks to include in the patch
        base_diff: Original full diff output
        
    Returns:
        Patch content that can be applied with git apply
    """
    if not hunks:
        return ""
    
    # Group hunks by file
    hunks_by_file = {}
    for hunk in hunks:
        if hunk.file_path not in hunks_by_file:
            hunks_by_file[hunk.file_path] = []
        hunks_by_file[hunk.file_path].append(hunk)
    
    # Parse the base diff to extract file headers
    base_lines = base_diff.split('\n')
    file_headers = {}
    
    i = 0
    while i < len(base_lines):
        line = base_lines[i]
        if line.startswith('diff --git'):
            # Extract file path from diff header
            match = re.match(r'diff --git a/(.*) b/(.*)', line)
            if match:
                file_path = match.group(2)
                header_lines = [line]
                i += 1
                
                # Collect all header lines until first @@ or next diff
                while i < len(base_lines):
                    next_line = base_lines[i]
                    if next_line.startswith('@@') or next_line.startswith('diff --git'):
                        break
                    header_lines.append(next_line)
                    i += 1
                
                file_headers[file_path] = header_lines
                continue
        i += 1
    
    # Build the patch
    patch_parts = []
    
    for file_path, file_hunks in hunks_by_file.items():
        # Add file header
        if file_path in file_headers:
            patch_parts.extend(file_headers[file_path])
        else:
            # Fallback header if not found in base diff
            patch_parts.extend([
                f"diff --git a/{file_path} b/{file_path}",
                f"index 0000000..1111111 100644",
                f"--- a/{file_path}",
                f"+++ b/{file_path}"
            ])
        
        # Add hunks for this file
        for hunk in sorted(file_hunks, key=lambda h: h.start_line):
            # Split hunk content and add each line
            hunk_lines = hunk.content.split('\n')
            for line in hunk_lines:
                if line:  # Skip completely empty lines
                    patch_parts.append(line)
    
    return '\n'.join(patch_parts) + '\n' if patch_parts else ""


def validate_hunk_combination(hunks: List[Hunk]) -> Tuple[bool, str]:
    """
    Validate that a combination of hunks can be applied together.
    
    Args:
        hunks: List of hunks to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if not hunks:
        return True, ""
    
    # Group by file and check for overlaps
    hunks_by_file = {}
    for hunk in hunks:
        if hunk.file_path not in hunks_by_file:
            hunks_by_file[hunk.file_path] = []
        hunks_by_file[hunk.file_path].append(hunk)
    
    for file_path, file_hunks in hunks_by_file.items():
        # Sort hunks by start line
        sorted_hunks = sorted(file_hunks, key=lambda h: h.start_line)
        
        # Check for overlapping hunks
        for i in range(len(sorted_hunks) - 1):
            current_hunk = sorted_hunks[i]
            next_hunk = sorted_hunks[i + 1]
            
            if current_hunk.end_line >= next_hunk.start_line:
                return False, f"Overlapping hunks in {file_path}: {current_hunk.id} and {next_hunk.id}"
    
    return True, ""


def analyze_hunk_change_type(hunk_content: str, file_path: str) -> str:
    """
    Analyze the type of change in a hunk to help with dependency detection.
    
    Args:
        hunk_content: The hunk content
        file_path: Path to the file being changed
        
    Returns:
        String describing the change type
    """
    lines = hunk_content.split('\n')
    
    # Check for import/export related changes
    import_patterns = [
        r'^\+.*import\s+.*from\s+[\'"]',  # ES6 imports
        r'^\+.*import\s+[\'"]',          # Import statements
        r'^\+.*require\s*\([\'"]',       # CommonJS require
        r'^\+.*from\s+[\'"].*[\'"]',     # From imports
    ]
    
    export_patterns = [
        r'^\+.*export\s+',               # Export statements
        r'^\+.*module\.exports\s*=',     # CommonJS exports
    ]
    
    # Count different types of changes
    additions = sum(1 for line in lines if line.startswith('+') and not line.startswith('+++'))
    deletions = sum(1 for line in lines if line.startswith('-') and not line.startswith('---'))
    
    # Check for import/export changes
    for line in lines:
        for pattern in import_patterns:
            if re.match(pattern, line):
                return "import"
        for pattern in export_patterns:
            if re.match(pattern, line):
                return "export"
    
    # Determine change type based on addition/deletion ratio
    if deletions == 0 and additions > 0:
        return "addition"
    elif additions == 0 and deletions > 0:
        return "deletion"
    else:
        return "modification"


def analyze_hunk_dependencies(hunks: List[Hunk]) -> None:
    """
    Analyze dependencies between hunks to enable intelligent grouping.
    
    Args:
        hunks: List of hunks to analyze (modified in place)
    """
    # Build maps for quick lookups
    hunks_by_file = {}
    import_export_map = {}
    
    for hunk in hunks:
        if hunk.file_path not in hunks_by_file:
            hunks_by_file[hunk.file_path] = []
        hunks_by_file[hunk.file_path].append(hunk)
        
        # Extract import/export information
        if hunk.change_type in ["import", "export"]:
            imports, exports = extract_import_export_info(hunk.content)
            import_export_map[hunk.id] = {"imports": imports, "exports": exports}
    
    # Analyze dependencies
    for hunk in hunks:
        # 1. Import/Export dependencies
        if hunk.id in import_export_map:
            hunk_info = import_export_map[hunk.id]
            
            # Find dependencies based on what this hunk imports
            for imported_module in hunk_info["imports"]:
                for other_hunk in hunks:
                    if other_hunk.id != hunk.id and other_hunk.id in import_export_map:
                        other_info = import_export_map[other_hunk.id]
                        if imported_module in other_info["exports"]:
                            hunk.dependencies.add(other_hunk.id)
                            other_hunk.dependents.add(hunk.id)
        
        # 2. Same file proximity dependencies (changes in the same file that are close together)
        for other_hunk in hunks_by_file.get(hunk.file_path, []):
            if other_hunk.id != hunk.id:
                # If hunks are very close (within 10 lines), they might be related
                line_distance = abs(hunk.start_line - other_hunk.start_line)
                if line_distance <= 10:
                    # Create weak dependencies for same-file proximity
                    if hunk.start_line > other_hunk.start_line:
                        hunk.dependencies.add(other_hunk.id)
                        other_hunk.dependents.add(hunk.id)
        
        # 3. Component usage dependencies (for frontend frameworks)
        if _is_frontend_file(hunk.file_path):
            component_deps = find_component_dependencies(hunk, hunks)
            for dep_id in component_deps:
                hunk.dependencies.add(dep_id)
                # Find the dependent hunk and update its dependents
                for other_hunk in hunks:
                    if other_hunk.id == dep_id:
                        other_hunk.dependents.add(hunk.id)
                        break


def extract_import_export_info(hunk_content: str) -> Tuple[Set[str], Set[str]]:
    """
    Extract import and export information from hunk content.
    
    Args:
        hunk_content: The hunk content to analyze
        
    Returns:
        Tuple of (imports, exports) as sets of module names
    """
    imports = set()
    exports = set()
    
    lines = hunk_content.split('\n')
    
    for line in lines:
        if not line.startswith('+'):
            continue
            
        line = line[1:].strip()  # Remove + prefix
        
        # Extract imports
        import_match = re.search(r'import\s+.*from\s+[\'"]([^\'"]+)[\'"]', line)
        if import_match:
            imports.add(import_match.group(1))
        
        import_match = re.search(r'import\s+[\'"]([^\'"]+)[\'"]', line)
        if import_match:
            imports.add(import_match.group(1))
        
        require_match = re.search(r'require\s*\([\'"]([^\'"]+)[\'"]\)', line)
        if require_match:
            imports.add(require_match.group(1))
        
        # Extract exports
        if 'export' in line:
            exports.add("__exported__")  # Simplified for now
    
    return imports, exports


def find_component_dependencies(hunk: Hunk, all_hunks: List[Hunk]) -> Set[str]:
    """
    Find component-related dependencies for frontend frameworks.
    
    Args:
        hunk: The hunk to analyze
        all_hunks: All hunks to search for dependencies
        
    Returns:
        Set of hunk IDs that this hunk depends on
    """
    dependencies = set()
    
    # Extract component names from the hunk content
    component_names = extract_component_names(hunk.content)
    
    # Look for hunks that define these components
    for other_hunk in all_hunks:
        if other_hunk.id != hunk.id:
            for component_name in component_names:
                if component_name in other_hunk.content:
                    dependencies.add(other_hunk.id)
                    break
    
    return dependencies


def extract_component_names(content: str) -> Set[str]:
    """
    Extract component names from content (simplified for now).
    
    Args:
        content: The content to analyze
        
    Returns:
        Set of component names found
    """
    component_names = set()
    
    # Simple patterns for common frontend frameworks
    patterns = [
        r'<(\w+)[^>]*>',           # HTML/JSX tags
        r'import\s+(\w+)\s+from',  # Import statements
        r'component\s*:\s*(\w+)',  # Vue component definitions
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if match and match[0].isupper():  # Component names typically start with uppercase
                component_names.add(match)
    
    return component_names


def _is_frontend_file(file_path: str) -> bool:
    """Check if a file is a frontend framework file."""
    frontend_extensions = ['.vue', '.svelte', '.jsx', '.tsx', '.js', '.ts']
    return any(file_path.endswith(ext) for ext in frontend_extensions)


def create_dependency_groups(hunks: List[Hunk]) -> List[List[Hunk]]:
    """
    Group hunks based on their dependencies for atomic application.
    
    Args:
        hunks: List of hunks with dependency information
        
    Returns:
        List of hunk groups that should be applied together
    """
    # Start with all hunks ungrouped
    ungrouped = set(hunk.id for hunk in hunks)
    hunk_map = {hunk.id: hunk for hunk in hunks}
    groups = []
    
    while ungrouped:
        # Start a new group with a hunk that has no ungrouped dependencies
        group_seeds = []
        for hunk_id in ungrouped:
            hunk = hunk_map[hunk_id]
            ungrouped_deps = hunk.dependencies & ungrouped
            if not ungrouped_deps:
                group_seeds.append(hunk_id)
        
        if not group_seeds:
            # If no seeds found, we have circular dependencies - break by picking the first one
            group_seeds = [next(iter(ungrouped))]
        
        # Build a group starting from a seed
        current_group = set()
        to_process = [group_seeds[0]]
        
        while to_process:
            current_id = to_process.pop(0)
            if current_id in ungrouped and current_id not in current_group:
                current_group.add(current_id)
                hunk = hunk_map[current_id]
                
                # Add all dependents that are still ungrouped
                for dependent_id in hunk.dependents:
                    if dependent_id in ungrouped and dependent_id not in current_group:
                        to_process.append(dependent_id)
                
                # Add dependencies that are still ungrouped
                for dep_id in hunk.dependencies:
                    if dep_id in ungrouped and dep_id not in current_group:
                        to_process.append(dep_id)
        
        # Convert group to list of hunks
        group_hunks = [hunk_map[hunk_id] for hunk_id in current_group]
        groups.append(group_hunks)
        
        # Remove grouped hunks from ungrouped
        ungrouped -= current_group
    
    return groups