"""Hunk applicator for staging specific hunks to git index."""

import subprocess
import tempfile
import os
from typing import List, Dict, Optional, Set
from .diff_parser import Hunk, validate_hunk_combination


class HunkApplicatorError(Exception):
    """Exception raised when hunk application fails."""
    pass


def apply_hunks(hunks: List[Hunk], hunk_map: Dict[str, Hunk]) -> None:
    """Apply specific hunks to the git staging area.
    
    Args:
        hunks: List of Hunk objects to apply
        hunk_map: Mapping from hunk IDs to Hunk objects for lookup
        
    Raises:
        HunkApplicatorError: If hunks cannot be applied
    """
    if not hunks:
        return
    
    # Validate that hunks can be applied together
    if not validate_hunk_combination(hunks):
        raise HunkApplicatorError("Hunks have overlapping line ranges and cannot be applied together")
    
    # Group hunks by file for more efficient processing
    files_hunks = _group_hunks_by_file(hunks)
    
    # Apply hunks file by file
    for file_path, file_hunks in files_hunks.items():
        try:
            _apply_file_hunks(file_path, file_hunks)
        except Exception as e:
            raise HunkApplicatorError(f"Failed to apply hunks for {file_path}: {e}")


def apply_hunks_by_ids(hunk_ids: List[str], hunk_map: Dict[str, Hunk]) -> None:
    """Apply specific hunks by their IDs.
    
    Args:
        hunk_ids: List of hunk IDs to apply
        hunk_map: Mapping from hunk IDs to Hunk objects
        
    Raises:
        HunkApplicatorError: If any hunk ID is not found or application fails
    """
    # Look up hunks by ID
    hunks = []
    missing_ids = []
    
    for hunk_id in hunk_ids:
        if hunk_id in hunk_map:
            hunks.append(hunk_map[hunk_id])
        else:
            missing_ids.append(hunk_id)
    
    if missing_ids:
        raise HunkApplicatorError(f"Hunk IDs not found: {missing_ids}")
    
    apply_hunks(hunks, hunk_map)


def create_patch_for_hunks(hunks: List[Hunk]) -> str:
    """Create a unified patch file for the given hunks.
    
    Args:
        hunks: List of Hunk objects to include in patch
        
    Returns:
        String containing the patch content
    """
    if not hunks:
        return ""
    
    # Group hunks by file
    files_hunks = _group_hunks_by_file(hunks)
    
    patch_parts = []
    
    for file_path, file_hunks in files_hunks.items():
        # Check if this is a new file by looking at the first hunk's content
        is_new_file = _is_new_file_from_hunks(file_hunks)
        
        # Create appropriate file header
        file_header = f"diff --git a/{file_path} b/{file_path}\n"
        
        if is_new_file:
            file_header += f"new file mode 100644\n"
            file_header += f"index 0000000..1111111\n"
            file_header += f"--- /dev/null\n"
            file_header += f"+++ b/{file_path}\n"
        else:
            file_header += f"index 0000000..1111111 100644\n"  # Dummy index line
            file_header += f"--- a/{file_path}\n"
            file_header += f"+++ b/{file_path}\n"
        
        patch_parts.append(file_header)
        
        # Add hunks for this file (sorted by line number)
        sorted_hunks = sorted(file_hunks, key=lambda h: h.start_line)
        for hunk in sorted_hunks:
            # Extract just the hunk content (without the diff header)
            hunk_lines = hunk.content.split('\n')
            # Find the @@ line and include everything after it
            hunk_content_lines = []
            found_hunk_header = False
            for line in hunk_lines:
                if line.startswith('@@'):
                    found_hunk_header = True
                if found_hunk_header:
                    hunk_content_lines.append(line)
            
            if hunk_content_lines:
                patch_parts.append('\n'.join(hunk_content_lines))
    
    return '\n'.join(patch_parts)


def _group_hunks_by_file(hunks: List[Hunk]) -> Dict[str, List[Hunk]]:
    """Group hunks by their file path.
    
    Args:
        hunks: List of Hunk objects
        
    Returns:
        Dictionary mapping file paths to lists of hunks
    """
    files_hunks = {}
    for hunk in hunks:
        if hunk.file_path not in files_hunks:
            files_hunks[hunk.file_path] = []
        files_hunks[hunk.file_path].append(hunk)
    
    return files_hunks


