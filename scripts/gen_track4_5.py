import json

challenges = []

def add_chal(cid, idx, mod, slug, title, diff, inst, starter, sol, func, tests, hints, xp=90):
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

# --- TRACK 4: Functions, Recursion & Logic (31-40) ---
add_chal("chal-31", 31, 4, "challenge-calculate-power", "Power with Optional Exponent", "easy",
         "Write `calculate_power(base: int, exp: int) -> int` returning base ** exp.",
         "def calculate_power(base: int, exp: int) -> int:\n    pass\n",
         "def calculate_power(base: int, exp: int) -> int:\n    return base ** exp\n",
         "calculate_power",
         [{"input": [2, 3], "expected": 8, "description": "2^3 = 8", "is_hidden": False},
          {"input": [5, 0], "expected": 1, "description": "5^0 = 1", "is_hidden": False},
          {"input": [10, 4], "expected": 10000, "description": "10^4 = 10000", "is_hidden": True}],
         ["Use ** operator.", "Handle base ** exp."], 75)

add_chal("chal-32", 32, 4, "challenge-sum-digits-rec", "Recursive Sum of Digits", "medium",
         "Write recursive `sum_digits(n: int) -> int` summing all digits of positive integer n.",
         "def sum_digits(n: int) -> int:\n    pass\n",
         "def sum_digits(n: int) -> int:\n    n = abs(n)\n    if n < 10:\n        return n\n    return (n % 10) + sum_digits(n // 10)\n",
         "sum_digits",
         [{"input": [123], "expected": 6, "description": "1+2+3 = 6", "is_hidden": False},
          {"input": [905], "expected": 14, "description": "9+0+5 = 14", "is_hidden": False},
          {"input": [9999], "expected": 36, "description": "9*4 = 36", "is_hidden": True}],
         ["Base case: if n < 10 return n.", "Recursive step: n % 10 + sum_digits(n // 10)."], 90)

add_chal("chal-33", 33, 4, "challenge-reverse-string-rec", "Recursive String Reversal", "medium",
         "Write recursive `reverse_string_rec(s: str) -> str` reversing a string without slices.",
         "def reverse_string_rec(s: str) -> str:\n    pass\n",
         "def reverse_string_rec(s: str) -> str:\n    if len(s) <= 1:\n        return s\n    return reverse_string_rec(s[1:]) + s[0]\n",
         "reverse_string_rec",
         [{"input": ["hello"], "expected": "olleh", "description": "hello -> olleh", "is_hidden": False},
          {"input": ["a"], "expected": "a", "description": "single char", "is_hidden": False},
          {"input": ["recursion"], "expected": "noisrucer", "description": "recursion", "is_hidden": True}],
         ["Base case: if len(s) <= 1 return s.", "Recurse on s[1:] + s[0]."], 90)

add_chal("chal-34", 34, 4, "challenge-apply-multiplier", "Multiplier Function Factory", "easy",
         "Write `apply_multiplier(factor: int, val: int) -> int` demonstrating higher-order closure multiplying val by factor.",
         "def apply_multiplier(factor: int, val: int) -> int:\n    pass\n",
         "def apply_multiplier(factor: int, val: int) -> int:\n    def make_multiplier(f):\n        return lambda x: x * f\n    multiplier = make_multiplier(factor)\n    return multiplier(val)\n",
         "apply_multiplier",
         [{"input": [3, 5], "expected": 15, "description": "3 * 5 = 15", "is_hidden": False},
          {"input": [10, 7], "expected": 70, "description": "10 * 7 = 70", "is_hidden": False},
          {"input": [-2, 4], "expected": -8, "description": "Negative factor", "is_hidden": True}],
         ["Create closure returning lambda x: x * factor."], 80)

add_chal("chal-35", 35, 4, "challenge-clamp-number", "Clamp Number in Range", "easy",
         "Write `clamp_number(val: float, min_val: float, max_val: float) -> float` bounding val between min_val and max_val.",
         "def clamp_number(val: float, min_val: float, max_val: float) -> float:\n    pass\n",
         "def clamp_number(val: float, min_val: float, max_val: float) -> float:\n    return max(min_val, min(val, max_val))\n",
         "clamp_number",
         [{"input": [15, 0, 10], "expected": 10, "description": "Clamp above max", "is_hidden": False},
          {"input": [-5, 0, 10], "expected": 0, "description": "Clamp below min", "is_hidden": False},
          {"input": [5, 0, 10], "expected": 5, "description": "Within bounds", "is_hidden": True}],
         ["Use max(min_val, min(val, max_val))."], 75)

