import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=150):
    challenges.append({
        "id": cid,
        "order_index": idx,
        "level_number": mod,
        "slug": slug,
        "title": title,
        "difficulty": diff,
        "instructions": inst,
        "starter_code": starter,
        "solution_code": sol,
        "entry_function_name": func,
        "test_cases": tests,
        "hints": hints,
        "xp_reward": xp,
        "time_limit_seconds": 300 + (idx * 2),
        "sandbox_timeout_seconds": 3.0
    })

# --- TRACK 10: Advanced Mastery & Real-World Capstones (91-100) ---
add_chal("chal-91", 91, 10, "challenge-trie-search", "Prefix Tree (Trie) Search", "hard",
         "Write `test_trie_search(words: list[str], prefix: str) -> bool` creating a Trie, inserting words, and returning True if prefix exists.",
         "def test_trie_search(words: list[str], prefix: str) -> bool:\n    pass\n",
         "def test_trie_search(words: list[str], prefix: str) -> bool:\n    root = {}\n    for word in words:\n        cur = root\n        for ch in word:\n            cur = cur.setdefault(ch, {})\n    cur = root\n    for ch in prefix:\n        if ch not in cur:\n            return False\n        cur = cur[ch]\n    return True\n",
         "test_trie_search",
         [{"input": [["apple", "app", "application"], "app"], "expected": True, "description": "app is prefix", "is_hidden": False},
          {"input": [["apple", "banana"], "cat"], "expected": False, "description": "cat is not prefix", "is_hidden": False},
          {"input": [["mastery", "python"], "mas"], "expected": True, "description": "mas prefix", "is_hidden": True}],
         ["Build nested dict tree.", "Follow prefix characters."], 120)

add_chal("chal-92", 92, 10, "challenge-lru-cache", "Simulate LRU Cache", "hard",
         "Write `simulate_lru_cache(capacity: int, operations: list[dict]) -> list` supporting {'op': 'put', 'k': k, 'v': v} and {'op': 'get', 'k': k} (returning value or -1).",
         "def simulate_lru_cache(capacity: int, operations: list[dict]) -> list:\n    pass\n",
         "def simulate_lru_cache(capacity: int, operations: list[dict]) -> list:\n    from collections import OrderedDict\n    cache = OrderedDict()\n    out = []\n    for op in operations:\n        if op['op'] == 'put':\n            k, v = op['k'], op['v']\n            if k in cache:\n                cache.move_to_end(k)\n            cache[k] = v\n            if len(cache) > capacity:\n                cache.popitem(last=False)\n        elif op['op'] == 'get':\n            k = op['k']\n            if k in cache:\n                cache.move_to_end(k)\n                out.append(cache[k])\n            else:\n                out.append(-1)\n    return out\n",
         "simulate_lru_cache",
         [{"input": [2, [{"op": "put", "k": 1, "v": 10}, {"op": "put", "k": 2, "v": 20}, {"op": "get", "k": 1}, {"op": "put", "k": 3, "v": 30}, {"op": "get", "k": 2}]], "expected": [10, -1], "description": "Key 2 evicted", "is_hidden": False},
          {"input": [1, [{"op": "put", "k": 1, "v": 5}, {"op": "get", "k": 1}, {"op": "get", "k": 2}]], "expected": [5, -1], "description": "Capacity 1", "is_hidden": False},
          {"input": [2, [{"op": "get", "k": 9}]], "expected": [-1], "description": "Missing key", "is_hidden": True}],
         ["Use collections.OrderedDict.", "Use move_to_end() and popitem(last=False)."], 130)

add_chal("chal-93", 93, 10, "challenge-rate-limiter-logic", "Sliding Window Rate Limiter", "hard",
         "Write `sliding_window_rate_limiter(timestamps: list[int], now: int, max_req: int, window: int) -> bool` returning True if count of timestamps in [now - window, now] < max_req.",
         "def sliding_window_rate_limiter(timestamps: list[int], now: int, max_req: int, window: int) -> bool:\n    pass\n",
         "def sliding_window_rate_limiter(timestamps: list[int], now: int, max_req: int, window: int) -> bool:\n    active = [t for t in timestamps if now - window <= t <= now]\n    return len(active) < max_req\n",
         "sliding_window_rate_limiter",
         [{"input": [[10, 20, 30], 40, 5, 30], "expected": True, "description": "3 requests in window < 5", "is_hidden": False},
          {"input": [[10, 15, 20], 25, 3, 20], "expected": False, "description": "3 requests >= max 3", "is_hidden": False},
          {"input": [[5], 100, 1, 10], "expected": True, "description": "Old request out of window", "is_hidden": True}],
         ["Filter timestamps where t >= now - window.", "Compare count < max_req."], 110)

