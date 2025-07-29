# akamaisdk

**akamaisdk** is a lightweight Python SDK for interacting with [Akamai APIs](https://developer.akamai.com/) using EdgeGrid authentication.

## ✨ Features
- ✅ HMAC-signed Akamai EdgeGrid authentication via `EdgeAuth`
- ✅ Simple wrapper for Akamai App & API Protector endpoints
- ✅ Modular, easy to extend

## 📦 Installation
```bash
pip install akamaisdk
```

## 🔧 Setup
```python
from akamaisdk import EdgeAuth, get_policies

auth = EdgeAuth(
    client_token="YOUR_CLIENT_TOKEN",
    client_secret="YOUR_CLIENT_SECRET",
    access_token="YOUR_ACCESS_TOKEN",
    base_url="https://akab-xxxx.luna.akamaisdks.net"
)
```

## 🚀 Examples

### List App & API Protector Policies
```python
policies = get_policies(auth)
for policy in policies.get("policies", []):
    print(policy["policyId"], policy["policyName"])
```

### Get a Specific Policy
```python
policy_id = "12345"
policy = get_policy_details(auth, policy_id)
print(policy)
```

## 🧱 SDK Architecture

```text
akamaisdk/
├── __init__.py         # Exports core classes/functions
├── edgeauth.py         # EdgeGrid authentication logic
├── appsec.py           # App & API Protector endpoints
```

## 🛡️ Authentication Internals
Akamai requires signed requests using the EG1-HMAC-SHA256 scheme. `EdgeAuth` handles:
- Timestamp and nonce generation
- Canonical request hashing
- Signature generation using HMAC-SHA256

## 📤 Contributing
1. Fork this repo
2. Create a new branch
3. Submit a pull request

## 📜 License
MIT

## 🧩 Roadmap
- [ ] Add support for other Akamai APIs (e.g. GTM, PAPI, Reporting)
- [ ] Async support with `httpx`
- [ ] CLI interface for fast testing

---

> Made with ☕, 💻 and pure edgegrid rage.