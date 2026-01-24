// Phoenix Forge Doctrine: UI Constraints
// Enforces friction, warnings, and consequence-first language

export interface UIConstraint {
  showWarning: boolean;
  requireConfirmation: boolean;
  showConsequences: boolean;
  frictionLevel: 'low' | 'medium' | 'high';
  language: 'consequence-first' | 'action-first';
}

export const PhoenixForgeUIConstraints: Record<string, UIConstraint> = {
  default: {
    showWarning: true,
    requireConfirmation: true,
    showConsequences: true,
    frictionLevel: 'high',
    language: 'consequence-first',
  },
  'admin.*': {
    showWarning: true,
    requireConfirmation: true,
    showConsequences: true,
    frictionLevel: 'high',
    language: 'consequence-first',
  },
  'delete.*': {
    showWarning: true,
    requireConfirmation: true,
    showConsequences: true,
    frictionLevel: 'high',
    language: 'consequence-first',
  },
};

export function getUIConstraint(action: string): UIConstraint {
  // Match action patterns
  for (const [pattern, constraint] of Object.entries(PhoenixForgeUIConstraints)) {
    if (pattern === 'default') continue;
    if (action.match(new RegExp(pattern.replace('*', '.*')))) {
      return constraint;
    }
  }
  return PhoenixForgeUIConstraints.default;
}

export function formatActionMessage(action: string, language: 'consequence-first' | 'action-first'): string {
  if (language === 'consequence-first') {
    return `This action will ${action}. Are you sure you want to proceed?`;
  } else {
    return `Execute ${action}?`;
  }
}
