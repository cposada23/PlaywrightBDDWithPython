#!/bin/bash

# Playwright BDD Test Runner Script
# This script provides easy test execution with defaults for debugging

set -e  # Exit on error

# Default configuration (optimized for debugging and development)
DEFAULT_HEADLESS="false"           # Run with visible browser by default
DEFAULT_SLOWMO="1500"             # 1 second slow motion by default
DEFAULT_PARALLEL="false"          # Run sequentially by default
DEFAULT_REPORT="allure"           # Use allure reports by default
DEFAULT_BROWSER="chromium"        # Default browser
DEFAULT_BASE_URL="https://blankfactor.com/"
DEFAULT_MARKERS=""               # No marker filter by default
DEFAULT_VERBOSE="true"           # Verbose output by default

# Initialize variables with defaults
HEADLESS="$DEFAULT_HEADLESS"
SLOWMO="$DEFAULT_SLOWMO"
PARALLEL="$DEFAULT_PARALLEL"
REPORT="$DEFAULT_REPORT"
BROWSER="$DEFAULT_BROWSER"
BASE_URL="$DEFAULT_BASE_URL"
MARKERS="$DEFAULT_MARKERS"
VERBOSE="$DEFAULT_VERBOSE"
HELP_REQUESTED=false

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to display help
show_help() {
    echo -e "${BLUE}🧪 Playwright BDD Test Runner${NC}"
    echo
    echo -e "${GREEN}Usage:${NC} $0 [OPTIONS]"
    echo
    echo -e "${GREEN}DESCRIPTION:${NC}"
    echo "  Easy test execution with debugging-friendly defaults."
    echo "  By default runs tests with visible browser, slow motion, and allure reports."
    echo
    echo -e "${GREEN}OPTIONS:${NC}"
    echo "  --headless=BOOL        Run browser in headless mode (default: false)"
    echo "  --slowmo=NUMBER        Slow down operations by milliseconds (default: 1000)"
    echo "  --parallel=BOOL        Run tests in parallel (default: false)"
    echo "  --report=TYPE          Report type: allure|html|both|none (default: allure)"
    echo "  --browser=NAME         Browser: chromium|firefox|webkit (default: chromium)"
    echo "  --base-url=URL         Base URL for tests (default: https://example.com)"
    echo "  --markers=MARKERS      Test markers to run (e.g., smoke, web, regression)"
    echo "  --verbose=BOOL         Verbose output (default: true)"
    echo "  --help, -h             Show this help message"
    echo
    echo -e "${GREEN}EXAMPLES:${NC}"
    echo "  $0                                    # Run with all defaults (debug mode)"
    echo "  $0 --headless=true                   # Run headless"
    echo "  $0 --parallel=true                   # Run in parallel"
    echo "  $0 --slowmo=500                      # Faster slow motion"
    echo "  $0 --markers=smoke                   # Run only smoke tests"
    echo "  $0 --report=html                     # Use HTML reports instead"
    echo "  $0 --browser=firefox --slowmo=0      # Firefox without slow motion"
    echo "  $0 --headless=true --parallel=true   # Fast headless parallel run"
    echo
    echo -e "${GREEN}CURRENT DEFAULTS:${NC}"
    echo "  Headless: ${YELLOW}$DEFAULT_HEADLESS${NC} (visible browser for debugging)"
    echo "  Slow Motion: ${YELLOW}${DEFAULT_SLOWMO}ms${NC} (see test actions clearly)"
    echo "  Parallel: ${YELLOW}$DEFAULT_PARALLEL${NC} (sequential for easier debugging)"
    echo "  Report: ${YELLOW}$DEFAULT_REPORT${NC} (interactive allure reports)"
    echo "  Browser: ${YELLOW}$DEFAULT_BROWSER${NC}"
    echo "  Verbose: ${YELLOW}$DEFAULT_VERBOSE${NC}"
    echo
}

# Function to parse boolean values
parse_bool() {
    local value="$1"
    case "$value" in
        true|True|TRUE|1|yes|Yes|YES|on|On|ON)
            echo "true"
            ;;
        false|False|FALSE|0|no|No|NO|off|Off|OFF)
            echo "false"
            ;;
        *)
            echo -e "${RED}❌ Invalid boolean value: '$value'. Use true/false${NC}" >&2
            exit 1
            ;;
    esac
}

# Function to validate report type
validate_report_type() {
    local report="$1"
    case "$report" in
        allure|html|both|none)
            echo "$report"
            ;;
        *)
            echo -e "${RED}❌ Invalid report type: '$report'. Use: allure|html|both|none${NC}" >&2
            exit 1
            ;;
    esac
}

