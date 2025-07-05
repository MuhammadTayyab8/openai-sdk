import os
import chainlit as cl
from dotenv import find_dotenv, load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Agent, Runner


load_dotenv(find_dotenv())
gemini_api_key = os.getenv("GEMINI_API_KEY")


# STEP # 1: PROVIDER
provider = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/" 
)


# STEP # 2: MODEL
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash", 
    openai_client=provider
)


# STEP # 3: Configuration
config = RunConfig(
    model=model,
    model_provider=provider,
    tracing_disabled = True,
)




# STEP # 4: Agent
agent = Agent(
    instructions="you are a helpful agent",
    name = "Tayyab Agent"
)





@cl.on_message
async def main(message: cl.Message):
    result = await Runner.run(
        agent,
        input=message.content,
        run_config=config
    )

    await cl.Message(result.final_output).send()

