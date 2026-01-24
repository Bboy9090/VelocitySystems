// Velocity Systems: Prometheus Action Panel
// Minimal friction, speed-first interface

import React, { useState } from 'react';
import { IntentCore } from '../../../../universal-core/prometheus/loader';

interface ActionPanelProps {
  intentCore: IntentCore;
  onChange: (intentCore: IntentCore) => void;
}

export const ActionPanel: React.FC<ActionPanelProps> = ({ intentCore, onChange }) => {
  const [objective, setObjective] = useState(intentCore.objective);

  const handleChange = () => {
    onChange({
      ...intentCore,
      objective,
      // Velocity: minimal required fields
      stakes_if_failure: intentCore.stakes_if_failure || "Lost momentum",
      definition_of_success: intentCore.definition_of_success || "Immediate execution",
    });
  };

  return (
    <div className="action-panel velocity-minimal">
      <h3>Action Path</h3>
      
      <label>
        What needs to happen?
        <input
          type="text"
          value={objective}
          onChange={(e) => {
            setObjective(e.target.value);
            handleChange();
          }}
          placeholder="Execute..."
          className="velocity-input"
        />
      </label>

      <button 
        onClick={() => onChange({ ...intentCore, objective })} 
        className="velocity-execute"
        disabled={!objective.trim()}
      >
        Execute
      </button>
    </div>
  );
};
