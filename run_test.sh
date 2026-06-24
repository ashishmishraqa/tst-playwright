#!/bin/bash

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${YELLOW}🧪 Running Playwright Test Suite${NC}"

# Parse arguments
MARKER=${1:-smoke}
WORKERS=${2:-1}
HEADED=${3:-false}
PYTEST_ARGS=("${@:4}")

echo -e "${YELLOW}📊 Test Suite: $MARKER | Workers: $WORKERS | Headed: $HEADED${NC}"

# Install browsers if needed
playwright install

# Run tests
pytest -m "$MARKER" \
    -n "$WORKERS" \
    --dist loadscope \
    --alluredir=allure-results \
    $([ "$HEADED" = "true" ] && echo "--headed") \
    "${PYTEST_ARGS[@]}"


# Check exit code
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Tests passed!${NC}"
    echo -e "${YELLOW}📈 Generating Allure report...${NC}"
    allure serve allure-results
else
    echo -e "${RED}❌ Tests failed!${NC}"
    exit 1
fi
#./run_test.sh smoke 1 false --lf -x
#./run_test.sh regression 2 false --lf -x
#./run_test.sh smoke 1 true --lf -x