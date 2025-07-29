"""
Hunk applicator module for applying specific hunks to the git staging area.
"""

import os
import re
import subprocess
import tempfile
from typing import List, Dict, Optional, Tuple
from .diff_parser import Hunk, create_hunk_patch, validate_hunk_combination, create_dependency_groups


class HunkApplicatorError(Exception):
    """Custom exception for hunk application errors."""
    pass


def apply_hunks(hunk_ids: List[str], hunks_by_id: Dict[str, Hunk], base_diff: str) -> bool:
    """
    Apply specific hunks to the git staging area using dependency-aware grouping.
    
    Args:
        hunk_ids: List of hunk IDs to apply
        hunks_by_id: Dictionary mapping hunk IDs to Hunk objects
        base_diff: Original full diff output
        
    Returns:
        True if successful, False otherwise
        
    Raises:
        HunkApplicatorError: If hunk application fails
    """
    if not hunk_ids:
        return True
    
    # Get the hunks to apply
    hunks_to_apply = []
    for hunk_id in hunk_ids:
        if hunk_id not in hunks_by_id:
            raise HunkApplicatorError(f"Hunk ID not found: {hunk_id}")
        hunks_to_apply.append(hunks_by_id[hunk_id])
    
    # Validate that hunks can be applied together
    is_valid, error_msg = validate_hunk_combination(hunks_to_apply)
    if not is_valid:
        raise HunkApplicatorError(f"Invalid hunk combination: {error_msg}")
    
    # Use dependency-aware application for better handling of complex changes
    return _apply_hunks_with_dependencies(hunks_to_apply, base_diff)


def _apply_hunks_with_dependencies(hunks: List[Hunk], base_diff: str) -> bool:
    """
    Apply hunks using dependency-aware grouping for better handling of complex changes.
    
    Args:
        hunks: List of hunks to apply
        base_diff: Original full diff output
        
    Returns:
        True if all hunks applied successfully, False otherwise
    """
    # Create dependency groups
    dependency_groups = create_dependency_groups(hunks)
    
    print(f"Dependency analysis: {len(dependency_groups)} groups identified")
    for i, group in enumerate(dependency_groups):
        print(f"  Group {i+1}: {len(group)} hunks")
        for hunk in group:
            deps = len(hunk.dependencies)
            dependents = len(hunk.dependents)
            print(f"    - {hunk.id} ({hunk.change_type}, deps: {deps}, dependents: {dependents})")
    
    # Apply groups in order
    for i, group in enumerate(dependency_groups):
        print(f"Applying group {i+1}/{len(dependency_groups)} ({len(group)} hunks)...")
        
        if len(group) == 1:
            # Single hunk - apply individually for better error isolation
            success = _apply_hunks_sequentially(group, base_diff)
        else:
            # Multiple interdependent hunks - try atomic application first
            success = _apply_dependency_group_atomically(group, base_diff)
            
            if not success:
                print("  Atomic application failed, trying sequential with smart ordering...")
                # Fallback to sequential application with dependency ordering
                success = _apply_dependency_group_sequentially(group, base_diff)
        
        if not success:
            print(f"Failed to apply group {i+1}")
            return False
        
        print(f"✓ Group {i+1} applied successfully")
    
    return True


