/**
 * Transporte Server-Sent Events (SSE) para servidores MCP remotos
 * Implementa el protocolo MCP usando SSE como especifica la documentación
 */

export interface SSEMessage {
  id?: string;
  event?: string;
  data: string;
  retry?: number;
}

export interface MCPRequest {
  jsonrpc: '2.0';
  id: string | number;
  method: string;
  params?: any;
}

export interface MCPResponse {
  jsonrpc: '2.0';
  id: string | number;
  result?: any;
  error?: {
    code: number;
    message: string;
    data?: any;
  };
}

export class SSETransport {
  private connections: Map<string, ReadableStreamDefaultController> = new Map();
  private messageQueue: Map<string, SSEMessage[]> = new Map();

  /**
   * Maneja una nueva conexión SSE
   */
  async handleConnection(request: Request, connectionId: string): Promise<Response> {
    const url = new URL(request.url);
    
    // Verificar que es una petición SSE
    const acceptHeader = request.headers.get('accept');
    if (!acceptHeader || !acceptHeader.includes('text/event-stream')) {
      return new Response('Se requiere Accept: text/event-stream', { status: 400 });
    }

    // Crear stream SSE
    const stream = new ReadableStream({
      start: (controller) => {
        // Guardar controlador de la conexión
        this.connections.set(connectionId, controller);
        
        // Enviar mensaje de conexión
        this.sendSSEMessage(controller, {
          event: 'connected',
          data: JSON.stringify({
            connectionId,
            timestamp: new Date().toISOString()
          })
        });

        // Enviar mensajes en cola si los hay
        const queuedMessages = this.messageQueue.get(connectionId);
        if (queuedMessages) {
          queuedMessages.forEach(message => {
            this.sendSSEMessage(controller, message);
          });
          this.messageQueue.delete(connectionId);
        }
      },
      cancel: () => {
        // Limpiar conexión cuando se cierre
        this.connections.delete(connectionId);
        this.messageQueue.delete(connectionId);
      }
    });

    return new Response(stream, {
      headers: {
        'Content-Type': 'text/event-stream',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Cache-Control',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
      }
    });
  }

  /**
   * Envía un mensaje SSE a una conexión específica
   */
  async sendMessage(connectionId: string, message: SSEMessage): Promise<boolean> {
    const controller = this.connections.get(connectionId);
    
    if (!controller) {
      // Si no hay conexión activa, guardar en cola
      if (!this.messageQueue.has(connectionId)) {
        this.messageQueue.set(connectionId, []);
      }
      this.messageQueue.get(connectionId)!.push(message);
      return false;
    }

    try {
      this.sendSSEMessage(controller, message);
      return true;
    } catch (error) {
      console.error('Error enviando mensaje SSE:', error);
      return false;
    }
  }

  /**
   * Envía un mensaje SSE a todas las conexiones activas
   */
  async broadcastMessage(message: SSEMessage): Promise<void> {
    const promises = Array.from(this.connections.keys()).map(connectionId => 
      this.sendMessage(connectionId, message)
    );
    
    await Promise.all(promises);
  }

  /**
   * Procesa una petición MCP y envía la respuesta
   */
  async handleMCPRequest(connectionId: string, request: MCPRequest): Promise<void> {
    try {
      // Aquí se procesaría la petición MCP
      // Por ahora, enviamos una respuesta de ejemplo
      const response: MCPResponse = {
        jsonrpc: '2.0',
        id: request.id,
        result: {
          message: 'Petición MCP procesada',
          method: request.method,
          timestamp: new Date().toISOString()
        }
      };

      await this.sendMessage(connectionId, {
        id: request.id.toString(),
        event: 'mcp-response',
        data: JSON.stringify(response)
      });

    } catch (error) {
      const errorResponse: MCPResponse = {
        jsonrpc: '2.0',
        id: request.id,
        error: {
          code: -32603,
          message: 'Error interno del servidor',
          data: error instanceof Error ? error.message : 'Error desconocido'
        }
      };

      await this.sendMessage(connectionId, {
        id: request.id.toString(),
        event: 'mcp-error',
        data: JSON.stringify(errorResponse)
      });
    }
  }

  /**
   * Cierra una conexión específica
   */
  async closeConnection(connectionId: string): Promise<void> {
    const controller = this.connections.get(connectionId);
    
    if (controller) {
      try {
        controller.close();
      } catch (error) {
        console.error('Error cerrando conexión SSE:', error);
      }
    }
    
    this.connections.delete(connectionId);
    this.messageQueue.delete(connectionId);
  }

  /**
   * Cierra todas las conexiones
   */
  async closeAllConnections(): Promise<void> {
    const promises = Array.from(this.connections.keys()).map(connectionId =>
      this.closeConnection(connectionId)
    );
    
    await Promise.all(promises);
  }

  /**
   * Obtiene el número de conexiones activas
   */
  getActiveConnectionsCount(): number {
    return this.connections.size;
  }

  /**
   * Obtiene información de las conexiones activas
   */
  getConnectionsInfo(): Array<{id: string, queuedMessages: number}> {
    return Array.from(this.connections.keys()).map(connectionId => ({
      id: connectionId,
      queuedMessages: this.messageQueue.get(connectionId)?.length || 0
    }));
  }

  /**
   * Envía un mensaje SSE usando el controlador
   */
  private sendSSEMessage(controller: ReadableStreamDefaultController, message: SSEMessage): void {
    let sseData = '';
    
    if (message.id) {
      sseData += `id: ${message.id}\n`;
    }
    
    if (message.event) {
      sseData += `event: ${message.event}\n`;
    }
    
    if (message.retry) {
      sseData += `retry: ${message.retry}\n`;
    }
    
    sseData += `data: ${message.data}\n\n`;
    
    try {
      controller.enqueue(new TextEncoder().encode(sseData));
    } catch (error) {
      console.error('Error enviando mensaje SSE:', error);
    }
  }

  /**
   * Envía un ping para mantener la conexión activa
   */
  async sendPing(connectionId: string): Promise<boolean> {
    return this.sendMessage(connectionId, {
      event: 'ping',
      data: JSON.stringify({
        timestamp: new Date().toISOString()
      })
    });
  }

  /**
   * Envía un ping a todas las conexiones
   */
  async broadcastPing(): Promise<void> {
    await this.broadcastMessage({
      event: 'ping',
      data: JSON.stringify({
        timestamp: new Date().toISOString()
      })
    });
  }
}
