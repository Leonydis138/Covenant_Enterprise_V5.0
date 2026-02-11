"""Test constitutional engine"""
import pytest
from covenant.core.engine import UltimateEngine, Action

@pytest.mark.asyncio
async def test_engine_creation():
    """Test engine initializes"""
    engine = UltimateEngine()
    assert engine.version == "5.0.0"
    assert len(engine.agents) == 6

@pytest.mark.asyncio
async def test_basic_evaluation():
    """Test basic evaluation"""
    engine = UltimateEngine()
    action = Action(type="test", description="Test action")
    result = await engine.evaluate(action)
    
    assert result.action_id == action.id
    assert isinstance(result.is_allowed, bool)
    assert 0 <= result.score <= 1
    assert result.confidence >= 0

def test_metrics():
    """Test metrics collection"""
    engine = UltimateEngine()
    metrics = engine.get_metrics()
    
    assert "total_evaluations" in metrics
    assert "version" in metrics
    assert metrics["version"] == "5.0.0"
