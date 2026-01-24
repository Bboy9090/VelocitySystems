// Phoenix Forge: Main Application UI
// Governance-first, consequence-aware interface

import React, { useState } from 'react';
import { getUIConstraint, formatActionMessage } from '../../../doctrines/phoenix_forge/ui_constraints';

interface Action {
  id: string;
  action: string;
  resource: string;
  requiresApproval: boolean;
  consequences: string[];
}

export const PhoenixForgeApp: React.FC = () => {
  const [selectedAction, setSelectedAction] = useState<Action | null>(null);
  const [justification, setJustification] = useState('');
  const [showConsequences, setShowConsequences] = useState(true);

  const handleActionClick = (action: Action) => {
    const constraint = getUIConstraint(action.action);
    setSelectedAction(action);
    setShowConsequences(constraint.showConsequences);
  };

  const handleExecute = () => {
    if (!selectedAction) return;
    
    const constraint = getUIConstraint(selectedAction.action);
    
    if (constraint.requireConfirmation) {
      if (!justification.trim()) {
        alert('Justification is required for this action.');
        return;
      }
    }

    // Execute action
    console.log('Executing action with justification:', justification);

    if (selectedAction.requiresApproval) {
      alert('This action requires approval. Request submitted.');
      return;
    }

    // Execute action
    console.log('Executing action with justification:', justification);
  };

  return (
    <div className="phoenix-forge-app">
      <header>
        <h1>Phoenix Forge</h1>
        <p className="tagline">Defensible Power. Unbreakable Truth.</p>
      </header>

      <main>
        {selectedAction && (() => {
          const constraint = getUIConstraint(selectedAction.action);
          return (
          <div className="action-details">
            <h2>{selectedAction.action}</h2>
            
            {constraint.showWarning && (
              <div className="warning-banner">
                ⚠️ This action requires careful consideration
              </div>
            )}

            {showConsequences && selectedAction.consequences.length > 0 && (
              <div className="consequences">
                <h3>Consequences:</h3>
                <ul>
                  {selectedAction.consequences.map((c, i) => (
                    <li key={i}>{c}</li>
                  ))}
                </ul>
              </div>
            )}

            <div className="justification-required">
              <label>
                Justification (Required):
                <textarea
                  value={justification}
                  onChange={(e) => setJustification(e.target.value)}
                  placeholder="Explain why this action is necessary..."
                  required
                />
              </label>
            </div>

            <div className="action-buttons">
              <button onClick={handleExecute} className="primary">
                {selectedAction.requiresApproval ? 'Request Approval' : 'Execute'}
              </button>
              <button onClick={() => setSelectedAction(null)} className="secondary">
                Cancel
              </button>
            </div>
          </div>
          );
        })()}

        <div className="audit-panel">
          <h3>Recent Audit Events</h3>
          <p>All actions are logged and auditable.</p>
        </div>
      </main>
    </div>
  );
};