add_chal("chal-94", 94, 10, "challenge-eval-rpn", "Evaluate Reverse Polish Notation", "hard",
         "Write `eval_rpn(tokens: list[str]) -> int` evaluating RPN expression supporting '+', '-', '*', '/' (integer division truncating toward zero).",
         "def eval_rpn(tokens: list[str]) -> int:\n    pass\n",
         "def eval_rpn(tokens: list[str]) -> int:\n    stack = []\n    for t in tokens:\n        if t in '+-*/':\n            b = stack.pop()\n            a = stack.pop()\n            if t == '+': stack.append(a + b)\n            elif t == '-': stack.append(a - b)\n            elif t == '*': stack.append(a * b)\n            elif t == '/': stack.append(int(a / b))\n        else:\n            stack.append(int(t))\n    return stack[0]\n",
         "eval_rpn",
         [{"input": [["2", "1", "+", "3", "*"]], "expected": 9, "description": "(2 + 1) * 3 = 9", "is_hidden": False},
          {"input": [["4", "13", "5", "/", "+"]], "expected": 6, "description": "4 + (13 / 5) = 6", "is_hidden": False},
          {"input": [["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]], "expected": 22, "description": "Complex RPN", "is_hidden": True}],
         ["Use a stack.", "Pop b then a, apply operator, push result."], 125)

add_chal("chal-95", 95, 10, "challenge-traffic-light", "Traffic Light State Machine", "easy",
         "Write `simulate_traffic_light(steps: int) -> str` cycling 'Green' -> 'Yellow' -> 'Red' -> 'Green' starting at 'Green' (0 steps = 'Green').",
         "def simulate_traffic_light(steps: int) -> str:\n    pass\n",
         "def simulate_traffic_light(steps: int) -> str:\n    states = ['Green', 'Yellow', 'Red']\n    return states[steps % 3]\n",
         "simulate_traffic_light",
         [{"input": [0], "expected": "Green", "description": "0 steps", "is_hidden": False},
          {"input": [1], "expected": "Yellow", "description": "1 step", "is_hidden": False},
          {"input": [5], "expected": "Red", "description": "5 steps = Red", "is_hidden": True}],
         ["States array ['Green', 'Yellow', 'Red'].", "Access steps % 3."], 80)

add_chal("chal-96", 96, 10, "challenge-bfs-shortest-path", "Graph Breadth-First Search", "hard",
         "Write `bfs_shortest_path(graph: dict[str, list[str]], start: str, target: str) -> list[str]` returning shortest path of node labels from start to target, or [] if no path.",
         "def bfs_shortest_path(graph: dict, start: str, target: str) -> list[str]:\n    pass\n",
         "def bfs_shortest_path(graph: dict, start: str, target: str) -> list[str]:\n    from collections import deque\n    if start == target:\n        return [start]\n    queue = deque([[start]])\n    visited = {start}\n    while queue:\n        path = queue.popleft()\n        node = path[-1]\n        for neighbor in graph.get(node, []):\n            if neighbor not in visited:\n                visited.add(neighbor)\n                new_path = path + [neighbor]\n                if neighbor == target:\n                    return new_path\n                queue.append(new_path)\n    return []\n",
         "bfs_shortest_path",
         [{"input": [{"A": ["B", "C"], "B": ["D"], "C": ["D"], "D": []}, "A", "D"], "expected": ["A", "B", "D"], "description": "A to D path", "is_hidden": False},
          {"input": [{"A": ["B"], "B": [], "C": []}, "A", "C"], "expected": [], "description": "No path", "is_hidden": False},
          {"input": [{"X": ["Y"], "Y": ["Z"], "Z": []}, "X", "Z"], "expected": ["X", "Y", "Z"], "description": "X-Y-Z path", "is_hidden": True}],
         ["Use a queue tracking paths.", "Return first path reaching target."], 130)

add_chal("chal-97", 97, 10, "challenge-overlapping-intervals", "Overlapping Intervals Detector", "medium",
         "Write `has_overlapping_intervals(intervals: list[list[int]]) -> bool` returning True if any intervals [start, end] overlap (exclusive of touching borders e.g. [1, 2] and [2, 3] do not overlap).",
         "def has_overlapping_intervals(intervals: list[list[int]]) -> bool:\n    pass\n",
         "def has_overlapping_intervals(intervals: list[list[int]]) -> bool:\n    sorted_intervals = sorted(intervals, key=lambda x: x[0])\n    for i in range(len(sorted_intervals) - 1):\n        if sorted_intervals[i][1] > sorted_intervals[i+1][0]:\n            return True\n    return False\n",
         "has_overlapping_intervals",
         [{"input": [[[1, 4], [2, 5]]], "expected": True, "description": "Overlap 2 to 4", "is_hidden": False},
          {"input": [[[1, 2], [2, 3], [3, 4]]], "expected": False, "description": "Touching borders do not overlap", "is_hidden": False},
          {"input": [[[1, 10], [15, 20]]], "expected": False, "description": "Disjoint intervals", "is_hidden": True}],
         ["Sort intervals by start.", "Check if cur_end > next_start."], 105)

add_chal("chal-98", 98, 10, "challenge-priority-tasks", "Priority Task Scheduler", "medium",
         "Write `schedule_priority_tasks(tasks: list[dict]) -> list[str]` where each task has {'name': str, 'priority': int} returning task names sorted by priority descending (ties broken by name).",
         "def schedule_priority_tasks(tasks: list[dict]) -> list[str]:\n    pass\n",
         "def schedule_priority_tasks(tasks: list[dict]) -> list[str]:\n    sorted_tasks = sorted(tasks, key=lambda t: (-t['priority'], t['name']))\n    return [t['name'] for t in sorted_tasks]\n",
         "schedule_priority_tasks",
         [{"input": [[{"name": "Fix Bug", "priority": 10}, {"name": "Write Docs", "priority": 3}, {"name": "Deploy", "priority": 10}]], "expected": ["Deploy", "Fix Bug", "Write Docs"], "description": "Priority 10 ties sorted alphabetically", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty tasks", "is_hidden": False},
          {"input": [[{"name": "A", "priority": 1}, {"name": "B", "priority": 2}]], "expected": ["B", "A"], "description": "Priority 2 then 1", "is_hidden": True}],
         ["Sort by (-t['priority'], t['name'])."], 105)

add_chal("chal-99", 99, 10, "challenge-event-bus", "In-Memory Event Dispatcher", "medium",
         "Write `simulate_event_bus(events: list[dict]) -> list[str]` recording dispatched events: each event has {'type': str, 'payload': str}, returning ['<type>: <payload>', ...].",
         "def simulate_event_bus(events: list[dict]) -> list[str]:\n    pass\n",
         "def simulate_event_bus(events: list[dict]) -> list[str]:\n    return [f\"{e['type']}: {e['payload']}\" for e in events]\n",
         "simulate_event_bus",
         [{"input": [[{"type": "LOGIN", "payload": "user1"}, {"type": "CLICK", "payload": "btn_submit"}]], "expected": ["LOGIN: user1", "CLICK: btn_submit"], "description": "Two events", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "No events", "is_hidden": False},
          {"input": [[{"type": "ERROR", "payload": "timeout"}]], "expected": ["ERROR: timeout"], "description": "Error event", "is_hidden": True}],
         ["Format each event as f\"{e['type']}: {e['payload']}\"."], 100)

add_chal("chal-100", 100, 10, "challenge-python-mastery-capstone", "Python Master Evaluator Capstone", "hard",
         "Write `python_master_evaluator(commands: list[str]) -> dict[str, int]` executing simple statements 'x = <int>' and 'x += <int>' or 'x -= <int>', returning final variables sorted by name.",
         "def python_master_evaluator(commands: list[str]) -> dict[str, int]:\n    pass\n",
         "def python_master_evaluator(commands: list[str]) -> dict[str, int]:\n    memory = {}\n    for cmd in commands:\n        parts = cmd.split()\n        if len(parts) == 3:\n            var, op, val_str = parts\n            val = int(val_str)\n            if op == '=':\n                memory[var] = val\n            elif op == '+=':\n                memory[var] = memory.get(var, 0) + val\n            elif op == '-=':\n                memory[var] = memory.get(var, 0) - val\n    return {k: memory[k] for k in sorted(memory.keys())}\n",
         "python_master_evaluator",
         [{"input": [["a = 10", "b = 20", "a += 5", "b -= 3"]], "expected": {"a": 15, "b": 17}, "description": "a and b assignments & ops", "is_hidden": False},
          {"input": [["x = 100", "x += 50", "x -= 25"]], "expected": {"x": 125}, "description": "Single var", "is_hidden": False},
          {"input": [["z = 0", "y = 10"]], "expected": {"y": 10, "z": 0}, "description": "Sorted keys", "is_hidden": True}],
         ["Parse commands line by line.", "Update memory dictionary."], 250)

with open("scripts/track10.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 10 generated: 10 challenges")
