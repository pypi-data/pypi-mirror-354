# Cursor Integration Guide for OnlyNet Tasks MCP Server

## Quick Setup

### 1. Install the Server

```bash
cd /home/kirkdeam/AI/mcp_develop/onlynet
pip install -r requirements.txt
```

### 2. Configure Cursor

**Option A: Specify Project Directory (Recommended)**

Add the following to your Cursor MCP settings, replacing `/path/to/your/project` with your actual project path:

```json
{
  "mcpServers": {
    "onlynet-tasks": {
      "command": "python",
      "args": ["/home/kirkdeam/AI/mcp_develop/onlynet/server.py"],
      "env": {
        "ONLYNET_DATA_DIR": "/path/to/your/project"
      },
      "description": "OnlyNet Tasks - PRD generation and task management"
    }
  }
}
```

**Option B: Auto-detection (May need manual setting)**

```json
{
  "mcpServers": {
    "onlynet-tasks": {
      "command": "python",
      "args": ["/home/kirkdeam/AI/mcp_develop/onlynet/server.py"],
      "env": {},
      "description": "OnlyNet Tasks - PRD generation and task management"
    }
  }
}
```

If auto-detection doesn't work (files created in wrong directory), use the `set_project_directory` tool first.

### 3. Restart Cursor

After adding the configuration, restart Cursor to load the MCP server.

## Using with Cursor Agents

### Available Tools

When the server is running, Cursor agents have access to these tools:

1. **set_project_directory** - Set the project directory (if auto-detection fails)
2. **generate_prd** - Start a new project with guided PRD creation
3. **update_prd** - Add answers to PRD sections
4. **create_tasks_from_prd** - Generate task breakdown from PRD
5. **read_task** - Read specific task or get next open task
6. **complete_task** - Mark tasks as completed
7. **list_all_tasks** - View all tasks with status and progress

### Example Agent Commands

Here are some example prompts you can use with Cursor agents:

#### Setting Project Directory (if needed)
```
First, set the project directory to /home/kirkdeam/AI/mcp_test using the OnlyNet Tasks server.
```

#### Starting a New Project
```
Using the OnlyNet Tasks server, create a PRD for a "Task Management Mobile App" that helps teams collaborate on projects.
```

#### Completing the PRD
```
Update the PRD with answers for all sections. For the Problem Statement, focus on remote team collaboration challenges.
```

#### Creating Tasks
```
Analyze the PRD and create a comprehensive task breakdown with appropriate complexity levels.
```

#### Working Through Tasks
```
Get the next open task and provide implementation suggestions based on its requirements.
```

#### Tracking Progress
```
Show me the current project progress and list all remaining open tasks.
```

### Best Practices for Cursor Agents

1. **Start with PRD**: Always begin by generating and completing a PRD
2. **Break Down Complexity**: Encourage the agent to create subtasks for complex items
3. **Check Dependencies**: Have the agent verify task dependencies before starting work
4. **Regular Updates**: Ask the agent to check progress regularly
5. **Context Awareness**: The agent can read task descriptions to understand implementation needs

### Advanced Usage

#### Automated Workflows
```
Create a complete project plan for an e-commerce website. Generate the PRD by asking me questions, then create a detailed task breakdown, and guide me through implementing the first three tasks.
```

#### Progress Reports
```
Generate a progress report showing completed tasks, remaining work, and complexity distribution.
```

#### Dependency Analysis
```
Analyze the task dependencies and suggest an optimal order for implementation.
```

## Troubleshooting

### Server Not Found
- Ensure the path in the Cursor configuration is absolute
- Check that Python is in your PATH
- Verify the server file has execute permissions

### Connection Issues
- Restart Cursor after configuration changes
- Check the Cursor logs for MCP-related errors
- Ensure no other process is using the same resources

### Data Persistence
- PRD is saved to `prd.md` in your project directory
- Tasks are saved to `tasks.json` in your project directory
- These files persist between sessions and are created where Cursor is running
- You can override the location with `ONLYNET_DATA_DIR` environment variable

## Integration Tips

1. **Use with Other MCP Servers**: OnlyNet Tasks can work alongside other MCP servers
2. **Custom Workflows**: Modify the server to add project-specific tools
3. **Team Collaboration**: Share the `data/` directory for team projects
4. **Version Control**: Track PRD and tasks in git for history

## Example Cursor Workflow

1. Open Cursor with the MCP server configured
2. Start a new conversation with an agent
3. Ask: "Let's create a new project using OnlyNet Tasks"
4. The agent will guide you through PRD creation
5. Review and approve the generated tasks
6. Work through tasks with agent assistance
7. Track progress as you complete work

This integration enables Cursor agents to manage your entire project workflow from requirements to implementation!
