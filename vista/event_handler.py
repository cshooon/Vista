from openai.lib.streaming import AssistantEventHandler
from typing_extensions import override

from settings import settings
from pymongo import MongoClient


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        print(f"\nassistant > ", end="", flush=True)

    @override
    def on_text_delta(self, delta, snapshot):
        if delta.value is not None:
            print(delta.value, end="", flush=True)

    def on_tool_call_created(self, tool_call):
        yield f"\nassistant > {tool_call.type}\n"

    async def on_tool_call_delta(self, delta, snapshot):
        if delta.type == 'code_interpreter':
            if delta.code_interpreter.input:
                print(delta.code_interpreter.input, end="", flush=True)
            if delta.code_interpreter.outputs:
                print(f"\n\noutput >", flush=True)
                for output in delta.code_interpreter.outputs:
                    if output.type == "image":
                        print(f"\nImage ID: {output.image}", flush=True)
                    elif output.type == "logs":
                        print(f"\n{output.logs}", flush=True)


async def generate_responses(client, thread_id):
    async def generator():
        with client.beta.threads.runs.create_and_stream(
                thread_id=thread_id,
                assistant_id=settings.ASSISTANT_ID,
                event_handler=EventHandler(),
        ) as stream:
            for event in stream:
                if event.event == 'thread.run.step.created':
                    if event.data.type == 'tool_calls':
                        print('\ntool_calls created!!')
                        yield '\ntool_calls created!!\n\n'
                    else:
                        print('\nMessage creation detected...')
                        yield '\nMessage creation detected...\n\n'
                elif event.event == 'thread.run.step.delta':
                    run_step_delta = event.data.delta
                    if run_step_delta.step_details and run_step_delta.step_details.type == "tool_calls":
                        for tool_call_delta in run_step_delta.step_details.tool_calls:
                            if tool_call_delta.code_interpreter.input:
                                yield tool_call_delta.code_interpreter.input
                            if tool_call_delta.code_interpreter.outputs:
                                for output in tool_call_delta.code_interpreter.outputs:
                                    if output.type == 'image':
                                        yield f'\nImage file ID: {output.image.file_id}'
                                    elif output.type == 'logs':
                                        yield output.logs
                elif event.event == "thread.message.delta":
                    message_delta = event.data.delta
                    if message_delta.content is not None:
                        for content_delta in message_delta.content:
                            if content_delta.type == "text" and content_delta.text.value:
                                yield content_delta.text.value
    return generator
