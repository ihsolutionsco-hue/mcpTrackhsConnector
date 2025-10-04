#!/usr/bin/env tsx

/**
 * Script de configuración automática para Vercel
 * Track HS MCP Connector
 * 
 * Este script automatiza la configuración del proyecto para Vercel
 * incluyendo verificación de dependencias, configuración de archivos
 * y validación del setup.
 */

import { execSync } from 'child_process';
import { writeFileSync, existsSync, readFileSync } from 'fs';
import { join } from 'path';

interface SetupResult {
  success: boolean;
  steps: string[];
  errors: string[];
  warnings: string[];
}

class VercelSetup {
  private result: SetupResult = {
    success: true,
    steps: [],
    errors: [],
    warnings: []
  };

  private log(message: string, type: 'info' | 'success' | 'warning' | 'error' = 'info') {
    const timestamp = new Date().toISOString();
    const prefix = {
      info: '📋',
      success: '✅',
      warning: '⚠️',
      error: '❌'
    }[type];
    
    console.log(`${prefix} [${timestamp}] ${message}`);
    
    this.result.steps.push(message);
    if (type === 'error') this.result.errors.push(message);
    if (type === 'warning') this.result.warnings.push(message);
  }

  private async checkVercelCLI(): Promise<boolean> {
    try {
      this.log('Verificando Vercel CLI...');
      execSync('vercel --version', { stdio: 'pipe' });
      this.log('Vercel CLI encontrado', 'success');
      return true;
    } catch {
      this.log('Vercel CLI no encontrado, instalando...', 'warning');
      try {
        execSync('npm install -g vercel@latest', { stdio: 'inherit' });
        this.log('Vercel CLI instalado correctamente', 'success');
        return true;
      } catch (error) {
        this.log(`Error instalando Vercel CLI: ${error}`, 'error');
        return false;
      }
    }
  }

  private async checkNodeVersion(): Promise<boolean> {
    try {
      const version = execSync('node --version', { encoding: 'utf8' }).trim();
      const majorVersion = parseInt(version.replace('v', '').split('.')[0]);
      
      if (majorVersion >= 18) {
        this.log(`Node.js ${version} - Compatible`, 'success');
        return true;
      } else {
        this.log(`Node.js ${version} - Se requiere versión 18+`, 'error');
        return false;
      }
    } catch {
      this.log('Node.js no encontrado', 'error');
      return false;
    }
  }

  private async checkDependencies(): Promise<boolean> {
    try {
      this.log('Verificando dependencias...');
      
      if (!existsSync('package.json')) {
        this.log('package.json no encontrado', 'error');
        return false;
      }

      const packageJson = JSON.parse(readFileSync('package.json', 'utf8'));
      
      // Verificar dependencias críticas
      const criticalDeps = ['@modelcontextprotocol/sdk', 'dotenv', 'tslib'];
      const missingDeps = criticalDeps.filter(dep => !packageJson.dependencies?.[dep]);
      
      if (missingDeps.length > 0) {
        this.log(`Dependencias faltantes: ${missingDeps.join(', ')}`, 'error');
        return false;
      }

      this.log('Dependencias verificadas', 'success');
      return true;
    } catch (error) {
      this.log(`Error verificando dependencias: ${error}`, 'error');
      return false;
    }
  }

  private async createVercelIgnore(): Promise<boolean> {
    try {
      const vercelIgnorePath = join(process.cwd(), '.vercelignore');
      
      if (existsSync(vercelIgnorePath)) {
        this.log('.vercelignore ya existe', 'info');
        return true;
      }

      const vercelIgnoreContent = `# Dependencies
node_modules/
npm-debug.log*

# Build outputs
dist/
*.tsbuildinfo

# Environment files
.env
.env.local
.env.production

# IDE
.vscode/
.idea/

# OS
.DS_Store
Thumbs.db

# Git
.git/
.gitignore

# Tests
coverage/
.nyc_output/

# Logs
logs/
*.log

# Vercel
.vercel/
`;

      writeFileSync(vercelIgnorePath, vercelIgnoreContent);
      this.log('.vercelignore creado', 'success');
      return true;
    } catch (error) {
      this.log(`Error creando .vercelignore: ${error}`, 'error');
      return false;
    }
  }

  private async checkTypeScriptConfig(): Promise<boolean> {
    try {
      const tsconfigPath = join(process.cwd(), 'tsconfig.json');
      
      if (!existsSync(tsconfigPath)) {
        this.log('tsconfig.json no encontrado', 'error');
        return false;
      }

      const tsconfig = JSON.parse(readFileSync(tsconfigPath, 'utf8'));
      
      // Verificar configuraciones críticas
      if (!tsconfig.compilerOptions?.target || !tsconfig.compilerOptions?.module) {
        this.log('tsconfig.json incompleto', 'warning');
      }

      this.log('TypeScript configurado', 'success');
      return true;
    } catch (error) {
      this.log(`Error verificando TypeScript: ${error}`, 'error');
      return false;
    }
  }