add_chal("chal-36", 36, 4, "challenge-curry-multiply", "Curried Binary Product", "easy",
         "Write `curry_multiply(a: int, b: int) -> int` simulating currying by returning a * b.",
         "def curry_multiply(a: int, b: int) -> int:\n    pass\n",
         "def curry_multiply(a: int, b: int) -> int:\n    curried = lambda x: lambda y: x * y\n    return curried(a)(b)\n",
         "curry_multiply",
         [{"input": [4, 5], "expected": 20, "description": "4 * 5 = 20", "is_hidden": False},
          {"input": [0, 99], "expected": 0, "description": "0 * 99 = 0", "is_hidden": False},
          {"input": [-3, 7], "expected": -21, "description": "Negatives", "is_hidden": True}],
         ["Return curried(a)(b)."], 80)

add_chal("chal-37", 37, 4, "challenge-gcd-recursive", "Recursive Greatest Common Divisor", "medium",
         "Write recursive `gcd_recursive(a: int, b: int) -> int` computing GCD using Euclid's algorithm.",
         "def gcd_recursive(a: int, b: int) -> int:\n    pass\n",
         "def gcd_recursive(a: int, b: int) -> int:\n    if b == 0:\n        return a\n    return gcd_recursive(b, a % b)\n",
         "gcd_recursive",
         [{"input": [48, 18], "expected": 6, "description": "GCD(48, 18) = 6", "is_hidden": False},
          {"input": [101, 10], "expected": 1, "description": "Coprime", "is_hidden": False},
          {"input": [54, 24], "expected": 6, "description": "GCD(54, 24) = 6", "is_hidden": True}],
         ["Base case: if b == 0 return a.", "Recursive step: gcd_recursive(b, a % b)."], 90)

add_chal("chal-38", 38, 4, "challenge-fib-memo", "Fibonacci with Memoization", "medium",
         "Write `fib_memo(n: int) -> int` computing the n-th Fibonacci number efficiently using memoization (0-indexed: fib(0)=0, fib(1)=1, fib(2)=1).",
         "def fib_memo(n: int) -> int:\n    pass\n",
         "def fib_memo(n: int) -> int:\n    memo = {0: 0, 1: 1}\n    def helper(k):\n        if k not in memo:\n            memo[k] = helper(k - 1) + helper(k - 2)\n        return memo[k]\n    return helper(n)\n",
         "fib_memo",
         [{"input": [10], "expected": 55, "description": "fib(10) = 55", "is_hidden": False},
          {"input": [20], "expected": 6765, "description": "fib(20) = 6765", "is_hidden": False},
          {"input": [30], "expected": 832040, "description": "fib(30) = 832040", "is_hidden": True}],
         ["Use a dict to store cached values.", "Lookup before recursing."], 95)

add_chal("chal-39", 39, 4, "challenge-compose-two", "Two-Function Pipeline Composition", "easy",
         "Write `compose_two(x: int) -> int` applying f(n) = n + 3 then g(n) = n * 2: return g(f(x)).",
         "def compose_two(x: int) -> int:\n    pass\n",
         "def compose_two(x: int) -> int:\n    f = lambda n: n + 3\n    g = lambda n: n * 2\n    return g(f(x))\n",
         "compose_two",
         [{"input": [5], "expected": 16, "description": "(5 + 3) * 2 = 16", "is_hidden": False},
          {"input": [0], "expected": 6, "description": "(0 + 3) * 2 = 6", "is_hidden": False},
          {"input": [-3], "expected": 0, "description": "(-3 + 3) * 2 = 0", "is_hidden": True}],
         ["Compute (x + 3) * 2."], 75)

add_chal("chal-40", 40, 4, "challenge-collatz-steps", "Collatz Conjecture Step Counter", "easy",
         "Write `collatz_steps(n: int) -> int` counting steps to reach 1 (if even n/2, if odd 3n+1).",
         "def collatz_steps(n: int) -> int:\n    pass\n",
         "def collatz_steps(n: int) -> int:\n    steps = 0\n    while n > 1:\n        if n % 2 == 0:\n            n = n // 2\n        else:\n            n = 3 * n + 1\n        steps += 1\n    return steps\n",
         "collatz_steps",
         [{"input": [6], "expected": 8, "description": "Collatz 6 takes 8 steps", "is_hidden": False},
          {"input": [1], "expected": 0, "description": "Collatz 1 takes 0 steps", "is_hidden": False},
          {"input": [12], "expected": 9, "description": "Collatz 12 takes 9 steps", "is_hidden": True}],
         ["While n > 1:", "Update n based on even/odd."], 85)

