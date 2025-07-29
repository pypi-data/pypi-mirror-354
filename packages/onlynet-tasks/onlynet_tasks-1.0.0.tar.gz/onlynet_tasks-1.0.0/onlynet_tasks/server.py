"""
OnlyNet Tasks MCP Server

A FastMCP server for managing PRDs and tasks, designed to work with Cursor agents.
"""

import json
import os
from typing import Dict, List, Optional, Any
from datetime import datetime
from pathlib import Path
from fastmcp import FastMCP, Context

# Initialize the MCP server
mcp = FastMCP("OnlyNet Tasks")

# Global variable to store the project directory (can be updated)
_project_directory = None

# Data storage paths - intelligently detect project directory
def _detect_project_directory() -> Path:
    """
    Intelligently detect the project directory by looking for common project indicators.
    Falls back to current working directory if no indicators found.
    """
    global _project_directory

    # If project directory was explicitly set via tool, use that
    if _project_directory is not None:
        return _project_directory

    # First, check if explicitly set via environment variable
    if "ONLYNET_DATA_DIR" in os.environ:
        return Path(os.environ["ONLYNET_DATA_DIR"])

    # Start from current working directory and walk up to find project root
    current = Path.cwd()

    # Common project indicators to look for (excluding global ones like .vscode/.cursor in home)
    project_indicators = [
        ".git",           # Git repository
        "package.json",   # Node.js project
        "pyproject.toml", # Python project
        "requirements.txt", # Python project
        "Cargo.toml",     # Rust project
        "go.mod",         # Go project
        ".project",       # General project marker
        "pom.xml",        # Maven project
        "build.gradle",   # Gradle project
        "Makefile",       # Make-based project
        "composer.json",  # PHP project
        "Gemfile",        # Ruby project
    ]

    # Walk up the directory tree looking for project indicators
    for parent in [current] + list(current.parents):
        # Skip home directory to avoid false positives
        if parent == Path.home():
            continue

        for indicator in project_indicators:
            if (parent / indicator).exists():
                return parent

    # If we reach home directory, check for README.md (common in project roots)
    if (current / "README.md").exists() and current != Path.home():
        return current

    # Fallback to current working directory
    return current


def _update_file_paths():
    """Update file paths when project directory changes"""
    global DATA_DIR, PRD_FILE, TASKS_FILE
    DATA_DIR = _detect_project_directory() / "onlynet"
    PRD_FILE = DATA_DIR / "prd.md"
    TASKS_FILE = DATA_DIR / "tasks.json"
    DATA_DIR.mkdir(exist_ok=True)

DATA_DIR = _detect_project_directory() / "onlynet"
PRD_FILE = DATA_DIR / "prd.md"
TASKS_FILE = DATA_DIR / "tasks.json"

# Ensure data directory exists
DATA_DIR.mkdir(exist_ok=True)

# Complexity levels
COMPLEXITY_LEVELS = {
    0: "Very easy task",
    1: "Easy",
    2: "Complex task",
    3: "Senior developer level"
}

# Status options
TASK_STATUS = ["Open", "Closed"]


