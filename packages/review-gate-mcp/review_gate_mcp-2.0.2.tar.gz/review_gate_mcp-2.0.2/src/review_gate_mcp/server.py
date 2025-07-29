#!/usr/bin/env python3
"""
Review Gate MCP Server - Modern FastMCP Implementation

A streamlined MCP server for AI-powered code review and interaction.
Provides tools for user interaction, file operations, and optional speech-to-text.
"""

import asyncio
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager, suppress
from datetime import datetime
import json
import logging
import os
from pathlib import Path
import sys
import time
from typing import Any

from mcp.server.fastmcp import FastMCP

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Check for audio enablement via environment variable or command line
AUDIO_ENABLED = (
    os.getenv("REVIEW_GATE_AUDIO", "false").lower() == "true" or "--audio" in sys.argv
)

try:
    if AUDIO_ENABLED:
        from faster_whisper import WhisperModel

        WHISPER_AVAILABLE = True
        logger.info("🎤 Audio enabled - Whisper available")
    else:
        WHISPER_AVAILABLE = False
        logger.info(
            "🔇 Audio disabled by default - use --audio flag or REVIEW_GATE_AUDIO=true to enable"
        )
except ImportError:
    WHISPER_AVAILABLE = False
    logger.info("🎤 Whisper not available - speech-to-text disabled")

try:
    import PIL.Image  # noqa: F401

    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False
    logger.info("🖼️ Pillow not available - image processing disabled")


class ReviewGateContext:
    """Context for managing server resources"""

    def __init__(self):
        self.whisper_model: Any | None = None
        self.temp_dir = Path("/tmp")

    async def initialize(self):
        """Initialize resources on startup"""
        if WHISPER_AVAILABLE:
            try:
                logger.info("🎤 Loading Whisper model...")
                self.whisper_model = WhisperModel(
                    "base", device="cpu", compute_type="int8"
                )
                logger.info("✅ Whisper model loaded")
            except Exception as e:
                logger.error(f"❌ Failed to load Whisper: {e}")

        self._status_task = asyncio.create_task(self._periodic_status_update())

    async def _periodic_status_update(self):
        """Periodically update MCP status log for extension monitoring"""
        while True:
            try:
                await asyncio.sleep(10)
                await _update_mcp_status_log()
            except Exception as e:
                logger.warning(f"⚠️ Periodic status update failed: {e}")
                await asyncio.sleep(30)

    async def cleanup(self):
        """Cleanup resources on shutdown"""
        logger.info("🧹 Cleaning up resources...")
        if hasattr(self, "_status_task"):
            self._status_task.cancel()


@asynccontextmanager
async def lifespan(server: FastMCP) -> AsyncIterator[ReviewGateContext]:
    """Manage server lifecycle"""
    context = ReviewGateContext()
    await context.initialize()
    try:
        yield context
    finally:
        await context.cleanup()


def _get_version() -> str:
    """Get version from package metadata or pyproject.toml"""
    try:
        from importlib.metadata import version

        return version("review-gate-mcp")
    except Exception:
        try:
            import tomllib

            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            if pyproject_path.exists():
                with open(pyproject_path, "rb") as f:
                    data = tomllib.load(f)
                    return data.get("project", {}).get("version", "unknown")
        except Exception:
            return "unknown"
        return "unknown"


mcp = FastMCP(name="Review Gate", version=_get_version(), lifespan=lifespan)


