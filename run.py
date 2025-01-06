#!/usr/bin/env python3
"""
this will start the main application
"""

import uvicorn
from src.app import main 

print("Hihi, from the voiceTool devs\n\n")


if __name__ == "__main__":
    main()
    uvicorn.run("src.app:app",reload=True)