def _generate_tasks_from_prd_analysis(prd_content: str, project_name: str) -> List[Dict[str, Any]]:
    """
    Analyze PRD content and generate appropriate tasks based on the project requirements.

    Args:
        prd_content: The PRD markdown content
        project_name: Name of the project

    Returns:
        List of generated tasks with subtasks
    """
    tasks = []
    task_counter = 1

    # Extract sections from PRD
    sections = _extract_prd_sections(prd_content)

    # Always start with project setup
    setup_task = {
        "id": f"TASK-{task_counter:03d}",
        "title": "Project Setup & Environment",
        "detailed_description": "Initialize the project structure, configure development environment, and set up necessary tools.",
        "complexity_level": 0,
        "complexity_description": COMPLEXITY_LEVELS[0],
        "current_status": "Open",
        "subtasks": [
            {
                "id": f"TASK-{task_counter:03d}-01",
                "title": "Initialize Version Control",
                "detailed_description": "Set up Git repository, create .gitignore, and establish branching strategy",
                "complexity_level": 0,
                "complexity_description": COMPLEXITY_LEVELS[0],
                "current_status": "Open",
                "dependencies": []
            },
            {
                "id": f"TASK-{task_counter:03d}-02",
                "title": "Setup Development Environment",
                "detailed_description": "Configure development tools, package managers, and local environment",
                "complexity_level": 0,
                "complexity_description": COMPLEXITY_LEVELS[0],
                "current_status": "Open",
                "dependencies": []
            }
        ],
        "dependencies": []
    }
    tasks.append(setup_task)
    task_counter += 1

    # Generate tasks based on technical requirements
    tech_requirements = sections.get("Technical Requirements", [])
    if tech_requirements:
        tech_task = _generate_technical_task(task_counter, tech_requirements, setup_task["id"])
        tasks.append(tech_task)
        task_counter += 1

    # Generate tasks based on user experience requirements
    ux_requirements = sections.get("User Experience", [])
    if ux_requirements:
        ux_task = _generate_ux_task(task_counter, ux_requirements, project_name)
        tasks.append(ux_task)
        task_counter += 1

    # Generate tasks based on problem statement and success criteria
    problem_statement = sections.get("Problem Statement", [])
    success_criteria = sections.get("Success Criteria", [])
    if problem_statement or success_criteria:
        feature_task = _generate_feature_task(task_counter, problem_statement, success_criteria, project_name)
        tasks.append(feature_task)
        task_counter += 1

    # Add testing and deployment tasks
    testing_task = _generate_testing_task(task_counter, [task["id"] for task in tasks])
    tasks.append(testing_task)
    task_counter += 1

    deployment_task = _generate_deployment_task(task_counter, testing_task["id"])
    tasks.append(deployment_task)

    return tasks


def _extract_prd_sections(prd_content: str) -> Dict[str, List[str]]:
    """Extract sections and their content from PRD markdown."""
    sections = {}
    current_section = None
    current_content = []

    lines = prd_content.split('\n')
    for line in lines:
        line = line.strip()
        if line.startswith('### ') and not line.startswith('### Created'):
            # Save previous section
            if current_section:
                sections[current_section] = current_content
            # Start new section
            current_section = line.replace('### ', '')
            current_content = []
        elif current_section and line and not line.startswith('#'):
            # Add content to current section
            if line.startswith(('1.', '2.', '3.', '4.')):
                current_content.append(line[3:].strip())

    # Save last section
    if current_section:
        sections[current_section] = current_content

    return sections


def _generate_technical_task(task_num: int, tech_requirements: List[str], dependency: str) -> Dict[str, Any]:
    """Generate technical architecture task based on requirements."""
    # Determine complexity based on tech requirements
    complexity = 1  # Default to Easy
    if any(keyword in ' '.join(tech_requirements).lower() for keyword in ['microservices', 'distributed', 'scalable', 'cloud']):
        complexity = 3
    elif any(keyword in ' '.join(tech_requirements).lower() for keyword in ['database', 'api', 'integration']):
        complexity = 2

    subtasks = [
        {
            "id": f"TASK-{task_num:03d}-01",
            "title": "Design System Architecture",
            "detailed_description": "Create overall system architecture and technology stack design",
            "complexity_level": complexity,
            "complexity_description": COMPLEXITY_LEVELS[complexity],
            "current_status": "Open",
            "dependencies": [dependency]
        }
    ]

    # Add database task if mentioned
    if any('database' in req.lower() for req in tech_requirements):
        subtasks.append({
            "id": f"TASK-{task_num:03d}-02",
            "title": "Database Design",
            "detailed_description": "Design database schema, relationships, and data models",
            "complexity_level": 2,
            "complexity_description": COMPLEXITY_LEVELS[2],
            "current_status": "Open",
            "dependencies": [f"TASK-{task_num:03d}-01"]
        })

    # Add API task if mentioned
    if any('api' in req.lower() for req in tech_requirements):
        subtasks.append({
            "id": f"TASK-{task_num:03d}-03",
            "title": "API Design",
            "detailed_description": "Design REST API endpoints, request/response formats, and documentation",
            "complexity_level": 2,
            "complexity_description": COMPLEXITY_LEVELS[2],
            "current_status": "Open",
            "dependencies": [f"TASK-{task_num:03d}-01"]
        })

    return {
        "id": f"TASK-{task_num:03d}",
        "title": "Technical Architecture & Design",
        "detailed_description": f"Implement technical requirements: {', '.join(tech_requirements[:2])}{'...' if len(tech_requirements) > 2 else ''}",
        "complexity_level": complexity,
        "complexity_description": COMPLEXITY_LEVELS[complexity],
        "current_status": "Open",
        "subtasks": subtasks,
        "dependencies": [dependency]
    }


