#!/usr/bin/env python3
import json
import os
from datetime import datetime, timezone

TASKS_PATH = os.path.join(os.path.dirname(__file__), 'tasks.json')

def load_tasks():
    p = TASKS_PATH
    if not os.path.exists(p):
        # fallback to workspace tasks
        p = '/root/.openclaw/workspace/tasks/tasks.json'
    with open(p) as f:
        return json.load(f)

def progress_bar(done, total, width=20):
    if total == 0:
        return '[{}] 100%'.format('█'*width)
    filled = int(width * done / total)
    return '[' + '█'*filled + '░'*(width-filled) + '] {:3d}%'.format(int(100*done/total))

def render():
    data = load_tasks()
    tasks = data.get('tasks', [])
    projects = data.get('projects', [])
    reminders = data.get('reminders', [])

    now = datetime.now(timezone.utc)

    # Summary
    total = len(tasks)
    done = sum(1 for t in tasks if t.get('status')=='done')
    lines = []
    lines.append('\nTOBI — Task Dashboard\n')
    lines.append('Summary: {} tasks — {} done'.format(total, done))
    lines.append(progress_bar(done, total))
    lines.append('')

    # Projects
    lines.append('Projects:')
    for p in projects:
        title = p.get('title')
        milestones = p.get('milestones', [])
        m_total = len(milestones)
        m_done = sum(1 for m in milestones if m.get('status')=='done') if m_total>0 else 0
        lines.append(' - {}: {}'.format(title, progress_bar(m_done, m_total)))
    lines.append('')

    # Tasks by status
    lines.append('Tasks:')
    for t in sorted(tasks, key=lambda x: (x.get('priority','P3'), x.get('due',''))):
        status = t.get('status')
        title = t.get('title')
        due = t.get('due','')
        lines.append(' - {} ({}) [{}]'.format(title, t.get('priority'), status) + (f' due {due}' if due else ''))
    lines.append('')

    # Upcoming events
    lines.append('Upcoming events:')
    for e in reminders:
        start = e.get('start')
        lines.append(' - {} at {} '.format(e.get('title'), start))
    lines.append('')

    print('\n'.join(lines))

if __name__=='__main__':
    render()