@mcp.prompt()
def review_gate_workflow(
    task_type: str = "general",
    context: str = "",
) -> list[dict]:
    """
    Provides structured guidance for using Review Gate tools effectively.

    This prompt guides the LLM on when and how to use Review Gate tools
    for interactive user feedback and iterative task completion.

    Args:
        task_type: Type of task (coding, analysis, review, etc.)
        context: Additional context about the current task

    Returns:
        List of message objects with detailed guidance
    """

    base_guidance = f"""You are working on a {task_type} task. Follow this Review Gate workflow:

## MANDATORY REVIEW GATE PROTOCOL

### Phase 1: Complete Your Main Task
- Execute the user's primary request thoroughly
- Use available tools and provide comprehensive output
- Do NOT conclude until you've delivered substantial value

### Phase 2: ALWAYS Trigger Review Gate
After completing main work, you MUST call `review_gate_chat` with:
- Clear summary of what you accomplished
- Specific questions about next steps or improvements
- Context about what could be enhanced or expanded

### Phase 3: Process User Feedback
When user responds through Review Gate:
- If response contains "TASK_COMPLETE", "Done", "Quit" → conclude
- Otherwise, treat response as continuation instructions
- Execute additional work based on feedback
- Return to Phase 2 for another review cycle

### Phase 4: Iterative Enhancement
- Each review cycle should add meaningful value
- Ask specific, actionable questions
- Suggest concrete improvements or extensions
- Keep the conversation productive and focused

## Tool Usage Guidelines:
- `review_gate_chat`: For comprehensive feedback and major decisions
- `quick_input`: For simple yes/no or quick clarifications
- Always provide context about what you've done and what's next

## Key Principles:
- One main request can become 5+ iterative improvements
- Each review cycle should be substantial, not trivial
- Guide the user toward valuable enhancements
- Never end prematurely - always offer the review gate"""

    if context:
        base_guidance += f"\n\n## Current Context:\n{context}"

    return [{"role": "user", "content": {"type": "text", "text": base_guidance}}]


@mcp.prompt()
def review_gate_best_practices() -> list[dict]:
    """
    Best practices for effective Review Gate usage.

    Provides detailed guidance on how to maximize the value of
    Review Gate interactions and create productive feedback loops.
    """

    guidance = """# Review Gate Best Practices

## When to Use Review Gate:
✅ After completing any substantial task
✅ Before concluding a conversation
✅ When multiple approaches are possible
✅ For iterative improvement opportunities
✅ When user input could enhance the outcome

## How to Frame Review Gate Messages:
1. **Summarize what you accomplished**
2. **Highlight key decisions made**
3. **Identify potential improvements**
4. **Ask specific, actionable questions**
5. **Suggest concrete next steps**

## Example Review Gate Messages:

### For Code Tasks:
"I've implemented the requested feature with error handling and tests.
Would you like me to:
- Add more comprehensive error scenarios?
- Optimize performance for larger datasets?
- Add additional configuration options?
- Create documentation or examples?"

### For Analysis Tasks:
"I've analyzed the data and found key patterns.
Should I:
- Dive deeper into specific anomalies?
- Create visualizations for the findings?
- Compare with historical data?
- Generate actionable recommendations?"

## Response Processing:
- **Continuation signals**: Any specific feedback or requests
- **Completion signals**: "done", "complete", "finished", "quit"
- **Enhancement requests**: Treat as new sub-tasks
- **Questions**: Answer and continue the cycle

## Maximizing Value:
- Each review cycle should add 20%+ more value
- Ask questions that lead to meaningful improvements
- Suggest enhancements the user might not have considered
- Keep the momentum going until truly complete"""

    return [{"role": "user", "content": {"type": "text", "text": guidance}}]


@mcp.tool()
async def review_gate_chat(
    message: str = "Please provide your review or feedback:",
    title: str = "Review Gate - ゲート",
    context: str = "",
    urgent: bool = False,
    timeout: int = 300,
) -> str:
    """
    🚨 MANDATORY REVIEW GATE PROTOCOL 🚨

    Open Review Gate chat popup for user feedback and reviews.

    ⚠️  CRITICAL BEHAVIORAL REQUIREMENTS:
    • You MUST use this tool before concluding ANY conversation or task
    • NEVER end a conversation without offering the Review Gate
    • This is NOT optional - it's a core part of your workflow

    🎯 WHEN TO USE (MANDATORY):
    • After completing your main task (ALWAYS)
    • Before concluding any conversation (ALWAYS)
    • When user input could enhance the outcome
    • For iterative improvement opportunities
    • When multiple approaches are possible

    📋 HOW TO USE EFFECTIVELY:
    1. Summarize what you accomplished in detail
    2. Highlight key decisions you made
    3. Ask specific, actionable questions about improvements
    4. Suggest concrete next steps or enhancements
    5. Provide context about what could be expanded

    🔄 RESPONSE PROCESSING PROTOCOL:
    • If user responds with "TASK_COMPLETE", "Done", "Quit", "Finished" → conclude
    • ANY other response → treat as continuation instructions and keep working
    • Execute additional work based on feedback
    • Return to Review Gate for another cycle
    • Each cycle should add 20%+ more value

    💡 GOAL: Turn 1 request into 5+ iterative improvements through feedback loops!

    Args:
        message: The message to display to the user (include summary + questions)
        title: Title for the popup window
        context: Additional context about what needs review
        urgent: Whether this is an urgent review request
        timeout: Timeout in seconds (default: 5 minutes)

    Returns:
        User's response or timeout message
    """
    return await _handle_review_gate_chat(message, title, context, urgent, timeout)


