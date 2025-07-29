import re
import subprocess
from pathlib import Path
from typing import Dict, Optional


def find_git_origin_url(file_or_folder_path: str) -> Optional[str]:
    path = Path(file_or_folder_path)
    dir_path = path.parent if path.is_file() else path
    git_dir = dir_path / ".git"
    if not git_dir.is_dir():
        return None

    try:
        result = subprocess.run(
            ["git", "-C", str(dir_path), "config", "--get", "remote.origin.url"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
        )
        url = result.stdout.strip()
        if url and url.startswith("git@"):
            url = f"ssh://{url}"

        return url if url else None
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def get_dynatrace_versions(full_version: Optional[str]) -> Dict[str, Optional[str]]:
    if isinstance(full_version, str):
        base_version = re.sub(r"\.\d+-\d+$", "", full_version)
    else:
        base_version = None

    return {"base": base_version, "full": full_version}
