/**
 * Manejador de autenticación OAuth para servidores MCP remotos
 * Implementa el flujo OAuth 2.0 requerido por Claude
 */

export interface OAuthConfig {
  clientId: string;
  clientSecret: string;
  redirectUri: string;
  authorizationUrl: string;
  tokenUrl: string;
  scope: string;
}

export interface OAuthToken {
  access_token: string;
  refresh_token?: string;
  token_type: string;
  expires_in: number;
  scope: string;
  created_at: number;
}

export interface OAuthUser {
  id: string;
  email: string;
  name: string;
  [key: string]: any;
}

export class OAuthHandler {
  private config: OAuthConfig;
  private tokens: Map<string, OAuthToken> = new Map();
  private users: Map<string, OAuthUser> = new Map();

  constructor(config: OAuthConfig) {
    this.config = config;
  }

  /**
   * Maneja la petición de autorización OAuth
   * Endpoint: /auth/authorize
   */
  async handleAuthorization(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      const responseType = url.searchParams.get('response_type');
      const clientId = url.searchParams.get('client_id');
      const redirectUri = url.searchParams.get('redirect_uri');
      const scope = url.searchParams.get('scope');
      const state = url.searchParams.get('state');

      // Validar parámetros requeridos
      if (responseType !== 'code') {
        return this.createErrorResponse('invalid_request', 'response_type debe ser "code"');
      }

      if (clientId !== this.config.clientId) {
        return this.createErrorResponse('invalid_client', 'client_id inválido');
      }

      if (redirectUri !== this.config.redirectUri) {
        return this.createErrorResponse('invalid_request', 'redirect_uri no coincide');
      }

      // Generar código de autorización
      const authCode = this.generateAuthCode();
      
      // Simular usuario (en producción, esto vendría de una base de datos)
      const user: OAuthUser = {
        id: 'user_123',
        email: 'usuario@trackhs.com',
        name: 'Usuario Track HS'
      };

      // Guardar código de autorización temporalmente
      this.tokens.set(authCode, {
        access_token: '',
        token_type: 'Bearer',
        expires_in: 0,
        scope: scope || this.config.scope,
        created_at: Date.now()
      });

      this.users.set(authCode, user);

      // Redirigir a Claude con el código de autorización
      const redirectUrl = new URL(redirectUri);
      redirectUrl.searchParams.set('code', authCode);
      if (state) {
        redirectUrl.searchParams.set('state', state);
      }

      return Response.redirect(redirectUrl.toString(), 302);

    } catch (error) {
      console.error('Error en autorización OAuth:', error);
      return this.createErrorResponse('server_error', 'Error interno del servidor');
    }
  }

  /**
   * Maneja el intercambio de código por token
   * Endpoint: /auth/token
   */
  async handleTokenExchange(request: Request): Promise<Response> {
    try {
      const body = await request.json();
      const { grant_type, code, redirect_uri, client_id, client_secret } = body;

      // Validar parámetros
      if (grant_type !== 'authorization_code') {
        return this.createErrorResponse('unsupported_grant_type', 'grant_type debe ser "authorization_code"');
      }

      if (client_id !== this.config.clientId || client_secret !== this.config.clientSecret) {
        return this.createErrorResponse('invalid_client', 'Credenciales de cliente inválidas');
      }

      if (redirect_uri !== this.config.redirectUri) {
        return this.createErrorResponse('invalid_request', 'redirect_uri no coincide');
      }

      // Verificar código de autorización
      const tokenData = this.tokens.get(code);
      if (!tokenData) {
        return this.createErrorResponse('invalid_grant', 'Código de autorización inválido o expirado');
      }

      // Generar tokens de acceso
      const accessToken = this.generateAccessToken();
      const refreshToken = this.generateRefreshToken();

      const oauthToken: OAuthToken = {
        access_token: accessToken,
        refresh_token: refreshToken,
        token_type: 'Bearer',
        expires_in: 3600, // 1 hora
        scope: tokenData.scope,
        created_at: Date.now()
      };

      // Guardar token
      this.tokens.set(accessToken, oauthToken);
      
      // Limpiar código de autorización
      this.tokens.delete(code);

      return new Response(JSON.stringify(oauthToken), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'POST',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization'
        }
      });

    } catch (error) {
      console.error('Error en intercambio de token:', error);
      return this.createErrorResponse('server_error', 'Error interno del servidor');
    }
  }

  /**
   * Maneja el callback de OAuth
   * Endpoint: /auth/callback
   */
  async handleCallback(request: Request): Promise<Response> {
    try {
      const url = new URL(request.url);
      const code = url.searchParams.get('code');
      const state = url.searchParams.get('state');

      if (!code) {
        return new Response('Código de autorización no encontrado', { status: 400 });
      }

      // Verificar que el código existe
      const user = this.users.get(code);
      if (!user) {
        return new Response('Código de autorización inválido', { status: 400 });
      }

      return new Response(JSON.stringify({
        success: true,
        message: 'Autenticación exitosa',
        user: user
      }), {
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        }
      });

    } catch (error) {
      console.error('Error en callback OAuth:', error);
      return new Response('Error interno del servidor', { status: 500 });
    }
  }

  /**
   * Valida un token de acceso
   */
  async validateToken(token: string): Promise<boolean> {
    const tokenData = this.tokens.get(token);
    if (!tokenData) {
      return false;
    }

    // Verificar expiración
    const now = Date.now();
    const expiresAt = tokenData.created_at + (tokenData.expires_in * 1000);
    
    if (now > expiresAt) {
      this.tokens.delete(token);
      return false;
    }

    return true;
  }

  /**
   * Obtiene información del usuario desde el token
   */
  async getUserFromToken(token: string): Promise<OAuthUser | null> {
    if (!await this.validateToken(token)) {
      return null;
    }

    // En una implementación real, esto vendría de la base de datos
    return {
      id: 'user_123',
      email: 'usuario@trackhs.com',
      name: 'Usuario Track HS'
    };
  }

  /**
   * Refresca un token de acceso
   */
  async refreshToken(refreshToken: string): Promise<OAuthToken | null> {
    // Buscar token por refresh_token
    for (const [accessToken, tokenData] of this.tokens.entries()) {
      if (tokenData.refresh_token === refreshToken) {
        // Generar nuevo token
        const newAccessToken = this.generateAccessToken();
        const newRefreshToken = this.generateRefreshToken();

        const newToken: OAuthToken = {
          access_token: newAccessToken,
          refresh_token: newRefreshToken,
          token_type: 'Bearer',
          expires_in: 3600,
          scope: tokenData.scope,
          created_at: Date.now()
        };

        // Actualizar tokens
        this.tokens.delete(accessToken);
        this.tokens.set(newAccessToken, newToken);

        return newToken;
      }
    }

    return null;
  }

  /**
   * Maneja la petición principal de OAuth
   */
  async handleRequest(request: Request): Promise<Response> {
    const url = new URL(request.url);
    const pathname = url.pathname;

    // CORS headers
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept'
    };

    // Manejar preflight
    if (request.method === 'OPTIONS') {
      return new Response(null, { headers: corsHeaders });
    }

    // Routing de endpoints OAuth
    if (pathname === '/auth/authorize' && request.method === 'GET') {
      return this.handleAuthorization(request);
    }

    if (pathname === '/auth/token' && request.method === 'POST') {
      return this.handleTokenExchange(request);
    }

    if (pathname === '/auth/callback' && request.method === 'GET') {
      return this.handleCallback(request);
    }

    return new Response('Endpoint OAuth no encontrado', { 
      status: 404, 
      headers: corsHeaders 
    });
  }

  /**
   * Genera un código de autorización único
   */
  private generateAuthCode(): string {
    return 'auth_' + Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  }

  /**
   * Genera un token de acceso único
   */
  private generateAccessToken(): string {
    return 'access_' + Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  }

  /**
   * Genera un token de refresh único
   */
  private generateRefreshToken(): string {
    return 'refresh_' + Math.random().toString(36).substring(2, 15) + 
           Math.random().toString(36).substring(2, 15);
  }

  /**
   * Crea una respuesta de error OAuth
   */
  private createErrorResponse(error: string, description: string): Response {
    return new Response(JSON.stringify({
      error,
      error_description: description
    }), {
      status: 400,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      }
    });
  }
}
