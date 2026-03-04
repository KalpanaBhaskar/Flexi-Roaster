import sys
import os
import asyncio
from datetime import datetime, timedelta
import uuid

# Add backend directory to module search path so backend.db imports work
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.db.models import Base, PipelineDB, ExecutionDB
from backend.ai.forecasting import PipelineForecaster
from backend.api.routes.ai import get_pipeline_forecast, forecaster

# Setup test database connection
engine = create_engine("sqlite:///./flexiroaster.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_test_data(db):
    """Creates a dummy pipeline with 14 days of execution history containing 1 hard anomaly"""
    pipeline_id = str(uuid.uuid4())
    
    # Create Pipeline
    pipeline = PipelineDB(
        id=pipeline_id,
        name="AI Forecasting Test Pipeline",
        description="Testing Prophet implementation",
        definition={"stages": [{"name": "extract"}, {"name": "load"}]} # 2 stages
    )
    db.add(pipeline)
    
    now = datetime.utcnow()
    
    # Create 14 normal executions (1 per day)
    for i in range(14):
        run_date = now - timedelta(days=14 - i)
        
        # Make one of them randomly fail (y=1)
        status = "completed"
        duration = 15.5 # normal duration
        
        if i == 5:
            # Day 5 fails
            status = "failed"
            duration = 18.2
            
        if i == 10:
            # Day 10 is an anomaly (took 500 seconds instead of ~15s)
            duration = 500.0
            
        execution = ExecutionDB(
            id=str(uuid.uuid4()),
            pipeline_id=pipeline_id,
            pipeline_name="AI Forecasting Test Pipeline",
            status=status,
            started_at=run_date,
            completed_at=run_date + timedelta(seconds=duration),
            duration=duration,
        )
        db.add(execution)
        
    db.commit()
    return pipeline_id


async def run_test():
    print("🚀 Initializing Forecasting Test")
    db = SessionLocal()
    pipeline_id = seed_test_data(db)
    print(f"✅ Created test pipeline {pipeline_id} with 14 past executions.")
    
    print("\n⏳ Triggering get_pipeline_forecast endpoint...")
    response = await get_pipeline_forecast(pipeline_id=pipeline_id, periods=7, db=db)
    
    print(f"✅ Target Pipeline Configured: {response.pipeline_id}")
    print(f"✅ Generating predictions for {response.forecast_days} days into the future.")
    print("-" * 40)
    
    print("📈 AI PREDICTIONS:")
    if not response.predictions:
        print("❌ FAILED: Prophet model returned NO predictions.")
    else:
        for p in response.predictions:
            print(f"   Date: {p.date} | Fail Chance: {p.failure_probability*100:.1f}%")
            
    print("-" * 40)
    print("🚨 ANOMALY ALERTS:")
    if not response.anomalies:
        print("❌ FAILED: Anomaly detection did not catch the 500s runaway execution.")
    else:
        for a in response.anomalies:
            print(f"   Timestamp: {a.timestamp} | Duration: {a.duration}s | Z-Score: {a.z_score:.1f}")
            if a.is_unusually_high:
                print("   ✅ CORRECTLY detected as unusually high duration.")

    db.close()


if __name__ == "__main__":
    asyncio.run(run_test())
