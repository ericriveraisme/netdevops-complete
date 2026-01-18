# Testing Environment - Staging

This directory contains isolated testing environments for code review and development.

## Structure

- `.env.test` - Test configuration (separate from production .env)
- `docker-compose.test.yml` - Isolated test containers
- `venv_test/` - Testing virtual environment
- `.test_lock` - Concurrency lock file (auto-created during test runs)
- `test.log` - Test execution logs

## Usage

```bash
cd ~/netdevops-project2/unified/project2-monitoring/tests/staging/

# Create test environment
python -m venv venv_test
source venv_test/bin/activate
pip install -r ../../requirements.txt

# Run isolated tests
cd ~/netdevops-project2/unified/project2-monitoring/tests/staging/
source venv_test/bin/activate
python -m pytest tests/ -v

# Manual code testing (with lock file)
./test_health_poller.sh
```

## Code Review Workflow

1. **Make Changes**: Edit scripts in production location
2. **Copy to Staging**: `cp health_poller.py tests/staging/`
3. **Run Isolated Tests**: Use staging .env.test and docker-compose.test.yml
4. **Verify Lock File**: Ensure no concurrent test runs
5. **Check Results**: Compare with production baseline
6. **Merge**: Once verified, commit to repo

## Lock File Safety

All test scripts check for `.test_lock` file:
```bash
LOCK_FILE=".test_lock"
if [ -f "$LOCK_FILE" ]; then
    echo "ERROR: Test already running (lock file exists)"
    exit 1
fi
trap "rm -f $LOCK_FILE" EXIT
touch "$LOCK_FILE"
```

This prevents concurrent test execution and ensures cleanup.
