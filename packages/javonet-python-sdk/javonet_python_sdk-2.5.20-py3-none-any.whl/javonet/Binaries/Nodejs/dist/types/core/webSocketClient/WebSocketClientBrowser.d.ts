/**
 * @typedef {object} Options
 * @property {boolean} [isDisconnectedAfterMessage]
 */
/** @type {Record<string, WebSocket>} */
export const clients: Record<string, WebSocket>;
export type Options = {
    isDisconnectedAfterMessage?: boolean | undefined;
};
/**
 * WebSocketClient class that handles WebSocket connection, message sending, and automatic disconnection.
 */
export class WebSocketClientBrowser {
    /**
     * @param {string} url
     * @param {Options} [options]
     */
    constructor(url: string, options?: Options);
    /** @type {string} */
    url: string;
    /** @type {boolean} */
    isDisconnectedAfterMessage: boolean;
    /** @type {WebSocket | null} */
    get instance(): WebSocket | null;
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
     * @returns {Promise<WebSocket>}
     */
    private _connect;
    /**
     * Sends the data to the WebSocket server and listens for a response.
     * @private
     * @param {WebSocket} client
     * @param {Int8Array} data
     * @param {(value: Int8Array) => void} resolve
     * @param {(reason?: any) => void} reject
     */
    private _sendMessage;
}
