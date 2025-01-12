import ast
from typing import Dict, Tuple, List

class ComplexityAnalyzer:
    def __init__(self):
        self.loop_keywords = {'for', 'while'}
        self.complexity_patterns = {
            'O(1)': ['constant', 'single operation'],
            'O(log n)': ['binary search', 'divide by', 'half'],
            'O(n)': ['linear', 'single loop'],
            'O(n log n)': ['sort', 'merge', 'quicksort'],
            'O(n²)': ['nested loop', 'bubble sort'],
            'O(2^n)': ['recursive fibonacci', 'combinations'],
        }

    def analyze_complexity(self, code: str) -> Dict[str, str]:
        try:
            tree = ast.parse(code)
            time_complexity = self._analyze_time_complexity(tree)
            space_complexity = self._analyze_space_complexity(tree)
            
            return {
                "time_complexity": time_complexity,
                "space_complexity": space_complexity,
                "explanation": self._generate_explanation(time_complexity, space_complexity)
            }
        except Exception as e:
            return {
                "error": f"Failed to analyze complexity: {str(e)}"
            }

    def _analyze_time_complexity(self, tree: ast.AST) -> str:
        nested_loops = self._count_nested_loops(tree)
        recursion = self._check_recursion(tree)
        
        if recursion:
            return "O(2^n)"  # Simplified assumption for recursive functions
        elif nested_loops > 1:
            return f"O(n^{nested_loops})"
        elif nested_loops == 1:
            return "O(n)"
        else:
            return "O(1)"

    def _analyze_space_complexity(self, tree: ast.AST) -> str:
        # Count variable declarations and data structure sizes
        variables = self._count_variables(tree)
        if variables > 10:  # Arbitrary threshold
            return "O(n)"
        return "O(1)"

    def _count_nested_loops(self, tree: ast.AST) -> int:
        class LoopCounter(ast.NodeVisitor):
            def __init__(self):
                self.max_depth = 0
                self.current_depth = 0

            def visit_For(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

            def visit_While(self, node):
                self.current_depth += 1
                self.max_depth = max(self.max_depth, self.current_depth)
                self.generic_visit(node)
                self.current_depth -= 1

        counter = LoopCounter()
        counter.visit(tree)
        return counter.max_depth

    def _check_recursion(self, tree: ast.AST) -> bool:
        class RecursionChecker(ast.NodeVisitor):
            def __init__(self):
                self.function_name = None
                self.has_recursion = False

            def visit_FunctionDef(self, node):
                old_name = self.function_name
                self.function_name = node.name
                self.generic_visit(node)
                self.function_name = old_name

            def visit_Call(self, node):
                if isinstance(node.func, ast.Name) and node.func.id == self.function_name:
                    self.has_recursion = True
                self.generic_visit(node)

        checker = RecursionChecker()
        checker.visit(tree)
        return checker.has_recursion

    def _count_variables(self, tree: ast.AST) -> int:
        class VariableCounter(ast.NodeVisitor):
            def __init__(self):
                self.count = 0

            def visit_Assign(self, node):
                self.count += len(node.targets)
                self.generic_visit(node)

        counter = VariableCounter()
        counter.visit(tree)
        return counter.count

    def _generate_explanation(self, time_complexity: str, space_complexity: str) -> str:
        explanation = f"Time Complexity: {time_complexity}\n"
        explanation += f"Space Complexity: {space_complexity}\n\n"
        
        explanation += "Explanation:\n"
        if time_complexity == "O(1)":
            explanation += "- The code has constant time complexity, meaning it performs a fixed number of operations.\n"
        elif time_complexity == "O(n)":
            explanation += "- The code has linear time complexity, typically involving a single loop through the input.\n"
        elif time_complexity.startswith("O(n^"):
            explanation += "- The code has polynomial time complexity due to nested loops.\n"
        elif time_complexity == "O(2^n)":
            explanation += "- The code has exponential time complexity, typically due to recursive operations.\n"

        return explanation 