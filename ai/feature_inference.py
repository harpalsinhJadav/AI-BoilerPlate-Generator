"""
AI Feature Inference
--------------------
Converts user app description → feature IDs.

Pipeline:

1. Try LLM semantic detection
2. If LLM unavailable → keyword fallback
3. Always return valid registry feature IDs
"""

from typing import List
import os

from core.feature_registry import (
    get_all_features,
    get_default_features,
)

# Optional LLM imports (safe if missing)
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langchain.prompts import PromptTemplate
    from langchain.chains import LLMChain

    LLM_AVAILABLE = True
except Exception:
    LLM_AVAILABLE = False


# --------------------------------------------------
# Keyword Fallback Detection
# --------------------------------------------------

def keyword_feature_detection(description: str, stack: str) -> List[str]:
    """
    Simple deterministic fallback using registry keywords.
    """
    description = description.lower()
    detected = set()

    for feature in get_all_features():
        if stack not in feature["stacks"]:
            continue

        for kw in feature["description_keywords"]:
            if kw in description:
                detected.add(feature["id"])

    # Always include defaults
    defaults = {f["id"] for f in get_default_features(stack)}

    return sorted(detected | defaults)


# --------------------------------------------------
# LLM Semantic Detection
# --------------------------------------------------

def llm_feature_detection(description: str, stack: str) -> List[str]:
    """
    Uses Gemini via LangChain to infer features.
    Falls back automatically if key missing or error occurs.
    """
    api_key = os.getenv("GOOGLE_API_KEY")

    if not api_key or not LLM_AVAILABLE:
        raise RuntimeError("LLM not available")

    features = get_all_features()

    feature_list_text = "\n".join(
        f"- {f['id']}: {f['label']}" for f in features if stack in f["stacks"]
    )

    prompt = PromptTemplate(
        input_variables=["description", "feature_list"],
        template="""
You are a senior mobile architect.

From the app description below,
select ONLY the relevant feature IDs from the provided list.

Rules:
- Return ONLY a comma-separated list of feature IDs.
- Do NOT invent new IDs.
- Include authentication if login/signup implied.
- Include navigation for multi-screen apps.

Available Features:
{feature_list}

App Description:
{description}

Answer:
""",
    )

    llm = ChatGoogleGenerativeAI(
        model="gemini-pro",
        temperature=0,
        google_api_key=api_key,
    )

    chain = LLMChain(llm=llm, prompt=prompt)

    result = chain.run(
        {
            "description": description,
            "feature_list": feature_list_text,
        }
    )

    raw_ids = [x.strip() for x in result.split(",")]

    valid_ids = {
        f["id"] for f in features if stack in f["stacks"]
    }

    return sorted(set(fid for fid in raw_ids if fid in valid_ids))


# --------------------------------------------------
# Public API
# --------------------------------------------------

def infer_features(description: str, stack: str) -> List[str]:
    """
    Main entry point used by generator engine.
    """

    if not description.strip():
        # No description → defaults only
        return [f["id"] for f in get_default_features(stack)]

    # Try LLM first
    try:
        return llm_feature_detection(description, stack)
    except Exception:
        # Safe deterministic fallback
        return keyword_feature_detection(description, stack)
