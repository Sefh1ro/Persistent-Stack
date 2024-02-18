import os
import pickle
import time

def load_stacks():
    if os.path.exists('stacks.pkl'):
        with open('stacks.pkl', 'rb') as f:
            return pickle.load(f)
    else:
        return {}

def save_stacks(stacks):
    with open('stacks.pkl', 'wb') as f:
        pickle.dump(stacks, f)
    
def process_request(request, stacks, current_stack):
    start_time = time.time()  # Записуємо час початку виконання функції

    if 'create' in request and request['name']:
        name = request['name']
        stacks[name] = []
        current_stack = name
    elif 'delete' in request and request['name'] in stacks:
        del stacks[request['name']]
        if current_stack == request['name']:
            current_stack = None
    elif 'switch' in request and request['name'] in stacks:
        current_stack = request['name']
        
    elif current_stack:
        if 'push' in request and request['value']:
            if stacks[current_stack]:
                stack = stacks[current_stack][-1].copy()
            else:
                stack = []
            stack.append(request['value'])
            stacks[current_stack].append(stack)
        elif 'pop' in request and stacks[current_stack] and stacks[current_stack][-1]:
            stack = stacks[current_stack][-1].copy()
            if stack:
                stack.pop()
                stacks[current_stack].append(stack)
    save_stacks(stacks)

    end_time = time.time()  # Записываем время окончания выполнения функции
    print(f"Час виконання: {end_time - start_time} секунд")

    return stacks, current_stack

def merge_stacks(stack1, stack2):
    steps = []
    merged_stack = []
    for item in stack1 + stack2:
        merged_stack.append(item)
        steps.append({
            'stack': merged_stack.copy(),
            'code': f'merged_stack.append({item})',
        })
    return steps