def _generate_ux_task(task_num: int, ux_requirements: List[str], project_name: str) -> Dict[str, Any]:
    """Generate UX/UI task based on user experience requirements."""
    return {
        "id": f"TASK-{task_num:03d}",
        "title": "User Experience & Interface Design",
        "detailed_description": f"Design and implement user interface for {project_name}",
        "complexity_level": 2,
        "complexity_description": COMPLEXITY_LEVELS[2],
        "current_status": "Open",
        "subtasks": [
            {
                "id": f"TASK-{task_num:03d}-01",
                "title": "UI/UX Wireframes",
                "detailed_description": "Create wireframes and user flow diagrams",
                "complexity_level": 1,
                "complexity_description": COMPLEXITY_LEVELS[1],
                "current_status": "Open",
                "dependencies": []
            },
            {
                "id": f"TASK-{task_num:03d}-02",
                "title": "Frontend Implementation",
                "detailed_description": "Implement user interface components and user interactions",
                "complexity_level": 2,
                "complexity_description": COMPLEXITY_LEVELS[2],
                "current_status": "Open",
                "dependencies": [f"TASK-{task_num:03d}-01"]
            }
        ],
        "dependencies": []
    }


def _generate_feature_task(task_num: int, problem_statement: List[str], success_criteria: List[str], project_name: str) -> Dict[str, Any]:
    """Generate core feature implementation task."""
    # Determine complexity based on problem complexity
    complexity = 2  # Default to Complex
    if problem_statement and any(keyword in ' '.join(problem_statement).lower() for keyword in ['simple', 'basic', 'straightforward']):
        complexity = 1
    elif problem_statement and any(keyword in ' '.join(problem_statement).lower() for keyword in ['complex', 'advanced', 'sophisticated', 'enterprise']):
        complexity = 3

    return {
        "id": f"TASK-{task_num:03d}",
        "title": "Core Feature Implementation",
        "detailed_description": f"Implement the main features and business logic for {project_name}",
        "complexity_level": complexity,
        "complexity_description": COMPLEXITY_LEVELS[complexity],
        "current_status": "Open",
        "subtasks": [
            {
                "id": f"TASK-{task_num:03d}-01",
                "title": "Backend Logic Implementation",
                "detailed_description": "Implement core business logic and data processing",
                "complexity_level": complexity,
                "complexity_description": COMPLEXITY_LEVELS[complexity],
                "current_status": "Open",
                "dependencies": []
            },
            {
                "id": f"TASK-{task_num:03d}-02",
                "title": "Feature Integration",
                "detailed_description": "Integrate features with user interface and data layer",
                "complexity_level": 2,
                "complexity_description": COMPLEXITY_LEVELS[2],
                "current_status": "Open",
                "dependencies": [f"TASK-{task_num:03d}-01"]
            }
        ],
        "dependencies": []
    }


def _generate_testing_task(task_num: int, dependencies: List[str]) -> Dict[str, Any]:
    """Generate testing task that depends on implementation tasks."""
    return {
        "id": f"TASK-{task_num:03d}",
        "title": "Testing & Quality Assurance",
        "detailed_description": "Implement comprehensive testing strategy and quality assurance",
        "complexity_level": 2,
        "complexity_description": COMPLEXITY_LEVELS[2],
        "current_status": "Open",
        "subtasks": [
            {
                "id": f"TASK-{task_num:03d}-01",
                "title": "Unit Testing",
                "detailed_description": "Write unit tests for core functionality",
                "complexity_level": 1,
                "complexity_description": COMPLEXITY_LEVELS[1],
                "current_status": "Open",
                "dependencies": dependencies[-2:]  # Depend on last 2 implementation tasks
            },
            {
                "id": f"TASK-{task_num:03d}-02",
                "title": "Integration Testing",
                "detailed_description": "Test integration between components and systems",
                "complexity_level": 2,
                "complexity_description": COMPLEXITY_LEVELS[2],
                "current_status": "Open",
                "dependencies": [f"TASK-{task_num:03d}-01"]
            }
        ],
        "dependencies": dependencies[-2:]  # Depend on implementation tasks
    }


