// Velocity Systems Doctrine: UI Constraints
// Minimal friction, speed-first flows

export interface UIConstraint {
  showWarning: boolean;
  requireConfirmation: boolean;
  showConsequences: boolean;
  frictionLevel: 'low' | 'medium' | 'high';
  language: 'consequence-first' | 'action-first';
}

export const VelocityUIConstraints: Record<string, UIConstraint> = {
  default: {
    showWarning: false,
    requireConfirmation: false,
    showConsequences: false,
    frictionLevel: 'low',
    language: 'action-first',
  },
  'catastrophic.*': {
    showWarning: true,
    requireConfirmation: true,
    showConsequences: false,
    frictionLevel: 'medium',
    language: 'action-first',
  },
};

export function getUIConstraint(action: string): UIConstraint {
  // Match action patterns
  for (const [pattern, constraint] of Object.entries(VelocityUIConstraints)) {
    if (pattern === 'default') continue;
    if (action.match(new RegExp(pattern.replace('*', '.*')))) {
      return constraint;
    }
  }
  return VelocityUIConstraints.default;
}

export function formatActionMessage(action: string, language: 'consequence-first' | 'action-first'): string {
  if (language === 'action-first') {
    return `Execute ${action}?`;
  } else {
    return `This action will ${action}. Are you sure you want to proceed?`;
  }
}
