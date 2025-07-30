import uuid
import json # 用于打印美观的JSON

# from your_module import MyArticleDecisionMaker, LLMClient # 假设你的代码在your_module.py
from .llm import MyLocalLLMClient
from .article_decision import MyArticleDecisionMaker
import graphviz  


class ArticleTreeNode:
    def __init__(self, content=None, is_leaf=True, article_id=None, node_id=None):
        self.node_id = node_id if node_id else str(uuid.uuid4())
        self.content = content
        self.is_leaf = is_leaf
        self.article_id = article_id
        self.children = []
        self.parent = None # Parent node reference

    def add_child(self, child_node):
        self.children.append(child_node)
        child_node.parent = self

    def remove_child(self, child_node):
        if child_node in self.children:
            self.children.remove(child_node)
            child_node.parent = None

    def __repr__(self):
        return f"Node(ID={self.node_id[:8]}..., Type={'Leaf' if self.is_leaf else 'Non-Leaf'}, Content='{self.content[:30]}...')"


class ArticleForest:
    MAX_DEPTH = 7 # 最高七层 (根节点深度为0, 叶子节点最大深度为7)

    def __init__(self, article_decision_maker: MyArticleDecisionMaker):
        self.root = ArticleTreeNode(content="Forest Root", is_leaf=False, article_id=None, node_id="forest_root")
        self.article_decision_maker = article_decision_maker
        self._node_map = {self.root.node_id: self.root} # 存储所有节点，方便通过ID查找

    def _add_node_to_map(self, node: ArticleTreeNode):
        self._node_map[node.node_id] = node

    def _remove_node_from_map(self, node: ArticleTreeNode):
        if node.node_id in self._node_map:
            del self._node_map[node.node_id]
        for child in node.children:
            self._remove_node_from_map(child)

    def _get_depth(self, node: ArticleTreeNode) -> int:
        """计算节点的深度 (根节点为0)"""
        depth = 0
        current = node
        while current and current.parent: # Iterate upwards until parent is None (i.e., self.root)
            depth += 1
            current = current.parent
        return depth

    def _update_non_leaf_commonality_and_propagate(self, node: ArticleTreeNode):
        """
        更新非叶子节点的共性内容（通过LLM）并向上层传播。
        当子节点发生变化时调用。
        """
        if node.is_leaf:
            return

        child_contents = [c.content for c in node.children if c.is_leaf] # 只聚合叶子内容的共性
        if child_contents:
            new_commonality = self.article_decision_maker.generate_commonality_for_cluster(child_contents)
            node.content = new_commonality
        else:
            node.content = "Empty Cluster" # Should ideally not happen for non-leaf with children

        # 递归向上更新父节点
        if node.parent:
            self._update_non_leaf_commonality_and_propagate(node.parent) # propagate up

    def _get_all_node_reprs(self) -> list[dict]:
        """
        获取当前森林中所有节点的代表信息，用于传递给决策函数。
        """
        all_reprs = []
        nodes_to_visit = [self.root]
        visited_nodes = set() # Avoid cycles in case of complex graph (not strictly a tree)

        while nodes_to_visit:
            current_node = nodes_to_visit.pop(0)
            if current_node.node_id in visited_nodes:
                continue
            visited_nodes.add(current_node.node_id)

            if current_node.node_id != self.root.node_id: # 不把根节点本身的信息传给外部决策函数
                all_reprs.append({
                    "node_id": current_node.node_id,
                    "content": current_node.content,
                    "is_leaf": current_node.is_leaf,
                    "depth": self._get_depth(current_node)
                })
            # Add children to visit queue
            nodes_to_visit.extend(current_node.children)
        return all_reprs


    def build_initial_forest(self, initial_articles_data: list[dict]):
        """
        使用 cluster_initial_articles 函数构建森林的初始结构。
        """
        if not initial_articles_data:
            print("No initial articles provided to build the forest.")
            return

        print("\n--- Building Initial Forest Structure ---")
        # 调用你提供的聚类函数
        clustered_results = self.article_decision_maker.cluster_initial_articles(initial_articles_data)

        if not clustered_results:
            print("No clusters formed from initial articles by LLM. Adding all as separate top-level leaves.")
            for article_data in initial_articles_data:
                leaf_node = ArticleTreeNode(content=article_data["content"], is_leaf=True, article_id=article_data["id"])
                self._add_node_to_map(leaf_node)
                self.root.add_child(leaf_node)
            return

        for cluster_info in clustered_results:
            common_theme = cluster_info.get("common_theme", "No theme provided")
            article_ids_in_cluster = cluster_info.get("article_ids", [])

            if not article_ids_in_cluster:
                continue

            # 创建新的非叶子节点作为顶级聚类（一棵树的根）
            cluster_node = ArticleTreeNode(content=common_theme, is_leaf=False)
            self._add_node_to_map(cluster_node)
            self.root.add_child(cluster_node) # 顶级聚类是根节点的直接子节点
            print(f"Created initial top-level cluster (tree root): {cluster_node.node_id[:8]}... ('{cluster_node.content[:30]}...')")

            # 将聚类内的文章作为叶子节点添加到该顶级聚类节点下
            for article_id in article_ids_in_cluster:
                article_data = next((item for item in initial_articles_data if item["id"] == article_id), None)
                if article_data:
                    leaf_node = ArticleTreeNode(content=article_data["content"], is_leaf=True, article_id=article_data["id"])
                    self._add_node_to_map(leaf_node)
                    cluster_node.add_child(leaf_node)
                    print(f"  Added article {article_id} to cluster {cluster_node.node_id[:8]}...")
                else:
                    print(f"  Warning: Article ID {article_id} not found in initial data. Skipping.")

            # 更新聚类节点的共性内容（如果需要，或者LLM已提供）
            # self._update_non_leaf_commonality_and_propagate(cluster_node) # Already set by LLM for initial clusters

        print("--- Initial Forest Building Complete ---")


    def add_article(self, article_content: str, article_id: str):
        """
        向森林中添加一篇新文章。
        """
        print(f"\n--- Adding New Article: {article_id} ---")

        new_leaf_node = ArticleTreeNode(content=article_content, is_leaf=True, article_id=article_id)
        self._add_node_to_map(new_leaf_node) # 添加到节点映射

        # 获取所有现有节点的代表信息，供决策函数使用
        all_nodes_repr = self._get_all_node_reprs()

        # 调用你提供的决策函数
        llm_decision = self.article_decision_maker.decide_placement_for_new_article(
            {"id": article_id, "content": article_content}, all_nodes_repr
        )

        action = llm_decision.get("action")
        target_node_id = llm_decision.get("target_node_id")
        suggested_common_theme = llm_decision.get("suggested_common_theme")

        target_node = self._node_map.get(target_node_id) if target_node_id else None

        if action == "create_new_top_level_cluster":
            new_cluster_node = ArticleTreeNode(
                content=suggested_common_theme if suggested_common_theme else f"New Topic for {article_id}",
                is_leaf=False
            )
            self._add_node_to_map(new_cluster_node)
            self.root.add_child(new_cluster_node)
            new_cluster_node.add_child(new_leaf_node)
            self._update_non_leaf_commonality_and_propagate(new_cluster_node)
            print(f"Article {article_id} CREATED a NEW TOP-LEVEL CLUSTER {new_cluster_node.node_id[:8]}... (Reason: {llm_decision.get('reasoning', 'N/A')}).")

        elif action == "merge_with_leaf":
            if target_node and target_node.is_leaf:
                parent_of_leaf = target_node.parent
                if parent_of_leaf:
                    # 检查是否会超出最大深度
                    if self._get_depth(parent_of_leaf) + 2 > self.MAX_DEPTH:
                        print(f"  Warning: Merging with {target_node.article_id} would exceed MAX_DEPTH {self.MAX_DEPTH}. Adding as sibling instead.")
                        parent_of_leaf.add_child(new_leaf_node)
                        self._update_non_leaf_commonality_and_propagate(parent_of_leaf)
                        print(f"Article {article_id} added as a sibling to {target_node.article_id}.")
                        return # Exit early

                    # 创建新的非叶子节点作为新抽象层
                    new_non_leaf_node = ArticleTreeNode(is_leaf=False)
                    new_non_leaf_node.content = suggested_common_theme if suggested_common_theme else f"Common theme for {target_node.article_id} and {article_id}"
                    self._add_node_to_map(new_non_leaf_node)

                    # 替换原有的叶子节点
                    parent_of_leaf.remove_child(target_node)
                    parent_of_leaf.add_child(new_non_leaf_node)

                    # 将两篇文章作为新抽象层的子节点
                    new_non_leaf_node.add_child(target_node)
                    new_non_leaf_node.add_child(new_leaf_node)
                    self._update_non_leaf_commonality_and_propagate(new_non_leaf_node)
                    print(f"Article {article_id} MERGED with {target_node.article_id}, creating new non-leaf node {new_non_leaf_node.node_id[:8]}... (Reason: {llm_decision.get('reasoning', 'N/A')}).")
                else:
                    # 极端情况：现有叶子是根节点直属，且只有它自己。
                    # 将其和新文章一起创建顶级聚类。
                    print(f"  Warning: Existing leaf {target_node.article_id} is a direct child of root. Creating new top-level cluster with both.")
                    self.root.remove_child(target_node)
                    new_cluster_node = ArticleTreeNode(
                        content=suggested_common_theme if suggested_common_theme else f"Combined theme for {target_node.article_id} and {article_id}",
                        is_leaf=False
                    )
                    self._add_node_to_map(new_cluster_node)
                    self.root.add_child(new_cluster_node)
                    new_cluster_node.add_child(target_node)
                    new_cluster_node.add_child(new_leaf_node)
                    self._update_non_leaf_commonality_and_propagate(new_cluster_node)
                    print(f"  Merged {article_id} and {target_node.article_id} into a NEW TOP-LEVEL CLUSTER {new_cluster_node.node_id[:8]}...")
            else:
                print(f"  Error: Merge target {target_node_id} not found or is not a leaf for merge action. Fallback to new top-level.")
                self.root.add_child(new_leaf_node)
                self._update_non_leaf_commonality_and_propagate(self.root)

        elif action == "add_to_existing_cluster":
            if target_node and not target_node.is_leaf:
                # 检查是否会超出最大深度
                if self._get_depth(target_node) + 1 > self.MAX_DEPTH:
                    print(f"  Warning: Adding to {target_node.node_id[:8]}... would exceed MAX_DEPTH {self.MAX_DEPTH}. Adding as sibling to its parent.")
                    if target_node.parent:
                        target_node.parent.add_child(new_leaf_node)
                        self._update_non_leaf_commonality_and_propagate(target_node.parent)
                    else: # If target node has no parent (e.g., a top-level cluster), add to forest root
                        self.root.add_child(new_leaf_node)
                        self._update_non_leaf_commonality_and_propagate(self.root)
                    print(f"Article {article_id} added as a sibling to {target_node.node_id[:8]}... or new top-level.")
                    return # Exit early

                target_node.add_child(new_leaf_node)
                # If LLM suggests updated common theme, set it
                if suggested_common_theme:
                    target_node.content = suggested_common_theme
                self._update_non_leaf_commonality_and_propagate(target_node)
                print(f"Article {article_id} ADDED as a child of existing non-leaf node {target_node.node_id[:8]}... (Reason: {llm_decision.get('reasoning', 'N/A')}).")
            else:
                print(f"  Error: Target node {target_node_id} not found or is a leaf for add action. Fallback to new top-level.")
                self.root.add_child(new_leaf_node)
                self._update_non_leaf_commonality_and_propagate(self.root)
        else:
            print(f"  Unknown action '{action}' from LLM or invalid decision. Fallback to new top-level.")
            self.root.add_child(new_leaf_node)
            self._update_non_leaf_commonality_and_propagate(self.root)

        print(f"--- Article {article_id} Addition Complete ---")

    def print_tree(self, node=None, prefix="", is_last=False):
        """
        以美观的ASCII树状图形式打印森林结构。

        Args:
            node (ArticleTreeNode, optional): 当前要打印的节点。默认从根节点开始。
            prefix (str, optional): 用于当前节点子节点的行前缀。
            is_last (bool, optional): 指示当前节点是否是其父节点的最后一个子节点。
        """
        if node is None:
            node = self.root

        # 特殊处理虚拟的森林根节点
        if node == self.root:
            if not node.children:
                print("Forest is empty.")
            else:
                for i, child in enumerate(node.children):
                    is_child_last = (i == len(node.children) - 1)
                    # 顶级树的根节点（即root的子节点）不需要缩进，直接从0深度开始打印
                    self.print_tree(child, "", is_child_last)
            return

        # 计算当前节点的连接符
        connector = "└── " if is_last else "├── "

        # 准备节点信息
        node_type = "Leaf" if node.is_leaf else "Non-Leaf"
        identifier_info = f"Article ID: {node.article_id}" if node.is_leaf else f"Node ID: {node.node_id[:8]}..."
        depth_info = f"Depth: {self._get_depth(node)}"
        child_count_info = f" ({len(node.children)} children)" if not node.is_leaf else ""

        # 格式化内容，处理换行符和截断
        content_preview = node.content.replace('\n', ' ').strip()
        content_preview = content_preview[:min(len(content_preview), 100)] + "..." if len(content_preview) > 100 else content_preview

        # 打印当前节点
        print(f"{prefix}{connector}[{node_type}] {identifier_info} {child_count_info} ({depth_info}) | \"{content_preview}\"")

        # 为子节点计算新的前缀
        next_prefix = prefix + ("    " if is_last else "│   ")

        # 递归打印子节点
        for i, child in enumerate(node.children):
            is_child_last = (i == len(node.children) - 1)
            self.print_tree(child, next_prefix, is_child_last)
            
    def export_graphviz(self, filename="article_forest", format="png"):
        """
        将森林结构导出为Graphviz图形文件。

        Args:
            filename (str): 输出文件的基本名称（不包含扩展名）。
            format (str): 输出图形的格式，如 'png', 'svg', 'pdf' 等。
        """
        dot = graphviz.Digraph(comment='Article Forest', graph_attr={'rankdir': 'TB', 'splines': 'spline'})

        if not self.root.children:
            print("Forest is empty. Nothing to export.")
            return

        nodes_to_process = list(self.root.children) # 从顶级聚类开始
        processed_nodes = set()

        while nodes_to_process:
            current_node = nodes_to_process.pop(0)

            if current_node.node_id in processed_nodes:
                continue
            processed_nodes.add(current_node.node_id)

            # --- 定义节点外观和标签 ---
            node_label = f"ID: {current_node.node_id[:8]}...\n"
            node_label += f"Depth: {self._get_depth(current_node)}\n"
            
            content_preview = current_node.content.replace('\n', ' ').strip()
            content_preview = content_preview[:min(len(content_preview), 80)] + "..." if len(content_preview) > 80 else content_preview
            
            if current_node.is_leaf:
                node_label += f"Article ID: {current_node.article_id}\n"
                node_label += f"Content: {content_preview}"
                node_attrs = {'shape': 'box', 'style': 'filled', 'fillcolor': '#e0f7fa'} # Light Cyan
            else:
                node_label += f"Theme: {content_preview}\n"
                node_label += f"Children: {len(current_node.children)}"
                node_attrs = {'shape': 'ellipse', 'style': 'filled', 'fillcolor': '#ffe0b2'} # Light Orange

            dot.node(current_node.node_id, node_label, **node_attrs)

            # --- 添加边 ---
            for child in current_node.children:
                dot.edge(current_node.node_id, child.node_id)
                nodes_to_process.append(child) # 将子节点加入待处理队列

        # 渲染图形并保存
        try:
            dot.render(filename, view=True, format=format)
            print(f"Graph exported to {filename}.{format}")
        except graphviz.backend.ExecutableNotFound:
            print("Error: Graphviz executable (dot) not found.")
            print("Please install Graphviz from https://graphviz.org/download/ and ensure it's in your system's PATH.")
        except Exception as e:
            print(f"An error occurred during graph rendering: {e}")