# --- TRACK 5: Object-Oriented Programming (41-50) ---
add_chal("chal-41", 41, 5, "challenge-bank-account", "Bank Account Class Operations", "easy",
         "Write `manage_bank_account(initial: int, deposits: list[int], withdrawals: list[int]) -> int` modeling a BankAccount class with deposit and withdraw (only withdraw if balance >= amount), returning final balance.",
         "def manage_bank_account(initial: int, deposits: list[int], withdrawals: list[int]) -> int:\n    pass\n",
         "def manage_bank_account(initial: int, deposits: list[int], withdrawals: list[int]) -> int:\n    class BankAccount:\n        def __init__(self, bal):\n            self.bal = bal\n        def deposit(self, amt):\n            self.bal += amt\n        def withdraw(self, amt):\n            if self.bal >= amt:\n                self.bal -= amt\n    acc = BankAccount(initial)\n    for d in deposits:\n        acc.deposit(d)\n    for w in withdrawals:\n        acc.withdraw(w)\n    return acc.bal\n",
         "manage_bank_account",
         [{"input": [100, [50, 20], [30, 40]], "expected": 100, "description": "100+70-70 = 100", "is_hidden": False},
          {"input": [50, [], [100]], "expected": 50, "description": "Insufficient funds ignored", "is_hidden": False},
          {"input": [0, [100], [50]], "expected": 50, "description": "Deposit and withdraw", "is_hidden": True}],
         ["Define class BankAccount with methods.", "Track self.balance."], 90)

add_chal("chal-42", 42, 5, "challenge-rectangle-class", "Rectangle Geometry Class", "easy",
         "Write `calculate_rectangle(w: float, h: float) -> dict` using a Rectangle class returning {'area': w*h, 'perimeter': 2*(w+h)}.",
         "def calculate_rectangle(w: float, h: float) -> dict:\n    pass\n",
         "def calculate_rectangle(w: float, h: float) -> dict:\n    class Rectangle:\n        def __init__(self, width, height):\n            self.width = width\n            self.height = height\n        def area(self):\n            return self.width * self.height\n        def perimeter(self):\n            return 2 * (self.width + self.height)\n    r = Rectangle(w, h)\n    return {'area': r.area(), 'perimeter': r.perimeter()}\n",
         "calculate_rectangle",
         [{"input": [4.0, 5.0], "expected": {"area": 20.0, "perimeter": 18.0}, "description": "4x5 rect", "is_hidden": False},
          {"input": [10.0, 10.0], "expected": {"area": 100.0, "perimeter": 40.0}, "description": "Square 10x10", "is_hidden": False},
          {"input": [1.5, 2.0], "expected": {"area": 3.0, "perimeter": 7.0}, "description": "Floats", "is_hidden": True}],
         ["Define Rectangle class.", "Return dict with area and perimeter."], 85)

add_chal("chal-43", 43, 5, "challenge-book-representation", "Book String Representation", "easy",
         "Write `format_book(title: str, author: str, year: int) -> str` defining a Book class whose `__str__` returns '<title> by <author> (<year>)'.",
         "def format_book(title: str, author: str, year: int) -> str:\n    pass\n",
         "def format_book(title: str, author: str, year: int) -> str:\n    class Book:\n        def __init__(self, t, a, y):\n            self.t, self.a, self.y = t, a, y\n        def __str__(self):\n            return f'{self.t} by {self.a} ({self.y})'\n    return str(Book(title, author, year))\n",
         "format_book",
         [{"input": ["1984", "George Orwell", 1949], "expected": "1984 by George Orwell (1949)", "description": "1984 book", "is_hidden": False},
          {"input": ["Clean Code", "Robert Martin", 2008], "expected": "Clean Code by Robert Martin (2008)", "description": "Clean Code", "is_hidden": False},
          {"input": ["Hamlet", "Shakespeare", 1603], "expected": "Hamlet by Shakespeare (1603)", "description": "Hamlet", "is_hidden": True}],
         ["Implement __str__ method on Book class."], 85)

