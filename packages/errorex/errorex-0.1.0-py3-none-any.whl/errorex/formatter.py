# errorex/formatter.py

def format_markdown(error_info: dict) -> str:
    lines = []

    lines.append(f"# Error Report - {error_info.get('timestamp', 'unknown')}\n")

    lines.append("## Exception:")
    lines.append(f"`{error_info['exc_type']}`: {error_info['exc_value']}\n")

    lines.append("## Traceback (User Code Only):")
    for entry in error_info.get("traceback", []):
        lines.append(f"- **File**: `{entry['file']}`, **Line**: {entry['line']}")
        lines.append("  ```python")
        lines.append(f"  {entry['code']}")
        lines.append("  ```")
    lines.append("")

    lines.append("## Local Variables at Crash:")
    for var in error_info.get("locals", []):
        lines.append(f"- `{var['name']}` (`{var['type']}`): `{var['value']}`")
    lines.append("")

    if error_info.get("suggestions"):
        lines.append("## Suggestions")
        for suggestion in error_info["suggestions"]:
            lines.append(f"- {suggestion}")
        lines.append("")

    lines.append("## LLM Debug Prompt")
    lines.append("```")
    lines.append("I encountered the following error in my Python script. Please help me understand and resolve it.\n")
    lines.append(f"Error:\n{error_info['exc_type']}: {error_info['exc_value']}\n")

    if error_info.get("traceback"):
        last = error_info["traceback"][-1]
        lines.append(f"Code:\n{last['code']}\n")

    if error_info.get("locals"):
        lines.append("Variables at time of error:")
        for var in error_info["locals"]:
            lines.append(f"- {var['name']}: {var['value']}")
    lines.append("\nWhat does this error mean and how can I fix it?")
    lines.append("```")

    return "\n".join(lines)
