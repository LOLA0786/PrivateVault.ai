#!/usr/bin/env python3
import os
import sys
import json
import argparse
from pathlib import Path
from datetime import datetime
import re

class TechDebtAnalyzer:
    def __init__(self):
        self.issues = []
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'issues_by_severity': {'critical': 0, 'high': 0, 'medium': 0, 'low': 0},
            'issues_by_category': {}
        }
        # Directories to exclude
        self.exclude_dirs = {'venv', 'node_modules', '__pycache__', '.git', 'build', 'dist', 'env'}
        
    def should_analyze(self, path):
        """Check if path should be analyzed"""
        parts = Path(path).parts
        return not any(excluded in parts for excluded in self.exclude_dirs)
    
    def analyze_directory(self, path, extensions=None):
        if extensions is None:
            extensions = {'.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.cs'}
        
        path = Path(path)
        files = []
        
        for ext in extensions:
            for file in path.rglob(f'*{ext}'):
                if self.should_analyze(file):
                    files.append(file)
        
        print(f"Found {len(files)} code files to analyze...")
        
        for file in files:
            self.analyze_file(file)
            self.stats['total_files'] += 1
        
        return self.generate_report()
    
    def analyze_file(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
                self.stats['total_lines'] += len(lines)
                self.check_all_patterns(filepath, content, lines)
        except Exception as e:
            print(f"Error analyzing {filepath}: {e}")
    
    def check_all_patterns(self, filepath, content, lines):
        patterns = {
            'Legacy Code': [
                (r'\bvar\s+\w+', 'Use let/const instead of var', 'medium'),
                (r'==(?!=)', 'Use strict equality (===)', 'low'),
            ],
            'Security': [
                (r'password\s*=\s*["\'][^"\']+["\']', 'Hard-coded password', 'critical'),
                (r'api[_-]?key\s*=\s*["\'][^"\']+["\']', 'Hard-coded API key', 'critical'),
            ],
            'Performance': [
                (r'for\s+\w+\s+in.*:\s*\n\s+for\s+\w+\s+in', 'Nested loops', 'medium'),
            ],
        }
        
        for i, line in enumerate(lines, 1):
            # Check for TODOs
            if 'TODO' in line.upper() or 'FIXME' in line.upper():
                self.add_issue('Documentation', 'low', 'TODO/FIXME found', filepath, i, True)
            
            # Check patterns
            for category, checks in patterns.items():
                for pattern, message, severity in checks:
                    if re.search(pattern, line):
                        self.add_issue(category, severity, message, filepath, i, True)
    
    def add_issue(self, category, severity, description, filepath, line, auto_fixable):
        issue = {
            'category': category,
            'severity': severity,
            'description': description,
            'file': str(filepath),
            'line': line,
            'auto_fixable': auto_fixable
        }
        self.issues.append(issue)
        self.stats['issues_by_severity'][severity] += 1
        self.stats['issues_by_category'][category] = \
            self.stats['issues_by_category'].get(category, 0) + 1
    
    def generate_report(self):
        total_issues = len(self.issues)
        critical = self.stats['issues_by_severity']['critical']
        
        health_score = max(0, 100 - (critical * 10) - (total_issues * 0.5))
        
        if critical > 0:
            overall_severity = 'critical'
        elif self.stats['issues_by_severity']['high'] > 5:
            overall_severity = 'high'
        elif total_issues > 20:
            overall_severity = 'medium'
        else:
            overall_severity = 'low'
        
        return {
            'timestamp': datetime.now().isoformat(),
            'health_score': round(health_score, 2),
            'overall_severity': overall_severity,
            'statistics': self.stats,
            'total_issues': total_issues,
            'issues': sorted(self.issues, 
                           key=lambda x: {'critical': 0, 'high': 1, 'medium': 2, 'low': 3}[x['severity']])[:50]
        }
    
    def print_report(self, report):
        print("\n" + "="*80)
        print("TECHNICAL DEBT ANALYSIS REPORT")
        print("="*80)
        print(f"Health Score: {report['health_score']}/100")
        print(f"Overall Severity: {report['overall_severity'].upper()}")
        print(f"Files Analyzed: {self.stats['total_files']}")
        print(f"Total Issues: {report['total_issues']}")
        
        print("\nTop 10 Issues:")
        for i, issue in enumerate(report['issues'][:10], 1):
            print(f"\n{i}. [{issue['severity'].upper()}] {issue['category']}")
            print(f"   {issue['description']}")
            print(f"   {issue['file']}:{issue['line']}")
    
    def save_report(self, report, output_file):
        # Create directory if it doesn't exist
        os.makedirs(os.path.dirname(output_file) or '.', exist_ok=True)
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        print(f"\nReport saved to: {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Technical Debt Analyzer')
    parser.add_argument('path', help='Path to analyze')
    parser.add_argument('-o', '--output', default='tech-debt-report.json')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.path):
        print(f"Error: Path not found: {args.path}")
        sys.exit(1)
    
    analyzer = TechDebtAnalyzer()
    print("Starting Technical Debt Analysis...")
    
    report = analyzer.analyze_directory(args.path)
    analyzer.print_report(report)
    analyzer.save_report(report, args.output)

if __name__ == '__main__':
    main()
