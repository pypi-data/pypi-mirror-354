# LUCA CLI Client

## Overview

The LUCA CLI Client is a command-line interface for your LUCA AI Copilot for Research.

It allows you to interact with your dedicated AI research assistant that lives in your terminal.
This is a non-intrusive user experience, that means you still have complete control over your terminal.
But your AI assistant is always a command away.

## Capabilities

We have designed the system to be able to:
 - Retrieve and search relevant research papers from ArXiv.
 - Retrieve experiments logged in a Weights & Biases project.
 - Generate and execute Python and bash commands.
 - Create presentations, reports, and analyze data.

With these capabilities, you can use the assistant to:
- Generate reports that theorize and summarize your research experiments.
- Generate a project plan to tackle a new research problem.
- Brainstorm, ideate, and generate new hypotheses based on your current experiments.
- Analyze experiment data and create visualizations.

## Pre-installation

Before installing the LUCA CLI, please make sure you have:

1. **Created an account** on the [LUCA platform](https://www.myluca.ai)
2. **Signed up for a research agent** (this provisions your dedicated VM)
3. **Created an API key** from your dashboard

## Installation

```bash
pip install luca-cli
```

## Setup

### Quick Setup (Interactive)

Run the interactive setup command to configure your API key:

```bash
luca setup
```

This will guide you through:
1. Getting your API key from the dashboard
2. Setting up your environment variables
3. Testing your connection

### Manual Setup

Alternatively, you can manually set up your environment:

1. **Get your API key** from [your dashboard](https://www.myluca.ai/dashboard)
2. **Set the environment variable**:
   ```bash
   export LUCA_API_KEY="luca_your_api_key_here"
   ```
3. **Add to your shell profile** (optional but recommended):
   ```bash
   echo 'export LUCA_API_KEY="luca_your_api_key_here"' >> ~/.bashrc
   # or for zsh:
   echo 'export LUCA_API_KEY="luca_your_api_key_here"' >> ~/.zshrc
   ```

### Verify Setup

Test your authentication:

```bash
luca auth
```

This will verify your API key and show your agent status.

## Usage

### Help and Commands

```bash
luca --help
```

View all available commands and configuration options.

### Initialize Your Agent

After setting up your API key, initialize your research agent:

```bash
luca init
```

This will initialize your dedicated research assistant and create a knowledge base in `$ROOT/.luca/kb.txt`.
This knowledge base will be updated with new information as you use the assistant.

### Start Research

You can start interacting with your research assistant by typing your prompt:

```bash
luca "Research papers on reinforcement learning"
```

```bash
luca "Analyze the experiment data in my current directory"
```

```bash
luca "Create a summary of recent advances in transformer architectures"
```

### Advanced Usage with W&B Integration

If you are using Weights & Biases to log your experiments, you can set your W&B credentials and re-initialize:

```bash
export WANDB_API_KEY="your-wandb-api-key"
export WANDB_ENTITY="your-wandb-entity"
luca init
```

This will update your assistant to access your W&B experiments. You can then create powerful reports:

```bash
luca "Export a PowerPoint report of all experiments in my wandb project <your-project-name>"
```

```bash
luca "Compare the performance of my last 5 experiments and suggest improvements"
```

### File Management

Any file your assistant creates will be synced to your local machine and saved in `$ROOT/.luca/artifacts/`:

```bash
luca artifacts  # List all created files
```

### Sync Knowledge Base

Keep your local knowledge base up to date:

```bash
luca sync
```

### Provide Feedback

Help us improve by sharing your experience:

```bash
luca feedback "I love how the assistant helps with data analysis!"
```

## Available Commands

| Command | Description |
|---------|-------------|
| `luca setup` | Interactive API key setup |
| `luca auth` | Check authentication status |
| `luca init` | Initialize your research agent |
| `luca sync` | Sync knowledge base from agent |
| `luca artifacts` | List all available artifacts |
| `luca feedback <message>` | Send feedback to our team |
| `luca "<prompt>"` | Ask your research assistant anything |

## Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `LUCA_API_KEY` | Your API key from the dashboard | Yes |
| `LUCA_GATEWAY_URL` | Gateway URL (default: https://www.myluca.ai/api/gateway) | No |
| `WANDB_API_KEY` | Your Weights & Biases API key | Optional |
| `WANDB_ENTITY` | Your Weights & Biases entity name | Optional |

### Security

- Your API key is used to authenticate with your dedicated research agent
- All communication is encrypted via HTTPS
- Your research agent runs on a dedicated VM that only you have access to
- API keys can be managed and revoked from your dashboard

## Troubleshooting

### Authentication Issues

```bash
❌ Error: LUCA_API_KEY environment variable not set.
```
**Solution**: Run `luca setup` or manually set your API key.

### Agent Not Ready

```bash
❌ Service Unavailable: Your agent is not ready
```
**Solution**: Your VM is still being provisioned. Wait 2-5 minutes and try again.

### Connection Issues

```bash
❌ Connection error. Please check your internet connection.
```
**Solution**: Check your internet connection and try again.

For more help, visit [your dashboard](https://www.myluca.ai/dashboard) or contact support.

## What's New

### v2.0.0 - API Key Authentication
- 🔐 **Secure API Key Authentication**: No more VM IP addresses to manage
- 🚀 **Improved Setup**: Interactive setup with `luca setup`
- 📊 **Better Status Checking**: Use `luca auth` to check your agent status
- 🛡️ **Enhanced Security**: All requests routed through secure gateway
- ✨ **Better Error Messages**: Clear, actionable error messages
- 🎯 **Simplified Configuration**: Just set your API key and go

## Roadmap

We plan to significantly expand the capabilities of your research assistant with each release:

- 📚 **Enhanced Literature Review**: Better paper discovery and summarization
- 🧪 **Experiment Management**: Advanced experiment tracking and analysis
- 📈 **Data Visualization**: Automatic chart and graph generation
- 🤝 **Team Collaboration**: Share insights and results with your team
- 🔧 **Custom Tools**: Integration with your favorite research tools

## Feedback

Your feedback helps us build better tools for researchers. Share your thoughts:

```bash
luca feedback "Your message here"
```

Or reach out through our [dashboard](https://www.myluca.ai/dashboard).

---

Happy researching! 🚀

**The LUCA Team**
