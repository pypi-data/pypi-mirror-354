import json
import time
import uuid
import re


class MyArticleDecisionMaker:
    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.retry_attempts = 3
        self.retry_delay = 2 # seconds

    def _safe_llm_call(self, system_prompt: str, user_prompt: str, json_mode: bool = False, max_retries: int = 3):
        """封装LLM调用，增加重试机制和JSON解析"""
        for attempt in range(max_retries):
            try:
                response_str = self.llm_client.generate_response(system_prompt + user_prompt)
                # response_str = self.llm.generate_response(user_prompt)
                if not response_str:
                    raise ValueError("Empty response from LLM.")
                if json_mode:
                    matrhc = re.search(r"```json(.*?)```",response_str,re.DOTALL)
                    response_str2 = matrhc.group(1).strip()
                    return json.loads(response_str2)
                return response_str
            except (json.JSONDecodeError, ValueError) as e:
                print(f"LLM call failed (attempt {attempt + 1}/{max_retries}): {e}. Retrying...")
            except Exception as e:
                print(f"An unexpected error occurred during LLM call: {e}. Retrying...")
        print("LLM call failed after multiple retries.")
        return None

    def cluster_initial_articles(self, articles_data: list[dict]) -> list[dict]:
        """
        【你的第一个函数】
        对一批初始文章进行聚类，形成森林的“第一层树”。
        LLM会返回每个聚类的共性主题和包含的文章ID列表。

        Args:
            articles_data (list[dict]): 包含文章ID和内容的字典列表。
                                       e.g., [{"id": "A1", "content": "..."}]

        Returns:
            list[dict]: 聚类结果。每个字典包含 'common_theme' (str) 和 'article_ids' (list[str])。
                        e.g., [{"common_theme": "AI Models", "article_ids": ["A1", "A5"]}]
        """
        print("\n[User Function: cluster_initial_articles] Asking LLM to cluster initial articles...")

        formatted_articles = "\n".join([f"Article ID: {a['id']}\nContent: {a['content']}\n---" for a in articles_data])

        # system_prompt = (
        #     "You are an expert text clustering and summarization AI. "
        #     "Your task is to group a list of articles by their main themes. "
        #     "For each cluster, identify a concise common topic/title. "
        #     "Output in JSON format only."
        # )
        # user_prompt = (
        #     f"Here are the articles:\n\n{formatted_articles}\n\n"
        #     "Group these articles into clusters based on their core themes. "
        #     "For each cluster, provide a `common_theme` and a list of `article_ids` belonging to that cluster. "
        #     "Ensure every article ID from the input is present in exactly one cluster."
        #     "Output format:\n"
        #     "```json\n"
        #     "[\n"
        #     "  {\n"
        #     "    \"common_theme\": \"Theme for Cluster 1\",\n"
        #     "    \"article_ids\": [\n"
        #     "      \"Article ID from input 1\",\n"
        #     "      \"Article ID from input 2\"\n"
        #     "    ]\n"
        #     "  },\n"
        #     "  {\n"
        #     "    \"common_theme\": \"Theme for Cluster 2\",\n"
        #     "    \"article_ids\": [\n"
        #     "      \"Article ID from input 3\",\n"
        #     "      \"Article ID from input 4\"\n"
        #     "    ]\n"
        #     "  }\n"
        #     "]\n```"
        # )
        system_prompt = (
            "你是文本聚类和抽象共性的人工智能的专家"
            "你的任务是根据相似度对文章列表进行分组, 对于每个集群，都应该采样与父类的相似程度"
            "仅以JSON格式输出。"
            ""
            "相似度的定义如下"
            "首先，确认文章的主题是解释类似的概念还是解决类似的问题"
            "第二个次要方面是，在解决类似问题的前提下，有相同的宏观组合或写作逻辑（即所谓的相似），而细节却被低估了。"
        )
        user_prompt = (
            f"这些是文章:\n\n{formatted_articles}\n\n"
            "根据核心主题将这些文章分组。"
            "对于每个集群，提供一个‘ common_theme ’和属于该集群的‘ article_ids ’列表。"
            "确保输入的每个文章ID都恰好出现在一个集群中。"
            "Output format:\n"
            "```json\n"
            "[\n"
            "  {\n"
            "    \"common_abstract_structure\": \"abstract_structure for Cluster 1\",\n"
            "    \"article_ids\": [\n"
            "      \"Article ID from input 1\",\n"
            "      \"Article ID from input 2\"\n"
            "    ]\n"
            "  },\n"
            "  {\n"
            "    \"common_abstract_structure\": \"abstract_structure for Cluster 2\",\n"
            "    \"article_ids\": [\n"
            "      \"Article ID from input 3\",\n"
            "      \"Article ID from input 4\"\n"
            "    ]\n"
            "  }\n"
            "]\n```"
        )

        llm_response = self._safe_llm_call(system_prompt, user_prompt, json_mode=True)

        if llm_response:
            print(f"[User Function: cluster_initial_articles] LLM finished clustering. Found {len(llm_response)} clusters.")
            return llm_response
        
        print("[User Function: cluster_initial_articles] LLM failed to cluster or returned invalid response. Returning empty list.")
        return [] # Fallback if LLM fails

    def decide_placement_for_new_article(
        self,
        new_article_data: dict, # {"id": "...", "content": "..."}
        all_existing_nodes_repr: list[dict] # [{"node_id": "...", "content": "...", "is_leaf": bool, "depth": int}]
    ) -> dict:
        """
        【你的第二个函数】
        当一篇新文章到来时，让LLM决定它应该归入哪个现有节点，或是否需要创建一个全新的顶级聚类。

        Args:
            new_article_data (dict): 新文章的ID和内容。
            all_existing_nodes_repr (list[dict]): 当前森林中所有节点的代表信息列表。
                                                 每个字典包含: 'node_id', 'content', 'is_leaf', 'depth'。

        Returns:
            dict: 包含LLM决策的字典。
                  Expected structure:
                  {
                    "action": "create_new_top_level_cluster" | "add_to_existing_cluster" | "merge_with_leaf",
                    "target_node_id": "ID of node to act upon (if action is not create_new_top_level_cluster)",
                    "suggested_common_theme": "Common theme for new cluster/parent (if applicable)",
                    "reasoning": "Explanation of decision"
                  }
        """
        print(f"\n[User Function: decide_placement_for_new_article] Asking LLM to decide placement for new article: '{new_article_data['id']}'")

        formatted_nodes = json.dumps(all_existing_nodes_repr, indent=2, ensure_ascii=False)

        system_prompt = (
            "You are an intelligent document organizer. "
            "Given a new article and a description of an existing hierarchical knowledge forest, "
            "your task is to determine the optimal placement for the new article. "
            "Provide your decision in a specific JSON format. "
            "Prioritize depth limits implicitly, aiming for the most precise and deepest placement possible without creating excessively granular categories for single articles unless necessary. "
            "If merging two articles, create a new non-leaf node above them."
        )
        user_prompt = (
            f"New Article to place:\n"
            f"ID: {new_article_data['id']}\n"
            f"Content: \"\"\"\n{new_article_data['content']}\n\"\"\"\n\n"
            f"Existing Forest Structure (relevant nodes):\n```json\n{formatted_nodes}\n```\n\n"
            "Decision Criteria:\n"
            "1.  **Merge with Existing Leaf?** If the new article is extremely similar to an *existing leaf article* (e.g., a slightly rephrased version or direct continuation), suggest merging them. This creates a new non-leaf parent for both, extracting their common theme. Specify `target_node_id` as the ID of the *existing leaf*.\n"
            "2.  **Add to Existing Cluster?** If the new article belongs conceptually to an *existing non-leaf cluster* (at any level), suggest adding it as a child. Specify `target_node_id` as the ID of the *existing non-leaf cluster*.\n"
            "3.  **Create New Top-Level Cluster?** If the new article is distinctly different from all existing top-level clusters or falls into no clear existing sub-category, suggest creating a new top-level cluster for it.\n"
            "\n"
            "Output Format (JSON only, choose one 'action'):\n"
            "```json\n"
            "{\n"
            "  \"action\": \"create_new_top_level_cluster\",\n"
            "  \"suggested_common_theme\": \"Brief theme for this new cluster\",\n"
            "  \"reasoning\": \"Explanation of why this action was chosen\"\n"
            "}\n"
            "```\nOR\n"
            "```json\n"
            "{\n"
            "  \"action\": \"add_to_existing_cluster\",\n"
            "  \"target_node_id\": \"ID of the non-leaf node to add to\",\n"
            "  \"suggested_common_theme\": \"Updated common theme for the target cluster (optional, if its theme should reflect the new article)\",\n"
            "  \"reasoning\": \"Explanation of why this action was chosen\"\n"
            "}\n"
            "```\nOR\n"
            "```json\n"
            "{\n"
            "  \"action\": \"merge_with_leaf\",\n"
            "  \"target_node_id\": \"ID of the existing leaf article to merge with\",\n"
            "  \"suggested_common_theme\": \"Brief common theme for the new non-leaf parent of the two merged articles\",\n"
            "  \"reasoning\": \"Explanation of why this action was chosen\"\n"
            "}\n"
            "```"
        )

        llm_decision = self._safe_llm_call(system_prompt, user_prompt, json_mode=True)

        if llm_decision and "action" in llm_decision:
            print(f"[User Function: decide_placement_for_new_article] LLM decided: {llm_decision.get('action', 'Unknown')} (Reason: {llm_decision.get('reasoning', 'No reasoning')[:50]}...)")
            return llm_decision
        
        print("[User Function: decide_placement_for_new_article] LLM failed to decide or returned invalid format. Defaulting to new top-level cluster.")
        return {"action": "create_new_top_level_cluster", "suggested_common_theme": f"New Topic for {new_article_data['id']}", "reasoning": "LLM fallback."}

    def generate_commonality_for_cluster(self, articles_content: list[str]) -> str:
        """
        LLM生成非叶子节点的共性摘要或关键词。

        Args:
            articles_content (list[str]): 一组相似文章的内容列表。

        Returns:
            str: 共性摘要或关键词。
        """
        print(f"[User Function: generate_commonality_for_cluster] Asking LLM for commonality of {len(articles_content)} articles.")
        if not articles_content:
            return "No common theme identified."

        formatted_articles = "\n".join([f"- {content[:100]}..." for content in articles_content])

        system_prompt = (
            "You are an expert summarization AI. Your task is to extract the most prominent common theme "
            "or a concise summary that represents all provided articles. Output only the theme/summary string."
        )
        user_prompt = (
            f"Given the following articles, provide a concise common theme or summary that encapsulates their main topics:\n\n"
            f"{formatted_articles}\n\n"
            "Common Theme/Summary:"
        )

        llm_response = self._safe_llm_call(system_prompt, user_prompt, json_mode=False)
        if llm_response:
            return llm_response.strip()
        
        print("[User Function: generate_commonality_for_cluster] LLM failed to generate commonality. Returning fallback.")
        return f"Common theme for {len(articles_content)} articles."

