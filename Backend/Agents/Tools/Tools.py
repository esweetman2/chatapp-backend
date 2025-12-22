from Backend.Agents.Tools.GoogleSheets import GoogleSheets

# google_sheet_name="Zermatt Honeymoon", worksheet="Schedule"
tools = [
    { 
        "type": 
        "web_search_preview" 
    },
    {
        "type": "function",
        "name": "read_google_sheet",
        "description": "You MUST use this tool when users ask for information regarding our schedule for the honey moon trip. The google sheet is Zermatt Honeymoon and the worksheet is Schedule. Read the google sheet and provide the information the user requests.",
        "parameters": {
            "type": "object",
            "properties": {
                "google_sheet_name": {
                    "type": "string",
                    "description": "The google sheet name.",
                },
                "worksheet": {
                    "type": "string",
                    "description": "The worksheet name.",
                },
            },
            "required": ["google_sheet_name", "worksheet"],
        },
    },
]

# CREATE TABLE agenttools (
#     id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
#     tool_type TEXT NOT NULL,            -- web_search_preview | function
#     name TEXT,                          -- NULL for non-function tools
#     description TEXT,
#     parameters JSONB,                   -- function schema
#     enabled BOOLEAN DEFAULT TRUE,
#     created_at TIMESTAMP DEFAULT NOW(),
#     CONSTRAINT unique_tool UNIQUE (tool_type, name)
# );

# CREATE TABLE agent_tools (
#     agent_id INT REFERENCES agents(id) ON DELETE CASCADE,
#     tool_id INT REFERENCES tools(id) ON DELETE CASCADE,
#     PRIMARY KEY (agent_id, tool_id)
# );