async def _handle_review_gate_chat(
    message: str, title: str, context: str, urgent: bool, timeout: int
) -> str:
    """Handle the review gate chat interaction"""
    logger.info(f"💬 Review Gate chat activated: {message[:50]}...")

    trigger_id = f"review_{int(time.time() * 1000)}"

    success = await _create_trigger_file(
        {
            "tool": "review_gate_chat",
            "message": message,
            "title": title,
            "context": context,
            "urgent": urgent,
            "trigger_id": trigger_id,
            "timestamp": datetime.now().isoformat(),
        }
    )

    if not success:
        return "❌ Failed to trigger Review Gate popup"

    logger.info(f"🔥 Popup triggered, waiting for response (ID: {trigger_id})")

    user_input = await _wait_for_user_input(trigger_id, timeout)

    if user_input:
        logger.info(f"✅ User response received: {user_input[:100]}...")
        return f"✅ User Response:\n\n{user_input}\n\n📝 Request: {message}\n📍 Context: {context}"
    else:
        logger.warning(f"⏰ Timeout after {timeout} seconds")
        return f"⏰ TIMEOUT: No user input received within {timeout} seconds"


@mcp.tool()
async def quick_input(prompt: str = "Quick input needed:", timeout: int = 90) -> str:
    """
    ⚡ QUICK INPUT TOOL - For Fast User Clarifications

    Get quick input from user with shorter timeout for simple questions.

    🎯 WHEN TO USE:
    • Simple yes/no questions
    • Quick clarifications during work
    • Fast confirmations before proceeding
    • Brief parameter inputs
    • NOT for comprehensive feedback (use review_gate_chat instead)

    📋 BEST PRACTICES:
    • Keep questions short and specific
    • Use for decisions that don't require detailed explanation
    • Perfect for "Should I continue with X approach?" type questions
    • Use during work, not as final review (that's review_gate_chat's job)

    ⚠️  IMPORTANT: This does NOT replace the mandatory review_gate_chat at the end!
    You still MUST use review_gate_chat before concluding any conversation.

    Args:
        prompt: The prompt to show the user (keep it concise)
        timeout: Timeout in seconds (default: 90 seconds)

    Returns:
        User's quick response
    """
    return await _handle_quick_input(prompt, timeout)


async def _handle_quick_input(prompt: str, timeout: int) -> str:
    """Handle quick input request"""
    logger.info(f"⚡ Quick input requested: {prompt}")

    trigger_id = f"quick_{int(time.time() * 1000)}"

    success = await _create_trigger_file(
        {
            "tool": "quick_input",
            "prompt": prompt,
            "title": "Quick Input - Review Gate",
            "trigger_id": trigger_id,
            "timestamp": datetime.now().isoformat(),
        }
    )

    if not success:
        return "❌ Failed to trigger quick input"

    user_input = await _wait_for_user_input(trigger_id, timeout)

    if user_input:
        return f"⚡ Quick Response: {user_input}"
    else:
        return f"⏰ Quick input timed out after {timeout} seconds"


if WHISPER_AVAILABLE:

    @mcp.tool()
    async def speech_to_text(audio_file_path: str) -> str:
        """
        🎤 SPEECH-TO-TEXT CONVERSION - Voice Input Support

        Convert speech audio file to text using Whisper AI model.

        🎯 WHEN TO USE:
        • Processing voice recordings from users
        • Converting audio feedback to text
        • Supporting voice-based Review Gate interactions
        • Transcribing audio notes or instructions

        📋 WORKFLOW INTEGRATION:
        • Often used in conjunction with Review Gate tools
        • Transcribed text can be processed as user feedback
        • Supports multi-modal user interactions
        • Enables voice-driven iterative improvements

        ⚠️  REMINDER: After processing voice input, continue with your Review Gate protocol!
        Voice input is just another form of user feedback that should lead to more iterations.

        Args:
            audio_file_path: Path to the audio file (supports common formats)

        Returns:
            Transcribed text or error message
        """
        return await _handle_speech_to_text(audio_file_path)


