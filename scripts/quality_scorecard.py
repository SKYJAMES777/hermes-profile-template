#!/usr/bin/env python3
"""Profile Quality Scorecard - #14 bounty 0.25 SOL"""

import os, json, sys, datetime

CHECKS = {
    "README": {"weight": 20, "desc": "README.md present and informative"},
    "CHANGELOG": {"weight": 15, "desc": "CHANGELOG.md tracks version history"},
    "LICENSE": {"weight": 10, "desc": "License file specifies terms"},
    "distribution.yaml": {"weight": 20, "desc": "Distribution metadata defined"},
    "validate_profile.py": {"weight": 15, "desc": "Validation script exists"},
    "generate_profile.py": {"weight": 10, "desc": "Profile generation script exists"},
    "CONTRIBUTING": {"weight": 10, "desc": "Contributing guidelines"},
}

def score_profile(repo_path="."):
    scores = {}
    details = {}
    total = 0
    max_total = sum(c["weight"] for c in CHECKS.values())
    
    for name, config in CHECKS.items():
        weight = config["weight"]
        desc = config["desc"]
        
        if name == "README":
            ok = os.path.exists(os.path.join(repo_path, "README.md"))
        elif name == "CHANGELOG":
            ok = os.path.exists(os.path.join(repo_path, "CHANGELOG.md"))
        elif name == "LICENSE":
            ok = os.path.exists(os.path.join(repo_path, "LICENSE")) or \
                 os.path.exists(os.path.join(repo_path, "LICENSE.txt"))
        elif name == "distribution.yaml":
            ok = os.path.exists(os.path.join(repo_path, "distribution.yaml"))
        elif name in ["validate_profile.py", "generate_profile.py"]:
            ok = os.path.exists(os.path.join(repo_path, "scripts", name)) or \
                 os.path.exists(os.path.join(repo_path, name))
        elif name == "CONTRIBUTING":
            ok = os.path.exists(os.path.join(repo_path, "CONTRIBUTING.md"))
        else:
            ok = False
        
        score = weight if ok else 0
        total += score
        scores[name] = {"score": score, "max": weight, "passed": ok}
        details[name] = "PASS" if ok else "MISSING"
    
    quality_pct = round((total / max_total) * 100, 1)
    grade = "A" if quality_pct >= 90 else "B" if quality_pct >= 75 else "C" if quality_pct >= 50 else "D"
    
    return {
        "score": total,
        "max_score": max_total,
        "percentage": quality_pct,
        "grade": grade,
        "checks": details,
        "timestamp": datetime.datetime.now().isoformat()
    }

def generate_report(result, output_path=None):
    report = []
    report.append("# Profile Quality Scorecard")
    report.append("")
    report.append("| Metric | Value |")
    report.append("|--------|-------|")
    report.append("| **Grade** | **%s** |" % result["grade"])
    report.append("| **Score** | %d/%d (%.1f%%) |" % (result["score"], result["max_score"], result["percentage"]))
    report.append("| **Checked** | %s |" % result["timestamp"])
    report.append("")
    report.append("## Check Details")
    report.append("")
    report.append("| Check | Status |")
    report.append("|-------|--------|")
    for name, status in result["checks"].items():
        emoji = "✓" if status == "PASS" else "✗"
        report.append("| %s | %s %s |" % (name, emoji, status))
    report.append("")
    if result["grade"] == "A":
        report.append("**Excellent quality! Ready for publishing.**")
    elif result["grade"] == "B":
        report.append("**Good quality.** Consider adding missing files to reach grade A.")
    else:
        report.append("**Needs improvement.** Add required files to improve score.")
    
    report_text = "\n".join(report)
    if output_path:
        with open(output_path, "w") as f:
            f.write(report_text)
    return report_text

if __name__ == "__main__":
    result = score_profile()
    report = generate_report(result)
    print(report)
    if len(sys.argv) > 1:
        with open(sys.argv[1], "w") as f:
            f.write(report)
