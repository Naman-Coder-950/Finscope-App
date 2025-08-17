# FinScope Backend (FastAPI + SQLite + Optional AI)

This backend is aligned with your Flutter screens:
- `login_screen.dart` → `/auth/register`, `/auth/login`
- `quiz_screen.dart` & `quiz_screen2.dart` → `/quiz?level=1|2`, `/quiz/submit?level=1|2`
- `chatbot_screen.dart` → `/chat` (proxies AI with safe fallback)
- `rewards_screen.dart` → `/rewards`, `/rewards/leaderboard`
- Fraud training (extra) → `/fraud/scenario`, `/fraud/answer`

## 1) Setup (one-time)

```bash
cd finscope-backend
python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

pip install -r requirements.txt
cp .env.example .env  # optionally put your OPENAI key
```

## 2) Run

```bash
uvicorn main:app --reload
# Open http://127.0.0.1:8000/docs
```

## 3) Seed sample quiz questions

```bash
python -m app.seed
```

## 4) Quick API calls (without Postman)

```bash
# Register
curl -X POST http://127.0.0.1:8000/auth/register -H "Content-Type: application/json" -d "{\"username\":\"test\", \"password\":\"123456\"}"

# Login
curl -X POST http://127.0.0.1:8000/auth/login -H "Content-Type: application/json" -d "{\"username\":\"test\", \"password\":\"123456\"}"
# Copy 'access_token' from output
TOKEN=PASTE_TOKEN_HERE

# Get questions
curl "http://127.0.0.1:8000/quiz?level=1"

# Submit quiz
curl -X POST "http://127.0.0.1:8000/quiz/submit?level=1" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"answers\":{\"1\":\"C\",\"2\":\"B\"}}"

# My rewards
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/rewards

# Leaderboard
curl http://127.0.0.1:8000/rewards/leaderboard

# Fraud scenario
curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:8000/fraud/scenario

# Fraud answer
curl -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" http://127.0.0.1:8000/fraud/answer -d "{\"id\":\"OTP123\", \"answer\":\"No\"}"

# AI Chat (fallback works even without OpenAI key)
curl -X POST http://127.0.0.1:8000/chat -H "Content-Type: application/json" -d "{\"message\":\"How to avoid OTP scams?\"}"
```

## 5) How Flutter can call APIs (example)

Add `http` in `pubspec.yaml`, then:

```dart
import 'dart:convert';
import 'package:http/http.dart' as http;

const baseUrl = 'http://127.0.0.1:8000'; // Android emulator: 10.0.2.2:8000

Future<String> login(String username, String password) async {
  final res = await http.post(
    Uri.parse('$baseUrl/auth/login'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'username': username, 'password': password}),
  );
  final data = jsonDecode(res.body);
  return data['access_token'];
}

Future<List<dynamic>> getQuiz(int level) async {
  final res = await http.get(Uri.parse('$baseUrl/quiz?level=$level'));
  return jsonDecode(res.body);
}

Future<Map<String, dynamic>> submitQuiz(String token, int level, Map<String, String> answers) async {
  final res = await http.post(
    Uri.parse('$baseUrl/quiz/submit?level=$level'),
    headers: {'Content-Type': 'application/json', 'Authorization': 'Bearer $token'},
    body: jsonEncode({'answers': answers}),
  );
  return jsonDecode(res.body);
}

Future<Map<String, dynamic>> myRewards(String token) async {
  final res = await http.get(
    Uri.parse('$baseUrl/rewards'),
    headers: {'Authorization': 'Bearer $token'},
  );
  return jsonDecode(res.body);
}

Future<Map<String, dynamic>> askAI(String message) async {
  final res = await http.post(
    Uri.parse('$baseUrl/chat'),
    headers: {'Content-Type': 'application/json'},
    body: jsonEncode({'message': message}),
  );
  return jsonDecode(res.body);
}
```

### Notes for Flutter emulator
- Android emulator cannot reach `localhost`. Use `10.0.2.2` instead of `127.0.0.1`.
- For a real device on the same Wi‑Fi, replace base URL with your computer’s local IP (e.g., `http://192.168.1.10:8000`).

## 6) Switch to MongoDB later (optional)
This project uses SQLite for simplicity. You can switch to MongoDB when needed.
