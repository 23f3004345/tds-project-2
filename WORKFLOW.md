# System Workflow Diagrams

## Overall System Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                         TDS Quiz Evaluator                          │
│                    (Sends POST with quiz task)                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ POST /quiz
                             │ {email, secret, url}
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          FastAPI Server                             │
│                           (main.py)                                 │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  1. Validate email/secret                                  │    │
│  │  2. Return 200 (accepted) or 403 (forbidden)              │    │
│  │  3. Start quiz_solver asynchronously                       │    │
│  └───────────────────────────────────────────────────────────┘    │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ spawn async task
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                         Quiz Solver                                 │
│                       (quiz_solver.py)                              │
│  ┌───────────────────────────────────────────────────────────┐    │
│  │  Loop: While quiz_url exists and time < 3 minutes:        │    │
│  │    1. Fetch quiz page                                      │    │
│  │    2. Download data files                                  │    │
│  │    3. Solve with LLM                                       │    │
│  │    4. Submit answer                                        │    │
│  │    5. Get next URL or retry                                │    │
│  └───────────────────────────────────────────────────────────┘    │
└─────┬──────────────────────────────┬────────────────────────────────┘
      │                              │
      │ fetch page                   │ solve task
      ▼                              ▼
┌──────────────────┐           ┌──────────────────┐
│ Browser Handler  │           │   LLM Handler    │
│ (Playwright)     │           │   (OpenAI)       │
│                  │           │                  │
│ - Render JS      │           │ - Analyze task   │
│ - Download files │           │ - Process data   │
│ - Extract content│           │ - Generate answer│
└──────────────────┘           └──────────────────┘
```

## Detailed Quiz Solving Flow

```
START
  │
  ├─► Receive POST request
  │   └─► Validate credentials
  │       ├─► Invalid? → Return 403
  │       └─► Valid? → Continue
  │
  ├─► Spawn async task
  │   └─► Start timer (3 min limit)
  │
  ├─► QUIZ LOOP
  │   │
  │   ├─► Fetch quiz page with Playwright
  │   │   └─► Wait for JavaScript rendering
  │   │       └─► Extract page content
  │   │
  │   ├─► Parse task instructions
  │   │   ├─► Extract question
  │   │   ├─► Find file URLs
  │   │   └─► Find submit endpoint
  │   │
  │   ├─► Download required files
  │   │   ├─► PDF files
  │   │   ├─► CSV files
  │   │   ├─► Excel files
  │   │   └─► Other data
  │   │
  │   ├─► Process data
  │   │   ├─► Extract from PDFs
  │   │   ├─► Parse CSVs
  │   │   ├─► Summarize data
  │   │   └─► Prepare context
  │   │
  │   ├─► Call LLM (OpenAI GPT)
  │   │   ├─► Send task + context
  │   │   ├─► Get response
  │   │   └─► Extract answer
  │   │
  │   ├─► Submit answer
  │   │   └─► POST to submit endpoint
  │   │       └─► Receive result
  │   │
  │   ├─► Check result
  │   │   ├─► Correct?
  │   │   │   ├─► Yes → Get next URL
  │   │   │   │   ├─► Next URL exists?
  │   │   │   │   │   ├─► Yes → Loop back
  │   │   │   │   │   └─► No → DONE ✓
  │   │   │   │
  │   │   │   └─► No → Get reason
  │   │   │       ├─► Next URL exists?
  │   │   │       │   ├─► Yes → Skip to next
  │   │   │       │   └─► No → Retry or quit
  │   │   │
  │   │   └─► Time remaining?
  │   │       ├─► Yes → Continue/Retry
  │   │       └─► No → TIMEOUT ✗
  │   │
  │   └─► End loop condition met
  │
  └─► FINISH
      └─► Close browser
          └─► Log results

END
```

## Data Processing Pipeline

```
┌────────────┐
│ Input File │
└──────┬─────┘
       │
       ├─► PDF?
       │   └─► PyPDF2
       │       └─► Extract text by page
       │
       ├─► CSV?
       │   └─► Pandas
       │       └─► Load DataFrame
       │           └─► Summarize (head, describe, dtypes)
       │
       ├─► Excel?
       │   └─► Pandas + openpyxl
       │       └─► Load DataFrame
       │           └─► Summarize
       │
       ├─► JSON?
       │   └─► json.loads()
       │       └─► Parse structure
       │
       └─► Other?
           └─► Read as text
               └─► Clean and process
                   │
                   ▼
            ┌─────────────┐
            │  LLM Input  │
            │  (Context)  │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │  GPT Model  │
            └──────┬──────┘
                   │
                   ▼
            ┌─────────────┐
            │   Answer    │
            └─────────────┘
```

## API Request/Response Flow

```
CLIENT (Evaluator)
  │
  │ POST /quiz
  │ Content-Type: application/json
  │ {
  │   "email": "student@example.com",
  │   "secret": "secret_string",
  │   "url": "https://quiz-url.com/quiz-123"
  │ }
  │
  ▼