def _apply_file_hunks(file_path: str, hunks: List[Hunk]) -> None:
    """Apply hunks for a single file.
    
    Args:
        file_path: Path to the file
        hunks: List of hunks for this file
        
    Raises:
        HunkApplicatorError: If application fails
    """
    # Sort hunks by line number
    sorted_hunks = sorted(hunks, key=lambda h: h.start_line)
    
    # Create a patch file containing just these hunks
    patch_content = create_patch_for_hunks(sorted_hunks)
    
    if not patch_content.strip():
        return
    
    # Write patch to temporary file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as f:
        f.write(patch_content)
        patch_file = f.name
    
    try:
        # Try to apply the patch to the staging area
        result = subprocess.run([
            'git', 'apply', '--cached', '--verbose', patch_file
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            # If direct application fails, try different strategies
            if 'does not apply' in result.stderr:
                # Try applying with 3-way merge
                _apply_with_fallback_strategies(file_path, sorted_hunks, patch_file)
            else:
                raise HunkApplicatorError(f"Git apply failed: {result.stderr}")
    
    finally:
        # Clean up temporary patch file
        try:
            os.unlink(patch_file)
        except OSError:
            pass


def _apply_with_fallback_strategies(file_path: str, hunks: List[Hunk], patch_file: str) -> None:
    """Try various fallback strategies when direct patch application fails.
    
    Args:
        file_path: Path to the file
        hunks: List of hunks to apply
        patch_file: Path to the patch file
        
    Raises:
        HunkApplicatorError: If all strategies fail
    """
    strategies = [
        # Strategy 1: Apply with --ignore-whitespace
        lambda: subprocess.run([
            'git', 'apply', '--cached', '--ignore-whitespace', patch_file
        ], capture_output=True, text=True),
        
        # Strategy 2: Apply individual hunks one by one
        lambda: _apply_hunks_individually(hunks),
        
        # Strategy 3: Fall back to file-based staging
        lambda: _fallback_to_file_staging(file_path)
    ]
    
    last_error = None
    for i, strategy in enumerate(strategies):
        try:
            result = strategy()
            if hasattr(result, 'returncode') and result.returncode == 0:
                return
            elif not hasattr(result, 'returncode'):  # Successful individual application
                return
        except Exception as e:
            last_error = e
            continue
    
    # All strategies failed
    raise HunkApplicatorError(f"All fallback strategies failed. Last error: {last_error}")


def _apply_hunks_individually(hunks: List[Hunk]) -> None:
    """Apply hunks one by one as a fallback strategy.
    
    Args:
        hunks: List of hunks to apply individually
        
    Raises:
        HunkApplicatorError: If any hunk fails to apply
    """
    for hunk in hunks:
        # Create a patch for just this hunk
        hunk_patch = create_patch_for_hunks([hunk])
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.patch', delete=False) as f:
            f.write(hunk_patch)
            hunk_patch_file = f.name
        
        try:
            result = subprocess.run([
                'git', 'apply', '--cached', '--ignore-whitespace', hunk_patch_file
            ], capture_output=True, text=True)
            
            if result.returncode != 0:
                raise HunkApplicatorError(f"Failed to apply hunk {hunk.id}: {result.stderr}")
        
        finally:
            try:
                os.unlink(hunk_patch_file)
            except OSError:
                pass


def _is_new_file_from_hunks(hunks: List[Hunk]) -> bool:
    """Determine if hunks represent a new file creation.
    
    Args:
        hunks: List of hunks for a single file
        
    Returns:
        True if this appears to be a new file
    """
    if not hunks:
        return False
    
    # Check if any hunk has a hunk header indicating new file (starts from line 0)
    for hunk in hunks:
        if '@@ -0,0 +' in hunk.hunk_header:
            return True
    
    return False


def _fallback_to_file_staging(file_path: str) -> None:
    """Fall back to staging the entire file when hunk application fails.
    
    Args:
        file_path: Path to the file to stage
        
    Raises:
        HunkApplicatorError: If file staging fails
    """
    # Check if file exists before trying to stage it
    if not os.path.exists(file_path):
        # File might be deleted, try staging the deletion
        result = subprocess.run([
            'git', 'add', file_path
        ], capture_output=True, text=True)
    else:
        result = subprocess.run([
            'git', 'add', file_path
        ], capture_output=True, text=True)
    
    if result.returncode != 0:
        raise HunkApplicatorError(f"Failed to stage file {file_path}: {result.stderr}")


def get_staged_hunks(all_hunks: List[Hunk]) -> Set[str]:
    """Get the IDs of hunks that are currently staged.
    
    Args:
        all_hunks: List of all available hunks
        
    Returns:
        Set of hunk IDs that are currently staged
    """
    try:
        # Get the diff of staged changes
        result = subprocess.run([
            'git', 'diff', '--cached'
        ], capture_output=True, text=True, check=True)
        
        if not result.stdout.strip():
            return set()
        
        # Parse the staged diff to find which hunks are included
        from .diff_parser import parse_diff
        staged_hunks = parse_diff(result.stdout)
        
        # Match staged hunks with our hunk IDs
        staged_ids = set()
        for staged_hunk in staged_hunks:
            # Find matching hunk in our list (by file and approximate line range)
            for original_hunk in all_hunks:
                if (staged_hunk.file_path == original_hunk.file_path and
                    abs(staged_hunk.start_line - original_hunk.start_line) <= 2):
                    staged_ids.add(original_hunk.id)
                    break
        
        return staged_ids
        
    except subprocess.CalledProcessError:
        return set()


def unstage_all_hunks() -> None:
    """Unstage all currently staged changes.
    
    Raises:
        HunkApplicatorError: If unstaging fails
    """
    try:
        result = subprocess.run([
            'git', 'reset', 'HEAD'
        ], capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        raise HunkApplicatorError(f"Failed to unstage changes: {e.stderr}")


def reset_to_base_branch(base_branch: str) -> None:
    """Reset the current branch to the base branch.
    
    Args:
        base_branch: Name of the base branch to reset to
        
    Raises:
        HunkApplicatorError: If reset fails
    """
    try:
        # First, reset the index and working tree to base branch
        result = subprocess.run([
            'git', 'reset', '--soft', base_branch
        ], capture_output=True, text=True, check=True)
        
        # Then unstage any changes that might be left
        unstage_all_hunks()
        
    except subprocess.CalledProcessError as e:
        raise HunkApplicatorError(f"Failed to reset to {base_branch}: {e.stderr}")