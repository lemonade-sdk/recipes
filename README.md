# recipes

Repository of Lemonade Server model recipes: custom model load settings for specific use cases.

## Directories

- `openclaw/`: Recipes selected for OpenClaw-style agent and assistant use cases.
- `coding-agents/`: Recipes tuned for coding-focused assistants.

## Validation

Validate recipe JSON files with:

```bash
python3 validate_recipe_json.py openclaw/*.json coding-agents/*.json
```
