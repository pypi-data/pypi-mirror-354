/** @type {Record<string, wsClient>} */
export const clients: Record<string, wsClient>;
export type wsClient = import("ws").WebSocket;
export type WebSocketClass = typeof import("ws").WebSocket;
/**
 * WebSocketClient class that handles WebSocket connection, message sending, and automatic disconnection.
 */
export class WebSocketClient {
    /**
     * @param {string} url
     * @param {{ isDisconnectedAfterMessage: boolean }} options
     */
    constructor(url: string, options: {
        isDisconnectedAfterMessage: boolean;
    });
    /** @type {string} */
    url: string;
    /** @type {boolean} */
    isDisconnectedAfterMessage: boolean;
    /** @type {wsClient | null} */
    get instance(): wsClient | null;
    get isConnected(): boolean;
    /**
     * Sends messageArray through websocket connection
     * @async
     * @param {Int8Array} messageArray
     * @returns {Promise<Int8Array>}
     */
    send(messageArray: Int8Array): Promise<Int8Array>;
    /**
     * Disconnects the WebSocket by terminating the connection.
     */
    disconnect(): void;
    /**
     * Connects to the WebSocket server.
     * @private
     * @async
     * @returns {Promise<wsClient>} - A promise that resolves when the connection is established.
     */
    private _connect;
}
