/**
 * Configuración de métricas de testing
 */

export interface TestingMetrics {
  coverage: {
    global: {
      branches: number;
      functions: number;
      lines: number;
      statements: number;
    };
    core: {
      branches: number;
      functions: number;
      lines: number;
      statements: number;
    };
    tools: {
      branches: number;
      functions: number;
      lines: number;
      statements: number;
    };
    types: {
      branches: number;
      functions: number;
      lines: number;
      statements: number;
    };
  };
  performance: {
    unitTests: {
      maxDuration: number; // en ms
      averageDuration: number; // en ms
    };
    integrationTests: {
      maxDuration: number; // en ms
      averageDuration: number; // en ms
    };
    e2eTests: {
      maxDuration: number; // en ms
      averageDuration: number; // en ms
    };
  };
  quality: {
    testCount: {
      unit: number;
      integration: number;
      e2e: number;
      total: number;
    };
    testPassRate: number; // porcentaje
    flakyTests: number; // número de tests inestables
  };
}

export const defaultMetrics: TestingMetrics = {
  coverage: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    core: {
      branches: 85,
      functions: 85,
      lines: 85,
      statements: 85
    },
    tools: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80
    },
    types: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  },
  performance: {
    unitTests: {
      maxDuration: 1000, // 1 segundo
      averageDuration: 500 // 0.5 segundos
    },
    integrationTests: {
      maxDuration: 5000, // 5 segundos
      averageDuration: 2000 // 2 segundos
    },
    e2eTests: {
      maxDuration: 30000, // 30 segundos
      averageDuration: 10000 // 10 segundos
    }
  },
  quality: {
    testCount: {
      unit: 0,
      integration: 0,
      e2e: 0,
      total: 0
    },
    testPassRate: 95, // 95% de tests deben pasar
    flakyTests: 0 // 0 tests inestables permitidos
  }
};

export const testingGoals = {
  shortTerm: {
    coverage: 80,
    testCount: 50,
    passRate: 90
  },
  mediumTerm: {
    coverage: 85,
    testCount: 100,
    passRate: 95
  },
  longTerm: {
    coverage: 90,
    testCount: 200,
    passRate: 98
  }
};

export function validateMetrics(current: Partial<TestingMetrics>, goals = testingGoals.mediumTerm): boolean {
  const coverage = current.coverage?.global;
  const quality = current.quality;

  if (!coverage || !quality) {
    return false;
  }

  return (
    coverage.lines >= goals.coverage &&
    coverage.functions >= goals.coverage &&
    coverage.branches >= goals.coverage &&
    coverage.statements >= goals.coverage &&
    quality.testPassRate >= goals.passRate
  );
}

export function generateMetricsReport(metrics: TestingMetrics): string {
  return `
# Reporte de Métricas de Testing

## Cobertura de Código
- **Global**: ${metrics.coverage.global.lines}% líneas, ${metrics.coverage.global.functions}% funciones
- **Core**: ${metrics.coverage.core.lines}% líneas, ${metrics.coverage.core.functions}% funciones
- **Tools**: ${metrics.coverage.tools.lines}% líneas, ${metrics.coverage.tools.functions}% funciones
- **Types**: ${metrics.coverage.types.lines}% líneas, ${metrics.coverage.types.functions}% funciones

## Performance
- **Unit Tests**: ${metrics.performance.unitTests.averageDuration}ms promedio
- **Integration Tests**: ${metrics.performance.integrationTests.averageDuration}ms promedio
- **E2E Tests**: ${metrics.performance.e2eTests.averageDuration}ms promedio

## Calidad
- **Total Tests**: ${metrics.quality.testCount.total}
- **Pass Rate**: ${metrics.quality.testPassRate}%
- **Flaky Tests**: ${metrics.quality.flakyTests}
  `;
}
