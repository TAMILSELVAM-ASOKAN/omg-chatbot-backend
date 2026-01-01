from langchain.tools import tool
from utils.vector_store import similarity_search

from utils.logger import get_logger
logger = get_logger("spiritual_story_search")


@tool
def spiritual_story_search(query: str) -> str:
    """
    Use this tool when the user asks about:
    - spiritual stories
    - god mythology
    - epics (Ramayana, Mahabharata, Bhagavatam)
    - legends, divine events
    """
    logger.info(f"[EXEC] spiritual_story_search | query={query}")

    results = similarity_search(query)
    
    if not results:
        logger.warning("[RESULT] spiritual_story_search returned EMPTY")
        return "No relevant spiritual stories found."

    context_blocks = []
    for r in results:
        context_blocks.append(
            f"[Source: {r['source']} | Score: {round(r['score'], 2)}]\n{r['content']}"
        )
    
    logger.info(
            f"[RESULT] spiritual_story_search size={len(context_blocks)} chars and Contents = {context_blocks}"
        )
    return "\n\n".join(context_blocks)