# Function to validate browser
validate_browser() {
    local browser="$1"
    case "$browser" in
        chromium|firefox|webkit)
            echo "$browser"
            ;;
        *)
            echo -e "${RED}❌ Invalid browser: '$browser'. Use: chromium|firefox|webkit${NC}" >&2
            exit 1
            ;;
    esac
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        --headless=*)
            HEADLESS=$(parse_bool "${1#*=}")
            shift
            ;;
        --slowmo=*)
            SLOWMO="${1#*=}"
            # Validate it's a number
            if ! [[ "$SLOWMO" =~ ^[0-9]+$ ]]; then
                echo -e "${RED}❌ Invalid slowmo value: '$SLOWMO'. Must be a number (milliseconds)${NC}" >&2
                exit 1
            fi
            shift
            ;;
        --parallel=*)
            PARALLEL=$(parse_bool "${1#*=}")
            shift
            ;;
        --report=*)
            REPORT=$(validate_report_type "${1#*=}")
            shift
            ;;
        --browser=*)
            BROWSER=$(validate_browser "${1#*=}")
            shift
            ;;
        --base-url=*)
            BASE_URL="${1#*=}"
            shift
            ;;
        --markers=*)
            MARKERS="${1#*=}"
            shift
            ;;
        --verbose=*)
            VERBOSE=$(parse_bool "${1#*=}")
            shift
            ;;
        --help|-h)
            HELP_REQUESTED=true
            shift
            ;;
        *)
            echo -e "${RED}❌ Unknown option: $1${NC}" >&2
            echo "Use --help for usage information."
            exit 1
            ;;
    esac
done

# Show help if requested
if [ "$HELP_REQUESTED" = true ]; then
    show_help
    exit 0
fi

# Display configuration
echo -e "${BLUE}🧪 Playwright BDD Test Runner${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "🌐 Browser:     ${YELLOW}$BROWSER${NC}"
echo -e "👁️  Headless:    ${YELLOW}$HEADLESS${NC}"
echo -e "🐌 Slow Motion: ${YELLOW}${SLOWMO}ms${NC}"
echo -e "⚡ Parallel:    ${YELLOW}$PARALLEL${NC}"
echo -e "📊 Report:      ${YELLOW}$REPORT${NC}"
echo -e "🔗 Base URL:    ${YELLOW}$BASE_URL${NC}"
if [ -n "$MARKERS" ]; then
    echo -e "🏷️  Markers:     ${YELLOW}$MARKERS${NC}"
fi
echo -e "📝 Verbose:     ${YELLOW}$VERBOSE${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo

# Check if uv is available
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ uv is not installed or not in PATH${NC}"
    echo "Please install uv: https://docs.astral.sh/uv/"
    exit 1
fi

# Check if virtual environment exists
if [ ! -d ".venv" ]; then
    echo -e "${YELLOW}⚠️  Virtual environment not found. Creating one...${NC}"
    uv venv
fi

# Activate virtual environment and sync dependencies
echo -e "${BLUE}📦 Syncing dependencies...${NC}"
uv sync

# Install playwright browsers if needed
if [ ! -d ".venv/lib/python*/site-packages/playwright/driver" ]; then
    echo -e "${BLUE}🎭 Installing Playwright browsers...${NC}"
    uv run playwright install
fi

# Prepare pytest command
PYTEST_CMD="uv run pytest"

# Add browser configuration
PYTEST_CMD="$PYTEST_CMD --browser=$BROWSER"
PYTEST_CMD="$PYTEST_CMD --headless=$HEADLESS"
PYTEST_CMD="$PYTEST_CMD --slowmo=$SLOWMO"
PYTEST_CMD="$PYTEST_CMD --base-url=$BASE_URL"

