from typing import List, Dict, Optional
from datetime import date, datetime, timedelta
from sqlalchemy.orm import Session

from app.models.fatigue import FatigueRecord, SleepRecord
from app.schemas.fatigue import FatigueRecordCreate, SleepRecordCreate, FatigueTrend, FatigueAnalysis


class FatigueCalculator:
    """疲劳度计算器"""

    # 疲劳度计算参数
    TASK_WEIGHT = 0.4          # 任务负载权重
    SLEEP_WEIGHT = 0.4         # 睡眠权重
    WORK_WEIGHT = 0.2          # 工作权重

    # 任务负载系数 (每小时的疲劳贡献)
    TASK_COEFFICIENT = 0.15

    # 睡眠不足系数 (每缺少1小时的疲劳贡献)
    SLEEP_DEFICIT_COEFFICIENT = 0.12

    # 工作时长系数
    WORK_COEFFICIENT = 0.05

    # 疲劳度阈值
    FATIGUE_LOW = 0.3
    FATIGUE_MEDIUM = 0.5
    FATIGUE_HIGH = 0.8

    def calculate_fatigue(
        self,
        total_tasks: int,
        total_task_duration: int,  # 分钟
        actual_sleep: Optional[float],
        target_sleep: Optional[float],
        work_hours: float = 0.0
    ) -> float:
        """
        计算疲劳度评分 (0.0 - 1.0)

        Args:
            total_tasks: 完成的任务数量
            total_task_duration: 总任务时长(分钟)
            actual_sleep: 实际睡眠时长(小时)
            target_sleep: 目标睡眠时长(小时)
            work_hours: 工作时长(小时)

        Returns:
            疲劳度评分 (0.0 = 精力充沛, 1.0 = 极度疲劳)
        """
        # 1. 计算任务负载 (0.0 - 1.0)
        task_hours = total_task_duration / 60.0
        task_load = min(task_hours * self.TASK_COEFFICIENT, 1.0)

        # 2. 计算睡眠不足 (0.0 - 1.0)
        sleep_deficit = 0.0
        if actual_sleep is not None and target_sleep is not None:
            deficit = max(0, target_sleep - actual_sleep)
            sleep_deficit = min(deficit * self.SLEEP_DEFICIT_COEFFICIENT, 1.0)

        # 3. 计算工作影响 (0.0 - 1.0)
        work_impact = min(work_hours * self.WORK_COEFFICIENT, 1.0)

        # 4. 综合计算 (加权平均)
        fatigue_score = (
            task_load * self.TASK_WEIGHT +
            sleep_deficit * self.SLEEP_WEIGHT +
            work_impact * self.WORK_WEIGHT
        )

        # 确保在 [0, 1] 范围内
        return round(max(0.0, min(1.0, fatigue_score)), 3)

    def calculate_from_tasks(
        self,
        parent_id: int,
        tasks: List[dict],
        actual_sleep: Optional[float],
        target_sleep: Optional[float],
        work_hours: float = 0.0
    ) -> Dict[str, float]:
        """
        从任务列表计算疲劳度

        Args:
            parent_id: 父母ID
            tasks: 任务列表 [{"duration_minutes": 30, "priority": 8}, ...]
            actual_sleep: 实际睡眠时长
            target_sleep: 目标睡眠时长
            work_hours: 工作时长

        Returns:
            {"fatigue_score": float, "task_load": float, "sleep_deficit": float, ...}
        """
        total_tasks = len(tasks)
        total_duration = sum(t.get("duration_minutes", 0) for t in tasks)

        fatigue_score = self.calculate_fatigue(
            total_tasks=total_tasks,
            total_task_duration=total_duration,
            actual_sleep=actual_sleep,
            target_sleep=target_sleep,
            work_hours=work_hours
        )

        # 计算各个组成部分
        task_hours = total_duration / 60.0
        task_load = round(min(task_hours * self.TASK_COEFFICIENT, 1.0), 3)

        sleep_deficit = 0.0
        if actual_sleep is not None and target_sleep is not None:
            deficit = max(0, target_sleep - actual_sleep)
            sleep_deficit = round(min(deficit * self.SLEEP_DEFICIT_COEFFICIENT, 1.0), 3)

        return {
            "fatigue_score": fatigue_score,
            "task_load": task_load,
            "sleep_deficit": sleep_deficit,
            "work_hours": work_hours,
            "total_tasks": total_tasks,
            "total_task_duration": total_duration
        }

    def save_fatigue_record(
        self,
        db: Session,
        record: FatigueRecordCreate
    ) -> FatigueRecord:
        """保存疲劳度记录到数据库"""
        # 计算疲劳度
        result = self.calculate_from_tasks(
            parent_id=record.parent_id,
            tasks=[],  # 如果有任务，应该传入
            actual_sleep=record.actual_sleep,
            target_sleep=record.target_sleep,
            work_hours=record.work_hours
        )

        # 创建记录
        db_record = FatigueRecord(
            parent_id=record.parent_id,
            record_date=record.record_date,
            fatigue_score=result["fatigue_score"],
            task_load=result["task_load"],
            sleep_deficit=result["sleep_deficit"],
            work_hours=result["work_hours"],
            total_tasks=record.total_tasks,
            total_task_duration=record.total_task_duration,
            actual_sleep=record.actual_sleep,
            target_sleep=record.target_sleep,
            notes=record.notes
        )

        db.add(db_record)
        db.commit()
        db.refresh(db_record)

        return db_record

    def get_fatigue_trend(
        self,
        db: Session,
        parent_id: int,
        days: int = 7
    ) -> List[FatigueRecord]:
        """获取疲劳度趋势"""
        start_date = date.today() - timedelta(days=days)

        records = db.query(FatigueRecord).filter(
            FatigueRecord.parent_id == parent_id,
            FatigueRecord.record_date >= start_date
        ).order_by(FatigueRecord.record_date.asc()).all()

        return records

    def analyze_fatigue(
        self,
        db: Session,
        parent_id: int,
        record_date: date
    ) -> FatigueAnalysis:
        """分析疲劳度"""
        # 获取当前记录
        current = db.query(FatigueRecord).filter(
            FatigueRecord.parent_id == parent_id,
            FatigueRecord.record_date == record_date
        ).first()

        if not current:
            raise ValueError("No fatigue record found for the given date")

        # 获取历史平均值
        all_records = db.query(FatigueRecord).filter(
            FatigueRecord.parent_id == parent_id
        ).all()

        if not all_records:
            historical_avg = current.fatigue_score
        else:
            historical_avg = sum(r.fatigue_score for r in all_records) / len(all_records)

        # 计算百分位
        sorted_scores = sorted([r.fatigue_score for r in all_records])
        percentile = (sorted_scores.index(current.fatigue_score) + 1) / len(sorted_scores) * 100

        # 风险等级
        if current.fatigue_score < self.FATIGUE_LOW:
            risk_level = "low"
        elif current.fatigue_score < self.FATIGUE_MEDIUM:
            risk_level = "medium"
        else:
            risk_level = "high"

        # 生成建议
        recommendations = self._generate_recommendations(current)

        return FatigueAnalysis(
            current_fatigue=current,
            historical_average=round(historical_avg, 3),
            percentile=round(percentile, 1),
            risk_level=risk_level,
            recommendations=recommendations
        )

    def _generate_recommendations(self, record: FatigueRecord) -> List[str]:
        """生成改善建议"""
        recommendations = []

        # 基于疲劳度等级
        if record.fatigue_score >= self.FATIGUE_HIGH:
            recommendations.append("疲劳度较高，建议增加休息时间")
            recommendations.append("可考虑调整任务分配，减轻负担")

        # 基于睡眠不足
        if record.sleep_deficit > 0.3:
            recommendations.append("睡眠不足明显，建议调整作息")

        # 基于任务负载
        if record.task_load > 0.5:
            recommendations.append("任务负载较重，建议适当减少任务")

        # 基于工作时长
        if record.work_hours > 8:
            recommendations.append("工作时间较长，注意劳逸结合")

        if not recommendations:
            recommendations.append("状态良好，保持当前作息")

        return recommendations

    def compare_parents_fatigue(
        self,
        db: Session,
        record_date: date,
        parent_ids: List[int]
    ) -> Dict:
        """对比父母的疲劳度"""
        records = db.query(FatigueRecord).filter(
            FatigueRecord.record_date == record_date,
            FatigueRecord.parent_id.in_(parent_ids)
        ).all()

        if len(records) < 2:
            return {"error": "Need at least 2 parents to compare"}

        fatigue_scores = [r.fatigue_score for r in records]
        gap = max(fatigue_scores) - min(fatigue_scores)

        # 负载均衡评分 (gap越小越好)
        balance_score = max(0, 1.0 - gap)

        return {
            "date": record_date,
            "parents": [
                {
                    "parent_id": r.parent_id,
                    "fatigue_score": r.fatigue_score,
                    "task_load": r.task_load,
                    "sleep_deficit": r.sleep_deficit
                }
                for r in records
            ],
            "balance_score": round(balance_score, 3),
            "gap": round(gap, 3)
        }


# 全局实例
fatigue_calculator = FatigueCalculator()