add_chal("chal-44", 44, 5, "challenge-static-temp", "Static Method Temperature Helper", "easy",
         "Write `convert_temp_static(c: float) -> float` using a class TemperatureConverter with `@staticmethod c_to_f(c)` returning C * 9/5 + 32.",
         "def convert_temp_static(c: float) -> float:\n    pass\n",
         "def convert_temp_static(c: float) -> float:\n    class TemperatureConverter:\n        @staticmethod\n        def c_to_f(val):\n            return round(val * 9.0 / 5.0 + 32.0, 1)\n    return TemperatureConverter.c_to_f(c)\n",
         "convert_temp_static",
         [{"input": [0.0], "expected": 32.0, "description": "0C", "is_hidden": False},
          {"input": [25.0], "expected": 77.0, "description": "25C", "is_hidden": False},
          {"input": [-40.0], "expected": -40.0, "description": "-40C = -40F", "is_hidden": True}],
         ["Use @staticmethod decorator."], 85)

add_chal("chal-45", 45, 5, "challenge-vehicle-hierarchy", "Vehicle Inheritance Hierarchy", "medium",
         "Write `evaluate_car_hierarchy(brand: str, model: str, battery_kwh: int) -> str` with Vehicle(brand, model) and ElectricCar inheriting Vehicle with get_info() returning '<brand> <model> with <battery_kwh>kWh battery'.",
         "def evaluate_car_hierarchy(brand: str, model: str, battery_kwh: int) -> str:\n    pass\n",
         "def evaluate_car_hierarchy(brand: str, model: str, battery_kwh: int) -> str:\n    class Vehicle:\n        def __init__(self, brand, model):\n            self.brand = brand\n            self.model = model\n    class ElectricCar(Vehicle):\n        def __init__(self, brand, model, battery_kwh):\n            super().__init__(brand, model)\n            self.battery_kwh = battery_kwh\n        def get_info(self):\n            return f'{self.brand} {self.model} with {self.battery_kwh}kWh battery'\n    car = ElectricCar(brand, model, battery_kwh)\n    return car.get_info()\n",
         "evaluate_car_hierarchy",
         [{"input": ["Tesla", "Model 3", 75], "expected": "Tesla Model 3 with 75kWh battery", "description": "Tesla", "is_hidden": False},
          {"input": ["Rivian", "R1T", 135], "expected": "Rivian R1T with 135kWh battery", "description": "Rivian", "is_hidden": False},
          {"input": ["Nissan", "Leaf", 40], "expected": "Nissan Leaf with 40kWh battery", "description": "Leaf", "is_hidden": True}],
         ["Use super().__init__(brand, model).", "Define get_info method."], 95)

add_chal("chal-46", 46, 5, "challenge-vector-dunder-add", "Vector 2D Dunder Addition", "medium",
         "Write `add_vectors(x1: int, y1: int, x2: int, y2: int) -> list[int]` implementing Vector(x, y) with `__add__` returning [x1+x2, y1+y2].",
         "def add_vectors(x1: int, y1: int, x2: int, y2: int) -> list[int]:\n    pass\n",
         "def add_vectors(x1: int, y1: int, x2: int, y2: int) -> list[int]:\n    class Vector:\n        def __init__(self, x, y):\n            self.x, self.y = x, y\n        def __add__(self, other):\n            return Vector(self.x + other.x, self.y + other.y)\n    v3 = Vector(x1, y1) + Vector(x2, y2)\n    return [v3.x, v3.y]\n",
         "add_vectors",
         [{"input": [1, 2, 3, 4], "expected": [4, 6], "description": "(1,2) + (3,4) = (4,6)", "is_hidden": False},
          {"input": [-1, 5, 1, -5], "expected": [0, 0], "description": "Cancel out", "is_hidden": False},
          {"input": [10, 20, 30, 40], "expected": [40, 60], "description": "Large coords", "is_hidden": True}],
         ["Implement __add__(self, other) on Vector."], 95)

add_chal("chal-47", 47, 5, "challenge-simulate-stack", "Stack Class with Dunder Length", "easy",
         "Write `simulate_stack(ops: list[str]) -> list` with Stack class handling 'push <val>' and 'pop' returning remaining items.",
         "def simulate_stack(ops: list[str]) -> list:\n    pass\n",
         "def simulate_stack(ops: list[str]) -> list:\n    class Stack:\n        def __init__(self):\n            self._items = []\n        def push(self, x):\n            self._items.append(x)\n        def pop(self):\n            return self._items.pop() if self._items else None\n    s = Stack()\n    for op in ops:\n        if op.startswith('push '):\n            s.push(op.split(' ')[1])\n        elif op == 'pop':\n            s.pop()\n    return s._items\n",
         "simulate_stack",
         [{"input": [["push A", "push B", "pop", "push C"]], "expected": ["A", "C"], "description": "push/pop sequence", "is_hidden": False},
          {"input": [["push 1", "pop", "pop"]], "expected": [], "description": "pop from empty", "is_hidden": False},
          {"input": [["push X", "push Y", "push Z"]], "expected": ["X", "Y", "Z"], "description": "Only pushes", "is_hidden": True}],
         ["Implement Stack with _items list."], 90)