def _generate_deployment_task(task_num: int, testing_dependency: str) -> Dict[str, Any]:
    """Generate deployment task."""
    return {
        "id": f"TASK-{task_num:03d}",
        "title": "Deployment & Launch",
        "detailed_description": "Deploy the application to production and manage launch",
        "complexity_level": 2,
        "complexity_description": COMPLEXITY_LEVELS[2],
        "current_status": "Open",
        "subtasks": [
            {
                "id": f"TASK-{task_num:03d}-01",
                "title": "Production Environment Setup",
                "detailed_description": "Configure production environment and deployment pipeline",
                "complexity_level": 2,
                "complexity_description": COMPLEXITY_LEVELS[2],
                "current_status": "Open",
                "dependencies": [testing_dependency]
            },
            {
                "id": f"TASK-{task_num:03d}-02",
                "title": "Go-Live & Monitoring",
                "detailed_description": "Deploy to production and set up monitoring and maintenance",
                "complexity_level": 1,
                "complexity_description": COMPLEXITY_LEVELS[1],
                "current_status": "Open",
                "dependencies": [f"TASK-{task_num:03d}-01"]
            }
        ],
        "dependencies": [testing_dependency]
    }


@mcp.tool()
async def set_project_directory(
    directory: str,
    ctx: Context
) -> Dict[str, str]:
    """
    Set the project directory where PRD and tasks files will be created.
    Useful when the auto-detection doesn't work correctly.

    Args:
        directory: Path to the project directory
        ctx: MCP context

    Returns:
        Dictionary containing the status of the directory change
    """
    global _project_directory

    dir_path = Path(directory).expanduser().resolve()

    if not dir_path.exists():
        return {"error": f"Directory does not exist: {dir_path}"}

    if not dir_path.is_dir():
        return {"error": f"Path is not a directory: {dir_path}"}

    # Update the global project directory
    _project_directory = dir_path

    # Update file paths
    _update_file_paths()

    await ctx.info(f"Project directory set to: {dir_path}")
    await ctx.info(f"OnlyNet files will be created in: {DATA_DIR}")

    return {
        "status": "success",
        "message": f"Project directory set to {dir_path}",
        "onlynet_directory": str(DATA_DIR)
    }


@mcp.tool()
async def generate_prd(
    project_name: str,
    initial_description: str,
    ctx: Context
) -> Dict[str, Any]:
    """
    Generate a comprehensive Product Requirements Document (PRD) by guiding the user
    through various aspects of the project with targeted questions.

    Args:
        project_name: Name of the project
        initial_description: Initial project description provided by the user
        ctx: MCP context for interactions

    Returns:
        Dictionary containing the PRD generation status and next steps
    """
    await ctx.info(f"Starting PRD generation for project: {project_name}")
    project_root = _detect_project_directory()
    await ctx.info(f"Detected project root: {project_root}")
    await ctx.info(f"Files will be created in: {DATA_DIR}")

    # Initialize PRD structure
    prd_content = f"""# Product Requirements Document

## Project: {project_name}

### Overview
{initial_description}

### Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}

---

## Project Details

"""

    # Define sections and questions for the PRD
    sections = {
        "Problem Statement": [
            "What specific problem does this project solve?",
            "Who experiences this problem most acutely?",
            "What are the current alternatives or workarounds?",
            "What is the impact of not solving this problem?"
        ],
        "Target Audience": [
            "Who is the primary user of this solution?",
            "What are their technical capabilities?",
            "What are their main goals and motivations?",
            "Are there secondary user groups to consider?"
        ],
        "Success Criteria": [
            "How will you measure the success of this project?",
            "What are the key performance indicators (KPIs)?",
            "What is the minimum viable product (MVP)?",
            "What would constitute a complete failure?"
        ],
        "Technical Requirements": [
            "What technologies or platforms should be used?",
            "Are there any existing systems to integrate with?",
            "What are the performance requirements?",
            "What are the security and compliance requirements?"
        ],
        "Constraints & Assumptions": [
            "What is the budget for this project?",
            "What is the timeline for delivery?",
            "What resources are available?",
            "What assumptions are we making about the solution?"
        ],
        "User Experience": [
            "What is the ideal user journey?",
            "What features are must-have vs nice-to-have?",
            "How should the interface look and feel?",
            "What accessibility requirements exist?"
        ]
    }

    # Save initial PRD
    with open(PRD_FILE, 'w') as f:
        f.write(prd_content)

    # Prepare response with guidance questions
    response = {
        "status": "initialized",
        "message": "PRD initialized. Please answer the following questions to create a comprehensive PRD.",
        "sections": {}
    }

    for section, questions in sections.items():
        response["sections"][section] = {
            "questions": questions,
            "instruction": f"Please provide detailed answers for the {section} section."
        }

    await ctx.info("PRD template created. Please use the update_prd tool to add answers to each section.")

    return response


