import dspy
from typing import List, Dict, Any, Optional, Callable, Awaitable
import asyncio

# Функции для создания инструментов с контекстом
def create_search_docs_handler(active_sources: List[str]):
    """Создает search_docs_handler с захваченным контекстом active_sources"""
    async def search_docs_handler(query: str) -> List[str]:
        """Search for documents based on a query."""
        try:
            print(f"\n🔍 SEARCH_DOCS TOOL CALLED")
            print(f"📝 Query: {query}")
            print(f"🎯 Active sources: {active_sources}")
            print("-" * 40)
            
            from mindbank_poc.core.retrieval.service import get_retrieval_service
            from mindbank_poc.core.agent.retrieval_wrapper import RetrievalWrapper
            
            # Create filters for the wrapper - передаем пустой список вместо None
            filters_for_wrapper = {"source_ids": active_sources} if active_sources else {"source_ids": []}
            
            # Get retrieval service 
            retrieval_service = await get_retrieval_service()
            retrieval_wrapper = RetrievalWrapper(retrieval_service)
            
            print(f"🔄 Calling search_context with filters: {filters_for_wrapper}")
            # Получаем ПОЛНЫЕ тексты без обрезки и суммаризации
            raw_results, _ = await retrieval_wrapper.search_context(
                query=query,
                limit=3,
                use_summarizer=False,
                filters=filters_for_wrapper
            )
            print(f"✅ Got {len(raw_results) if raw_results else 0} full documents")
            
            if not raw_results:
                print("❌ No documents found")
                return ["No relevant documents found for this query."]
            
            # Возвращаем ПОЛНЫЕ тексты БЕЗ обрезки
            documents = []
            for i, result in enumerate(raw_results):
                print(f"📄 Document {i+1}: {len(result)} chars (FULL TEXT)")
                documents.append(str(result))  # Полный текст без обрезки!
            
            print(f"🎯 Returning {len(documents)} FULL documents to ReAct agent")
            print("-" * 40)
            return documents
            
        except Exception as e:
            error_msg = f"❌ Error searching documents: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return [error_msg]
    
    return search_docs_handler

async def get_segment_full_text(segment) -> str:
    """Получает полный текст сегмента из его юнитов"""
    try:
        from mindbank_poc.core.knowledge_store import get_knowledge_store
        knowledge_store = get_knowledge_store()
        
        # Получаем юниты по их ID (используем get() как в роутере)
        texts = []
        for unit_id in segment.raw_unit_ids:
            try:
                unit = await knowledge_store.get(unit_id)
                if unit and hasattr(unit, 'text_repr'):
                    texts.append(unit.text_repr)
            except Exception as e:
                print(f"⚠️ Error getting unit {unit_id}: {e}")
                continue
        
        return "\n".join(texts) if texts else segment.summary
    except Exception as e:
        print(f"⚠️ Error getting segment full text: {e}")
        return segment.summary