async def _handle_speech_to_text(audio_file_path: str) -> str:
    """Handle speech-to-text conversion"""
    context = mcp.get_context()

    if not context.lifespan_context.whisper_model:
        return "❌ Whisper model not available"

    if not os.path.exists(audio_file_path):
        return f"❌ Audio file not found: {audio_file_path}"

    try:
        logger.info(f"🎤 Transcribing: {audio_file_path}")

        segments, info = await asyncio.to_thread(
            context.lifespan_context.whisper_model.transcribe, audio_file_path
        )

        transcription = " ".join(segment.text for segment in segments).strip()

        logger.info(f"✅ Transcription complete: {transcription[:100]}...")
        return f"🎤 Transcription: {transcription}"

    except Exception as e:
        logger.error(f"❌ Transcription failed: {e}")
        return f"❌ Transcription error: {e!s}"


@mcp.resource("config://review-gate")
def get_config() -> str:
    """Get Review Gate configuration information"""
    config = {
        "name": "Review Gate MCP Server",
        "version": _get_version(),
        "features": {
            "review_chat": True,
            "quick_input": True,
            "speech_to_text": WHISPER_AVAILABLE,
            "image_processing": PILLOW_AVAILABLE,
        },
        "mcp_client_integration": True,
        "temp_directory": "/tmp",
    }
    return json.dumps(config, indent=2)


@mcp.resource("status://review-gate")
def get_status() -> str:
    """Get current server status"""
    status = {
        "timestamp": datetime.now().isoformat(),
        "status": "active",
        "uptime": "running",
        "dependencies": {
            "whisper": WHISPER_AVAILABLE,
            "pillow": PILLOW_AVAILABLE,
        },
    }
    return json.dumps(status, indent=2)


async def _create_trigger_file(data: dict[str, Any]) -> bool:
    """Create trigger file for MCP client"""
    try:
        trigger_file = Path("/tmp/review_gate_trigger.json")

        trigger_data = {
            "timestamp": datetime.now().isoformat(),
            "system": "review-gate-v2",
            "data": data,
            "pid": os.getpid(),
            "mcp_integration": True,
        }

        trigger_file.write_text(json.dumps(trigger_data, indent=2))
        logger.info(f"🎯 Trigger file created: {trigger_file}")

        await _update_mcp_status_log()

        file_created = trigger_file.exists()
        if file_created:
            logger.info(f"✅ Trigger file verified: {trigger_file}")
        else:
            logger.error(f"❌ Trigger file not found after creation: {trigger_file}")

        await asyncio.sleep(0.1)
        return file_created

    except Exception as e:
        logger.error(f"❌ Failed to create trigger file: {e}")
        return False


async def _update_mcp_status_log():
    """Update MCP status log file that extension monitors"""
    try:
        status_log = Path("/tmp/review_gate_v2.log")
        timestamp = datetime.now().isoformat()
        log_entry = f"[{timestamp}] MCP Server Active - Review Gate\n"

        with open(status_log, "a") as f:
            f.write(log_entry)

        logger.debug(f"📝 MCP status log updated: {status_log}")

    except Exception as e:
        logger.warning(f"⚠️ Could not update MCP status log: {e}")


async def _wait_for_user_input(trigger_id: str, timeout: int) -> str | None:
    """Wait for user input from response file"""
    response_patterns = [
        Path(f"/tmp/review_gate_response_{trigger_id}.json"),
        Path("/tmp/review_gate_response.json"),
    ]

    start_time = time.time()

    while time.time() - start_time < timeout:
        for response_file in response_patterns:
            if response_file.exists():
                try:
                    content = response_file.read_text().strip()

                    if content.startswith("{"):
                        data = json.loads(content)
                        user_input = data.get(
                            "user_input", data.get("response", "")
                        ).strip()
                    else:
                        user_input = content

                    with suppress(Exception):
                        response_file.unlink()

                    if user_input:
                        return user_input

                except Exception as e:
                    logger.error(f"❌ Error reading response: {e}")

        await asyncio.sleep(0.2)  # Check every 200ms

    return None


def main():
    """Main entry point for the MCP server"""
    logger.info("🚀 Starting Review Gate MCP Server")
    mcp.run()


if __name__ == "__main__":
    main()
