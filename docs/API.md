# API Reference

## Base URL
`http://localhost:8000`

## Endpoints

### GET /
Get API information

### GET /health
Health check

**Response:**
```json
{
  "status": "healthy",
  "version": "5.0.0",
  "agents": 6,
  "uptime": "operational"
}
```

### POST /api/v1/evaluate
Evaluate an action

**Request:**
```json
{
  "action_type": "data_access",
  "description": "Access medical records",
  "actor": "doctor_123",
  "parameters": {
    "patient_id": "P456",
    "purpose": "treatment"
  },
  "context": {
    "consent": true,
    "emergency": false
  },
  "verification_level": "STANDARD"
}
```

**Response:**
```json
{
  "action_id": "uuid",
  "is_allowed": true,
  "confidence": 0.95,
  "score": 0.87,
  "violations": [],
  "warnings": [],
  "execution_time_ms": 12.5,
  "proof_chain": ["action:abc123", "consensus:def456"],
  "metadata": {
    "verification_level": "STANDARD",
    "agents_consulted": 6
  }
}
```

### GET /api/v1/metrics
Get system metrics

**Response:**
```json
{
  "total_evaluations": 10000,
  "approved": 9500,
  "denied": 500,
  "approval_rate": 95.0,
  "average_latency_ms": 15.2,
  "active_agents": 6,
  "version": "5.0.0"
}
```

## Verification Levels
- `BASIC` - Fast, basic checks
- `STANDARD` - Balanced (default)
- `ENHANCED` - More thorough
- `FORMAL` - Formal verification
- `CERTIFIED` - Maximum rigor
