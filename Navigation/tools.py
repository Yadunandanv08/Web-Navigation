from Navigation.mcp_manager import MCPSessionKeeper
import time

manager = MCPSessionKeeper.get_instance()


def browser_navigate(url: str):
    """
    Opens a URL in the Playwright MCP server browser.
    """
    try:
        manager.start()
        result = manager.call_tool("browser_navigate", {"url": url})
        return result
    except Exception as e:
        return f"Error navigating: {e}"


def browser_snapshot():
    """Extracts elements in webpage and returns it for choosing the required one"""
    try:
        time.sleep(5)

        raw = manager.call_tool("browser_snapshot", {})
        
        snapshot_text = ""
        if hasattr(raw, "content") and isinstance(raw.content, list):
            for content_block in raw.content:
                if content_block.type == "text":
                    snapshot_text += content_block.text
        
        return {"elements": snapshot_text}

    except Exception as e:
        return {"error": str(e)}


def browser_click(ref: str):
    """
    Click an element using its MCP ref-id.
    """
    try:
        result = manager.call_tool("browser_click", {"ref": ref})
        return f"Clicked element with ref={ref}"
    except Exception as e:
        return f"Error clicking element: {e}"


def browser_type(ref: str, text: str):
    """
    Types text into an element using MCP ref-id.
    """
    try:
        result = manager.call_tool("browser_type", {
            "ref": ref,
            "text": text,
        })
        return f"Typed into element ref={ref}"
    except Exception as e:
        return f"Error typing: {e}"

def browser_press(key: str):
    """
    Presses a keyboard key inside the open page.
    """
    try:
        manager.call_tool("browser_press", {"key": key})
        return f"Pressed key: {key}"
    except Exception as e:
        return f"Error pressing key: {e}"

def browser_close():
    """
    Closes the current page/session.
    """
    try:
        manager.call_tool("browser_close", {})
        manager.stop()
        return "Browser session closed."
    except Exception as e:
        return f"Error closing browser: {e}"
