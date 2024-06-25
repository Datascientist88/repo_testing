import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import axios from "axios";

function CaseAnalysis() {
  const { transcript } = useParams();
  const [analysisResult, setAnalysisResult] = useState("");
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAnalysisResult = async () => {
      try {
        const response = await axios.post(
          "http://localhost:5001/api/generate",
          { input: decodeURIComponent(transcript) }
        );
        setAnalysisResult(response.data.response);
      } catch (error) {
        console.error("Error during case analysis:", error);
        setError("An error occurred while analyzing the case.");
      }
    };

    fetchAnalysisResult();
  }, [transcript]);

  const handleMedicalTranscriptionClick = () => {
    navigate("/");
  };

  return (
    <div className="case-analysis-page">
      <h1>Case Analysis</h1>
      <div className="case-analysis-content">
        <h2>Transcript:</h2>
        <pre>{decodeURIComponent(transcript)}</pre>
        <h2>Analysis Result:</h2>
        {error ? <pre>{error}</pre> : <pre>{analysisResult}</pre>}
      </div>
      <button onClick={handleMedicalTranscriptionClick}>
        Medical Transcription
      </button>
    </div>
  );
}

export default CaseAnalysis;
