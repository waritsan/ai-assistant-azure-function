# Azure Function: Azure OpenAI Assistant

This project is an Azure Function written in Python that interacts with Azure OpenAI using the openai Python SDK.

## Setup

1. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   pip install openai requests
   ```
2. **Configure environment variables:**
   - `AZURE_OPENAI_ENDPOINT`: Your Azure OpenAI endpoint
   - `AZURE_OPENAI_API_KEY`: Your Azure OpenAI API key

3. **Run locally:**
   ```sh
   func start
   ```

## Project Structure
- `function_app.py`: Main entry point for Azure Functions.
- `.github/copilot-instructions.md`: Copilot custom instructions.
- `requirements.txt`: Python dependencies.

## Next Steps
- Implement the Azure Function to initialize the AzureOpenAI client and create an assistant as described in the setup.

## Run local
source .venv/bin/activate && func start

curl -X POST http://localhost:7071/api/openai-assistant \
  -H "Content-Type: application/json" \
  -d '{"prompt": "hello"}'

## Create
az functionapp create --resource-group ai-skincare-reccommender --consumption-plan-location eastus --runtime python --runtime-version 3.9 --functions-version 4 --name ai-assistant-function --storage-account skinstorage123

## Deploy
func azure functionapp publish ai-assistant-function

## Set env
az functionapp config appsettings set --name ai-assistant-function --resource-group ai-skincare-reccommender --settings AZURE_OPENAI_ENDPOINT="https://ai-skincare-reccommender-instance.openai.azure.com/" AZURE_OPENAI_API_KEY="REMOVED"

curl -X POST https://ai-assistant-function.azurewebsites.net/api/openai-assistant \
  -H "Content-Type: application/json" \
  -d '{"prompt": "Hello"}'