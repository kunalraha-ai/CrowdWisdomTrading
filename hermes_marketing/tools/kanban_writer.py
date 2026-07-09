import os
import re

KANBAN_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "obsidian_vault", "Marketing Kanban.md"))

def read_kanban() -> str:
    if not os.path.exists(KANBAN_PATH):
        # Create default kanban structure if it's missing
        default_content = "---\nkanban-plugin: board\n---\n\n## Backlog\n\n## In Progress\n\n## Done\n"
        os.makedirs(os.path.dirname(KANBAN_PATH), exist_ok=True)
        with open(KANBAN_PATH, "w", encoding="utf-8") as f:
            f.write(default_content)
        return default_content
    with open(KANBAN_PATH, "r", encoding="utf-8") as f:
        return f.read()

def write_kanban(content: str):
    os.makedirs(os.path.dirname(KANBAN_PATH), exist_ok=True)
    with open(KANBAN_PATH, "w", encoding="utf-8") as f:
        f.write(content)

def update_kanban_board(task_name: str, status: str) -> str:
    """
    Moves a task to a target column (Backlog, In Progress, Done).
    """
    content = read_kanban()
    
    # Split content by H2 headers
    sections = re.split(r'^(## .*)$', content, flags=re.MULTILINE)
    
    # We will reconstruct the board
    header_yaml = sections[0]
    lanes = {}
    
    current_lane = None
    for item in sections[1:]:
        if item.startswith("## "):
            current_lane = item.strip().replace("## ", "")
            lanes[current_lane] = []
        elif current_lane is not None:
            # Parse tasks in this lane
            lines = item.strip().split("\n")
            for line in lines:
                if line.strip():
                    lanes[current_lane].append(line.strip())

    # Ensure our standard lanes exist in the dict
    for lane_name in ["Backlog", "In Progress", "Done"]:
        if lane_name not in lanes:
            lanes[lane_name] = []

    # Clean the task name for comparison
    clean_task_name = task_name.strip().lower()

    # Find and remove the task from any existing lane
    found = False
    task_text = task_name # Default text
    for lane, tasks in lanes.items():
        new_tasks = []
        for t in tasks:
            # Matches "- [ ] Task" or "- [x] Task" or just "- Task"
            match = re.match(r'^-\s+\[[ x]\]\s+(.*)$', t)
            extracted = match.group(1) if match else t.replace("- ", "")
            if extracted.strip().lower() == clean_task_name:
                found = True
                task_text = extracted.strip() # Preserve original casing
            else:
                new_tasks.append(t)
        lanes[lane] = new_tasks

    # Format the task for its target lane
    if status.lower() == "done":
        formatted_task = f"- [x] {task_text}"
    else:
        formatted_task = f"- [ ] {task_text}"

    # Add to the target lane
    target_lane = None
    for name in lanes.keys():
        if name.lower() == status.lower():
            target_lane = name
            break
            
    if not target_lane:
        # Fallback if lane not found
        target_lane = "Backlog"

    lanes[target_lane].append(formatted_task)

    # Reconstruct Markdown content
    new_content = header_yaml.rstrip() + "\n\n"
    for lane_name in ["Backlog", "In Progress", "Done"]:
        new_content += f"## {lane_name}\n"
        for t in lanes.get(lane_name, []):
            new_content += f"{t}\n"
        new_content += "\n"
        
    write_kanban(new_content)
    return f"Successfully moved task '{task_text}' to '{target_lane}'."

if __name__ == "__main__":
    # Small test
    print(update_kanban_board("Competitor Research", "In Progress"))
