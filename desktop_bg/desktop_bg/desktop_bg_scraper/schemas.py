computer_schema = {
    "type": "object",
    "properties": {
        "processor": {"type": "string"},
        "gpu": {"type": "string"},
        "motherboard": {"type": "string"},
        "ram": {"type": "string"},
    },
    "required": ["processor", "gpu", "motherboard", "ram"]
}