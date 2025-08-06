import azure.functions as func
import datetime
import json
import logging
import os
import time
from openai import AzureOpenAI


def load_local_settings():
    """Load environment variables from local.settings.json for local testing."""
    try:
        with open("local.settings.json") as f:
            settings = json.load(f)
            values = settings.get("Values", {})
            for k, v in values.items():
                if k not in os.environ:
                    os.environ[k] = v
    except Exception as e:
        print(f"Warning: Could not load local.settings.json: {e}")



app = func.FunctionApp()

@app.function_name(name="OpenAIAssistantHttpTrigger")
@app.route(route="openai-assistant", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def openai_assistant_http_trigger(req: func.HttpRequest) -> func.HttpResponse:
    try:
        # Get prompt from request body
        req_body = req.get_json()
        prompt = req_body.get("prompt", "hi")

        # Initialize Azure OpenAI client
        client = AzureOpenAI(
            azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
            api_key=os.getenv("AZURE_OPENAI_API_KEY"),
            api_version="2024-05-01-preview"
        )

        # Create assistant
        assistant = client.beta.assistants.create(
            model="gpt-35-turbo",  # replace with model deployment name.
            instructions="Respond in the same language as the user's question.",
            tools=[{"type": "file_search"}],
            tool_resources={"file_search": {"vector_store_ids": ["vs_sgjvlbgxltrP9k58KcCsHGFw"]}},
            temperature=1,
            top_p=1
        )

        # Create a thread
        thread = client.beta.threads.create()

        # Add a user question to the thread
        message = client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=prompt
        )

        # Run the thread
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=assistant.id
        )

        # Looping until the run completes or fails
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )

        if run.status == 'completed':
            messages = client.beta.threads.messages.list(
                thread_id=thread.id
            )
            # Return the full messages object for debugging
            return func.HttpResponse(
                json.dumps({"messages": [m.model_dump() for m in messages.data]}),
                mimetype="application/json",
                status_code=200
            )
        elif run.status == 'requires_action':
            return func.HttpResponse(
                json.dumps({"error": "Assistant requires action."}),
                mimetype="application/json",
                status_code=202
            )
        else:
            return func.HttpResponse(
                json.dumps({"error": run.status}),
                mimetype="application/json",
                status_code=500
            )
    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            mimetype="application/json",
            status_code=500
        )






