from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from typing import Dict, List, Any

app = FastAPI(title="CharactAI ML Service", version="1.0.0")

# Pre-trained mock centroids for K-Means to ensure deterministic clustering behavior
# In a production scenario, you would train this on the database and save via joblib
MOCK_CLUSTER_CENTERS = np.array([
    [90, 85, 60, 50, 70], # Cluster 0: Academic & Learning Focused
    [70, 70, 95, 80, 50], # Cluster 1: Technical Innovator
    [80, 80, 80, 80, 80], # Cluster 2: Balanced Achiever
    [60, 50, 60, 90, 95], # Cluster 3: Community & Leadership Oriented
    [50, 60, 75, 50, 90]  # Cluster 4: Creative & Extracurricular
])

ARCHETYPES = {
    0: "Academic Scholar",
    1: "Technical Innovator",
    2: "Balanced Achiever",
    3: "Community Leader",
    4: "Creative All-Rounder"
}

class AssessmentScores(BaseModel):
    academic_engagement: float = 0
    learning_orientation: float = 0
    technical_engagement: float = 0
    leadership: float = 0
    extracurricular_involvement: float = 0

class ClusteringRequest(BaseModel):
    student_id: str
    scores: AssessmentScores

@app.post("/api/ml/cluster")
async def cluster_student(req: ClusteringRequest):
    """
    Takes 12-dimensional or 5-core-dimensional scores and uses K-Means clustering 
    to classify the student's development archetype professionally.
    """
    try:
        # 1. Feature Extraction
        features = np.array([[
            req.scores.academic_engagement,
            req.scores.learning_orientation,
            req.scores.technical_engagement,
            req.scores.leadership,
            req.scores.extracurricular_involvement
        ]])
        
        # 2. Model Initialization (In real app, load trained model)
        kmeans = KMeans(n_clusters=5, n_init=1, random_state=42)
        kmeans.cluster_centers_ = MOCK_CLUSTER_CENTERS
        
        # 3. Prediction
        distances = kmeans.transform(features)
        cluster_id = np.argmin(distances, axis=1)[0]
        confidence = float(1.0 / (1.0 + np.min(distances))) # Simple confidence score based on distance
        
        archetype = ARCHETYPES.get(int(cluster_id), "Emerging Talent")
        
        return {
            "student_id": req.student_id,
            "cluster_id": int(cluster_id),
            "archetype": archetype,
            "confidence_score": round(confidence * 100, 2),
            "algorithm": "K-Means Clustering"
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "ok", "service": "charactai-ml-engine"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
