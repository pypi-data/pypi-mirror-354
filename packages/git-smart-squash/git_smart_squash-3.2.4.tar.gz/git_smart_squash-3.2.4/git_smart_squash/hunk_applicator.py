"""
Hunk applicator module for applying specific hunks to the git staging area.
"""

import os
import re
import subprocess
import tempfile
from typing import List, Dict, Optional
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
            # Pre-validate that the hunk can be applied to the current file state
            if not _validate_hunk_can_be_applied(hunk):
                print(f"Error: Hunk {hunk.id} cannot be applied to current file state")
                return False
            
            # Create a patch for this single hunk
            single_hunk_patch = create_hunk_patch([hunk], base_diff)
            
            if not single_hunk_patch.strip():
                print(f"Warning: Empty patch generated for hunk {hunk.id}")
                continue
            
            # Validate the patch before applying
            if not _validate_patch_format(single_hunk_patch):
                print(f"Error: Invalid patch format for hunk {hunk.id}")
                return False
            
            # Apply this individual hunk
            success = _apply_patch_to_staging(single_hunk_patch)
            if not success:
                print(f"Failed to apply hunk {hunk.id} ({i+1}/{len(ordered_hunks)})")
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
            # Pre-validate that the hunk can be applied to the current file state
            if not _validate_hunk_can_be_applied(hunk):
                print(f"Error: Hunk {hunk.id} cannot be applied to current file state")
                return False
            
            # Create a patch for this single hunk
            single_hunk_patch = create_hunk_patch([hunk], base_diff)
            
            if not single_hunk_patch.strip():
                print(f"Warning: Empty patch generated for hunk {hunk.id}")
                continue
            
            # Validate the patch before applying
            if not _validate_patch_format(single_hunk_patch):
                print(f"Error: Invalid patch format for hunk {hunk.id}")
                return False
            
            # Apply this individual hunk
            success = _apply_patch_to_staging(single_hunk_patch)
            if not success:
                print(f"Failed to apply hunk {hunk.id} ({i+1}/{len(sorted_hunks)})")
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


def _validate_hunk_can_be_applied(hunk: Hunk) -> bool:
    """
    Validate that a hunk can be applied to the current file state.
    
    Args:
        hunk: The hunk to validate
        
    Returns:
        True if the hunk can likely be applied successfully
    """
    try:
        # Read the current file content
        with open(hunk.file_path, 'r', encoding='utf-8', errors='ignore') as f:
            current_lines = f.readlines()
    except (FileNotFoundError, IOError):
        print(f"Warning: Cannot read file {hunk.file_path} for hunk validation")
        return False
    
    # Parse the hunk header to get line information
    hunk_lines = hunk.content.split('\n')
    if not hunk_lines or not hunk_lines[0].startswith('@@'):
        print(f"Warning: Invalid hunk header for {hunk.id}")
        return False
    
    header_match = re.match(r'@@ -(\d+)(?:,(\d+))? \+(\d+)(?:,(\d+))? @@', hunk_lines[0])
    if not header_match:
        print(f"Warning: Cannot parse hunk header for {hunk.id}: {hunk_lines[0]}")
        return False
    
    old_start = int(header_match.group(1))
    old_count = int(header_match.group(2)) if header_match.group(2) else 1
    
    # Check if the line numbers are within the file bounds
    if old_start < 1 or old_start > len(current_lines):
        print(f"Warning: Hunk {hunk.id} references invalid line number {old_start} (file has {len(current_lines)} lines)")
        return False
    
    # Check if the end line is within bounds
    old_end = old_start + old_count - 1
    if old_end > len(current_lines):
        print(f"Warning: Hunk {hunk.id} extends beyond file end (line {old_end} > {len(current_lines)})")
        return False
    
    # Validate context lines match the current file
    context_lines = []
    for line in hunk_lines[1:]:
        if line.startswith(' '):  # Context line
            context_lines.append(line[1:])
        elif line.startswith('-'):
            context_lines.append(line[1:])
    
    # Check that at least some context lines match the current file
    if context_lines:
        file_section = current_lines[old_start-1:old_start-1+len(context_lines)]
        matches = 0
        for i, context_line in enumerate(context_lines):
            if i < len(file_section):
                # Normalize whitespace for comparison
                if context_line.strip() == file_section[i].strip():
                    matches += 1
        
        # Require at least 50% of context lines to match
        match_ratio = matches / len(context_lines) if context_lines else 1.0
        if match_ratio < 0.5:
            print(f"Warning: Hunk {hunk.id} context mismatch (only {match_ratio:.1%} of lines match current file)")
            return False
    
    return True


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