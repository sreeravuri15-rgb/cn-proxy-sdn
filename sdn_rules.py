import json
import os
import threading

RULE_FILE = "sdn_rules.json"
rules_lock = threading.Lock()


def normalize_site(site):
    """Make rule comparisons case-insensitive and consistent."""
    return site.strip().lower()


def load_rules():
    if not os.path.exists(RULE_FILE):
        return []

    try:
        with open(RULE_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_rules(rules):
    with open(RULE_FILE, "w", encoding="utf-8") as file:
        json.dump(rules, file, indent=4)


def install_rule(site, action):
    site = normalize_site(site)
    action = action.upper()

    if not site or action not in {"ALLOW", "BLOCK"}:
        print("Invalid rule.")
        return

    with rules_lock:
        rules = load_rules()
        rules = [rule for rule in rules if normalize_site(rule.get("site", "")) != site]
        rules.append({"site": site, "action": action})
        save_rules(rules)

    print(f"SDN Rule Installed: {action} -> {site}")


def remove_rule(site):
    site = normalize_site(site)

    with rules_lock:
        rules = load_rules()
        rules = [rule for rule in rules if normalize_site(rule.get("site", "")) != site]
        save_rules(rules)

    print(f"SDN Rule Removed: {site}")


def check_rule(site):
    """Return BLOCK/ALLOW for the current request. Default is ALLOW."""
    site = normalize_site(site)

    with rules_lock:
        rules = load_rules()

    for rule in rules:
        if normalize_site(rule.get("site", "")) == site:
            return rule.get("action", "ALLOW").upper()

    return "ALLOW"


def show_rules():
    rules = load_rules()

    print("\nCurrent SDN Rules:")
    if not rules:
        print("  No rules installed. Default action: ALLOW")
        return

    for rule in rules:
        print(f"  {rule['action']} -> {rule['site']}")