@mcp.tool()
async def update_prd(
    section: str,
    answers: List[str],
    ctx: Context
) -> Dict[str, str]:
    """
    Update the PRD with answers to specific section questions.

    Args:
        section: The section name to update
        answers: List of answers corresponding to the section questions
        ctx: MCP context

    Returns:
        Dictionary containing update status
    """
    if not PRD_FILE.exists():
        return {"error": "PRD not initialized. Please run generate_prd first."}

    # Read existing PRD
    with open(PRD_FILE, 'r') as f:
        prd_content = f.read()

    # Add section with answers
    section_content = f"\n### {section}\n\n"
    for i, answer in enumerate(answers, 1):
        section_content += f"{i}. {answer}\n\n"

    # Append to PRD
    with open(PRD_FILE, 'a') as f:
        f.write(section_content)

    await ctx.info(f"Updated PRD section: {section}")

    return {
        "status": "success",
        "message": f"Successfully updated {section} section in PRD"
    }


@mcp.tool()
async def create_tasks_from_prd(ctx: Context) -> Dict[str, Any]:
    """
    Read the PRD and create a comprehensive task breakdown with subtasks,
    complexity levels, and dependencies.

    Args:
        ctx: MCP context for logging

    Returns:
        Dictionary containing the created tasks structure
    """
    if not PRD_FILE.exists():
        return {"error": "PRD not found. Please generate a PRD first."}

    # Read PRD content
    with open(PRD_FILE, 'r') as f:
        prd_content = f.read()

    await ctx.info("Analyzing PRD to create task breakdown...")
    await ctx.info(f"Tasks will be saved to: {TASKS_FILE}")

    # Extract project name from PRD if available
    project_name = "OnlyNet Tasks Project"
    lines = prd_content.split('\n')
    for line in lines:
        if line.startswith("## Project:"):
            project_name = line.replace("## Project:", "").strip()
            break

    # Initialize tasks structure
    tasks_data = {
        "project_name": project_name,
        "created_at": datetime.now().isoformat(),
        "last_updated": datetime.now().isoformat(),
        "tasks": []
    }

    # Generate tasks from PRD content
    generated_tasks = _generate_tasks_from_prd_analysis(prd_content, project_name)
    tasks_data["tasks"] = generated_tasks

    # Save tasks to file
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks_data, f, indent=2)

    await ctx.info(f"Created {len(tasks_data['tasks'])} main tasks with subtasks")

    return {
        "status": "success",
        "message": f"Successfully created {len(tasks_data['tasks'])} tasks from PRD",
        "tasks_file": str(TASKS_FILE),
        "task_count": len(tasks_data['tasks']),
        "total_subtasks": sum(len(task.get('subtasks', [])) for task in tasks_data['tasks'])
    }


@mcp.tool()
async def read_task(
    task_id: Optional[str] = None,
    read_next: bool = False,
    ctx: Context = None
) -> Dict[str, Any]:
    """
    Read specific task/subtask information or get the next open task.

    Args:
        task_id: Specific task ID to read (e.g., "TASK-001" or "TASK-001-01")
        read_next: If True, returns the next open task
        ctx: MCP context

    Returns:
        Dictionary containing task information
    """
    if not TASKS_FILE.exists():
        return {"error": "Tasks file not found. Please create tasks from PRD first."}

    with open(TASKS_FILE, 'r') as f:
        tasks_data = json.load(f)

    if read_next:
        # Find next open task
        for task in tasks_data['tasks']:
            if task['current_status'] == 'Open':
                return {
                    "task": task,
                    "message": "Next open task found"
                }
            # Check subtasks
            for subtask in task.get('subtasks', []):
                if subtask['current_status'] == 'Open':
                    return {
                        "task": subtask,
                        "parent_task_id": task['id'],
                        "message": "Next open subtask found"
                    }

        return {"message": "No open tasks found"}

    elif task_id:
        # Search for specific task
        for task in tasks_data['tasks']:
            if task['id'] == task_id:
                return {"task": task}
            # Check subtasks
            for subtask in task.get('subtasks', []):
                if subtask['id'] == task_id:
                    return {
                        "task": subtask,
                        "parent_task_id": task['id']
                    }

        return {"error": f"Task {task_id} not found"}

    else:
        return {"error": "Please provide either task_id or set read_next=True"}


