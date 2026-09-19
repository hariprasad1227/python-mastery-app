/**
 * Python Mastery - API Client
 * Connects frontend to the FastAPI backend with JWT authentication,
 * server-controlled execution, and attempt tracking.
 */

export function getApiBaseUrl(): string {
  if (typeof window !== "undefined") {
    const urlParams = new URLSearchParams(window.location.search);
    const queryApi = urlParams.get("api") || urlParams.get("apiUrl");
    if (queryApi) {
      const clean = queryApi.replace(/\/$/, "");
      localStorage.setItem("python_mastery_api_url", clean);
      return clean;
    }
    const stored = localStorage.getItem("python_mastery_api_url");
    if (stored) {
      return stored.replace(/\/$/, "");
    }
  }
  return process.env.NEXT_PUBLIC_API_URL || "/api";
}

const API_BASE_URL = getApiBaseUrl();

export interface TestResultItem {
  test_index: number;
  description: string;
  is_hidden: boolean;
  passed: boolean;
  input: any;
  expected: any;
  actual: any;
  error?: string;
}

export interface ExecuteResult {
  submission_id: string;
  passed: boolean;
  stdout: string;
  stderr: string;
  execution_time_ms: number;
  attempt_duration_seconds: number;
  test_results: TestResultItem[];
  status: string;
  xp_earned: number;
  total_xp: number;
  current_level: number;
  new_streak?: number;
  unlocked_next: boolean;
  badges_awarded: string[];
}

export interface UserProfile {
  id: string;
  username: string;
  display_name: string;
  total_xp: number;
  current_level: number;
  current_rank?: string;
  performance_score?: number;
  current_streak: number;
  longest_streak: number;
  badges: Array<{
    code: string;
    name: string;
    description: string;
    icon: string;
    xp_bonus: number;
    awarded: boolean;
  }>;
}

export interface LevelItem {
  level_number: number;
  title: string;
  description: string;
  topics_total: number;
  topics_completed: number;
  final_test_passed: boolean;
  final_test_score: number | null;
  final_test_id: string;
  xp_required: number;
  next_level_xp_required: number;
  user_xp: number;
  unlocked: boolean;
  completed: boolean;
  can_take_final_test: boolean;
}

export interface LevelDetailTopic {
  id: string;
  order_index: number;
  title: string;
  description: string;
  xp_reward: number;
  unlocked: boolean;
  exam_passed: boolean;
}

export interface LevelDetail {
  level_number: number;
  title: string;
  description: string;
  xp_required: number;
  next_level_xp_required: number;
  user_xp: number;
  unlocked: boolean;
  topics_total: number;
  topics_completed: number;
  final_test_passed: boolean;
  final_test_score: number | null;
  can_take_final_test: boolean;
  can_unlock_next: boolean;
  topics: LevelDetailTopic[];
}

export interface LevelFinalTestQuestion {
  id: string;
  order_index: number;
  question_type: "mcq" | "output_prediction" | "debugging" | "short_answer";
  question_text: string;
  code_snippet?: string;
  options: string[];
  points: number;
}

export interface LevelFinalTest {
  test_id: string;
  level_number: number;
  title: string;
  description: string;
  time_limit_minutes: number;
  pass_percentage: number;
  xp_reward: number;
  total_questions: number;
  questions: LevelFinalTestQuestion[];
  attempts_count: number;
  best_percentage: number | null;
  is_passed: boolean;
}

export interface QuestionEvaluation {
  question_id: string;
  question_type: string;
  question_text: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  points_awarded: number;
  max_points: number;
  explanation?: string;
}

export interface LevelTestSubmitResult {
  attempt_id: string;
  test_id: string;
  level_number: number;
  score: number;
  max_score: number;
  percentage: number;
  pass_percentage: number;
  passed: boolean;
  xp_awarded: number;
  total_xp: number;
  unlocked_next_level: boolean;
  next_level_number: number | null;
  current_rank: string;
  performance_score: number;
  rank_changed: boolean;
  change_type: string | null;
  results: QuestionEvaluation[];
}