add_chal("chal-48", 48, 5, "challenge-shape-polymorphism", "Shape Polymorphism", "medium",
         "Write `calculate_shape_areas(shapes: list[dict]) -> list[float]` using polymorphic classes Circle(radius) and Square(side) returning areas rounded to 2 decimals (pi=3.14159).",
         "def calculate_shape_areas(shapes: list[dict]) -> list[float]:\n    pass\n",
         "def calculate_shape_areas(shapes: list[dict]) -> list[float]:\n    class Circle:\n        def __init__(self, r):\n            self.r = r\n        def area(self):\n            return round(3.14159 * self.r * self.r, 2)\n    class Square:\n        def __init__(self, s):\n            self.s = s\n        def area(self):\n            return round(self.s * self.s, 2)\n    out = []\n    for item in shapes:\n        if item['type'] == 'circle':\n            out.append(Circle(item['val']).area())\n        elif item['type'] == 'square':\n            out.append(Square(item['val']).area())\n    return out\n",
         "calculate_shape_areas",
         [{"input": [[{"type": "circle", "val": 2}, {"type": "square", "val": 4}]], "expected": [12.57, 16.0], "description": "Circle(2), Square(4)", "is_hidden": False},
          {"input": [[{"type": "square", "val": 3}]], "expected": [9.0], "description": "Single square", "is_hidden": False},
          {"input": [[]], "expected": [], "description": "Empty list", "is_hidden": True}],
         ["Implement area() on both classes."], 95)

add_chal("chal-49", 49, 5, "challenge-track-employee-count", "Class Method Instance Counter", "easy",
         "Write `track_employee_count(names: list[str]) -> int` where Employee class tracks total instances created via class variable and returns Employee.get_count().",
         "def track_employee_count(names: list[str]) -> int:\n    pass\n",
         "def track_employee_count(names: list[str]) -> int:\n    class Employee:\n        count = 0\n        def __init__(self, name):\n            self.name = name\n            Employee.count += 1\n        @classmethod\n        def get_count(cls):\n            return cls.count\n    for n in names:\n        Employee(n)\n    return Employee.get_count()\n",
         "track_employee_count",
         [{"input": [["Alice", "Bob", "Charlie"]], "expected": 3, "description": "3 employees", "is_hidden": False},
          {"input": [[]], "expected": 0, "description": "0 employees", "is_hidden": False},
          {"input": [["One"]], "expected": 1, "description": "1 employee", "is_hidden": True}],
         ["Increment Employee.count in __init__.", "Return count using @classmethod."], 85)

add_chal("chal-50", 50, 5, "challenge-simulate-queue", "FIFO Queue Class Operations", "easy",
         "Write `simulate_queue(ops: list[str]) -> list` implementing a Queue with enqueue and dequeue (FIFO) returning final items.",
         "def simulate_queue(ops: list[str]) -> list:\n    pass\n",
         "def simulate_queue(ops: list[str]) -> list:\n    class Queue:\n        def __init__(self):\n            self._q = []\n        def enqueue(self, val):\n            self._q.append(val)\n        def dequeue(self):\n            return self._q.pop(0) if self._q else None\n    q = Queue()\n    for op in ops:\n        if op.startswith('enqueue '):\n            q.enqueue(op.split(' ')[1])\n        elif op == 'dequeue':\n            q.dequeue()\n    return q._q\n",
         "simulate_queue",
         [{"input": [["enqueue A", "enqueue B", "dequeue", "enqueue C"]], "expected": ["B", "C"], "description": "FIFO queue", "is_hidden": False},
          {"input": [["dequeue"]], "expected": [], "description": "Empty dequeue", "is_hidden": False},
          {"input": [["enqueue 1", "enqueue 2", "enqueue 3"]], "expected": ["1", "2", "3"], "description": "Only enqueues", "is_hidden": True}],
         ["Use list.pop(0) for FIFO dequeue."], 90)

with open("scripts/track4_5.json", "w", encoding="utf-8") as f:
    json.dump(challenges, f, indent=2)
print("Track 4 & 5 generated: 20 challenges")
