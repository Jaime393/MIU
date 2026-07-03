# MIU + OpenHands Integration
> Autonomous coding agent for MIU ecosystem
> github.com/OpenHands/OpenHands

## What OpenHands can do for MIU

1. Write unit tests for D_f calculators
2. Refactor Python tools in tools/
3. Generate new analysis scripts
4. Debug and fix workflow code
5. Document functions and modules

## Integration via Groq (fallback without server)

The MIU workflow uses Groq Llama-3.3-70B as OpenHands-style agent:
- Decomposes task into atomic steps
- Generates clean, documented code
- Commits directly to GitHub tools/

## Future: Full OpenHands server

pip install openhands-ai
openhands --runtime local
# Point MIU workflow to: http://localhost:3000/api

## Agent capabilities roadmap

- [ ] Full OpenHands server on Cloudflare Workers
- [ ] MCP server integration (codegraph)
- [ ] Auto-PR creation on GitHub
- [ ] Test execution and validation