def create_filter_segments_handler():
    """Создает filter_segments_handler для фильтрации сегментов"""
    async def filter_segments_handler(
        source: str = None,
        source_name: str = None, 
        title_contains: str = None,
        limit: int = 10,
        sort_order: str = "desc"
    ) -> List[str]:
        """Filter segments by source, source_name, title or other criteria.
        
        Args:
            source: Source type (e.g., 'telegram', 'buffer', 'meeting-transcript')
            source_name: Specific source name (e.g., 'AI Brainstorm room', 'meeting-transcript')
            title_contains: Search in segment titles (partial match)
            limit: Maximum number of results (default: 10)
            sort_order: Sort order 'desc' for newest first, 'asc' for oldest first
            
        Returns:
            List of formatted segment information
        """
        try:
            print(f"\n📋 FILTER_SEGMENTS TOOL CALLED")
            print(f"🏷️ Source: {source}")
            print(f"🏷️ Source name: {source_name}")
            print(f"📝 Title contains: {title_contains}")
            print(f"🔢 Limit: {limit}")
            print(f"📊 Sort order: {sort_order}")
            print("-" * 40)
            
            from mindbank_poc.core.knowledge_store import get_knowledge_store
            
            # Get knowledge store
            ks = get_knowledge_store()
            
            # Call filter_segments
            segments = await ks.filter_segments(
                source=source,
                source_name=source_name,
                title_contains=title_contains,
                limit=limit,
                sort_by="created_at",
                sort_order=sort_order
            )
            
            print(f"✅ Got {len(segments)} segments")
            print("\n📊 Найденные сегменты:")
            for i, segment in enumerate(segments):
                metadata = getattr(segment, 'metadata', {})
                source_meta = metadata.get('source_metadata', {})
                print(f"\n{i+1}. {segment.title[:100]}...")
                print(f"   Source: {source_meta.get('source', 'N/A')}")
                print(f"   Source Name: {source_meta.get('source_name', 'N/A')}")
                print(f"   Created: {segment.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                print(f"   Summary: {segment.summary[:200]}{'...' if len(segment.summary) > 200 else ''}")
                print(f"   Units: {len(segment.raw_unit_ids)}")
            print("-" * 40)
            
            if not segments:
                return [f"No segments found with the specified criteria (source: {source}, source_name: {source_name}, title_contains: {title_contains})"]
            
            # Format results for the agent
            results = []
            for i, segment in enumerate(segments):
                metadata = getattr(segment, 'metadata', {})
                source_meta = metadata.get('source_metadata', {})
                
                # Получаем полный текст из юнитов
                full_text = await get_segment_full_text(segment)
                
                result = f"""Segment {i+1}:
📄 Title: {segment.title}
📋 Summary: {segment.summary}
📄 Full Text: {full_text}
🕒 Created: {segment.created_at.strftime('%Y-%m-%d %H:%M:%S')}
🔗 Units: {len(segment.raw_unit_ids)}
🏷️ Source: {source_meta.get('source', 'N/A')}
🏷️ Source Name: {source_meta.get('source_name', 'N/A')}
👥 Group: {segment.group_id}
🆔 ID: {segment.id}"""
                
                results.append(result)
            
            print(f"🎯 Returning {len(results)} formatted segments")
            print("-" * 40)
            return results
            
        except Exception as e:
            error_msg = f"❌ Error filtering segments: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return [error_msg]
    
    return filter_segments_handler

def create_filter_units_handler():
    """Создает filter_units_handler для фильтрации юнитов"""
    async def filter_units_handler(
        archetype: str = None,
        source: str = None,
        source_name: str = None,
        author: str = None,
        date_from: str = None,
        date_to: str = None,
        limit: int = 10,
        sort_order: str = "desc"
    ) -> List[str]:
        """Filter units by various criteria.
        
        Args:
            archetype: Content archetype (e.g., 'messaging', 'document', 'meeting')
            source: Source type (e.g., 'telegram', 'meeting-transcript')
            source_name: Specific source name
            author: Content author
            date_from: Start date (YYYY-MM-DD format)
            date_to: End date (YYYY-MM-DD format)
            limit: Maximum number of results (default: 10)
            sort_order: Sort order 'desc' for newest first, 'asc' for oldest first
            
        Returns:
            List of formatted unit information
        """
        try:
            print(f"\n📄 FILTER_UNITS TOOL CALLED")
            print(f"🏷️ Archetype: {archetype}")
            print(f"🏷️ Source: {source}")
            print(f"🏷️ Source name: {source_name}")
            print(f"👤 Author: {author}")
            print(f"📅 Date from: {date_from}")
            print(f"📅 Date to: {date_to}")
            print(f"🔢 Limit: {limit}")
            print(f"📊 Sort order: {sort_order}")
            print("-" * 40)
            
            from mindbank_poc.core.retrieval.service import get_retrieval_service
            from datetime import datetime
            
            # Parse dates
            date_from_dt = None
            date_to_dt = None
            
            if date_from:
                try:
                    date_from_dt = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                except ValueError:
                    try:
                        date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
                    except ValueError:
                        print(f"⚠️ Invalid date_from format: {date_from}")
            
            if date_to:
                try:
                    date_to_dt = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                except ValueError:
                    try:
                        date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
                    except ValueError:
                        print(f"⚠️ Invalid date_to format: {date_to}")
            
            # Get retrieval service
            retrieval_service = await get_retrieval_service()
            
            # Call filter_search
            results = await retrieval_service.filter_search(
                archetype=archetype,
                source=source,
                source_name=source_name,
                author=author,
                date_from=date_from_dt,
                date_to=date_to_dt,
                limit=limit,
                sort_by="created_at",
                sort_order=sort_order
            )
            
            print(f"✅ Got {len(results)} units")
            
            if not results:
                return [f"No units found with the specified criteria"]
            
            # Format results for the agent
            formatted_results = []
            for i, result in enumerate(results):
                unit = result.unit
                created_at_str = "N/A"
                if hasattr(unit, 'created_at') and unit.created_at:
                    created_at_str = unit.created_at.strftime('%Y-%m-%d %H:%M:%S')
                
                # Get source info from metadata
                source_info = getattr(unit, 'source', 'N/A')
                archetype_info = getattr(unit, 'archetype', 'N/A')
                
                formatted_result = f"""Unit {i+1}:
📄 Text: {unit.text_repr[:300]}{'...' if len(unit.text_repr) > 300 else ''}
🕒 Created: {created_at_str}
🏷️ Archetype: {archetype_info}
🏷️ Source: {source_info}
👥 Group: {unit.group_id}
📊 Score: {result.score:.3f}
🆔 ID: {unit.id}"""
                
                formatted_results.append(formatted_result)
            
            print(f"🎯 Returning {len(formatted_results)} formatted units")
            print("-" * 40)
            return formatted_results
            
        except Exception as e:
            error_msg = f"❌ Error filtering units: {str(e)}"
            print(error_msg)
            import traceback
            traceback.print_exc()
            return [error_msg]
    
    return filter_units_handler

async def echo_handler(message: str = "Tool is working correctly!") -> str:
    """Echo tool for testing."""
    return f"Echo response: {message}"

# Создаем базовый echo tool (не зависит от контекста)
echo_tool = dspy.Tool(
    func=echo_handler,
    name="echo",
    desc="Returns an echo response with optional message parameter"
)

def create_tools_with_context(active_sources: List[str]) -> List:
    """Создает инструменты с контекстом active_sources"""
    search_handler = create_search_docs_handler(active_sources)
    search_docs_tool = dspy.Tool(
        func=search_handler,
        name="search_docs",
        desc="Performs semantic search across the knowledge base to find content related to concepts, topics, or themes. Returns detailed content from relevant documents. Use this for general exploration of topics."
    )
    
    # Добавляем новые инструменты фильтрации
    filter_segments_handler = create_filter_segments_handler()
    filter_segments_tool = dspy.Tool(
        func=filter_segments_handler,
        name="filter_segments",
        desc="Finds specific content segments by source type, name, or title keywords. Great for finding meeting transcripts (source='meeting-transcript'), telegram conversations (source='telegram'), or content containing specific topics. Parameters: source, source_name, title_contains, limit (default 10, max 20), sort_order"
    )
    
    filter_units_handler = create_filter_units_handler()
    filter_units_tool = dspy.Tool(
        func=filter_units_handler,
        name="filter_units", 
        desc="Searches for content by specific criteria like author, date range, content type (archetype), or source. Perfect for finding 'what did [person] say', 'content from [date]', or specific types of content. Parameters: archetype, source, source_name, author, date_from, date_to, limit, sort_order"
    )
    
    return [search_docs_tool, filter_segments_tool, filter_units_tool, echo_tool]

class ReActAgent:
    """
    A ReAct agent using DSPy's built-in ReAct module with proper async tool handling.
    """

    def __init__(
        self,
        tools: Optional[List] = None,
        max_steps: int = 5,
        trace: bool = True,
    ):
        # NOTE: tools будут созданы динамически в run() с правильным контекстом
        self.base_tools = tools  # Сохраняем базовые инструменты
        self.max_steps = max_steps
        self.trace_enabled = trace
        self.reasoning_trace: List[Dict[str, Any]] = [] 
        self.react_module = None  # Будет создан в run() с правильными инструментами 

        # AgentSignature будет создан в run() вместе с react_module

    def reset_trace(self):
        """Reset the reasoning trace."""
        self.reasoning_trace = []

    async def run(
        self,
        user_input: str,
        chat_history: List[Dict[str, Any]],
        active_sources: List[str]
    ) -> Dict[str, Any]:
        """
        Main reasoning loop using dspy.ReAct with async tools.
        
        Args:
            user_input: The user's question/input
            chat_history: List of previous messages
            active_sources: List of active sources (connectors)
            
        Returns:
            Dict with 'answer' and 'trace' keys
        """
        self.reset_trace()

        # Создаем инструменты с контекстом active_sources
        print(f"🛠️ Creating tools with active_sources: {active_sources}")
        tools_with_context = create_tools_with_context(active_sources or [])
        
        # Создаем сигнатуру для ReAct
        class AgentSignature(dspy.Signature):
            """
            You are MindBank's expert knowledge assistant. Your role is to help users understand and explore 
            their knowledge base with detailed, insightful responses.

            CORE PRINCIPLES:
            1. ALWAYS provide specific details, examples, and concrete information from the retrieved content
            2. Structure your answers clearly with headings, bullet points, or numbered lists when appropriate
            3. Include key quotes, names, dates, numbers, and actionable insights from the sources
            4. Be conversational and helpful - explain WHY information is important, not just WHAT was found
            5. If you find multiple relevant pieces, synthesize them into a coherent narrative

            TOOL STRATEGY:
            - search_docs: Use for general semantic search when you need to find information about concepts/topics
            - filter_segments: Use when looking for specific meetings, telegram conversations, or content by source
            - filter_units: Use when searching by person, date range, or specific content types. 
            Always request at least 5 units/segments to get better context and avoid fragmented information
            
            If you need to find specific content, use filter_units first.
            If you need to find specific content segments, use filter_segments first.
            If you need to find specific content units, use filter_units first.
            
            RESPONSE GUIDELINES:
            - Start with a direct answer to the user's question
            - Provide specific details, examples, and context from the retrieved information
            - Use formatting (bullet points, sections) to make complex information digestible
            - Include relevant dates, names, and specific facts when available
            - End with actionable insights or follow-up suggestions when appropriate
            - Respond in the same language as the user's question
            - If you can't find relevant information, suggest alternative searches or clarify what you did find

            EXAMPLE GOOD RESPONSE STRUCTURE:
            ## [Direct Answer]
            [Specific answer with key details]

            ## Key Details:
            • [Specific fact 1 with context]
            • [Specific fact 2 with details]
            • [Important insight or decision]

            ## Additional Context:
            [Relevant background information, timeline, or implications]

            Remember: Users want insights and understanding, not just summaries. Help them discover valuable information!
            """
            question: str = dspy.InputField(
                desc="The user's question that needs to be answered using MindBank's knowledge base"
            )
            sources: List[str] = dspy.InputField(
                desc="List of active sources (connectors) to use for searching"
            )
            answer: str = dspy.OutputField(
                desc="A detailed, well-structured answer that provides specific insights and actionable information "
                     "from the knowledge base. Include concrete details, examples, and clear explanations that help "
                     "the user understand not just what happened, but why it matters."
            )
        
        # Создаем ReAct модуль с правильными инструментами
        react_module = dspy.ReAct(
            signature=AgentSignature,
            tools=tools_with_context,
            max_iters=self.max_steps
        )

        # Формируем полный вопрос с улучшенным контекстом
        history_str = "\n".join([f"{msg['role']}: {msg['content']}" for msg in chat_history[-5:]])
        
        full_question = (
            f"USER'S QUESTION: {user_input}\n\n"
            f"CONTEXT: You are helping a user explore their knowledge base. "
            f"The user is asking about content from these sources: {', '.join(active_sources) if active_sources else 'all available sources'}.\n\n"
            f"RECENT CONVERSATION:\n{history_str}\n\n"
            f"INSTRUCTIONS:\n"
            f"1. Use the appropriate tools to find detailed information related to the user's question\n"
            f"2. Provide a comprehensive answer with specific details, examples, and insights\n"
            f"3. Structure your response clearly with sections/bullet points for complex information\n"
            f"4. Include relevant dates, names, quotes, and concrete facts from the retrieved content\n"
            f"5. Explain the significance and implications of the information you find\n"
            f"6. Respond in Russian (the user's language)\n\n"
            f"Remember: The user wants detailed insights and understanding, not just brief summaries!"
        )
        try:
            print(f"🤖 Starting ReAct execution with {len(tools_with_context)} tools")
            # Use acall for async execution with proper error handling
            response = await react_module.acall(question=full_question, sources=active_sources)
            # Ensure response.answer is converted to string to avoid ModelResponse issues
            final_answer = str(response.answer) if response.answer else "No answer provided"
            print(f"🔄 ReAct response: {final_answer}")
            print("ReAct trajectory: ", response.trajectory)
            # Extract trace information
            reasoning_steps = []
            if self.trace_enabled:
                # Try to get trace from the module or LM history
                if hasattr(react_module, 'trajectory') and react_module.trajectory:
                    for i, step in enumerate(react_module.trajectory):
                        reasoning_steps.append({
                            "step": i + 1,
                            "thought": str(step.get("thought", "")),
                            "action": str(step.get("action", "")),
                            "observation": str(step.get("observation", ""))
                        })
                elif hasattr(dspy.settings, 'lm') and hasattr(dspy.settings.lm, 'history') and dspy.settings.lm.history:
                    # Fallback to LM history
                    recent_history = dspy.settings.lm.history[-3:] if dspy.settings.lm.history else []
                    for i, entry in enumerate(recent_history):
                        prompt_text = str(entry.get('prompt', '')) if entry.get('prompt') else ''
                        response_text = str(entry.get('response', '')) if entry.get('response') else ''
                        reasoning_steps.append({
                            "step": i + 1,
                            "prompt": prompt_text[:200] + "..." if len(prompt_text) > 200 else prompt_text,
                            "response": response_text[:200] + "..." if len(response_text) > 200 else response_text
                        })                   
                else:
                    reasoning_steps.append({"note": "Trace information not available"})

            self.reasoning_trace = reasoning_steps

            return {
                "answer": final_answer,
                "trace": self.reasoning_trace
            }
            
        except Exception as e:
            error_msg = f"Error during ReAct execution: {str(e)}"
            print(error_msg)
            
            self.reasoning_trace = [{"error": error_msg}]
            
            return {
                "answer": "I encountered an error while processing your request. Please try again.",
                "trace": self.reasoning_trace
            }

# Factory function to create ReAct agent with default tools
def create_react_agent(max_steps: int = 5, trace: bool = True) -> ReActAgent:
    """Create a ReAct agent with default configuration."""
    return ReActAgent(
        tools=None,  # Инструменты будут созданы динамически с контекстом
        max_steps=max_steps,
        trace=trace
    )
