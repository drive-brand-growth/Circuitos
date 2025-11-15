export type AgentRunSummary = {
  id: string;
  mode: string;
  evaluated: number;
  acted: number;
  dry_run: boolean;
  status: string;
  started_at: string;
  completed_at: string;
  config_version?: string | null;
  notes?: string | null;
};

export type AgentActionRecord = {
  id: string;
  run_id: string;
  type: string;
  status: string;
  payload: Record<string, unknown>;
  created_at: string;
};

export type AgentRunDetail = AgentRunSummary & {
  actions: AgentActionRecord[];
};

export type AgentRunResponse = {
  run_id: string;
  evaluated: number;
  acted: number;
  outcomes: Array<{ type: string; status: string; payload: Record<string, unknown> }>;
  started_at: string;
  completed_at: string;
};
