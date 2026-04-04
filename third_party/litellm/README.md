# LiteLLM Proxy — Azure OpenAI → OpenAI Translator

This directory contains scripts to host a [LiteLLM](https://docs.litellm.ai/) proxy server that translates **Azure OpenAI** endpoints into standard **OpenAI-compatible** endpoints.

Any tool or agent that expects `OPENAI_API_BASE` + `OPENAI_API_KEY` (e.g. Codex CLI, LangChain, etc.) can point at this proxy and transparently use Azure OpenAI models.

## Quick Start

```bash
# 1. Install LiteLLM
./setup.sh

# 2. Configure your Azure credentials
cp .env.example .env
vim .env   # fill in your values

# 3. Start the proxy
./run.sh
```

The proxy listens on `http://localhost:4000` by default.

## Connecting Clients

Once the proxy is running, configure your downstream tools:

```bash
export OPENAI_API_BASE=http://localhost:4000
export OPENAI_API_KEY=sk-litellm-proxy   # or your custom LITELLM_MASTER_KEY
```

For the LongAgentBench project specifically, add these to your root `.env`:

```bash
OPENAI_API_KEY=sk-litellm-proxy
OPENAI_API_BASE=http://localhost:4000
```

## Files

| File | Description |
|------|-------------|
| `setup.sh` | Installs `litellm[proxy]` and seeds `.env` |
| `run.sh` | Starts the proxy (foreground, background, or Docker) |
| `stop.sh` | Stops a background or Docker proxy instance |
| `config.yaml` | LiteLLM model routing configuration |
| `.env.example` | Template for required environment variables |

## Configuration

### Adding Models

Edit [config.yaml](config.yaml) to add or modify model mappings. Each entry maps a client-facing `model_name` to an Azure deployment:

```yaml
- model_name: gpt-4o          # what clients request
  litellm_params:
    model: azure/gpt-4o       # azure/<deployment-name>
    api_key: os.environ/AZURE_API_KEY
    api_base: os.environ/AZURE_API_BASE
    api_version: os.environ/AZURE_API_VERSION
```

### Run Options

```bash
./run.sh                    # foreground on port 4000
./run.sh --port 8000        # custom port
./run.sh --background       # nohup background mode
./run.sh --docker           # run via Docker container
```

### Docker Mode

```bash
./run.sh --docker --port 4000
# Stop with:
./stop.sh
```

## Troubleshooting

- **Missing env vars**: Ensure `AZURE_API_KEY`, `AZURE_API_BASE`, and `AZURE_API_VERSION` are set in `.env` or exported.
- **Model not found**: The `model_name` in `config.yaml` must match what the client requests. The `litellm_params.model` must match your actual Azure deployment name (prefixed with `azure/`).
- **Port in use**: Use `--port` to pick a different port, or stop the existing proxy with `./stop.sh`.
