# errorex/main.py

from rich import print
import traceback
import sys
from errorex.logger import log_to_markdown
from errorex.suggester import suggest_fixes

def explain_errors(log=True, suggest=True, raise_error=True):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception:
                exc_type, exc_value, exc_tb = sys.exc_info()
                tb_list = traceback.extract_tb(exc_tb)

                print(f"\n[bold red]⚠️ Exception Caught:[/bold red] {exc_value}")
                print("[blue]Traceback (User Code Only):[/blue]")

                for entry in tb_list:
                    if "site-packages" not in entry.filename:
                        print(f"[cyan]File:[/cyan] {entry.filename}, [cyan]Line:[/cyan] {entry.lineno}")
                        print(f"  [yellow]{entry.line}[/yellow]")

                tb = exc_tb
                user_frame = None
                while tb:
                    frame = tb.tb_frame
                    if "site-packages" not in frame.f_code.co_filename:
                        user_frame = frame
                    tb = tb.tb_next

                error_info = {
                    "exc_type": exc_type.__name__,
                    "exc_value": str(exc_value),
                    "traceback": [
                        {
                            "file": entry.filename,
                            "line": entry.lineno,
                            "code": entry.line
                        }
                        for entry in tb_list if "site-packages" not in entry.filename
                    ],
                    "locals": []
                }

                if user_frame:
                    for var, val in user_frame.f_locals.items():
                        try:
                            val_str = str(val)
                            if len(val_str) > 200:
                                val_str = val_str[:200] + "..."
                            error_info["locals"].append({
                                "name": var,
                                "type": type(val).__name__,
                                "value": val_str
                            })
                        except Exception:
                            error_info["locals"].append({
                                "name": var,
                                "type": "Unknown",
                                "value": "<unable to stringify>"
                            })

                if suggest:
                    error_info["suggestions"] = suggest_fixes(
                        exc_value=str(exc_value),
                        local_vars=error_info["locals"]
                    )

                if log:
                    log_to_markdown(error_info)

                print("\n[dim]Use traceback above to locate the bug.[/dim]")
                if raise_error:
                    raise

        return wrapper
    return decorator
