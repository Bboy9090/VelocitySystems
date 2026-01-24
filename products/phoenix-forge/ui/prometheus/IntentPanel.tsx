// Phoenix Forge: Prometheus Intent Panel
// Enforces intent core requirements

import React, { useState } from 'react';
import { IntentCore } from '../../../../universal-core/prometheus/loader';

interface IntentPanelProps {
  intentCore: IntentCore;
  onChange: (intentCore: IntentCore) => void;
  doctrine: 'phoenix_forge' | 'velocity_systems';
}

export const IntentPanel: React.FC<IntentPanelProps> = ({ intentCore, onChange, doctrine }) => {
  const [objective, setObjective] = useState(intentCore.objective);
  const [stakes, setStakes] = useState(intentCore.stakes_if_failure);
  const [success, setSuccess] = useState(intentCore.definition_of_success);

  const handleChange = () => {
    onChange({
      ...intentCore,
      objective,
      stakes_if_failure: stakes,
      definition_of_success: success,
    });
  };

  const isValid = objective.trim().length > 0 && stakes.trim().length > 0 && success.trim().length > 0;

  return (
    <div className="intent-panel">
      <h3>Intent Core</h3>
      {doctrine === 'phoenix_forge' && (
        <div className="warning">
          ⚠️ Phoenix requires explicit objective, stakes, and success criteria
        </div>
      )}
      
      <label>
        Objective (Required):
        <textarea
          value={objective}
          onChange={(e) => {
            setObjective(e.target.value);
            handleChange();
          }}
          placeholder="Single, measurable objective..."
          required
        />
      </label>

      <label>
        Stakes if Failure (Required):
        <textarea
          value={stakes}
          onChange={(e) => {
            setStakes(e.target.value);
            handleChange();
          }}
          placeholder="Real-world impact if this fails..."
          required
        />
      </label>

      <label>
        Definition of Success (Required):
        <textarea
          value={success}
          onChange={(e) => {
            setSuccess(e.target.value);
            handleChange();
          }}
          placeholder="Binary, testable success criteria..."
          required
        />
      </label>

      {!isValid && (
        <div className="error">
          All fields are required. Cannot generate prompt until complete.
        </div>
      )}
    </div>
  );
};