# Add parallel execution if enabled
if [ "$PARALLEL" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD -n auto"
fi

# Add markers if specified
if [ -n "$MARKERS" ]; then
    PYTEST_CMD="$PYTEST_CMD -m $MARKERS"
fi

# Add verbose output if enabled
if [ "$VERBOSE" = "true" ]; then
    PYTEST_CMD="$PYTEST_CMD -v"
fi

# Prepare reports directory and clean old results
mkdir -p reports

# Clean up old report files before running new tests
echo -e "${BLUE}🧹 Cleaning up old reports...${NC}"
case "$REPORT" in
    allure)
        # Clean allure results directory
        if [ -d "reports/allure-results" ]; then
            rm -rf reports/allure-results/*
            echo "   Cleared old Allure results"
        fi
        PYTEST_CMD="$PYTEST_CMD --alluredir=reports/allure-results"
        ;;
    html)
        # Remove old HTML report
        if [ -f "reports/report.html" ]; then
            rm -f reports/report.html
            echo "   Removed old HTML report"
        fi
        PYTEST_CMD="$PYTEST_CMD --html=reports/report.html --self-contained-html"
        ;;
    both)
        # Clean both report types
        if [ -d "reports/allure-results" ]; then
            rm -rf reports/allure-results/*
            echo "   Cleared old Allure results"
        fi
        if [ -f "reports/report.html" ]; then
            rm -f reports/report.html
            echo "   Removed old HTML report"
        fi
        PYTEST_CMD="$PYTEST_CMD --alluredir=reports/allure-results --html=reports/report.html --self-contained-html"
        ;;
    none)
        # No report flags added
        echo "   No reports will be generated"
        ;;
esac

# Run the tests
echo -e "${GREEN}🚀 Running tests...${NC}"
echo -e "${BLUE}Command: $PYTEST_CMD${NC}"
echo

# Execute the command
eval $PYTEST_CMD
TEST_EXIT_CODE=$?

# Handle reports based on type and test results
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo -e "${GREEN}✅ Tests completed successfully!${NC}"
else
    echo -e "${YELLOW}⚠️  Some tests failed or had issues.${NC}"
fi

# Verify and open reports if tests completed (even with failures)
echo
echo -e "${BLUE}📊 Processing reports...${NC}"

case "$REPORT" in
    allure)
        echo -e "${BLUE}📊 Checking Allure results...${NC}"
        if [ -d "reports/allure-results" ]; then
            # Count result files to verify generation
            RESULT_COUNT=$(find reports/allure-results -name "*.json" | wc -l)
            echo "   Found $RESULT_COUNT Allure result files"
            
            if [ "$RESULT_COUNT" -gt 0 ]; then
                echo -e "${GREEN}✅ Allure results generated successfully${NC}"
                echo -e "${BLUE}📊 Opening interactive Allure report...${NC}"
                if command -v allure &> /dev/null; then
                    # Use generate + open for better reliability than serve
                    allure generate reports/allure-results --clean -o reports/allure-report
                    allure open reports/allure-report
                else
                    echo -e "${YELLOW}⚠️  Allure command not found. Install it to view interactive reports.${NC}"
                    echo "   macOS: brew install allure"
                    echo "   Linux: sudo apt-get install allure"
                    echo "   Windows: scoop install allure"
                    echo "   📁 Results saved in: reports/allure-results/"
                    echo "   📄 File count: $RESULT_COUNT JSON files"
                fi
            else
                echo -e "${RED}❌ No Allure results found! Check pytest-allure plugin installation.${NC}"
                echo "   Try: uv add allure-pytest"
            fi
        else
            echo -e "${RED}❌ Allure results directory not found!${NC}"
        fi
        ;;
    html)
        if [ -f "reports/report.html" ]; then
            echo -e "${GREEN}✅ HTML report generated: reports/report.html${NC}"
            # Try to open in default browser (optional)
            if command -v open &> /dev/null; then  # macOS
                open reports/report.html
            elif command -v xdg-open &> /dev/null; then  # Linux
                xdg-open reports/report.html
            else
                echo "   📁 Open reports/report.html in your browser to view results"
            fi
        else
            echo -e "${RED}❌ HTML report not found!${NC}"
        fi
        ;;
    both)
        echo -e "${BLUE}📊 Checking both report types...${NC}"
        
        # Check HTML report
        if [ -f "reports/report.html" ]; then
            echo -e "${GREEN}   ✅ HTML: reports/report.html${NC}"
        else
            echo -e "${RED}   ❌ HTML report not generated${NC}"
        fi
        
        # Check Allure results
        if [ -d "reports/allure-results" ]; then
            RESULT_COUNT=$(find reports/allure-results -name "*.json" | wc -l)
            if [ "$RESULT_COUNT" -gt 0 ]; then
                echo -e "${GREEN}   ✅ Allure: $RESULT_COUNT result files${NC}"
                if command -v allure &> /dev/null; then
                    echo -e "${BLUE}📊 Opening interactive Allure report...${NC}"
                    allure generate reports/allure-results --clean -o reports/allure-report
                    allure open reports/allure-report
                else
                    echo -e "${YELLOW}   ⚠️  Allure command not found for interactive report.${NC}"
                fi
            else
                echo -e "${RED}   ❌ No Allure results found${NC}"
            fi
        else
            echo -e "${RED}   ❌ Allure results directory not found${NC}"
        fi
        ;;
    none)
        echo -e "${BLUE}📊 No reports generated (as requested)${NC}"
        ;;
esac

echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${BLUE}🎉 Test execution completed!${NC}"

exit $TEST_EXIT_CODE