  private async testBuild(): Promise<boolean> {
    try {
      this.log('Probando build del proyecto...');
      execSync('npm run build', { stdio: 'inherit' });
      
      // Verificar que dist/ existe
      if (existsSync('dist')) {
        this.log('Build exitoso - dist/ creado', 'success');
        return true;
      } else {
        this.log('Build fallido - dist/ no encontrado', 'error');
        return false;
      }
    } catch (error) {
      this.log(`Error en build: ${error}`, 'error');
      return false;
    }
  }

  private async checkEnvironmentFile(): Promise<boolean> {
    try {
      const envExamplePath = join(process.cwd(), 'env.example');
      
      if (!existsSync(envExamplePath)) {
        this.log('env.example no encontrado', 'warning');
        return true; // No es crítico
      }

      this.log('Archivo de variables de entorno encontrado', 'success');
      return true;
    } catch (error) {
      this.log(`Error verificando archivo de entorno: ${error}`, 'error');
      return false;
    }
  }

  private async checkGitHubActions(): Promise<boolean> {
    try {
      const workflowPath = join(process.cwd(), '.github/workflows/deploy.yml');
      
      if (!existsSync(workflowPath)) {
        this.log('GitHub Actions no configurado', 'warning');
        return true; // No es crítico para el setup básico
      }

      this.log('GitHub Actions configurado', 'success');
      return true;
    } catch (error) {
      this.log(`Error verificando GitHub Actions: ${error}`, 'error');
      return false;
    }
  }

  private async generateSetupReport(): Promise<void> {
    const reportPath = join(process.cwd(), 'vercel-setup-report.json');
    const report = {
      timestamp: new Date().toISOString(),
      result: this.result,
      nextSteps: [
        '1. Ejecutar: vercel login',
        '2. Ejecutar: vercel --prod',
        '3. Configurar variables de entorno en Vercel Dashboard',
        '4. Configurar GitHub Secrets para CI/CD',
        '5. Probar el health check: https://tu-app.vercel.app/api/health'
      ],
      documentation: 'docs/VERCEL_DEPLOYMENT.md'
    };

    writeFileSync(reportPath, JSON.stringify(report, null, 2));
    this.log(`Reporte generado: ${reportPath}`, 'info');
  }

  public async run(): Promise<void> {
    console.log('🚀 Configurando Track HS MCP Connector para Vercel...\n');

    // Verificaciones críticas
    const checks = [
      { name: 'Node.js Version', fn: () => this.checkNodeVersion() },
      { name: 'Dependencies', fn: () => this.checkDependencies() },
      { name: 'TypeScript Config', fn: () => this.checkTypeScriptConfig() },
      { name: 'Build Test', fn: () => this.testBuild() }
    ];

    // Verificaciones opcionales
    const optionalChecks = [
      { name: 'Vercel CLI', fn: () => this.checkVercelCLI() },
      { name: 'Environment File', fn: () => this.checkEnvironmentFile() },
      { name: 'GitHub Actions', fn: () => this.checkGitHubActions() }
    ];

    // Crear archivos necesarios
    await this.createVercelIgnore();

    // Ejecutar verificaciones críticas
    for (const check of checks) {
      const success = await check.fn();
      if (!success) {
        this.result.success = false;
      }
    }

    // Ejecutar verificaciones opcionales
    for (const check of optionalChecks) {
      await check.fn();
    }

    // Generar reporte
    await this.generateSetupReport();

    // Mostrar resumen
    console.log('\n📊 Resumen de Configuración:');
    console.log(`✅ Pasos completados: ${this.result.steps.length}`);
    console.log(`⚠️ Advertencias: ${this.result.warnings.length}`);
    console.log(`❌ Errores: ${this.result.errors.length}`);

    if (this.result.success) {
      console.log('\n🎉 ¡Configuración completada exitosamente!');
      console.log('\n📋 Próximos pasos:');
      console.log('1. Ejecutar: vercel login');
      console.log('2. Ejecutar: vercel --prod');
      console.log('3. Configurar variables de entorno en Vercel Dashboard');
      console.log('4. Configurar GitHub Secrets para CI/CD');
      console.log('\n🔗 Documentación: docs/VERCEL_DEPLOYMENT.md');
    } else {
      console.log('\n❌ Configuración fallida. Revisa los errores arriba.');
      process.exit(1);
    }
  }
}

// Ejecutar setup
async function main() {
  const setup = new VercelSetup();
  await setup.run();
}

main().catch(console.error);
