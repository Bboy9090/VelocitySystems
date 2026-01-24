// Velocity Systems: Main Application UI
// Speed-first, frictionless interface

import React, { useState } from 'react';
import { getUIConstraint, formatActionMessage } from '../../../doctrines/velocity_systems/ui_constraints';

interface Action {
  id: string;
  action: string;
  resource: string;
  oneClick: boolean;
}

export const VelocityApp: React.FC = () => {
  const [actions, setActions] = useState<Action[]>([]);
  const [executing, setExecuting] = useState<string | null>(null);

  const handleQuickAction = (action: Action) => {
    const constraint = getUIConstraint(action.action);
    
    if (constraint.requireConfirmation && !action.oneClick) {
      // Minimal confirmation for non-catastrophic actions
      if (window.confirm(formatActionMessage(action.action, constraint.language))) {
        executeAction(action);
      }
    } else {
      // One-click execution
      executeAction(action);
    }
  };

  const executeAction = (action: Action) => {
    setExecuting(action.id);
    // Execute immediately - no approval, no justification
    console.log('Executing action:', action.action);
    setTimeout(() => {
      setExecuting(null);
    }, 500);
  };

  return (
    <div className="velocity-app">
      <header>
        <h1>Velocity Systems</h1>
        <p className="tagline">Move Fast. Stay in Control.</p>
      </header>

      <main>
        <div className="quick-actions">
          <h2>Quick Actions</h2>
          <div className="action-grid">
            {actions.map((action) => (
              <button
                key={action.id}
                className={`action-button ${executing === action.id ? 'executing' : ''}`}
                onClick={() => handleQuickAction(action)}
                disabled={executing === action.id}
              >
                {action.action}
                {executing === action.id && <span className="spinner">⚡</span>}
              </button>
            ))}
          </div>
        </div>

        <div className="status-bar">
          <span>Ready</span>
          <span className="status-indicator active"></span>
        </div>
      </main>
    </div>
  );
};
