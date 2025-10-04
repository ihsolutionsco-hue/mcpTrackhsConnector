/**
 * Test sequencer para ordenar la ejecución de tests
 */

import { Sequencer } from '@jest/test-sequencer';

class CustomSequencer extends Sequencer {
  sort(tests) {
    // Ordenar tests por tipo y prioridad
    const testOrder = [
      // Tests unitarios primero (más rápidos)
      'unit',
      // Tests de integración después
      'integration', 
      // Tests E2E al final (más lentos)
      'e2e'
    ];

    return tests.sort((testA, testB) => {
      const getTestType = (test) => {
        if (test.path.includes('/unit/')) return 'unit';
        if (test.path.includes('/integration/')) return 'integration';
        if (test.path.includes('/e2e/')) return 'e2e';
        return 'other';
      };

      const typeA = getTestType(testA);
      const typeB = getTestType(testB);

      const indexA = testOrder.indexOf(typeA);
      const indexB = testOrder.indexOf(typeB);

      // Si ambos están en el orden definido, ordenar por índice
      if (indexA !== -1 && indexB !== -1) {
        return indexA - indexB;
      }

      // Si solo uno está en el orden, ese va primero
      if (indexA !== -1) return -1;
      if (indexB !== -1) return 1;

      // Si ninguno está en el orden, ordenar alfabéticamente
      return testA.path.localeCompare(testB.path);
    });
  }
}

export default CustomSequencer;
