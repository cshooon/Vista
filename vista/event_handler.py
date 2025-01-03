from openai.lib.streaming import AssistantEventHandler
from typing_extensions import override

from settings import settings
from pymongo import MongoClient


class EventHandler(AssistantEventHandler):
    @override
    def on_text_created(self, text) -> None:
        pass

    @override
    def on_text_delta(self, delta, snapshot):
        if delta.value is not None:
            pass


async def generate_responses(client, assistant_id, thread_id):

    async def generator():
        with client.beta.threads.runs.stream(
                assistant_id=assistant_id,
                thread_id=thread_id,
                event_handler=EventHandler(),
        ) as stream:
            for event in stream:
                if event.event == 'thread.run.step.created':
                    if event.data.type == 'tool_calls':
                        pass
                        # yield '\ntool_calls created!!\n\n'
                        # yield '\nMessage creation detected...\n\n'
                # elif event.event == 'thread.run.step.delta':
                #     run_step_delta = event.data.delta
                #     if run_step_delta.step_details and run_step_delta.step_details.type == "tool_calls":
                #         for tool_call_delta in run_step_delta.step_details.tool_calls:
                #             if tool_call_delta.code_interpreter.input:
                #                 yield tool_call_delta.code_interpreter.input
                #             if tool_call_delta.code_interpreter.outputs:
                #                 for output in tool_call_delta.code_interpreter.outputs:
                #                     if output.type == 'image':
                #                         yield f'\nImage file ID: {output.image.file_id}'
                #                     elif output.type == 'logs':
                #                         yield output.logs
                elif event.event == "thread.message.delta":
                    message_delta = event.data.delta
                    if message_delta.content is not None:
                        for content_delta in message_delta.content:
                            if content_delta.type == "text" and content_delta.text.value:
                                yield content_delta.text.value
    return generator
