from typing import Dict, List


LOCAL_GUIDES: Dict[str, str] = {
    "youtube upload": "To upload content to YouTube, sign in to YouTube Studio, choose Create > Upload videos, select your file, add a title and description, choose visibility settings, then publish.",
    "youtube": "YouTube lets you upload videos, add metadata, and publish them from YouTube Studio.",
    "upload video": "Upload videos from YouTube Studio by selecting Create > Upload videos and following the prompts.",
    "screen guide": "Screen Guide is a guide-based app that provides structured help for common tasks and workflows.",
}


def find_local_match(question: str) -> str | None:
    normalized = question.lower().strip()
    if not normalized:
        return None

    for key, answer in LOCAL_GUIDES.items():
        if key in normalized:
            return answer

    return None