export interface PeriodicTestItem {
  id: string;
  test_type: "weekly" | "monthly";
  period_number: number;
  week_or_month_number: number;
  title: string;
  description: string;
  time_limit_minutes: number;
  pass_percentage: number;
  xp_reward: number;
  attempts_count: number;
  best_score: number | null;
  passed: boolean;
}

export interface PeriodicTestDetail {
  id: string;
  test_type: "weekly" | "monthly";
  period_number: number;
  week_or_month_number: number;
  title: string;
  description: string;
  time_limit_minutes: number;
  pass_percentage: number;
  xp_reward: number;
  total_questions: number;
  questions: LevelFinalTestQuestion[];
}

export interface PeriodicTestSubmitResult {
  attempt_id: string;
  test_id: string;
  test_type: string;
  score: number;
  max_score: number;
  percentage: number;
  pass_percentage: number;
  passed: boolean;
  xp_awarded: number;
  current_rank: string;
  performance_score: number;
  rank_changed: boolean;
  change_type: string | null;
  results: QuestionEvaluation[];
}

export interface PerformanceComponents {
  topic_exam_avg: number;
  coding_performance: number;
  weekly_test_avg: number;
  monthly_test_avg: number;
  consistency_score: number;
  performance_score: number;
}

export interface PromotionCriterion {
  name: string;
  target: number;
  current: number;
  met: boolean;
}

export interface RankProfile {
  current_rank: "GOLD" | "PLATINUM" | "DIAMOND" | "MASTER";
  performance_score: number;
  components: PerformanceComponents;
  consecutive_low_count: number;
  next_rank: string | null;
  promotion_criteria: PromotionCriterion[];
  total_xp: number;
  current_level: number;
}

export interface RankHistoryItem {
  id: string;
  old_rank: string;
  new_rank: string;
  performance_score: number;
  reason: string;
  changed_at: string;
}

export interface XPHistoryItem {
  id: string;
  amount: number;
  source: string;
  source_type: string;
  source_id?: string;
  transaction_key?: string;
  created_at: string;
}

export interface Challenge {
  id: string;
  slug: string;
  title: string;
  instructions: string;
  starter_code: string;
  entry_function_name?: string;
  xp_reward: number;
  status: "locked" | "available" | "in_progress" | "exam_available" | "passed" | "completed";
  hints: string[];
}

export interface TopicUnlockStatus {
  topic_id: string;
  topic_title: string;
  status: "locked" | "available" | "in_progress" | "exam_available" | "passed" | "completed";
  is_unlocked: boolean;
  lesson_completed: boolean;
  practice_completed: boolean;
  exam_passed: boolean;
  prerequisite_exam_id?: string | null;
  prerequisite_topic_title?: string | null;
  prerequisite_passed?: boolean;
}

export interface ExamQuestionItem {
  id: string;
  question_type: "mcq" | "output_prediction" | "debugging" | "short_answer";
  prompt: string;
  code_snippet?: string;
  options: string[];
  points: number;
  order_index: number;
}

export interface TopicExam {
  id: string;
  topic_id: string;
  topic_title: string;
  title: string;
  description: string;
  passing_percentage: number;
  time_limit_minutes: number;
  total_questions: number;
  questions: ExamQuestionItem[];
}

export interface ExamAnswerResult {
  question_id: string;
  prompt: string;
  code_snippet?: string;
  user_answer: string;
  correct_answer: string;
  is_correct: boolean;
  explanation: string;
  points_earned: number;
  max_points: number;
}

export interface ExamSubmitResult {
  attempt_id: string;
  exam_id: string;
  topic_id: string;
  score: number;
  total_points: number;
  percentage: number;
  passing_percentage: number;
  passed: boolean;
  next_unlocked_topic_id?: string | null;
  attempt_number: number;
  xp_awarded: number;
  results: ExamAnswerResult[];
}

export interface ExamAttemptSummary {
  attempt_id: string;
  attempt_number: number;
  score: number;
  total_points: number;
  percentage: number;
  passed: boolean;
  created_at: string;
}

export interface Module {
  id: string;
  slug: string;
  title: string;
  description: string;
  level_number: number;
  order_index: number;
  is_locked: boolean;
  challenges: Challenge[];
}

