from typing import List, Dict, Tuple
from app.schemas.scheduler import ScheduledTask, DailySchedule


class LoadBalancingOptimizer:
    """负载均衡优化器 - 简化版用于MVP"""

    def __init__(self):
        """初始化优化器"""
        self.ideal_ratio = 0.5  # 理想分配比例 (50/50)

    def calculate_balance_score(
        self,
        parent1_tasks: int,
        parent2_tasks: int
    ) -> float:
        """
        计算负载均衡评分

        Args:
            parent1_tasks: 父母1的任务数
            parent2_tasks: 父母2的任务数

        Returns:
            均衡评分 (0.0 = 极不均衡, 1.0 = 完全均衡)
        """
        total = parent1_tasks + parent2_tasks
        if total == 0:
            return 1.0  # 没有任务时认为完全均衡

        # 计算任务比例
        ratio1 = parent1_tasks / total
        ratio2 = parent2_tasks / total

        # 计算与理想比例(0.5)的差距
        deviation1 = abs(ratio1 - self.ideal_ratio)
        deviation2 = abs(ratio2 - self.ideal_ratio)

        # 均衡评分 = 1 - 平均偏差
        balance_score = 1.0 - (deviation1 + deviation2) / 2

        return round(max(0.0, balance_score), 3)

    def analyze_imbalance(
        self,
        tasks: List[ScheduledTask]
    ) -> Dict:
        """
        分析负载不均衡情况

        Args:
            tasks: 任务列表

        Returns:
            包含不均衡分析的字典
        """
        # 统计每个父母的任务数
        parent_task_counts = {}
        parent_task_durations = {}

        for task in tasks:
            parent_id = task.assigned_to
            parent_task_counts[parent_id] = parent_task_counts.get(parent_id, 0) + 1
            parent_task_durations[parent_id] = parent_task_durations.get(parent_id, 0) + task.duration_minutes

        # 获取父母ID
        parent_ids = list(parent_task_counts.keys())

        if len(parent_ids) < 2:
            return {
                "error": "Need at least 2 parents to analyze imbalance",
                "parent_task_counts": parent_task_counts
            }

        parent1_id, parent2_id = parent_ids[0], parent_ids[1]

        # 计算均衡评分
        balance_score = self.calculate_balance_score(
            parent_task_counts[parent1_id],
            parent_task_counts[parent2_id]
        )

        # 计算任务数差距
        task_gap = abs(parent_task_counts[parent1_id] - parent_task_counts[parent2_id])

        # 计算时长差距
        duration_gap = abs(
            parent_task_durations.get(parent1_id, 0) -
            parent_task_durations.get(parent2_id, 0)
        )

        # 确定哪一方负载更重
        if parent_task_counts[parent1_id] > parent_task_counts[parent2_id]:
            heavier_parent = parent1_id
            lighter_parent = parent2_id
        else:
            heavier_parent = parent2_id
            lighter_parent = parent1_id

        return {
            "balance_score": balance_score,
            "parent1": {
                "id": parent1_id,
                "task_count": parent_task_counts[parent1_id],
                "total_duration": parent_task_durations.get(parent1_id, 0)
            },
            "parent2": {
                "id": parent2_id,
                "task_count": parent_task_counts[parent2_id],
                "total_duration": parent_task_durations.get(parent2_id, 0)
            },
            "task_gap": task_gap,
            "duration_gap": duration_gap,
            "heavier_parent": heavier_parent,
            "lighter_parent": lighter_parent,
            "is_balanced": balance_score >= 0.7
        }

    def suggest_reassignments(
        self,
        tasks: List[ScheduledTask],
        max_suggestions: int = 5
    ) -> List[Dict]:
        """
        建议任务重新分配以改善负载均衡

        Args:
            tasks: 任务列表
            max_suggestions: 最大建议数量

        Returns:
            重新分配建议列表
        """
        # 分析不均衡情况
        analysis = self.analyze_imbalance(tasks)

        if "error" in analysis or analysis["is_balanced"]:
            # 已经均衡或无法分析
            return []

        suggestions = []
        heavier_parent = analysis["heavier_parent"]
        lighter_parent = analysis["lighter_parent"]

        # 找出负载较重父母的任务，按优先级排序（低优先级优先转移）
        heavier_tasks = [
            t for t in tasks
            if t.assigned_to == heavier_parent and not t.is_recurring
        ]

        # 按优先级排序（优先级低的排前面）
        heavier_tasks_sorted = sorted(heavier_tasks, key=lambda t: t.priority)

        # 生成重新分配建议
        for task in heavier_tasks_sorted[:max_suggestions]:
            # 检查任务是否可以重新分配
            if self._can_reassign(task):
                suggestion = {
                    "task_id": task.id or task.name,
                    "task_name": task.name,
                    "current_assignee": task.assigned_to,
                    "suggested_assignee": lighter_parent,
                    "priority": task.priority,
                    "duration_minutes": task.duration_minutes,
                    "time_slot": task.time_slot,
                    "reason": "低优先级任务，可转移到负载较轻的一方",
                    "impact": self._calculate_impact(task)
                }
                suggestions.append(suggestion)

        return suggestions

    def _can_reassign(self, task: ScheduledTask) -> bool:
        """
        判断任务是否可以重新分配

        Args:
            task: 任务

        Returns:
            是否可以重新分配
        """
        # 重复任务通常不应轻易重新分配
        if task.is_recurring:
            return False

        # 高优先级任务(>=9)不重新分配
        if task.priority >= 9:
            return False

        return True

    def _calculate_impact(self, task: ScheduledTask) -> str:
        """
        计算重新分配的影响

        Args:
            task: 任务

        Returns:
            影响描述
        """
        if task.priority >= 8:
            return "中等影响"
        elif task.priority >= 5:
            return "较小影响"
        else:
            return "微小影响"

    def optimize_schedule(
        self,
        schedule: DailySchedule
    ) -> Dict:
        """
        优化日程安排

        Args:
            schedule: 日程

        Returns:
            优化结果
        """
        # 分析当前负载均衡
        analysis = self.analyze_imbalance(schedule.tasks)

        # 如果已经很均衡，不需要优化
        if analysis.get("is_balanced", False):
            return {
                "optimization_needed": False,
                "balance_score": analysis["balance_score"],
                "message": "负载已经均衡，无需优化"
            }

        # 生成优化建议
        suggestions = self.suggest_reassignments(schedule.tasks)

        # 估算优化后的效果
        estimated_improvement = self._estimate_improvement(
            analysis,
            len(suggestions)
        )

        return {
            "optimization_needed": True,
            "current_balance_score": analysis["balance_score"],
            "estimated_balance_score": estimated_improvement,
            "suggestions": suggestions,
            "suggestion_count": len(suggestions),
            "message": f"建议转移 {len(suggestions)} 个任务以改善负载均衡"
        }

    def _estimate_improvement(
        self,
        analysis: Dict,
        num_suggestions: int
    ) -> float:
        """
        估算优化后的均衡评分

        Args:
            analysis: 当前不均衡分析
            num_suggestions: 建议数量

        Returns:
            估算的优化后均衡评分
        """
        current_score = analysis["balance_score"]
        task_gap = analysis["task_gap"]

        if task_gap == 0:
            return current_score

        # 简单估算：每个转移的任务缩小一半的差距
        estimated_reduction = min(num_suggestions, task_gap // 2 + 1)
        estimated_gap = max(0, task_gap - estimated_reduction)

        # 计算新的均衡评分
        total_tasks = analysis["parent1"]["task_count"] + analysis["parent2"]["task_count"]
        if total_tasks == 0:
            return 1.0

        estimated_ratio = min(estimated_gap / total_tasks, 0.5)
        estimated_score = 1.0 - (estimated_ratio * 2)

        return round(min(1.0, estimated_score), 3)


# 全局实例
load_balancing_optimizer = LoadBalancingOptimizer()
