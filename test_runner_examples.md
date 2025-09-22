# Test Runner Script Examples

This document shows various ways to use the `run_tests.sh` script.

## 🎯 Quick Start Examples

### Development & Debugging (Default behavior)
```bash
# Run with all debugging defaults
./run_tests.sh
# → Visible browser + 1000ms slow motion + allure reports + sequential execution
```

### Fast CI/Production Run
```bash
# Headless, parallel, no slow motion
./run_tests.sh --headless=true --parallel=true --slowmo=0
```

### Specific Test Categories
```bash
# Run only smoke tests
./run_tests.sh --markers=smoke

# Run only web tests
./run_tests.sh --markers=web

# Run regression tests in Firefox
./run_tests.sh --markers=regression --browser=firefox
```

### Different Report Types
```bash
# HTML report instead of Allure
./run_tests.sh --report=html

# Both HTML and Allure reports
./run_tests.sh --report=both

# No reports (fastest)
./run_tests.sh --report=none
```

### Different Environments
```bash
# Test against staging
./run_tests.sh --base-url=https://staging.myapp.com

# Test against local development
./run_tests.sh --base-url=http://localhost:3000
```

### Browser-Specific Testing
```bash
# Run in Firefox with slower motion for debugging
./run_tests.sh --browser=firefox --slowmo=2000

# Run in WebKit (Safari) headless
./run_tests.sh --browser=webkit --headless=true
```

## 🔧 Advanced Combinations

### Debug Specific Test
```bash
# Debug a failing smoke test in slow motion
./run_tests.sh --markers=smoke --slowmo=2000 --headless=false
```

### Quick Smoke Test
```bash
# Fast smoke test run for quick validation
./run_tests.sh --markers=smoke --headless=true --slowmo=0 --parallel=true
```

### Full Regression Suite
```bash
# Complete regression testing with detailed reports
./run_tests.sh --markers=regression --report=both --verbose=true
```

### Cross-Browser Testing
```bash
# Test the same scenario across all browsers
./run_tests.sh --browser=chromium --report=html
./run_tests.sh --browser=firefox --report=html  
./run_tests.sh --browser=webkit --report=html
```