def _apply_dependency_group_atomically(hunks: List[Hunk], base_diff: str) -> bool:
    """
    Try to apply a dependency group as a single atomic patch.
    
    Args:
        hunks: List of hunks in the dependency group
        base_diff: Original full diff output
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Create a combined patch for all hunks in the group
        combined_patch = create_hunk_patch(hunks, base_diff)
        
        if not combined_patch.strip():
            print("Warning: Empty combined patch generated")
            return True
        
        # Validate the patch before applying
        if not _validate_patch_format(combined_patch):
            print("Error: Invalid combined patch format")
            return False
        
        # Apply the combined patch atomically
        return _apply_patch_to_staging(combined_patch)
        
    except Exception as e:
        print(f"Error in atomic application: {e}")
        return False


def _apply_dependency_group_sequentially(hunks: List[Hunk], base_diff: str) -> bool:
    """
    Apply hunks in a dependency group sequentially with smart ordering.
    
    Args:
        hunks: List of hunks in the dependency group
        base_diff: Original full diff output
        
    Returns:
        True if successful, False otherwise
    """
    # Order hunks by dependencies (topological sort)
    ordered_hunks = _topological_sort_hunks(hunks)
    
    if not ordered_hunks:
        # Fallback to simple ordering if topological sort fails
        ordered_hunks = sorted(hunks, key=lambda h: (h.file_path, h.start_line))
    
    # Apply hunks in dependency order
    for i, hunk in enumerate(ordered_hunks):
        try:
            # Use intelligent relocation instead of rigid validation
            success = _relocate_and_apply_hunk(hunk, base_diff)
            if not success:
                print(f"Failed to apply hunk {hunk.id} ({i+1}/{len(ordered_hunks)}) after relocation")
                return False
            
        except Exception as e:
            print(f"Error applying hunk {hunk.id}: {e}")
            return False
    
    return True


def _topological_sort_hunks(hunks: List[Hunk]) -> List[Hunk]:
    """
    Sort hunks based on their dependencies using topological sort.
    
    Args:
        hunks: List of hunks to sort
        
    Returns:
        List of hunks in dependency order, or empty list if cyclic dependencies
    """
    # Build hunk map for quick lookups
    hunk_map = {hunk.id: hunk for hunk in hunks}
    hunk_ids = set(hunk.id for hunk in hunks)
    
    # Calculate in-degrees (number of dependencies within this group)
    in_degree = {}
    for hunk in hunks:
        # Only count dependencies that are within this group
        local_deps = hunk.dependencies & hunk_ids
        in_degree[hunk.id] = len(local_deps)
    
    # Start with hunks that have no dependencies within the group
    queue = [hunk_id for hunk_id in hunk_ids if in_degree[hunk_id] == 0]
    result = []
    
    while queue:
        current_id = queue.pop(0)
        result.append(hunk_map[current_id])
        
        # Reduce in-degree for dependents
        current_hunk = hunk_map[current_id]
        for dependent_id in current_hunk.dependents:
            if dependent_id in hunk_ids:
                in_degree[dependent_id] -= 1
                if in_degree[dependent_id] == 0:
                    queue.append(dependent_id)
    
    # Check for cycles
    if len(result) != len(hunks):
        print("Warning: Cyclic dependencies detected, using fallback ordering")
        return []
    
    return result


def _apply_hunks_sequentially(hunks: List[Hunk], base_diff: str) -> bool:
    """
    Apply hunks one by one for better reliability and error isolation.
    
    Args:
        hunks: List of hunks to apply
        base_diff: Original full diff output
        
    Returns:
        True if all hunks applied successfully, False otherwise
    """
    from .diff_parser import create_hunk_patch
    
    # Sort hunks by file and line number for consistent application order
    sorted_hunks = sorted(hunks, key=lambda h: (h.file_path, h.start_line))
    
    for i, hunk in enumerate(sorted_hunks):
        try:
            # Use intelligent relocation instead of rigid validation
            success = _relocate_and_apply_hunk(hunk, base_diff)
            if not success:
                print(f"Failed to apply hunk {hunk.id} ({i+1}/{len(sorted_hunks)}) after relocation")
                return False
            
        except Exception as e:
            print(f"Error applying hunk {hunk.id}: {e}")
            return False
    
    return True


def _validate_patch_format(patch_content: str) -> bool:
    """
    Validate that a patch has the correct format before applying.
    
    Args:
        patch_content: The patch content to validate
        
    Returns:
        True if patch format is valid, False otherwise
    """
    lines = patch_content.strip().split('\n')
    
    if not lines:
        return False
    
    # Must start with diff --git
    if not lines[0].startswith('diff --git'):
        return False
    
    # Must have at least one @@ hunk header
    has_hunk = any(line.startswith('@@') for line in lines)
    if not has_hunk:
        return False
    
    # Check for basic file header structure
    has_file_markers = any(line.startswith('---') for line in lines) and \
                      any(line.startswith('+++') for line in lines)
    
    if not has_file_markers:
        return False
    
    return True


def _apply_patch_to_staging(patch_content: str) -> bool:
    """
    Apply a patch to the git staging area using git apply --cached.
    
    Args:
        patch_content: The patch content to apply
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get the staging area state before applying the patch
        pre_apply_diff = _get_staged_diff()
        
        # Create a temporary file for the patch
        with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as patch_file:
            patch_file.write(patch_content)
            patch_file_path = patch_file.name
        
        try:
            # Apply the patch to the staging area with tolerant flags
            result = subprocess.run(
                ['git', 'apply', '--cached', '--whitespace=nowarn', '--ignore-space-change', '--ignore-whitespace', patch_file_path],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                # Try with even more permissive flags
                result = subprocess.run(
                    ['git', 'apply', '--cached', '--whitespace=fix', '--ignore-space-change', '--ignore-whitespace', patch_file_path],
                    capture_output=True,
                    text=True,
                    check=False
                )
                
                if result.returncode != 0:
                    print(f"Git apply failed even with permissive flags: {result.stderr}")
                    # Only show debug info for individual hunk failures, not the massive combined patches
                    if len(patch_content) < 1000:  # Only show debug for small patches
                        print(f"Debug: Patch content:\n{patch_content}")
                    else:
                        print(f"Debug: Large patch ({len(patch_content)} chars), first 200 chars:\n{patch_content[:200]}")
                    return False
                else:
                    print("✓ Applied with whitespace fixes")
            
            # CRITICAL: Verify that the intended changes were actually staged
            post_apply_diff = _get_staged_diff()
            if not _verify_patch_was_applied(patch_content, pre_apply_diff, post_apply_diff):
                print(f"Warning: Git apply reported success but intended changes were not staged")
                if len(patch_content) < 1000:
                    print(f"Debug: Expected patch content:\n{patch_content}")
                print(f"Debug: Staging area changes detected: {bool(post_apply_diff != pre_apply_diff)}")
                return False
            
            return True
            
        finally:
            # Clean up the temporary file
            try:
                os.unlink(patch_file_path)
            except OSError:
                pass
                
    except Exception as e:
        print(f"Error applying patch: {e}")
        return False


def _get_staged_diff() -> str:
    """
    Get the current diff of the staging area.
    
    Returns:
        String containing the staged diff
    """
    try:
        result = subprocess.run(
            ['git', 'diff', '--cached'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.stdout
    except Exception:
        return ""


def _verify_patch_was_applied(patch_content: str, pre_diff: str, post_diff: str) -> bool:
    """
    Verify that the intended patch changes are actually present in the staging area.
    
    Args:
        patch_content: The patch that was supposed to be applied
        pre_diff: Staging area diff before applying the patch
        post_diff: Staging area diff after applying the patch
        
    Returns:
        True if the patch changes are present in the staging area
    """
    # If there's no change in the staging area, the patch wasn't applied
    if pre_diff == post_diff:
        return False
    
    # Extract the meaningful content changes from the patch
    patch_additions = []
    patch_deletions = []
    
    for line in patch_content.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            # Remove the + prefix and normalize whitespace
            content = line[1:].rstrip()
            if content:  # Skip empty lines
                patch_additions.append(content)
        elif line.startswith('-') and not line.startswith('---'):
            # Remove the - prefix and normalize whitespace
            content = line[1:].rstrip()
            if content:  # Skip empty lines
                patch_deletions.append(content)
    
    # If the patch has no meaningful content, consider it applied
    if not patch_additions and not patch_deletions:
        return True
    
    # Check if the expected additions are present in the staging area
    staging_additions = []
    staging_deletions = []
    
    for line in post_diff.split('\n'):
        if line.startswith('+') and not line.startswith('+++'):
            content = line[1:].rstrip()
            if content:
                staging_additions.append(content)
        elif line.startswith('-') and not line.startswith('---'):
            content = line[1:].rstrip()
            if content:
                staging_deletions.append(content)
    
    # Verify that the expected changes are present
    # Check additions
    for expected_addition in patch_additions:
        found = any(expected_addition.strip() in staged.strip() for staged in staging_additions)
        if not found:
            print(f"Debug: Expected addition not found in staging: '{expected_addition}'")
            return False
    
    # Check deletions
    for expected_deletion in patch_deletions:
        found = any(expected_deletion.strip() in staged.strip() for staged in staging_deletions)
        if not found:
            print(f"Debug: Expected deletion not found in staging: '{expected_deletion}'")
            return False
    
    return True


def _relocate_and_apply_hunk(hunk: Hunk, base_diff: str) -> bool:
    """
    Intelligently relocate and apply a hunk using content-based matching.
    This is the core solution for the fundamental hunk application problem.
    
    Args:
        hunk: The hunk to relocate and apply
        base_diff: Original full diff for context
        
    Returns:
        True if successfully applied, False otherwise
    """
    try:
        # Step 1: Analyze the hunk content to understand what changes it makes
        additions, deletions, context_lines = _parse_hunk_content(hunk)
        
        # Step 2: Handle file operations (creation/deletion) specially
        if _is_file_operation_hunk(hunk):
            return _apply_file_operation_hunk(hunk, additions, deletions)
        
        # Step 3: Use content-based matching to find the best location
        best_location = _find_best_hunk_location(hunk, additions, deletions, context_lines)
        
        if best_location is None:
            print(f"Could not find suitable location for hunk {hunk.id}")
            return False
        
        # Step 4: Reconstruct the patch with correct line numbers for current file state
        relocated_patch = _reconstruct_patch_for_location(hunk, best_location, additions, deletions, context_lines)
        
        # Step 5: Apply the relocated patch
        return _apply_patch_to_staging(relocated_patch)
        
    except Exception as e:
        print(f"Error relocating hunk {hunk.id}: {e}")
        return False


def _parse_hunk_content(hunk: Hunk) -> Tuple[List[str], List[str], List[str]]:
    """
    Parse hunk content to extract additions, deletions, and context lines.
    
    Args:
        hunk: The hunk to parse
        
    Returns:
        Tuple of (additions, deletions, context_lines)
    """
    additions = []
    deletions = []
    context_lines = []
    
    for line in hunk.content.split('\n')[1:]:  # Skip header
        if not line:
            continue
        elif line.startswith('+') and not line.startswith('+++'):
            additions.append(line[1:])  # Remove + prefix
        elif line.startswith('-') and not line.startswith('---'):
            deletions.append(line[1:])  # Remove - prefix
        elif line.startswith(' '):
            context_lines.append(line[1:])  # Remove space prefix
    
    return additions, deletions, context_lines


def _is_file_operation_hunk(hunk: Hunk) -> bool:
    """
    Determine if a hunk represents a file creation or deletion operation.
    
    Args:
        hunk: The hunk to check
        
    Returns:
        True if this is a file operation hunk
    """
    # Check if this is a complete file deletion (hunk covers entire file)
    if hunk.start_line == 0 and hunk.end_line == 0:
        return True
    
    # Check if file doesn't exist (creation case)
    if not os.path.exists(hunk.file_path):
        return True
    
    # Check if hunk contains only additions (likely file creation)
    additions, deletions, _ = _parse_hunk_content(hunk)
    if deletions == [] and len(additions) > 10:  # Threshold for "new file"
        return True
    
    return False


def _apply_file_operation_hunk(hunk: Hunk, additions: list, deletions: list) -> bool:
    """
    Handle file creation and deletion operations specially.
    
    Args:
        hunk: The hunk representing file operation
        additions: Lines being added
        deletions: Lines being deleted
        
    Returns:
        True if operation succeeded
    """
    try:
        if not os.path.exists(hunk.file_path) and additions:
            # File creation case
            print(f"Creating new file: {hunk.file_path}")
            os.makedirs(os.path.dirname(hunk.file_path), exist_ok=True)
            with open(hunk.file_path, 'w', encoding='utf-8') as f:
                f.write('\n'.join(additions))
            
            # Stage the new file
            result = subprocess.run(['git', 'add', hunk.file_path], capture_output=True, text=True)
            return result.returncode == 0
        
        elif os.path.exists(hunk.file_path) and not additions and deletions:
            # File deletion case
            print(f"Deleting file: {hunk.file_path}")
            result = subprocess.run(['git', 'rm', hunk.file_path], capture_output=True, text=True)
            return result.returncode == 0
        
        else:
            # Fall back to content-based application
            return False
            
    except Exception as e:
        print(f"Error handling file operation for {hunk.file_path}: {e}")
        return False


def _find_best_hunk_location(hunk: Hunk, additions: list, deletions: list, context_lines: list) -> Optional[int]:
    """
    Find the best location in the current file to apply the hunk using content-based matching.
    
    Args:
        hunk: The hunk to locate
        additions: Lines being added
        deletions: Lines being deleted  
        context_lines: Context lines from the hunk
        
    Returns:
        Line number where hunk should be applied, or None if not found
    """
    try:
        # Read current file content
        with open(hunk.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            current_lines = [line.rstrip('\n') for line in f.readlines()]
    except (FileNotFoundError, IOError):
        return None
    
    if not current_lines:
        return 1  # Empty file, start at line 1
    
    # Strategy 1: Look for exact deletion matches
    if deletions:
        for i in range(len(current_lines) - len(deletions) + 1):
            if _lines_match_fuzzy(current_lines[i:i+len(deletions)], deletions):
                return i + 1  # Convert to 1-based line numbers
    
    # Strategy 2: Look for context matches
    if context_lines:
        for i in range(len(current_lines) - len(context_lines) + 1):
            if _lines_match_fuzzy(current_lines[i:i+len(context_lines)], context_lines):
                return i + 1
    
    # Strategy 3: Use original line number if it's reasonable
    if 1 <= hunk.start_line <= len(current_lines):
        return hunk.start_line
    
    # Strategy 4: Append to end of file
    return len(current_lines) + 1


def _lines_match_fuzzy(file_lines: list, target_lines: list, threshold: float = 0.7) -> bool:
    """
    Check if lines match with fuzzy matching (handles whitespace, etc.).
    
    Args:
        file_lines: Lines from the current file
        target_lines: Lines we're trying to match
        threshold: Minimum match ratio (0.0 to 1.0)
        
    Returns:
        True if lines match above threshold
    """
    if len(file_lines) != len(target_lines):
        return False
    
    if not target_lines:
        return True
    
    matches = 0
    for file_line, target_line in zip(file_lines, target_lines):
        # Normalize whitespace and compare
        if file_line.strip() == target_line.strip():
            matches += 1
        # Also allow partial matches for similar content
        elif target_line.strip() in file_line.strip() or file_line.strip() in target_line.strip():
            matches += 0.5
    
    match_ratio = matches / len(target_lines)
    return match_ratio >= threshold


def _reconstruct_patch_for_location(hunk: Hunk, line_number: int, additions: list, deletions: list, context_lines: list) -> str:
    """
    Reconstruct a valid patch for the specified location in the current file.
    
    Args:
        hunk: Original hunk
        line_number: Line number where patch should be applied
        additions: Lines being added
        deletions: Lines being deleted
        context_lines: Context lines
        
    Returns:
        Valid patch content
    """
    try:
        # Read current file to get actual context
        with open(hunk.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            current_lines = [line.rstrip('\n') for line in f.readlines()]
    except (FileNotFoundError, IOError):
        current_lines = []
    
    # Calculate patch parameters
    old_start = line_number
    old_count = len(deletions) + len(context_lines)
    new_start = line_number  
    new_count = len(additions) + len(context_lines)
    
    # Ensure counts are at least 1 if there are changes
    if old_count == 0 and (deletions or context_lines):
        old_count = 1
    if new_count == 0 and (additions or context_lines):
        new_count = 1
    
    # Build the patch
    patch_lines = []
    
    # Add file header
    patch_lines.extend([
        f"diff --git a/{hunk.file_path} b/{hunk.file_path}",
        f"index 0000000..1111111 100644",
        f"--- a/{hunk.file_path}",
        f"+++ b/{hunk.file_path}"
    ])
    
    # Add hunk header
    patch_lines.append(f"@@ -{old_start},{old_count} +{new_start},{new_count} @@")
    
    # Add context before deletions
    context_before = max(0, line_number - 3)
    for i in range(context_before, min(line_number - 1, len(current_lines))):
        if i >= 0:
            patch_lines.append(f" {current_lines[i]}")
    
    # Add deletions
    for deletion in deletions:
        patch_lines.append(f"-{deletion}")
    
    # Add additions
    for addition in additions:
        patch_lines.append(f"+{addition}")
    
    # Add context after
    context_after_start = line_number + len(deletions) - 1
    for i in range(context_after_start, min(context_after_start + 3, len(current_lines))):
        if i >= 0 and i < len(current_lines):
            patch_lines.append(f" {current_lines[i]}")
    
    return '\n'.join(patch_lines) + '\n'


def apply_hunks_with_fallback(hunk_ids: List[str], hunks_by_id: Dict[str, Hunk], base_diff: str) -> bool:
    """
    Apply hunks using the hunk-based approach only.
    
    Args:
        hunk_ids: List of hunk IDs to apply
        hunks_by_id: Dictionary mapping hunk IDs to Hunk objects
        base_diff: Original full diff output
        
    Returns:
        True if successful, False otherwise
    """
    return apply_hunks(hunk_ids, hunks_by_id, base_diff)


def _apply_files_fallback(hunk_ids: List[str], hunks_by_id: Dict[str, Hunk]) -> bool:
    """
    Fallback method: stage entire files that contain the specified hunks.
    
    Args:
        hunk_ids: List of hunk IDs
        hunks_by_id: Dictionary mapping hunk IDs to Hunk objects
        
    Returns:
        True if successful, False otherwise
    """
    try:
        # Get unique file paths from the hunks
        file_paths = set()
        for hunk_id in hunk_ids:
            if hunk_id in hunks_by_id:
                file_paths.add(hunks_by_id[hunk_id].file_path)
        
        if not file_paths:
            return True
        
        # Stage the files
        for file_path in file_paths:
            result = subprocess.run(
                ['git', 'add', file_path],
                capture_output=True,
                text=True,
                check=False
            )
            
            if result.returncode != 0:
                print(f"Failed to stage file {file_path}: {result.stderr}")
                return False
        
        return True
        
    except Exception as e:
        print(f"Error in file fallback: {e}")
        return False


def reset_staging_area():
    """Reset the staging area to match HEAD."""
    try:
        result = subprocess.run(
            ['git', 'reset', 'HEAD'],
            capture_output=True,
            text=True,
            check=False
        )
        return result.returncode == 0
    except Exception:
        return False


def create_patch_file_for_hunks(hunks: List[Hunk], base_diff: str, output_path: str) -> bool:
    """
    Create a patch file containing only the specified hunks.
    
    Args:
        hunks: List of hunks to include
        base_diff: Original full diff output
        output_path: Path where to save the patch file
        
    Returns:
        True if successful, False otherwise
    """
    try:
        patch_content = create_hunk_patch(hunks, base_diff)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(patch_content)
        
        return True
        
    except Exception as e:
        print(f"Error creating patch file: {e}")
        return False


def preview_hunk_application(hunk_ids: List[str], hunks_by_id: Dict[str, Hunk]) -> str:
    """
    Generate a preview of what would be applied when staging these hunks.
    
    Args:
        hunk_ids: List of hunk IDs to preview
        hunks_by_id: Dictionary mapping hunk IDs to Hunk objects
        
    Returns:
        String description of what would be applied
    """
    if not hunk_ids:
        return "No hunks selected."
    
    # Group hunks by file
    files_affected = {}
    for hunk_id in hunk_ids:
        if hunk_id in hunks_by_id:
            hunk = hunks_by_id[hunk_id]
            if hunk.file_path not in files_affected:
                files_affected[hunk.file_path] = []
            files_affected[hunk.file_path].append(hunk)
    
    # Generate preview
    preview_lines = []
    for file_path, hunks in files_affected.items():
        preview_lines.append(f"File: {file_path}")
        for hunk in sorted(hunks, key=lambda h: h.start_line):
            line_range = f"lines {hunk.start_line}-{hunk.end_line}"
            preview_lines.append(f"  - {hunk.id} ({line_range})")
        preview_lines.append("")
    
    return "\n".join(preview_lines)


def get_staging_status() -> Dict[str, List[str]]:
    """
    Get the current staging status.
    
    Returns:
        Dictionary with 'staged' and 'modified' file lists
    """
    try:
        result = subprocess.run(
            ['git', 'status', '--porcelain'],
            capture_output=True,
            text=True,
            check=True
        )
        
        staged = []
        modified = []
        
        for line in result.stdout.strip().split('\n'):
            if len(line) >= 2:
                status = line[:2]
                file_path = line[3:]
                
                if status[0] != ' ' and status[0] != '?':  # Staged changes
                    staged.append(file_path)
                if status[1] != ' ' and status[1] != '?':  # Modified changes
                    modified.append(file_path)
        
        return {'staged': staged, 'modified': modified}
        
    except Exception:
        return {'staged': [], 'modified': []}