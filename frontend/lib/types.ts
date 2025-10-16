/**
 * TypeScript interfaces for CARE Assistant frontend.
 *
 * These types define the shape of data exchanged between the frontend
 * and backend API, ensuring type safety throughout the application.
 */

/**
 * Represents a single message in the conversation.
 */
export interface Message {
  /** Unique identifier for the message */
  id: string;
  /** Role of the message sender: 'user' or 'assistant' */
  role: 'user' | 'assistant';
  /** Content of the message */
  content: string;
  /** Timestamp when the message was created */
  timestamp: string;
  /** Optional: Is this a progress message (e.g., "Let me check your claims...") */
  isProgress?: boolean;
}

/**
 * Represents a single entry in the execution trace.
 * Shows which node was executed, when, and what it did.
 */
export interface TraceEntry {
  /** Name of the node that was executed (e.g., "identify_user", "orchestrator") */
  node: string;
  /** ISO 8601 timestamp of when the node executed */
  timestamp: string;
  /** Description of what the node did */
  action: string;
  /** Optional additional details about the node execution */
  details?: Record<string, unknown>;
}

/**
 * User profile data from the insurance system.
 */
export interface UserProfile {
  /** Unique user identifier */
  user_id: string;
  /** User's full name */
  name: string;
  /** User's age */
  age: number;
  /** Insurance plan ID */
  plan_id: string;
  /** Date user became a member */
  member_since: string;
  /** Annual deductible amount */
  deductible_annual: number;
  /** Amount of deductible met */
  deductible_met: number;
  /** Maximum out-of-pocket spending */
  out_of_pocket_max: number;
  /** Amount of out-of-pocket spent */
  out_of_pocket_spent: number;
  /** Number of dependents */
  dependents: number;
  /** Additional notes */
  notes?: string;
}

/**
 * Conversation state maintained by the backend.
 * This is a subset of the full LangGraph state, containing only
 * what the frontend needs to display.
 */
export interface ConversationState {
  /** Currently identified user ID */
  user_id: string | null;
  /** Full user profile data (loaded after identification) */
  user_profile: UserProfile | null;
  /** Results from tool calls in the current turn */
  tool_results: Record<string, unknown>;
}

/**
 * Request body for POST /api/chat endpoint.
 */
export interface ChatRequest {
  /** Session ID for maintaining conversation state */
  session_id: string | null;
  /** User's message */
  message: string;
}

/**
 * Response from POST /api/chat endpoint.
 */
export interface ChatResponse {
  /** Session ID (returned on first message, used for subsequent requests) */
  session_id: string;
  /** AI's response message */
  response: string;
  /** Execution trace for this turn */
  trace: TraceEntry[];
  /** Current conversation state */
  state: ConversationState;
  /** Optional: Progress messages to display while processing */
  progress_messages?: string[];
}

/**
 * Error response from the API.
 */
export interface APIError {
  /** Error message to display to the user */
  detail: string;
  /** HTTP status code */
  status_code: number;
}
