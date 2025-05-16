from langchain_community.llms import Ollama
from agents.user_input_agent import classify_user_intent

# Initialize the model
llm = Ollama(model="mistral")

# List of troubleshooting keywords (you can expand this list if needed)
keywords = [
    "error", "bug", "issue", "crash", "fail", "doesn't work", "broken", "not responding", "freeze", "stuck",
    "how to", "can't", "unable to", "steps", "guide", "usage", "tutorial", "instructions", "configure", "settings", 
    "setup", "API", "endpoint", "token", "authentication", "headers", "request", "response", "payload", "webhook", 
    "callback", "401", "403", "500", "install", "setup", "environment", "dependencies", "package", "module", "pip", 
    "npm", "yarn", "docker", "container", "build", "compile", "traceback", "log", "output", "stacktrace", "console", 
    "debugger", "print", "trace", "breakpoint", "diagnose", "login", "logout", "password", "reset", "token", 
    "OAuth", "JWT", "permission", "access denied", "security", "session expired", "slow", "lag", "optimize", "latency", 
    "memory leak", "CPU usage", "RAM", "performance drop", "button not working", "layout broken", "style issue", 
    "not showing", "alignment", "responsive", "CSS", "HTML", "JS error", "upload", "download", "save", "export", 
    "import", "database", "query", "SQL", "no data", "missing file", "corrupted file", "file type", "timeout", 
    "server down", "DNS", "connection failed", "unreachable", "proxy", "VPN", "firewall", "ping", "no internet connection","Wi-Fi","app not working",
    "network issue", "connectivity", "sync", "syncing", "out of sync", "data loss", "backup", "restore",
    "recovery", "rollback", "undo", "redo", "version control", "git", "branch", "merge", "conflict", "commit", 
    "deployment", "integration", "connection timeout", "API failure", "gateway timeout", "service unavailable",
    "request timeout", "server error", "out of memory", "disk full", "memory overflow", "segmentation fault", 
    "stack overflow", "permission denied", "file not found", "data corruption", "sync error", "version mismatch", 
    "conflict resolution", "file transfer", "data loss prevention", "data synchronization", "proxy error", 
    "server crash", "data breach", "database corruption", "invalid input", "user authentication", "encryption", 
    "decryption", "SSL certificate", "firewall issue", "DNS resolution", "login failure", "API rate limit", 
    "session timeout", "user permissions", "multi-factor authentication", "auth token expired", "rate limiting", 
    "back-end failure", "front-end issue", "cross-origin resource sharing", "CORS", "session storage", "local storage", 
    "OAuth token", "authentication token", "JWT token", "403 forbidden", "404 not found", "505 HTTP version", 
    "500 internal server error", "502 bad gateway", "501 not implemented", "dependency conflict", "package not found", 
    "update failure", "rollback failed", "configuration error", "syntax error", "compilation error", "version upgrade", 
    "build failure", "test failure", "unit test failure", "integration test failure", "missing dependencies", 
    "incompatible dependencies", "runtime error", "undefined behavior", "race condition", "deadlock", "lock contention", 
    "threading error", "network latency", "slow query", "database lock", "database query timeout", "slow response", 
    "bug fix", "patch deployment", "hotfix", "memory leak detected", "high CPU usage", "CPU throttling", 
    "unresponsive UI", "slow rendering", "app crash", "force quit", "stack trace", "debugging", "trace logging", 
    "error logs", "recovery mode", "system restore", "data restore", "system backup", "unreachable host", 
    "connectivity loss", "server overload", "disk I/O error", "corrupted cache", "cache clearance", "file access denied", 
    "file system error", "mount error", "read-only file system", "write permission", "disk error", "storage full", 
    "upload failed", "download failed", "transfer interrupted", "connection reset", "reset connection", 
    "reconnect failed", "network congestion", "route failure", "port blocked", "router issue", "interface error", 
    "IP conflict", "DNS issue", "default gateway", "connection refused", "authentication failure", "user authentication failed", 
    "certificate error", "SSL handshake failed", "VPN connection failed", "remote desktop error", "SSH connection error", 
    "webhook failure", "callback failure", "data inconsistency", "data sync failed", "data replication error", 
    "file import failure", "data export failure", "module error", "package error", "unsupported format", 
    "non-responsive server", "no network", "Wi-Fi disconnect", "ping timeout", "socket error", "packet loss", 
    "router disconnect", "signal interference", "network configuration error", "adapter error", "app not responding", 
    "service outage", "backend issue", "frontend error", "UI bug", "app freeze", "app hangs", "app not loading", 
    "server timeout", "database timeout", "proxy connection failed", "user session expired", "session error", 
    "network dropout", "data inconsistency", "endpoint failure", "API connection refused", "authentication error", 
    "service crash", "service disruption", "host not found", "node failure", "cluster issue", "container crash", 
    "docker error", "deployment error", "container issue", "virtual machine error", "hypervisor issue", "cloud error", 
    "cloud outage", "cloud storage issue", "SaaS issue", "data integrity", "SQL injection", "XSS attack", 
    "file corruption", "data export error", "file permission error", "certificate expired", "SSL timeout", 
    "no response", "server deadlock", "server not responding", "query failure", "invalid query", "outdated version", 
    "failed request", "service unavailability", "configuration mismatch", "DNS failure", "TCP error", "UDP error"

]

# def suggest_basic_troubleshooting(issue: str) -> str:
#     # Check for relevant keywords in the issue
#     found_keywords = [kw for kw in keywords if kw in issue.lower()]
    
#     if not found_keywords:
#         return """
#         I see you're having an issue. Could you tell me a bit more about the specific problem you're facing? 
#         This will help me understand better and guide you more effectively. 😊
#         """
    
#     # Prepare a conversational troubleshooting response
#     response = f"""
#     I noticed you're having trouble with the following issue(s): {', '.join(found_keywords)}. Let's try to fix this together! 😊

#     Here are a few steps we can take:

#     1. **Check Your Internet Settings**: It sounds like you might have an app reporting 'no internet connection.' Ensure the app has access to your Wi-Fi and isn't restricted by any app-specific network settings.
    
#     2. **Restart the App and Router**: Sometimes, apps or routers can get 'stuck' and need a reset. Try restarting both the app and the router to resolve temporary issues.

#     3. **Clear App Cache**: Apps can get bogged down with cached data. Try clearing the app cache from your device’s settings and check if the issue persists.

#     4. **Check for Updates**: If your app is outdated, it might be unable to connect properly. Go ahead and check if there are any app or system updates pending.

#     5. **Reinstall the App**: If nothing seems to work, uninstall the app and reinstall it to ensure a fresh start.

#     If you’re still stuck, feel free to share more details about what you’ve tried, and I’ll guide you further! 💡
#     """
    
#     return response

def suggest_basic_troubleshooting(issue: str) -> str:
    found_keywords = [kw for kw in keywords if kw in issue.lower()]

    if not found_keywords:
        return ("""
I see you're facing some kind of issue, but I need a little more context to help you better.
Could you tell me more about what's happening or provide any error messages or symptoms you're seeing?
I'll guide you step by step to resolve the issue. 😊
""")

    response = f"""
It looks like you're facing an issue related to: {', '.join(found_keywords)}.

Let's try to troubleshoot this together! 😊

If it still doesn't work, let me know and I can guide you further!
"""
    return response