@mcp.tool()
async def complete_task(
    task_id: str,
    ctx: Context
) -> Dict[str, str]:
    """
    Mark a task or subtask as completed (Closed status).

    Args:
        task_id: The ID of the task to complete
        ctx: MCP context

    Returns:
        Dictionary containing completion status
    """
    if not TASKS_FILE.exists():
        return {"error": "Tasks file not found. Please create tasks from PRD first."}

    with open(TASKS_FILE, 'r') as f:
        tasks_data = json.load(f)

    task_found = False

    # Search and update task status
    for task in tasks_data['tasks']:
        if task['id'] == task_id:
            task['current_status'] = 'Closed'
            task_found = True
            await ctx.info(f"Completed task: {task['title']}")
            break

        # Check subtasks
        for subtask in task.get('subtasks', []):
            if subtask['id'] == task_id:
                subtask['current_status'] = 'Closed'
                task_found = True
                await ctx.info(f"Completed subtask: {subtask['title']}")

                # Check if all subtasks are closed
                all_subtasks_closed = all(
                    st['current_status'] == 'Closed'
                    for st in task.get('subtasks', [])
                )
                if all_subtasks_closed and task['current_status'] == 'Open':
                    await ctx.info(f"All subtasks completed. Consider closing parent task {task['id']}")
                break

    if not task_found:
        return {"error": f"Task {task_id} not found"}

    # Update timestamp and save
    tasks_data['last_updated'] = datetime.now().isoformat()

    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks_data, f, indent=2)

    return {
        "status": "success",
        "message": f"Task {task_id} marked as completed"
    }


@mcp.tool()
async def list_all_tasks(ctx: Context) -> Dict[str, Any]:
    """
    List all tasks and subtasks with their title, complexity, and status.

    Args:
        ctx: MCP context

    Returns:
        Dictionary containing formatted task list
    """
    if not TASKS_FILE.exists():
        return {"error": "Tasks file not found. Please create tasks from PRD first."}

    with open(TASKS_FILE, 'r') as f:
        tasks_data = json.load(f)

    await ctx.info(f"Listing all tasks for project: {tasks_data.get('project_name', 'Unknown')}")

    task_list = []
    open_count = 0
    closed_count = 0

    for task in tasks_data['tasks']:
        # Add main task
        task_summary = {
            "id": task['id'],
            "title": task['title'],
            "complexity": f"Level {task['complexity_level']} - {task['complexity_description']}",
            "status": task['current_status'],
            "type": "Main Task",
            "dependencies": task.get('dependencies', [])
        }
        task_list.append(task_summary)

        if task['current_status'] == 'Open':
            open_count += 1
        else:
            closed_count += 1

        # Add subtasks
        for subtask in task.get('subtasks', []):
            subtask_summary = {
                "id": subtask['id'],
                "title": f"  └─ {subtask['title']}",
                "complexity": f"Level {subtask['complexity_level']} - {subtask['complexity_description']}",
                "status": subtask['current_status'],
                "type": "Subtask",
                "parent_id": task['id'],
                "dependencies": subtask.get('dependencies', [])
            }
            task_list.append(subtask_summary)

            if subtask['current_status'] == 'Open':
                open_count += 1
            else:
                closed_count += 1

    return {
        "project_name": tasks_data.get('project_name'),
        "last_updated": tasks_data.get('last_updated'),
        "summary": {
            "total_tasks": len(task_list),
            "open_tasks": open_count,
            "closed_tasks": closed_count,
            "completion_percentage": round((closed_count / len(task_list)) * 100, 1) if task_list else 0
        },
        "tasks": task_list
    }


def main():
    """Main entry point for the OnlyNet Tasks MCP server."""
    mcp.run()


# Run the server
if __name__ == "__main__":
    main()