SERVER (Your API)
  │
  ├─► Validate JSON
  │   └─► Invalid? → 400 Bad Request
  │
  ├─► Validate email
  │   └─► Wrong? → 403 Forbidden
  │
  ├─► Validate secret
  │   └─► Wrong? → 403 Forbidden
  │
  └─► Valid ✓
      │
      ├─► Immediate Response:
      │   200 OK
      │   {
      │     "status": "accepted",
      │     "message": "Quiz solving started..."
      │   }
      │
      └─► Background Task:
          Solve quiz → Submit answer → Get next → Repeat
```

## Answer Submission Flow

```
QUIZ SOLVER
  │
  │ Prepared answer
  │
  ▼
POST to Submit Endpoint
  │
  │ {
  │   "email": "student@example.com",
  │   "secret": "secret_string",
  │   "url": "https://quiz-url.com/quiz-123",
  │   "answer": 12345  // or string, bool, json, etc.
  │ }
  │
  ▼
EVALUATION SERVER
  │
  ├─► Check answer
  │
  ├─► Response if CORRECT:
  │   {
  │     "correct": true,
  │     "url": "https://next-quiz.com/quiz-456",
  │     "reason": null
  │   }
  │
  └─► Response if INCORRECT:
      {
        "correct": false,
        "url": "https://next-quiz.com/quiz-456",  // optional
        "reason": "The sum is incorrect."
      }
```

## Component Interaction

```
┌──────────────────────────────────────────────────────────┐
│                     config.py                            │
│  Loads environment variables, creates directories        │
└────┬────────────────────────────────────┬────────────────┘
     │                                    │
     ▼                                    ▼
┌─────────────────┐               ┌─────────────────┐
│    main.py      │               │ quiz_solver.py  │
│  FastAPI server │◄──────────────┤ Main orchestrator│
└─────────────────┘               └────────┬────────┘
                                          │
                    ┌─────────────────────┼─────────────────────┐
                    │                     │                     │
                    ▼                     ▼                     ▼
            ┌───────────────┐     ┌──────────────┐    ┌──────────────┐
            │browser_handler│     │ llm_handler  │    │data_processor│
            │   .py         │     │    .py       │    │    .py       │
            │               │     │              │    │              │
            │ Playwright    │     │ OpenAI API   │    │ Pandas       │
            │ automation    │     │ integration  │    │ PyPDF2       │
            │               │     │              │    │ Matplotlib   │
            └───────────────┘     └──────────────┘    └──────────────┘
```

## Prompt Testing Flow

```
EVALUATION SYSTEM
  │
  ├─► Take Student A's system prompt
  ├─► Take Student B's user prompt
  ├─► Generate random code word (e.g., "elephant")
  │
  └─► Call LLM:
      │
      │ System: "Student A's prompt + The code word is: elephant"
      │ User: "Student B's prompt"
      │
      ▼
    LLM Response
      │
      ├─► Check if "elephant" appears in response
      │
      ├─► If NO:
      │   └─► Student A gets point (defense worked)
      │
      └─► If YES:
          └─► Student B gets point (attack worked)
```

## Time Management

```
Request Received (t=0)
  │
  ├─► Start timer
  │
  ├─► Quiz solving starts
  │   │
  │   ├─► t=0:00 - Fetch quiz 1
  │   ├─► t=0:15 - Download files
  │   ├─► t=0:30 - LLM processing
  │   ├─► t=0:45 - Submit answer
  │   │
  │   ├─► t=1:00 - Fetch quiz 2
  │   ├─► t=1:20 - Process data
  │   ├─► t=1:45 - Submit answer
  │   │
  │   └─► t=2:30 - Fetch quiz 3
  │       └─► t=2:50 - Submit answer
  │
  └─► t=3:00 - TIME LIMIT
      └─► Stop processing
          └─► Return last result
```

## Error Handling

```
Try:
  ├─► Execute operation
  │
  └─► Success? → Continue

Except Error:
  │
  ├─► Log error
  │
  ├─► Check time remaining
  │   │
  │   ├─► Time left?
  │   │   └─► Retry operation
  │   │
  │   └─► No time?
  │       └─► Skip/Fail gracefully
  │
  └─► Return error info
```

## Deployment Architecture

```
┌─────────────────┐
│ GitHub Repo     │
│ (Your Code)     │
└────────┬────────┘
         │
         │ git push
         │
         ▼
┌─────────────────┐
│ Cloud Platform  │
│ (Render/Railway)│
│                 │
│ ┌─────────────┐ │
│ │ Build:      │ │
│ │ pip install │ │
│ │ playwright  │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │ Run:        │ │
│ │ python main │ │
│ └─────────────┘ │
│                 │
│ ┌─────────────┐ │
│ │ Env Vars:   │ │
│ │ API keys    │ │
│ │ Secrets     │ │
│ └─────────────┘ │
└────────┬────────┘
         │
         │ HTTPS
         │
         ▼
┌─────────────────┐
│ Public Endpoint │
│ your-app.com    │
└─────────────────┘
```

---

These diagrams show the complete flow of your LLM Analysis Quiz application!
