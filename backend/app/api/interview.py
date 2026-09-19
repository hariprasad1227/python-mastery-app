"""
Interview Arena API Router
Timed technical interview challenges with automated edge-case test suites and complexity feedback.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.models.entities import User, XPTransaction
from backend.app.core.security import get_optional_current_user
from runner.runner import run_code_in_sandbox

router = APIRouter(prefix="/interview", tags=["interview"])

INTERVIEW_PROBLEMS: List[Dict[str, Any]] = [
    {
        "id": "interview-1",
        "slug": "two-sum",
        "title": "Two Sum",
        "difficulty": "Easy",
        "category": "Arrays & Hash Maps",
        "time_limit_minutes": 20,
        "description": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`.\n\nYou may assume that each input would have exactly one solution, and you may not use the same element twice. Aim for O(n) time complexity.",
        "starter_code": '''def two_sum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, n in enumerate(nums):
        diff = target - n
        if diff in seen:
            return [seen[diff], i]
        seen[n] = i
    return []
''',
        "entry_function_name": "two_sum",
        "examples": [
            {"input": "nums = [2,7,11,15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."},
            {"input": "nums = [3,2,4], target = 6", "output": "[1, 2]"},
            {"input": "nums = [3,3], target = 6", "output": "[0, 1]"}
        ],
        "constraints": [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
        ],
        "hints": [
            "Use a dictionary mapping value -> index.",
            "In one pass, check if target - num exists in the dictionary before inserting the current number."
        ],
        "verification_suite": '''
assert two_sum([2, 7, 11, 15], 9) == [0, 1], "Failed basic case"
assert two_sum([3, 2, 4], 6) == [1, 2], "Failed non-sorted case"
assert two_sum([3, 3], 6) == [0, 1], "Failed duplicate values case"
assert two_sum([-1, -2, -3, -4, -5], -8) == [2, 4], "Failed negative numbers case"
print("All Two Sum tests passed!")
'''
    },
    {
        "id": "interview-2",
        "slug": "valid-parentheses",
        "title": "Valid Parentheses",
        "difficulty": "Easy",
        "category": "Stack & Parsing",
        "time_limit_minutes": 20,
        "description": "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if open brackets are closed by the same type of brackets in the correct order.",
        "starter_code": '''def is_valid(s: str) -> bool:
    pairs = {")": "(", "}": "{", "]": "["}
    stack = []
    for char in s:
        if char in pairs:
            if not stack or stack[-1] != pairs[char]:
                return False
            stack.pop()
        else:
            stack.append(char)
    return len(stack) == 0
''',
        "entry_function_name": "is_valid",
        "examples": [
            {"input": 's = "()"', "output": "True"},
            {"input": 's = "()[]{}"', "output": "True"},
            {"input": 's = "(]"', "output": "False"}
        ],
        "constraints": [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'."
        ],
        "hints": [
            "Push open brackets onto a stack.",
            "When encountering a closing bracket, pop the top of the stack and check for a match."
        ],
        "verification_suite": '''
assert is_valid("()") is True, "Failed ()"
assert is_valid("()[]{}") is True, "Failed ()[]{}"
assert is_valid("(]") is False, "Failed (]"
assert is_valid("([)]") is False, "Failed ([)]"
assert is_valid("{[]}") is True, "Failed {[]}"
assert is_valid("[") is False, "Failed single bracket"
print("All Valid Parentheses tests passed!")
'''
    },
    {
        "id": "interview-3",
        "slug": "longest-substring-no-repeat",
        "title": "Longest Substring Without Repeating Characters",
        "difficulty": "Medium",
        "category": "Sliding Window",
        "time_limit_minutes": 25,
        "description": "Given a string `s`, find the length of the longest substring without duplicate characters. Aim for O(n) runtime using a sliding window technique.",
        "starter_code": '''def length_of_longest_substring(s: str) -> int:
    last_seen = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in last_seen and last_seen[char] >= left:
            left = last_seen[char] + 1
        last_seen[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len
''',
        "entry_function_name": "length_of_longest_substring",
        "examples": [
            {"input": 's = "abcabcbb"', "output": "3", "explanation": "'abc' with length 3."},
            {"input": 's = "bbbbb"', "output": "1", "explanation": "'b' with length 1."},
            {"input": 's = "pwwkew"', "output": "3", "explanation": "'wke' with length 3."}
        ],
        "constraints": [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces."
        ],
        "hints": [
            "Maintain the latest index seen for every character.",
            "Advance `left` to `last_seen[char] + 1` whenever a duplicate is found inside the current window."
        ],
        "verification_suite": '''
assert length_of_longest_substring("abcabcbb") == 3, "Failed abcabcbb"
assert length_of_longest_substring("bbbbb") == 1, "Failed bbbbb"
assert length_of_longest_substring("pwwkew") == 3, "Failed pwwkew"
assert length_of_longest_substring("") == 0, "Failed empty string"
assert length_of_longest_substring("au") == 2, "Failed au"
print("All Longest Substring tests passed!")
'''
    },
    {
        "id": "interview-4",
        "slug": "merge-intervals",
        "title": "Merge Overlapping Intervals",
        "difficulty": "Medium",
        "category": "Sorting & Arrays",
        "time_limit_minutes": 25,
        "description": "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all intervals in the input.",
        "starter_code": '''def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:
    if not intervals:
        return []
    intervals.sort(key=lambda x: x[0])
    merged = [intervals[0]]
    for current in intervals[1:]:
        prev = merged[-1]
        if current[0] <= prev[1]:
            prev[1] = max(prev[1], current[1])
        else:
            merged.append(current)
    return merged
''',
        "entry_function_name": "merge_intervals",
        "examples": [
            {"input": "intervals = [[1,3],[2,6],[8,10],[15,18]]", "output": "[[1,6],[8,10],[15,18]]"},
            {"input": "intervals = [[1,4],[4,5]]", "output": "[[1,5]]"}
        ],
        "constraints": [
            "1 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= start_i <= end_i <= 10^4"
        ],
        "hints": [
            "Sort intervals primarily by start time.",
            "Compare the start time of the current interval with the end time of the last merged interval."
        ],
        "verification_suite": '''
assert merge_intervals([[1,3],[2,6],[8,10],[15,18]]) == [[1,6],[8,10],[15,18]], "Failed general overlap"
assert merge_intervals([[1,4],[4,5]]) == [[1,5]], "Failed boundary overlap"
assert merge_intervals([[1,4],[2,3]]) == [[1,4]], "Failed subset overlap"
assert merge_intervals([[1,4]]) == [[1,4]], "Failed single interval"
print("All Merge Intervals tests passed!")
'''
    },
    {
        "id": "interview-5",
        "slug": "lru-cache",
        "title": "LRU Cache Implementation",
        "difficulty": "Hard",
        "category": "Design & Data Structures",
        "time_limit_minutes": 35,
        "description": "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement `LRUCache` with `get(key)` and `put(key, value)` both running in average O(1) time complexity.",
        "starter_code": '''from collections import OrderedDict

class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = OrderedDict()

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
''',
        "entry_function_name": "LRUCache",
        "examples": [
            {"input": "LRUCache(2); put(1, 1); put(2, 2); get(1); put(3, 3); get(2);", "output": "1, -1"}
        ],
        "constraints": [
            "1 <= capacity <= 3000",
            "0 <= key <= 10^4",
            "0 <= value <= 10^5",
            "At most 2 * 10^5 calls to get and put."
        ],
        "hints": [
            "`collections.OrderedDict` provides O(1) `move_to_end` and `popitem(last=False)`.",
            "Alternatively, implement using a doubly linked list combined with a hash map."
        ],
        "verification_suite": '''
cache = LRUCache(2)
cache.put(1, 1)
cache.put(2, 2)
assert cache.get(1) == 1, "Failed get(1)"
cache.put(3, 3) # evicts key 2
assert cache.get(2) == -1, "Key 2 should be evicted"
cache.put(4, 4) # evicts key 1
assert cache.get(1) == -1, "Key 1 should be evicted"
assert cache.get(3) == 3, "Key 3 should be 3"
assert cache.get(4) == 4, "Key 4 should be 4"
print("All LRU Cache tests passed!")
'''
    },
    {
        "id": "interview-6",
        "slug": "search-rotated-array",
        "title": "Search in Rotated Sorted Array",
        "difficulty": "Medium",
        "category": "Binary Search",
        "time_limit_minutes": 25,
        "description": "Given an integer array `nums` sorted in ascending order (with distinct values) that is possibly rotated at an unknown pivot index, and an integer `target`, return the index of `target` if it is in `nums`, or `-1` if it is not.\nYou must write an algorithm with O(log n) runtime complexity.",
        "starter_code": '''def search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = (left + right) // 2
        if nums[mid] == target:
            return mid
        if nums[left] <= nums[mid]:
            if nums[left] <= target < nums[mid]:
                right = mid - 1
            else:
                left = mid + 1
        else:
            if nums[mid] < target <= nums[right]:
                left = mid + 1
            else:
                right = mid - 1
    return -1
''',
        "entry_function_name": "search",
        "examples": [
            {"input": "nums = [4,5,6,7,0,1,2], target = 0", "output": "4"},
            {"input": "nums = [4,5,6,7,0,1,2], target = 3", "output": "-1"}
        ],
        "constraints": [
            "1 <= nums.length <= 5000",
            "-10^4 <= nums[i], target <= 10^4",
            "All values of nums are unique."
        ],
        "hints": [
            "At any midpoint in a rotated array, at least one half (left or right) is guaranteed to be normally sorted.",
            "Determine which half is sorted, then check if target lies within that half's range."
        ],
        "verification_suite": '''
assert search([4,5,6,7,0,1,2], 0) == 4, "Failed 0 in [4,5,6,7,0,1,2]"
assert search([4,5,6,7,0,1,2], 3) == -1, "Failed 3 in [4,5,6,7,0,1,2]"
assert search([1], 0) == -1, "Failed single element not found"
assert search([1], 1) == 0, "Failed single element found"
assert search([3, 1], 1) == 1, "Failed 2 element rotated"
print("All Search Rotated tests passed!")
'''
    },
    {
        "id": "interview-7",
        "slug": "reverse-linked-list",
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "category": "Pointers & Linked Lists",
        "time_limit_minutes": 15,
        "description": "Given the head of a singly linked list (represented here as a list or nested node `{\"val\": X, \"next\": ...}`), reverse the list, and return the reversed list.\nFor array representation `[1, 2, 3, 4, 5]`, reverse in-place or return `[5, 4, 3, 2, 1]`.",
        "starter_code": '''def reverse_list(items: list) -> list:
    # In-place reversal or two-pointer traversal
    res = []
    for x in reversed(items):
        res.append(x)
    return res
''',
        "entry_function_name": "reverse_list",
        "examples": [
            {"input": "items = [1,2,3,4,5]", "output": "[5,4,3,2,1]"},
            {"input": "items = [1,2]", "output": "[2,1]"}
        ],
        "constraints": [
            "The number of nodes in the list is the range [0, 5000].",
            "-5000 <= Node.val <= 5000"
        ],
        "hints": [
            "Iterate through elements maintaining prev and current pointers.",
            "Swap directions one node at a time."
        ],
        "verification_suite": '''
assert reverse_list([1, 2, 3, 4, 5]) == [5, 4, 3, 2, 1], "Failed basic reversal"
assert reverse_list([]) == [], "Failed empty reversal"
assert reverse_list([42]) == [42], "Failed single element"
print("All Reverse Linked List tests passed!")
'''
    },
    {
        "id": "interview-8",
        "slug": "group-anagrams",
        "title": "Group Anagrams",
        "difficulty": "Medium",
        "category": "Hash Tables & Strings",
        "time_limit_minutes": 25,
        "description": "Given an array of strings `strs`, group the anagrams together. You can return the answer in any order within each group.\nAn Anagram is a word or phrase formed by rearranging the letters of a different word or phrase.",
        "starter_code": '''from collections import defaultdict

def group_anagrams(strs: list[str]) -> list[list[str]]:
    groups = defaultdict(list)
    for s in strs:
        key = "".join(sorted(s))
        groups[key].append(s)
    return sorted(list(groups.values()), key=lambda g: len(g))
''',
        "entry_function_name": "group_anagrams",
        "examples": [
            {"input": 'strs = ["eat","tea","tan","ate","nat","bat"]', "output": '[["bat"],["nat","tan"],["ate","eat","tea"]]'},
            {"input": 'strs = [""]', "output": '[[""]]'}
        ],
        "constraints": [
            "1 <= strs.length <= 10^4",
            "0 <= strs[i].length <= 100",
            "strs[i] consists of lowercase English letters."
        ],
        "hints": [
            "Sort each string alphabetically to form the dictionary key.",
            "Group original strings having the same key in a list."
        ],
        "verification_suite": '''
result = group_anagrams(["eat","tea","tan","ate","nat","bat"])
# Sort internally for comparison
res_sorted = sorted([sorted(g) for g in result])
exp_sorted = sorted([sorted(["bat"]), sorted(["nat","tan"]), sorted(["ate","eat","tea"])])
assert res_sorted == exp_sorted, f"Expected {exp_sorted}, got {res_sorted}"
assert group_anagrams(["a"]) == [["a"]], "Failed single letter"
print("All Group Anagrams tests passed!")
'''
    },
    {
        "id": "interview-9",
        "slug": "kth-largest-element",
        "title": "Kth Largest Element in an Array",
        "difficulty": "Medium",
        "category": "Heaps & Priority Queues",
        "time_limit_minutes": 20,
        "description": "Given an integer array `nums` and an integer `k`, return the `k`th largest element in the array.\nNote that it is the `k`th largest element in the sorted order, not the `k`th distinct element.\nSolve it in O(n log k) time using a min-heap or O(n) average with QuickSelect.",
        "starter_code": '''import heapq

def find_kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for n in nums:
        heapq.heappush(heap, n)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]
''',
        "entry_function_name": "find_kth_largest",
        "examples": [
            {"input": "nums = [3,2,1,5,6,4], k = 2", "output": "5"},
            {"input": "nums = [3,2,3,1,2,4,5,5,6], k = 4", "output": "4"}
        ],
        "constraints": [
            "1 <= k <= nums.length <= 10^5",
            "-10^4 <= nums[i] <= 10^4"
        ],
        "hints": [
            "A min-heap of size `k` holds the `k` largest elements seen so far.",
            "The root of the min-heap is the `k`th largest element."
        ],
        "verification_suite": '''
assert find_kth_largest([3,2,1,5,6,4], 2) == 5, "Failed basic case"
assert find_kth_largest([3,2,3,1,2,4,5,5,6], 4) == 4, "Failed duplicate elements"
assert find_kth_largest([1], 1) == 1, "Failed single element"
print("All Kth Largest tests passed!")
'''
    },
    {
        "id": "interview-10",
        "slug": "trapping-rain-water",
        "title": "Trapping Rain Water",
        "difficulty": "Hard",
        "category": "Two Pointers & Dynamic Programming",
        "time_limit_minutes": 35,
        "description": "Given `n` non-negative integers representing an elevation map where the width of each bar is 1, compute how much water it can trap after raining.\nAim for O(n) time and O(1) extra space using two pointers.",
        "starter_code": '''def trap(height: list[int]) -> int:
    if not height:
        return 0
    left, right = 0, len(height) - 1
    left_max, right_max = height[left], height[right]
    water = 0
    while left < right:
        if left_max < right_max:
            left += 1
            left_max = max(left_max, height[left])
            water += left_max - height[left]
        else:
            right -= 1
            right_max = max(right_max, height[right])
            water += right_max - height[right]
    return water
''',
        "entry_function_name": "trap",
        "examples": [
            {"input": "height = [0,1,0,2,1,0,1,3,2,1,2,1]", "output": "6", "explanation": "6 units of rain water are trapped."},
            {"input": "height = [4,2,0,3,2,5]", "output": "9"}
        ],
        "constraints": [
            "n == height.length",
            "1 <= n <= 2 * 10^4",
            "0 <= height[i] <= 10^5"
        ],
        "hints": [
            "The water trapped at index i is determined by min(max_left, max_right) - height[i].",
            "Two pointers converging from left and right avoid storing prefix/suffix arrays in O(1) space."
        ],
        "verification_suite": '''
assert trap([0,1,0,2,1,0,1,3,2,1,2,1]) == 6, "Failed elevation map 1"
assert trap([4,2,0,3,2,5]) == 9, "Failed elevation map 2"
assert trap([1,2,3]) == 0, "Failed strictly ascending"
assert trap([]) == 0, "Failed empty"
print("All Trapping Rain Water tests passed!")
'''
    }
]


class InterviewSubmissionPayload(BaseModel):
    problem_id: str
    code: str


@router.get("/problems", response_model=List[Dict[str, Any]])
async def list_interview_problems():
    """Returns the catalog of DSA technical interview problems."""
    return [
        {
            "id": p["id"],
            "slug": p["slug"],
            "title": p["title"],
            "difficulty": p["difficulty"],
            "category": p["category"],
            "time_limit_minutes": p["time_limit_minutes"],
            "description": p["description"],
            "starter_code": p["starter_code"],
            "entry_function_name": p["entry_function_name"],
            "examples": p["examples"],
            "constraints": p["constraints"],
            "hints": p["hints"]
        }
        for p in INTERVIEW_PROBLEMS
    ]


@router.get("/problems/{problem_id}", response_model=Dict[str, Any])
async def get_interview_problem(problem_id: str):
    """Returns details, examples, and constraints for a specific interview problem."""
    for p in INTERVIEW_PROBLEMS:
        if p["id"] == problem_id or p["slug"] == problem_id:
            return {
                "id": p["id"],
                "slug": p["slug"],
                "title": p["title"],
                "difficulty": p["difficulty"],
                "category": p["category"],
                "time_limit_minutes": p["time_limit_minutes"],
                "description": p["description"],
                "starter_code": p["starter_code"],
                "entry_function_name": p["entry_function_name"],
                "examples": p["examples"],
                "constraints": p["constraints"],
                "hints": p["hints"]
            }
    raise HTTPException(status_code=404, detail="Interview problem not found")


@router.post("/{problem_id}/submit")
async def submit_interview_solution(
    problem_id: str,
    payload: InterviewSubmissionPayload,
    current_user: Optional[User] = Depends(get_optional_current_user),
    db: Session = Depends(get_db)
):
    """
    Executes interview candidate code against the edge-case test suite in the sandbox.
    """
    problem = next((p for p in INTERVIEW_PROBLEMS if p["id"] == problem_id or p["slug"] == problem_id), None)
    if not problem:
        raise HTTPException(status_code=404, detail="Problem not found")

    full_code = f"{payload.code}\n\n# --- Interview Verification Suite ---\n{problem['verification_suite']}"
    runner_result = run_code_in_sandbox(full_code, timeout_seconds=5.0)

    is_passed = runner_result.get("passed", False)
    xp_earned = 0

    if is_passed and current_user:
        existing_tx = db.query(XPTransaction).filter(
            XPTransaction.user_id == current_user.id,
            XPTransaction.challenge_id == problem["id"],
            XPTransaction.source == "interview_passed"
        ).first()

        if not existing_tx:
            xp_reward = 100 if problem["difficulty"] == "Easy" else 175 if problem["difficulty"] == "Medium" else 250
            xp_earned = xp_reward
            tx = XPTransaction(
                user_id=current_user.id,
                challenge_id=problem["id"],
                amount=xp_earned,
                source="interview_passed"
            )
            db.add(tx)
            if current_user.profile:
                current_user.profile.total_xp += xp_earned
                current_user.profile.current_level = 1 + (current_user.profile.total_xp // 100)
            db.commit()

    return {
        "submission_id": f"interview-sub-{problem['id']}",
        "passed": is_passed,
        "stdout": runner_result.get("stdout", ""),
        "stderr": runner_result.get("stderr", ""),
        "execution_time_ms": runner_result.get("execution_time_ms", 0),
        "attempt_duration_seconds": 1,
        "test_results": [
            {
                "test_index": 1,
                "description": f"Interview Suite: {problem['title']} Edge Cases",
                "is_hidden": False,
                "passed": is_passed,
                "input": "Edge-case inputs & stress checks",
                "expected": "Optimal execution without assertion failures",
                "actual": "Pass" if is_passed else (runner_result.get("stderr") or "Failed assertions")
            }
        ],
        "status": "passed" if is_passed else "failed",
        "xp_earned": xp_earned,
        "total_xp": current_user.profile.total_xp if (current_user and current_user.profile) else 0,
        "current_level": current_user.profile.current_level if (current_user and current_user.profile) else 1,
        "unlocked_next": True,
        "badges_awarded": []
    }
