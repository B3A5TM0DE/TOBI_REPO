#!/usr/bin/env python3
import json, os
from datetime import datetime

TASKS_PATH = os.path.join(os.path.dirname(__file__), 'tasks.json')
if not os.path.exists(TASKS_PATH):
    TASKS_PATH = '/root/.openclaw/workspace/tasks/tasks.json'

def load_tasks():
    with open(TASKS_PATH) as f:
        return json.load(f)

def bar(done,total,width=10):
    if total==0:
        return '█'*width + ' 100%'
    filled=int(width*done/total)
    return '█'*filled + '░'*(width-filled) + f' {int(100*done/total)}%'

if __name__=='__main__':
    data=load_tasks()
    tasks=data.get('tasks',[])
    total=len(tasks)
    done=sum(1 for t in tasks if t.get('status')=='done')
    s=[]
    s.append('TOBI — Daily Summary')
    s.append(f'Tasks: {done}/{total} complete')
    s.append(bar(done,total))
    s.append('Top tasks:')
    for t in tasks[:5]:
        s.append(f"- {t.get('title')} ({t.get('priority')}) [{t.get('status')}]")
    print('\n'.join(s))
