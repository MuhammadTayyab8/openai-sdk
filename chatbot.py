import chainlit as cl


@cl.on_message
async def main(message: cl.Message):
    response = f"Recieved: {message.content}"
    await cl.Message(response).send()