export interface ChallengeDetail {
  id: string;
  slug: string;
  title: string;
  difficulty: string;
  level_number: number;
  instructions: string;
  starter_code: string;
  entry_function_name?: string;
  xp_reward: number;
  time_limit_seconds: number;
  test_cases: Array<{
    test_index: number;
    description: string;
    input: any;
    expected: any;
    is_hidden: boolean;
  }>;
  hints: string[];
  lesson?: {
    track_number: number;
    track_title: string;
    concept_headline: string;
    theory_overview: string;
    core_concepts: Array<{
      name: string;
      explanation: string;
      example_code: string;
    }>;
    common_pitfalls: string[];
  };
}

export interface TrackLesson {
  track_number: number;
  title: string;
  subtitle: string;
  reading_time_minutes: number;
  overview: string;
  core_concepts: Array<{
    name: string;
    explanation: string;
    example_code: string;
  }>;
  common_pitfalls: string[];
}

export interface SyntaxPart {
  part: string;
  meaning: string;
}

export interface LineExplanation {
  line: string;
  explanation: string;
}

export interface LessonExample {
  title: string;
  code: string;
  expected_output: string;
  line_by_line: LineExplanation[];
}

export interface CommonMistake {
  description: string;
  incorrect_code: string;
  correct_code: string;
  why_it_fails: string;
}

export interface Subtopic {
  id: string;
  title: string;
  order: number;
  explanation: string;
  analogy?: string;
  syntax?: {
    code: string;
    breakdown: SyntaxPart[];
  };
  examples: LessonExample[];
  common_mistakes: CommonMistake[];
}

export interface QuizQuestion {
  id: string;
  question: string;
  options: string[];
  correct_index?: number;
  explanation?: string;
}

export interface StructuredLesson {
  id: string;
  challenge_id: string;
  level_number: number;
  track_number: number;
  track_title: string;
  title: string;
  introduction: string;
  learning_objectives: string[];
  subtopics: Subtopic[];
  quiz: QuizQuestion[];
  xp_reward: number;
}

export interface QuizResultItem {
  question_id: string;
  question: string;
  user_answer: number;
  correct_answer: number;
  is_correct: boolean;
  explanation: string;
}

export interface QuizEvaluationResponse {
  lesson_id: string;
  total: number;
  correct: number;
  score_percent: number;
  passed: boolean;
  xp_awarded: number;
  results: QuizResultItem[];
}

export interface StructuredLessonSummary {
  id: string;
  challenge_id: string;
  level_number: number;
  track_number: number;
  track_title: string;
  title: string;
  subtopics_count: number;
  quiz_questions_count: number;
  xp_reward: number;
}

export interface ProjectItem {
  id: string;
  slug: string;
  title: string;
  difficulty: "beginner" | "intermediate" | "advanced";
  description: string;
  tech_stack: string[];
  estimated_hours: number;
  status: "locked" | "available" | "completed";
  xp_reward: number;
  requirements: string[];
  starter_code: string;
}

export interface InterviewProblem {
  id: string;
  slug: string;
  title: string;
  difficulty: "Easy" | "Medium" | "Hard";
  category: string;
  time_limit_minutes: number;
  description: string;
  starter_code: string;
  entry_function_name: string;
  examples: Array<{
    input: string;
    output: string;
    explanation?: string;
  }>;
  constraints: string[];
  hints: string[];
  status?: "unsolved" | "solved";
}

export interface MentorHintResponse {
  hint_level: number;
  hint: string;
  socratic_question: string;
  encouragement: string;
}

export interface ChatMessage {
  role: "user" | "assistant" | "system";
  content: string;
}

export interface MentorChatRequest {
  messages: ChatMessage[];
  current_topic?: string;
  code_context?: string;
  error_context?: string;
  language?: "auto" | "en" | "te";
}

export interface MentorChatResponse {
  reply: string;
  suggestions: string[];
  code_snippet?: string;
}

function getAuthHeaders(): HeadersInit {
  const headers: HeadersInit = { "Content-Type": "application/json" };
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("mastery_token");
    if (token) {
      headers["Authorization"] = `Bearer ${token}`;
    }
  }
  return headers;
}

