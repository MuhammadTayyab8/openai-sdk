import os
import chainlit as cl
from dotenv import find_dotenv, load_dotenv
from agents import AsyncOpenAI, OpenAIChatCompletionsModel, RunConfig, Agent, Runner
from openai.types.responses import ResponseTextDeltaEvent


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




@cl.on_chat_start
async def handle_chat_start():
    cl.user_session.set("history", [])
    await cl.Message("Hello! I am a Helpful Agent.").send()








@cl.on_message
async def main(message: cl.Message):

    history = cl.user_session.get("history")

    msg = cl.Message(content="")
    await msg.send()

    history.append({"role": "user", "content": message.content})


    result = Runner.run_streamed(
        agent,
        input=history,
        run_config=config
    )


    collected = ''

    async for event in result.stream_events():
        if event.type == "raw_response_event" and isinstance(event.data, ResponseTextDeltaEvent):
            token = event.data.delta
            collected += token
            await msg.stream_token(token)

    history.append({"role": "assistant", "content": result.final_output})

    msg.content = collected
    await msg.update()
 

