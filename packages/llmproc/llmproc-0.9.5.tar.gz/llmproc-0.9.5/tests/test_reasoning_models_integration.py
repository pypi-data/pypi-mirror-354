"""Integration tests for O3-mini reasoning models with different reasoning levels.

These tests validate that O3-mini models with different reasoning levels (high, medium, low)
function correctly and produce outputs reflecting their respective reasoning capabilities.
"""

import asyncio
import os
import time

import pytest
from llmproc import LLMProcess, LLMProgram


async def load_reasoning_model(config_path) -> LLMProcess:
    """Load a reasoning model from a TOML configuration file."""
    program = LLMProgram.from_toml(config_path)
    return await program.start()


def test_reasoning_models_configuration(tmp_path):
    """Test that reasoning model configurations load correctly with proper parameters."""
    # Create temporary config files for each reasoning level
    high_config = tmp_path / "o3-mini-high.toml"
    medium_config = tmp_path / "o3-mini-medium.toml"
    low_config = tmp_path / "o3-mini-low.toml"

    # Write high reasoning config content
    high_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini High Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using high reasoning effort."

    [parameters]
    reasoning_effort = "high"
    max_completion_tokens = 25000
    """
    )

    # Write medium reasoning config content
    medium_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini Medium Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using medium reasoning effort."

    [parameters]
    reasoning_effort = "medium"
    max_completion_tokens = 10000
    """
    )

    # Write low reasoning config content
    low_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini Low Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using low reasoning effort."

    [parameters]
    reasoning_effort = "low"
    max_completion_tokens = 5000
    """
    )

    # Load all three reasoning model configurations from temporary files
    high_program = LLMProgram.from_toml(high_config)
    medium_program = LLMProgram.from_toml(medium_config)
    low_program = LLMProgram.from_toml(low_config)

    # Verify high reasoning configuration
    assert high_program.model_name == "o3-mini"
    assert high_program.provider == "openai"
    assert high_program.parameters["reasoning_effort"] == "high"
    assert high_program.parameters["max_completion_tokens"] == 25000

    # Verify medium reasoning configuration
    assert medium_program.model_name == "o3-mini"
    assert medium_program.provider == "openai"
    assert medium_program.parameters["reasoning_effort"] == "medium"
    assert medium_program.parameters["max_completion_tokens"] == 10000

    # Verify low reasoning configuration
    assert low_program.model_name == "o3-mini"
    assert low_program.provider == "openai"
    assert low_program.parameters["reasoning_effort"] == "low"
    assert low_program.parameters["max_completion_tokens"] == 5000


# Helper function to validate reasoning model parameters without API calls
def validate_reasoning_parameters(program):
    """Validate the reasoning model parameters structure from a program configuration."""
    # Check basic configuration requirements
    assert program.model_name == "o3-mini"
    assert program.provider == "openai"

    # Check reasoning parameters format
    assert "reasoning_effort" in program.parameters
    assert program.parameters["reasoning_effort"] in ["low", "medium", "high"]
    assert "max_completion_tokens" in program.parameters
    assert "max_tokens" not in program.parameters

    # Return effort level and token limit for specific assertions
    return program.parameters["reasoning_effort"], program.parameters["max_completion_tokens"]


# Test parameter validation without requiring API access
def test_reasoning_models_parameter_validation(tmp_path):
    """Test reasoning model parameter validation without API access."""
    # Create temporary config files for each reasoning level
    high_config = tmp_path / "o3-mini-high.toml"
    medium_config = tmp_path / "o3-mini-medium.toml"
    low_config = tmp_path / "o3-mini-low.toml"

    # Write high reasoning config content
    high_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini High Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using high reasoning effort."

    [parameters]
    reasoning_effort = "high"
    max_completion_tokens = 25000
    """
    )

    # Write medium reasoning config content
    medium_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini Medium Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using medium reasoning effort."

    [parameters]
    reasoning_effort = "medium"
    max_completion_tokens = 10000
    """
    )

    # Write low reasoning config content
    low_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini Low Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using low reasoning effort."

    [parameters]
    reasoning_effort = "low"
    max_completion_tokens = 5000
    """
    )

    # Load all three reasoning model configurations from temporary files
    high_program = LLMProgram.from_toml(high_config)
    medium_program = LLMProgram.from_toml(medium_config)
    low_program = LLMProgram.from_toml(low_config)

    # Validate parameters for each model and check specific values
    high_effort, high_tokens = validate_reasoning_parameters(high_program)
    medium_effort, medium_tokens = validate_reasoning_parameters(medium_program)
    low_effort, low_tokens = validate_reasoning_parameters(low_program)

    # Verify the specific effort levels
    assert high_effort == "high"
    assert medium_effort == "medium"
    assert low_effort == "low"

    # Verify token limits follow expected pattern (higher for more complex reasoning)
    assert high_tokens == 25000
    assert medium_tokens == 10000
    assert low_tokens == 5000
    assert high_tokens > medium_tokens > low_tokens


@pytest.mark.llm_api
@pytest.mark.extended_api
async def test_reasoning_models_basic_functionality(tmp_path):
    """Test that reasoning models run successfully with a simple query."""
    # Skip if no OpenAI API key
    if not os.environ.get("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY environment variable not set")

    # Create a temporary config file for low reasoning
    low_config = tmp_path / "o3-mini-low.toml"

    # Write low reasoning config content
    low_config.write_text(
        """
    [model]
    name = "o3-mini"
    provider = "openai"
    display_name = "O3-Mini Low Reasoning"

    [prompt]
    system_prompt = "You are a helpful AI assistant using low reasoning effort."

    [parameters]
    reasoning_effort = "low"
    max_completion_tokens = 5000
    """
    )

    # Simple problem for testing
    simple_problem = "What is 24 * 7?"

    # Load medium reasoning model from temporary file
    medium_process = await load_reasoning_model(low_config)

    # Run the model
    result = await medium_process.run(simple_problem)

    # Verify we got a response
    assert result
    assert medium_process.get_last_message()
    assert "168" in medium_process.get_last_message()  # Basic check for correct answer
