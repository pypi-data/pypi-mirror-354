import asyncio
import io
from typing import Generator

import pytest
from prompt_toolkit import PromptSession
from prompt_toolkit.input import create_pipe_input, PipeInput
from prompt_toolkit.output import DummyOutput
from ptcmd import Cmd


@pytest.fixture
def pipe_input() -> Generator[PipeInput, None, None]:
    """Fixture providing pipe input for testing."""
    with create_pipe_input() as inp:
        yield inp

@pytest.fixture
def cmd(pipe_input: PipeInput) -> Cmd:
    """Fixture providing a BaseCmd instance with mocked stdout and real session."""
    stdout = io.StringIO()
    # Create real PromptSession with pipe input
    session = PromptSession(
        input=pipe_input,
        output=DummyOutput()
    )
    return Cmd(stdout=stdout, session=session)


def test_parseline(cmd: Cmd) -> None:
    """Test command line parsing."""
    # Test basic command
    cmd_name, args, line = cmd.parseline("test arg1 arg2")
    assert cmd_name == "test"
    assert args == ["arg1", "arg2"]
    assert line == "test arg1 arg2"

    # Test shortcut
    cmd_name, args, line = cmd.parseline("? arg1")
    assert cmd_name == "help"
    assert args == ["arg1"]


@pytest.mark.asyncio
async def test_cmdloop_async(cmd: Cmd, pipe_input: PipeInput) -> None:
    """Test async command loop with real input."""
    # Send input command
    pipe_input.send_text("exit\n")

    # Run cmdloop with timeout
    try:
        await asyncio.wait_for(cmd.cmdloop_async(), timeout=1.0)
    except asyncio.TimeoutError:
        pytest.fail("cmdloop_async did not complete within timeout")
