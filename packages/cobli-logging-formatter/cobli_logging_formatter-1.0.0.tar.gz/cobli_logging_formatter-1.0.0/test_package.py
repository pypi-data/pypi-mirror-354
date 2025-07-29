"""
Simple test script to verify the package structure works.
"""

import sys
import os

# Add the package to the path
sys.path.insert(0, '/Users/pellizzetti/Workspace/cobli/python-logging-data-model-formatter')

# Mock ddtrace for testing
class MockTracer:
    def current_trace_context(self):
        return None

class MockModule:
    tracer = MockTracer()

sys.modules['ddtrace'] = MockModule()

# Now import our package
from cobli_logging import JsonFormatter, configure_logging, get_logger

def test_formatter():
    """Test the JsonFormatter directly."""
    print("=== Testing JsonFormatter ===")
    
    import logging
    import json
    
    formatter = JsonFormatter(service_name="test-service", version="1.0.0")
    
    # Create a test log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="Test message with data",
        args=(),
        exc_info=None
    )
    
    # Add custom fields
    record.user_id = 123
    record.action = "test"
    
    # Format the record
    result = formatter.format(record)
    log_data = json.loads(result)
    
    print("Formatted log:")
    print(json.dumps(log_data, indent=2))
    
    # Verify structure
    assert "timestamp" in log_data
    assert "level" in log_data
    assert "message" in log_data
    assert "custom" in log_data
    assert log_data["custom"]["user_id"] == 123
    assert log_data["custom"]["action"] == "test"
    
    print("✅ JsonFormatter test passed!")

def test_configuration():
    """Test configuration functions."""
    print("\n=== Testing Configuration ===")
    
    # Test get_logger
    logger = get_logger(service_name="test-config", log_level="DEBUG")
    
    print(f"Logger name: {logger.name}")
    print(f"Logger level: {logger.level}")
    print(f"Number of handlers: {len(logger.handlers)}")
    
    if logger.handlers:
        formatter = logger.handlers[0].formatter
        print(f"Formatter type: {type(formatter).__name__}")
        
        assert isinstance(formatter, JsonFormatter)
        print("✅ Configuration test passed!")

if __name__ == "__main__":
    try:
        test_formatter()
        test_configuration()
        print("\n🎉 All tests passed! The package structure is working correctly.")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
