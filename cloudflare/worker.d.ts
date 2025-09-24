/**
 * Cloudflare Worker para Track HS MCP Remote Server
 */
interface Env {
    TRACKHS_API_URL: string;
    TRACKHS_USERNAME: string;
    TRACKHS_PASSWORD: string;
    ENVIRONMENT?: string;
}
declare const _default: {
    fetch(request: Request, env: Env): Promise<Response>;
};
export default _default;
//# sourceMappingURL=worker.d.ts.map