export const api = {
  setToken(token: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("mastery_token", token);
    }
  },

  getToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("mastery_token");
    }
    return null;
  },

  clearToken() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("mastery_token");
    }
  },

  setApiUrl(url: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("python_mastery_api_url", url.replace(/\/$/, ""));
    }
  },

  getApiUrl(): string {
    return getApiBaseUrl();
  },

  async signup(data: { email: string; password: string; username: string; display_name?: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/signup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Signup failed");
    }
    const result = await res.json();
    this.setToken(result.access_token);
    return result;
  },

  async login(data: { email: string; password: string }) {
    const res = await fetch(`${API_BASE_URL}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data)
    });
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Login failed");
    }
    const result = await res.json();
    this.setToken(result.access_token);
    return result;
  },

  async getMe() {
    const res = await fetch(`${API_BASE_URL}/auth/me`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Not authenticated");
    return res.json();
  },

  async getProfile(): Promise<UserProfile> {
    const res = await fetch(`${API_BASE_URL}/progression/profile`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch profile");
    return res.json();
  },

  async getCurriculum(): Promise<Module[]> {
    const res = await fetch(`${API_BASE_URL}/progression/curriculum`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch curriculum");
    return res.json();
  },

  async executeCode(payload: {
    challenge_id: string;
    code: string;
    attempt_started_at?: number;
  }): Promise<ExecuteResult> {
    const res = await fetch(`${API_BASE_URL}/runner/execute`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Execution request failed" }));
      throw new Error(err.detail || "Execution request failed");
    }
    return res.json();
  },

  async getSubmissions(challengeId: string) {
    const res = await fetch(`${API_BASE_URL}/progression/challenges/${challengeId}/submissions`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return [];
    return res.json();
  },

  async getMentorHint(payload: {
    challenge_title: string;
    challenge_instructions: string;
    learner_code: string;
    error_message?: string;
    hint_level: number;
  }): Promise<MentorHintResponse> {
    const res = await fetch(`${API_BASE_URL}/mentor/hint`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to get mentor hint");
    return res.json();
  },

  async chatWithMentor(payload: MentorChatRequest): Promise<MentorChatResponse> {
    const res = await fetch(`${API_BASE_URL}/mentor/chat`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify(payload)
    });
    if (!res.ok) throw new Error("Failed to communicate with AI Mentor");
    return res.json();
  },

  async getChallengeDetail(challengeId: string): Promise<ChallengeDetail> {
    const res = await fetch(`${API_BASE_URL}/progression/challenges/${challengeId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const errData = await res.json().catch(() => null);
      const message = typeof errData?.detail === "string" ? errData.detail : errData?.detail?.message || `Failed to fetch challenge details for ${challengeId}`;
      const err = new Error(message);
      (err as any).status = res.status;
      (err as any).lockData = typeof errData?.detail === "object" ? errData.detail : errData;
      throw err;
    }
    return res.json();
  },

  async getProjects(): Promise<ProjectItem[]> {
    const res = await fetch(`${API_BASE_URL}/projects`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      // Return default projects if backend endpoint is initializing
      return [
        {
          id: "proj-1",
          slug: "cli-task-manager",
          title: "CLI Task & Expense Tracker",
          difficulty: "beginner",
          description: "Build a persistent command-line task and expense manager supporting JSON serialization, priority tagging, and summary reporting.",
          tech_stack: ["Python 3.11", "JSON", "argparse / sys"],
          estimated_hours: 3,
          status: "available",
          xp_reward: 200,
          requirements: [
            "Add, list, update, and delete tasks/expenses with timestamps.",
            "Persist data safely to a JSON file with atomic write semantics.",
            "Calculate expense totals grouped by category (e.g. food, tech, bills)."
          ],
          starter_code: `import json\nfrom datetime import datetime\n\nclass TaskManager:\n    def __init__(self, storage_path="tasks.json"):\n        self.storage_path = storage_path\n        self.items = []\n\n    def add_item(self, title: str, category: str, amount: float = 0.0) -> dict:\n        # Implement item creation\n        pass\n`
        },
        {
          id: "proj-2",
          slug: "async-web-scraper",
          title: "Resilient Web Scraper & HTTP Client",
          difficulty: "intermediate",
          description: "Build a fault-tolerant web scraper and HTTP crawler with rate-limiting, exponential backoff, regex content extraction, and structured JSON export.",
          tech_stack: ["Python 3.11", "urllib / HTTP", "Regex", "Queue"],
          estimated_hours: 5,
          status: "available",
          xp_reward: 350,
          requirements: [
            "Implement exponential backoff retry logic (1s, 2s, 4s).",
            "Extract structured metadata (titles, links, timestamps) via regex.",
            "Enforce sliding-window rate limit of max 5 requests per second."
          ],
          starter_code: `import time\nimport re\n\nclass ResilientClient:\n    def __init__(self, max_retries: int = 3, rate_limit: int = 5):\n        self.max_retries = max_retries\n        self.rate_limit = rate_limit\n\n    def fetch_with_retry(self, url: str) -> str:\n        # Implement resilient fetch with retry\n        pass\n`
        },
        {
          id: "proj-3",
          slug: "fastapi-microservice",
          title: "RESTful Inventory Microservice",
          difficulty: "intermediate",
          description: "Develop a complete production REST API with Pydantic schemas, CRUD operations, query filtering, pagination, and error handlers.",
          tech_stack: ["FastAPI", "Pydantic", "SQLite", "SQLAlchemy"],
          estimated_hours: 6,
          status: "available",
          xp_reward: 450,
          requirements: [
            "Create schema models for Products, Categories, and Orders.",
            "Implement GET with pagination (?skip=0&limit=20) and category filter.",
            "Handle 404 and 422 validation errors with RFC-7807 compliant bodies."
          ],
          starter_code: `from typing import List, Optional\n\nclass InventoryService:\n    def __init__(self):\n        self.db = {}\n\n    def create_item(self, item_data: dict) -> dict:\n        # Implement item creation and validation\n        pass\n`
        },
        {
          id: "proj-4",
          slug: "etl-data-pipeline",
          title: "High-Throughput ETL Pipeline",
          difficulty: "advanced",
          description: "Architect an end-to-end data processing pipeline that ingests messy CSVs, validates records against schemas, cleans anomalies, and generates analytical summaries.",
          tech_stack: ["Python 3.11", "csv", "itertools", "statistics"],
          estimated_hours: 8,
          status: "available",
          xp_reward: 600,
          requirements: [
            "Stream massive CSV lines with memory-efficient generator processing.",
            "Filter corrupted rows, convert date formats, and deduplicate entries.",
            "Generate statistical aggregations: mean, median, IQR, and top percentiles."
          ],
          starter_code: `import csv\nimport io\n\nclass ETLPipeline:\n    def __init__(self, schema_rules: dict):\n        self.schema_rules = schema_rules\n\n    def process_stream(self, csv_stream) -> dict:\n        # Process generator stream and compute aggregates\n        pass\n`
        }
      ];
    }
    return res.json();
  },

  async getProjectDetail(id: string): Promise<ProjectItem> {
    const res = await fetch(`${API_BASE_URL}/projects/${id}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const all = await this.getProjects();
      const match = all.find((p) => p.id === id || p.slug === id);
      if (match) return match;
      throw new Error(`Project ${id} not found`);
    }
    return res.json();
  },

  async verifyProject(projectId: string, code: string): Promise<ExecuteResult> {
    const res = await fetch(`${API_BASE_URL}/projects/${projectId}/verify`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ project_id: projectId, code })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Project verification failed" }));
      throw new Error(err.detail || "Project verification failed");
    }
    return res.json();
  },

  async getInterviewProblems(): Promise<InterviewProblem[]> {
    const res = await fetch(`${API_BASE_URL}/interview/problems`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      // Fallback interview catalog
      return [
        {
          id: "interview-1",
          slug: "two-sum",
          title: "Two Sum",
          difficulty: "Easy",
          category: "Arrays & Hash Tables",
          time_limit_minutes: 20,
          description: "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice. Aim for O(n) time complexity.",
          starter_code: `def two_sum(nums: list[int], target: int) -> list[int]:\n    # Optimal O(n) solution using hash map\n    pass\n`,
          entry_function_name: "two_sum",
          examples: [
            { input: "nums = [2,7,11,15], target = 9", output: "[0, 1]", explanation: "nums[0] + nums[1] == 9, so return [0, 1]." },
            { input: "nums = [3,2,4], target = 6", output: "[1, 2]" },
            { input: "nums = [3,3], target = 6", output: "[0, 1]" }
          ],
          constraints: [
            "2 <= nums.length <= 10^4",
            "-10^9 <= nums[i] <= 10^9",
            "-10^9 <= target <= 10^9",
            "Only one valid answer exists."
          ],
          hints: [
            "Can we search for the complement (target - num) in O(1) time?",
            "Use a dictionary mapping value -> index as you iterate through the list."
          ]
        },
        {
          id: "interview-2",
          slug: "valid-parentheses",
          title: "Valid Parentheses",
          difficulty: "Easy",
          category: "Stack & Parsing",
          time_limit_minutes: 20,
          description: "Given a string `s` containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid.\n\nAn input string is valid if:\n1. Open brackets must be closed by the same type of brackets.\n2. Open brackets must be closed in the correct order.\n3. Every close bracket has a corresponding open bracket of the same type.",
          starter_code: `def is_valid(s: str) -> bool:\n    # Stack-based matching\n    pass\n`,
          entry_function_name: "is_valid",
          examples: [
            { input: 's = "()"', output: "True" },
            { input: 's = "()[]{}"', output: "True" },
            { input: 's = "(]"', output: "False" }
          ],
          constraints: [
            "1 <= s.length <= 10^4",
            "s consists of parentheses only '()[]{}'."
          ],
          hints: [
            "A Last-In, First-Out (LIFO) stack helps match the most recently opened bracket.",
            "If you see a closing bracket, the top of the stack must be its matching open bracket."
          ]
        },
        {
          id: "interview-3",
          slug: "longest-substring-no-repeat",
          title: "Longest Substring Without Repeating Characters",
          difficulty: "Medium",
          category: "Sliding Window",
          time_limit_minutes: 25,
          description: "Given a string `s`, find the length of the longest substring without duplicate characters. Aim for O(n) runtime using a sliding window technique.",
          starter_code: `def length_of_longest_substring(s: str) -> int:\n    # Sliding window approach\n    pass\n`,
          entry_function_name: "length_of_longest_substring",
          examples: [
            { input: 's = "abcabcbb"', output: "3", explanation: "The answer is 'abc', with the length of 3." },
            { input: 's = "bbbbb"', output: "1", explanation: "The answer is 'b', with the length of 1." },
            { input: 's = "pwwkew"', output: "3", explanation: "The answer is 'wke', with length 3." }
          ],
          constraints: [
            "0 <= s.length <= 5 * 10^4",
            "s consists of English letters, digits, symbols and spaces."
          ],
          hints: [
            "Maintain a window [left, right] and a hash map of last seen indices for each character.",
            "When encountering a duplicate, slide the left pointer right after the duplicate's last position."
          ]
        },
        {
          id: "interview-4",
          slug: "merge-intervals",
          title: "Merge Overlapping Intervals",
          difficulty: "Medium",
          category: "Sorting & Intervals",
          time_limit_minutes: 25,
          description: "Given an array of `intervals` where `intervals[i] = [start_i, end_i]`, merge all overlapping intervals, and return an array of the non-overlapping intervals that cover all the intervals in the input.",
          starter_code: `def merge_intervals(intervals: list[list[int]]) -> list[list[int]]:\n    # Sorting and merging\n    pass\n`,
          entry_function_name: "merge_intervals",
          examples: [
            { input: "intervals = [[1,3],[2,6],[8,10],[15,18]]", output: "[[1,6],[8,10],[15,18]]", explanation: "Since intervals [1,3] and [2,6] overlap, merge them into [1,6]." },
            { input: "intervals = [[1,4],[4,5]]", output: "[[1,5]]" }
          ],
          constraints: [
            "1 <= intervals.length <= 10^4",
            "intervals[i].length == 2",
            "0 <= start_i <= end_i <= 10^4"
          ],
          hints: [
            "First sort intervals by their start times: `intervals.sort(key=lambda x: x[0])`.",
            "Iterate through sorted intervals and compare current start with previous interval's end."
          ]
        },
        {
          id: "interview-5",
          slug: "lru-cache",
          title: "LRU Cache Implementation",
          difficulty: "Hard",
          category: "Design & Data Structures",
          time_limit_minutes: 30,
          description: "Design a data structure that follows the constraints of a Least Recently Used (LRU) cache.\n\nImplement the `LRUCache` class:\n- `__init__(capacity: int)`: Initialize with positive size `capacity`.\n- `get(key: int) -> int`: Return the value of `key` if it exists, otherwise return `-1`.\n- `put(key: int, value: int) -> None`: Update or insert key-value. When capacity is exceeded, evict the least recently used key.\nBoth `get` and `put` must run in O(1) average time complexity.",
          starter_code: `class LRUCache:\n    def __init__(self, capacity: int):\n        # Initialize LRU Cache\n        pass\n\n    def get(self, key: int) -> int:\n        pass\n\n    def put(self, key: int, value: int) -> None:\n        pass\n`,
          entry_function_name: "LRUCache",
          examples: [
            { input: "LRUCache(2); put(1, 1); put(2, 2); get(1); put(3, 3); get(2);", output: "[null, null, null, 1, null, -1]" }
          ],
          constraints: [
            "1 <= capacity <= 3000",
            "0 <= key <= 10^4",
            "0 <= value <= 10^5",
            "At most 2 * 10^5 calls to get and put."
          ],
          hints: [
            "An OrderedDict or a combination of a hash map with a doubly linked list allows O(1) lookup and O(1) node relocation.",
            "When getting or updating an element, move it to the most recently used end."
          ]
        }
      ];
    }
    return res.json();
  },

  async getInterviewProblemDetail(id: string): Promise<InterviewProblem> {
    const res = await fetch(`${API_BASE_URL}/interview/problems/${id}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const all = await this.getInterviewProblems();
      const match = all.find((p) => p.id === id || p.slug === id);
      if (match) return match;
      throw new Error(`Interview problem ${id} not found`);
    }
    return res.json();
  },

  async submitInterview(problemId: string, code: string): Promise<ExecuteResult> {
    const res = await fetch(`${API_BASE_URL}/interview/${problemId}/submit`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ problem_id: problemId, code })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Interview submission failed" }));
      throw new Error(err.detail || "Interview submission failed");
    }
    return res.json();
  },

  async getTrackLessons(): Promise<TrackLesson[]> {
    const res = await fetch(`${API_BASE_URL}/progression/lessons`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch track lessons");
    return res.json();
  },

  async getTrackLesson(trackNum: number): Promise<TrackLesson> {
    const res = await fetch(`${API_BASE_URL}/progression/lessons/${trackNum}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to fetch lesson for track ${trackNum}`);
    return res.json();
  },

  async getStructuredLessons(): Promise<StructuredLessonSummary[]> {
    const res = await fetch(`${API_BASE_URL}/progression/structured-lessons`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch structured lessons");
    return res.json();
  },

  async getStructuredLesson(lessonId: string): Promise<StructuredLesson> {
    const res = await fetch(`${API_BASE_URL}/progression/structured-lessons/${lessonId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to fetch structured lesson ${lessonId}`);
    return res.json();
  },

  async getStructuredLessonByChallenge(challengeId: string): Promise<StructuredLesson> {
    const res = await fetch(`${API_BASE_URL}/progression/structured-lessons/by-challenge/${challengeId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to fetch structured lesson for challenge ${challengeId}`);
    return res.json();
  },

  async submitLessonQuiz(lessonId: string, answers: Record<string, number>): Promise<QuizEvaluationResponse> {
    const res = await fetch(`${API_BASE_URL}/progression/structured-lessons/${lessonId}/quiz`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ answers })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Quiz evaluation failed" }));
      throw new Error(err.detail || "Quiz evaluation failed");
    }
    return res.json();
  },

  async getTopicUnlockStatus(topicId: string): Promise<TopicUnlockStatus> {
    const res = await fetch(`${API_BASE_URL}/progression/topics/${topicId}/unlock-status`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to check lock status for topic ${topicId}`);
    return res.json();
  },

  async completeTopicLesson(topicId: string): Promise<{ status: string; topic_status: string; lesson_completed: boolean; exam_id: string; message: string }> {
    const res = await fetch(`${API_BASE_URL}/progression/topics/${topicId}/complete-lesson`, {
      method: "POST",
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to mark lesson complete for ${topicId}`);
    return res.json();
  },

  async getTopicExam(topicId: string): Promise<TopicExam> {
    const res = await fetch(`${API_BASE_URL}/progression/topics/${topicId}/exam`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to fetch topic exam" }));
      throw new Error(err.detail || `Failed to fetch exam for topic ${topicId}`);
    }
    return res.json();
  },

  async submitTopicExam(examId: string, answers: Record<string, string>): Promise<ExamSubmitResult> {
    const res = await fetch(`${API_BASE_URL}/progression/exams/${examId}/submit`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ answers })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to submit exam" }));
      throw new Error(err.detail || "Failed to submit topic exam");
    }
    return res.json();
  },

  async getExamAttempts(examId: string): Promise<ExamAttemptSummary[]> {
    const res = await fetch(`${API_BASE_URL}/progression/exams/${examId}/attempts`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return [];
    return res.json();
  },

  async getLevels(): Promise<LevelItem[]> {
    const res = await fetch(`${API_BASE_URL}/progression/levels`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch levels");
    return res.json();
  },

  async getLevelDetails(levelNumber: number): Promise<LevelDetail> {
    const res = await fetch(`${API_BASE_URL}/progression/levels/${levelNumber}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error(`Failed to fetch details for level ${levelNumber}`);
    return res.json();
  },

  async getLevelFinalTest(levelNumber: number): Promise<LevelFinalTest> {
    const res = await fetch(`${API_BASE_URL}/progression/levels/${levelNumber}/final-test`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to fetch final test" }));
      throw new Error(err.detail || `Failed to fetch final test for level ${levelNumber}`);
    }
    return res.json();
  },

  async submitLevelFinalTest(levelNumber: number, answers: Record<string, string>): Promise<LevelTestSubmitResult> {
    const res = await fetch(`${API_BASE_URL}/progression/levels/${levelNumber}/final-test/submit`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ answers })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to submit level final test" }));
      throw new Error(err.detail || "Failed to submit level final test");
    }
    return res.json();
  },

  async getPeriodicTests(): Promise<PeriodicTestItem[]> {
    const res = await fetch(`${API_BASE_URL}/progression/tests/periodic`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch periodic tests");
    return res.json();
  },

  async getPeriodicTest(testId: string): Promise<PeriodicTestDetail> {
    const res = await fetch(`${API_BASE_URL}/progression/tests/periodic/${testId}`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to fetch periodic test" }));
      throw new Error(err.detail || `Failed to fetch periodic test ${testId}`);
    }
    return res.json();
  },

  async submitPeriodicTest(testId: string, answers: Record<string, string>): Promise<PeriodicTestSubmitResult> {
    const res = await fetch(`${API_BASE_URL}/progression/tests/periodic/${testId}/submit`, {
      method: "POST",
      headers: getAuthHeaders(),
      body: JSON.stringify({ answers })
    });
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: "Failed to submit periodic test" }));
      throw new Error(err.detail || "Failed to submit periodic test");
    }
    return res.json();
  },

  async getRankProfile(): Promise<RankProfile> {
    const res = await fetch(`${API_BASE_URL}/progression/profile/rank`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) throw new Error("Failed to fetch rank profile");
    return res.json();
  },

  async getRankHistory(): Promise<RankHistoryItem[]> {
    const res = await fetch(`${API_BASE_URL}/progression/profile/rank-history`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return [];
    return res.json();
  },

  async getXPHistory(): Promise<XPHistoryItem[]> {
    const res = await fetch(`${API_BASE_URL}/progression/profile/xp-history`, {
      headers: getAuthHeaders()
    });
    if (!res.ok) return [];
    return res.json();
  }
};
