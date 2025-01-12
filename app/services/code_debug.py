import ast
import re
from typing import Dict, List, Tuple
from dataclasses import dataclass

@dataclass
class DebugIssue:
    line_number: int
    issue_type: str
    description: str
    suggestion: str
    severity: str

class CodeDebugger:
    def __init__(self):
        self.common_errors = {
            'IndentationError': 'Incorrect indentation',
            'SyntaxError': 'Invalid syntax',
            'NameError': 'Undefined variable',
            'TypeError': 'Invalid operation between types',
            'IndexError': 'Invalid index access',
            'KeyError': 'Invalid dictionary key',
            'AttributeError': 'Invalid object attribute',
            'ZeroDivisionError': 'Division by zero',
        }

    def debug_code(self, code: str) -> Dict:
        issues = []
        issues.extend(self._check_syntax(code))
        issues.extend(self._analyze_common_patterns(code))
        issues.extend(self._check_best_practices(code))
        
        fixed_code = self._attempt_fix(code, issues)
        
        return {
            "issues": [self._format_issue(issue) for issue in issues],
            "fixed_code": fixed_code,
            "summary": self._generate_summary(issues)
        }

    def _check_syntax(self, code: str) -> List[DebugIssue]:
        issues = []
        
        # Check basic syntax
        try:
            ast.parse(code)
        except SyntaxError as e:
            issues.append(DebugIssue(
                line_number=e.lineno,
                issue_type="SyntaxError",
                description=str(e),
                suggestion=self._get_syntax_suggestion(str(e)),
                severity="high"
            ))
        except IndentationError as e:
            issues.append(DebugIssue(
                line_number=e.lineno,
                issue_type="IndentationError",
                description="Incorrect indentation",
                suggestion="Check indentation level. Use 4 spaces for each level.",
                severity="high"
            ))
            
        return issues

    def _analyze_common_patterns(self, code: str) -> List[DebugIssue]:
        issues = []
        lines = code.split('\n')
        
        for i, line in enumerate(lines, 1):
            # Check for common comparison mistakes
            if "is" in line and not any(x in line for x in ["is not", "isinstance"]):
                if re.search(r'\bis\s+[\'\"\d]', line):
                    issues.append(DebugIssue(
                        line_number=i,
                        issue_type="LogicError",
                        description="Using 'is' for literal comparison",
                        suggestion="Use '==' instead of 'is' for value comparison",
                        severity="medium"
                    ))
            
            # Check for potential infinite loops
            if "while" in line and "True" in line:
                if not any("break" in l for l in lines[i:]):
                    issues.append(DebugIssue(
                        line_number=i,
                        issue_type="LogicError",
                        description="Potential infinite loop detected",
                        suggestion="Add a break condition to prevent infinite execution",
                        severity="high"
                    ))
            
            # Check for bare except clauses
            if line.strip().startswith("except:"):
                issues.append(DebugIssue(
                    line_number=i,
                    issue_type="StyleError",
                    description="Bare except clause",
                    suggestion="Specify the exception type(s) to catch",
                    severity="medium"
                ))

        return issues

    def _check_best_practices(self, code: str) -> List[DebugIssue]:
        issues = []
        
        try:
            tree = ast.parse(code)
            
            # Check for unused variables
            class UnusedVariableChecker(ast.NodeVisitor):
                def __init__(self):
                    self.defined_vars = {}
                    self.used_vars = set()

                def visit_Name(self, node):
                    if isinstance(node.ctx, ast.Store):
                        self.defined_vars[node.id] = node.lineno
                    elif isinstance(node.ctx, ast.Load):
                        self.used_vars.add(node.id)

            checker = UnusedVariableChecker()
            checker.visit(tree)
            
            for var, line_no in checker.defined_vars.items():
                if var not in checker.used_vars:
                    issues.append(DebugIssue(
                        line_number=line_no,
                        issue_type="StyleWarning",
                        description=f"Unused variable '{var}'",
                        suggestion=f"Remove unused variable or use it in the code",
                        severity="low"
                    ))

        except Exception:
            pass  # If parsing fails, skip best practices check
            
        return issues

    def _attempt_fix(self, code: str, issues: List[DebugIssue]) -> str:
        fixed_code = code
        lines = code.split('\n')
        
        # Sort issues by line number in reverse order to avoid offset issues
        sorted_issues = sorted(issues, key=lambda x: x.line_number, reverse=True)
        
        for issue in sorted_issues:
            if issue.issue_type == "IndentationError":
                # Fix indentation
                lines[issue.line_number - 1] = "    " + lines[issue.line_number - 1].lstrip()
            elif issue.issue_type == "LogicError":
                # Fix comparison operators
                if "is" in lines[issue.line_number - 1]:
                    lines[issue.line_number - 1] = lines[issue.line_number - 1].replace(" is ", " == ")
            
        return "\n".join(lines)

    def _get_syntax_suggestion(self, error_msg: str) -> str:
        suggestions = {
            "EOF while scanning": "Add closing quotation mark or parenthesis",
            "invalid syntax": "Check for missing colons, parentheses, or invalid operators",
            "unexpected indent": "Remove extra indentation",
            "expected an indented block": "Add indentation after this line"
        }
        
        for key, suggestion in suggestions.items():
            if key in error_msg:
                return suggestion
        return "Check syntax near this line"

    def _format_issue(self, issue: DebugIssue) -> Dict:
        return {
            "line": issue.line_number,
            "type": issue.issue_type,
            "description": issue.description,
            "suggestion": issue.suggestion,
            "severity": issue.severity
        }

    def _generate_summary(self, issues: List[DebugIssue]) -> str:
        if not issues:
            return "No issues found in the code."
        
        severity_counts = {
            "high": len([i for i in issues if i.severity == "high"]),
            "medium": len([i for i in issues if i.severity == "medium"]),
            "low": len([i for i in issues if i.severity == "low"])
        }
        
        summary = f"Found {len(issues)} issue(s):\n"
        summary += f"- {severity_counts['high']} high severity\n"
        summary += f"- {severity_counts['medium']} medium severity\n"
        summary += f"- {severity_counts['low']} low severity\n"
        
        return summary 