from typing import List, Optional
from app.schemas.knowledge import (
    VaccineSchedule,
    FoodRecommendation,
    EducationActivity,
    DevelopmentMilestone,
    KnowledgeBaseResponse
)


class KnowledgeBaseService:
    """知识库服务 - 提供疫苗、辅食、早教等知识"""

    # 疫苗接种计划 (0-24个月)
    VACCINE_SCHEDULE = [
        # 出生
        {
            "id": 1,
            "vaccine_name": "乙肝疫苗(第1针)",
            "age_months": 0,
            "description": "预防乙型肝炎病毒感染",
            "importance": "required",
            "side_effects": "接种部位红肿、发热，通常1-2天内消失",
            "notes": "出生24小时内接种"
        },
        {
            "id": 2,
            "vaccine_name": "卡介苗",
            "age_months": 0,
            "description": "预防结核病",
            "importance": "required",
            "side_effects": "接种部位红肿、化脓，形成疤痕",
            "notes": "出生后尽快接种"
        },
        # 1个月
        {
            "id": 3,
            "vaccine_name": "乙肝疫苗(第2针)",
            "age_months": 1,
            "description": "预防乙型肝炎病毒感染",
            "importance": "required",
            "side_effects": "接种部位红肿、发热",
            "notes": "与第1针间隔1个月"
        },
        # 2个月
        {
            "id": 4,
            "vaccine_name": "脊灰疫苗(第1针)",
            "age_months": 2,
            "description": "预防脊髓灰质炎",
            "importance": "required",
            "side_effects": "发热、轻微腹泻",
            "notes": "口服减毒活疫苗"
        },
        {
            "id": 5,
            "vaccine_name": "五联疫苗(第1针)",
            "age_months": 2,
            "description": "预防白喉、破伤风、百日咳、脊灰、Hib",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": "可替代脊灰、百白破、Hib疫苗"
        },
        # 3个月
        {
            "id": 6,
            "vaccine_name": "脊灰疫苗(第2针)",
            "age_months": 3,
            "description": "预防脊髓灰质炎",
            "importance": "required",
            "side_effects": "发热、轻微腹泻",
            "notes": ""
        },
        {
            "id": 7,
            "vaccine_name": "五联疫苗(第2针)",
            "age_months": 3,
            "description": "预防白喉、破伤风、百日咳、脊灰、Hib",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        {
            "id": 8,
            "vaccine_name": "肺炎疫苗(第1针)",
            "age_months": 3,
            "description": "预防肺炎球菌感染",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": "自费疫苗，推荐接种"
        },
        # 4个月
        {
            "id": 9,
            "vaccine_name": "脊灰疫苗(第3针)",
            "age_months": 4,
            "description": "预防脊髓灰质炎",
            "importance": "required",
            "side_effects": "发热、轻微腹泻",
            "notes": ""
        },
        {
            "id": 10,
            "vaccine_name": "五联疫苗(第3针)",
            "age_months": 4,
            "description": "预防白喉、破伤风、百日咳、脊灰、Hib",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        {
            "id": 11,
            "vaccine_name": "肺炎疫苗(第2针)",
            "age_months": 4,
            "description": "预防肺炎球菌感染",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        # 5个月
        {
            "id": 12,
            "vaccine_name": "五联疫苗(第4针)",
            "age_months": 5,
            "description": "预防白喉、破伤风、百日咳、脊灰、Hib",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        {
            "id": 13,
            "vaccine_name": "肺炎疫苗(第3针)",
            "age_months": 5,
            "description": "预防肺炎球菌感染",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        # 6个月
        {
            "id": 14,
            "vaccine_name": "乙肝疫苗(第3针)",
            "age_months": 6,
            "description": "预防乙型肝炎病毒感染",
            "importance": "required",
            "side_effects": "接种部位红肿、发热",
            "notes": ""
        },
        {
            "id": 15,
            "vaccine_name": "流脑A群(第1针)",
            "age_months": 6,
            "description": "预防流行性脑脊髓膜炎",
            "importance": "required",
            "side_effects": "发热、接种部位红肿",
            "notes": "2针间隔3个月"
        },
        # 8个月
        {
            "id": 16,
            "vaccine_name": "麻疹疫苗(第1针)",
            "age_months": 8,
            "description": "预防麻疹",
            "importance": "required",
            "side_effects": "发热、皮疹",
            "notes": "8月龄接种"
        },
        {
            "id": 17,
            "vaccine_name": "乙脑减毒活疫苗(第1针)",
            "age_months": 8,
            "description": "预防流行性乙型脑炎",
            "importance": "required",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        # 9个月
        {
            "id": 18,
            "vaccine_name": "流脑A群(第2针)",
            "age_months": 9,
            "description": "预防流行性脑脊髓膜炎",
            "importance": "required",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        # 12个月
        {
            "id": 19,
            "vaccine_name": "水痘疫苗",
            "age_months": 12,
            "description": "预防水痘-带状疱疹病毒感染",
            "importance": "recommended",
            "side_effects": "发热、皮疹",
            "notes": "自费疫苗，推荐接种"
        },
        {
            "id": 20,
            "vaccine_name": "EV71手足口病疫苗(第1针)",
            "age_months": 12,
            "description": "预防EV71病毒所致手足口病",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": "自费疫苗，2针间隔1个月"
        },
        # 18个月
        {
            "id": 21,
            "vaccine_name": "五联疫苗(加强针)",
            "age_months": 18,
            "description": "预防白喉、破伤风、百日咳、脊灰、Hib",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": "加强免疫"
        },
        {
            "id": 22,
            "vaccine_name": "麻疹疫苗(第2针)",
            "age_months": 18,
            "description": "预防麻疹",
            "importance": "required",
            "side_effects": "发热、皮疹",
            "notes": ""
        },
        {
            "id": 23,
            "vaccine_name": "乙脑减毒活疫苗(第2针)",
            "age_months": 18,
            "description": "预防流行性乙型脑炎",
            "importance": "required",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        {
            "id": 24,
            "vaccine_name": "甲肝减毒活疫苗",
            "age_months": 18,
            "description": "预防甲型肝炎",
            "importance": "required",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        },
        # 24个月
        {
            "id": 25,
            "vaccine_name": "EV71手足口病疫苗(第2针)",
            "age_months": 24,
            "description": "预防EV71病毒所致手足口病",
            "importance": "recommended",
            "side_effects": "发热、接种部位红肿",
            "notes": ""
        }
    ]

    # 辅食推荐 (按月龄)
    FOOD_RECOMMENDATIONS = [
        # 4-6个月
        {
            "id": 1,
            "food_name": "米糊",
            "category": "grain",
            "age_months_from": 4,
            "age_months_to": 6,
            "nutrition": "富含碳水化合物，易于消化",
            "preparation": "婴儿米粉用温水调成糊状，由稀到稠",
            "precautions": "首次尝试少量，观察过敏反应",
            "allergy_risk": False
        },
        {
            "id": 2,
            "food_name": "苹果泥",
            "category": "fruit",
            "age_months_from": 4,
            "age_months_to": 6,
            "nutrition": "富含维生素C和膳食纤维",
            "preparation": "蒸煮后压成泥",
            "precautions": "酸性较强，从少量开始",
            "allergy_risk": False
        },
        {
            "id": 3,
            "food_name": "香蕉泥",
            "category": "fruit",
            "age_months_from": 4,
            "age_months_to": 6,
            "nutrition": "富含钾和维生素B6",
            "preparation": "熟透香蕉压成泥",
            "precautions": "天然甜味，宝宝容易接受",
            "allergy_risk": False
        },
        # 6-8个月
        {
            "id": 4,
            "food_name": "南瓜泥",
            "category": "vegetable",
            "age_months_from": 6,
            "age_months_to": 8,
            "nutrition": "富含β-胡萝卜素和维生素C",
            "preparation": "蒸煮后压成泥",
            "precautions": "天然甜味，口感顺滑",
            "allergy_risk": False
        },
        {
            "id": 5,
            "food_name": "胡萝卜泥",
            "category": "vegetable",
            "age_months_from": 6,
            "age_months_to": 8,
            "nutrition": "富含β-胡萝卜素和维生素A",
            "preparation": "蒸煮后压成泥，用橄榄油调味",
            "precautions": "需要油脂帮助吸收",
            "allergy_risk": False
        },
        {
            "id": 6,
            "food_name": "土豆泥",
            "category": "vegetable",
            "age_months_from": 6,
            "age_months_to": 8,
            "nutrition": "富含碳水化合物和钾",
            "preparation": "蒸煮后压成泥",
            "precautions": "口感细腻，宝宝易接受",
            "allergy_risk": False
        },
        {
            "id": 7,
            "food_name": "蛋黄泥",
            "category": "grain",
            "age_months_from": 6,
            "age_months_to": 8,
            "nutrition": "富含蛋白质、铁和维生素",
            "preparation": "煮熟鸡蛋，取1/4个蛋黄压泥",
            "precautions": "从少量开始，观察过敏",
            "allergy_risk": True
        },
        {
            "id": 8,
            "food_name": "小米粥",
            "category": "grain",
            "age_months_from": 6,
            "age_months_to": 8,
            "nutrition": "富含B族维生素和矿物质",
            "preparation": "小米煮至软烂",
            "precautions": "煮得足够烂",
            "allergy_risk": False
        },
        # 8-10个月
        {
            "id": 9,
            "food_name": "肉泥(猪肉/鸡肉)",
            "category": "meat",
            "age_months_from": 8,
            "age_months_to": 10,
            "nutrition": "富含优质蛋白质和铁",
            "preparation": "蒸煮后打成泥",
            "precautions": "从少量开始，确保肉新鲜",
            "allergy_risk": False
        },
        {
            "id": 10,
            "food_name": "肝泥",
            "category": "meat",
            "age_months_from": 8,
            "age_months_to": 10,
            "nutrition": "富含铁和维生素A",
            "preparation": "猪肝/鸡肝蒸熟后打成泥",
            "precautions": "每周1-2次即可",
            "allergy_risk": False
        },
        {
            "id": 11,
            "food_name": "菠菜泥",
            "category": "vegetable",
            "age_months_from": 8,
            "age_months_to": 10,
            "nutrition": "富含铁和叶酸",
            "preparation": "焯水后打成泥",
            "precautions": "草酸含量高，需要焯水",
            "allergy_risk": False
        },
        {
            "id": 12,
            "food_name": "豆腐",
            "category": "meat",
            "age_months_from": 8,
            "age_months_to": 10,
            "nutrition": "富含植物蛋白质和钙",
            "preparation": "切小块，蒸煮软烂",
            "precautions": "豆制品过敏者慎用",
            "allergy_risk": True
        },
        # 10-12个月
        {
            "id": 13,
            "food_name": "手指食物(软块)",
            "category": "grain",
            "age_months_from": 10,
            "age_months_to": 12,
            "nutrition": "锻炼自主进食能力",
            "preparation": "蔬菜、水果切小软块",
            "precautions": "大小适中，防噎食",
            "allergy_risk": False
        },
        {
            "id": 14,
            "food_name": "碎肉末",
            "category": "meat",
            "age_months_from": 10,
            "age_months_to": 12,
            "nutrition": "富含蛋白质和铁",
            "preparation": "肉剁碎，炒或蒸",
            "precautions": "质地细腻易消化",
            "allergy_risk": False
        },
        {
            "id": 15,
            "food_name": "全蛋",
            "category": "grain",
            "age_months_from": 10,
            "age_months_to": 12,
            "nutrition": "完整蛋白质",
            "preparation": "蒸蛋羹、炒蛋",
            "precautions": "确保不过敏",
            "allergy_risk": True
        },
        {
            "id": 16,
            "food_name": "酸奶",
            "category": "meat",
            "age_months_from": 10,
            "age_months_to": 12,
            "nutrition": "富含钙和益生菌",
            "preparation": "选择无糖原味酸奶",
            "precautions": "乳糖不耐受者慎用",
            "allergy_risk": True
        }
    ]

    # 早教活动 (按月龄)
    EDUCATION_ACTIVITIES = [
        # 0-3个月
        {
            "id": 1,
            "activity_name": "追视训练",
            "category": "cognitive",
            "age_months_from": 0,
            "age_months_to": 3,
            "description": "用红色或黑白卡片在宝宝眼前缓慢移动，引导宝宝追视",
            "duration_minutes": 5,
            "benefits": "发展视觉能力和注意力",
            "materials": "红色球、黑白卡片",
            "instructions": "在宝宝清醒时，距离20-30cm缓慢移动物体"
        },
        {
            "id": 2,
            "activity_name": "抬头练习",
            "category": "motor",
            "age_months_from": 0,
            "age_months_to": 3,
            "description": "趴在床上，引导宝宝抬头",
            "duration_minutes": 3,
            "benefits": "增强颈部和背部肌肉",
            "materials": "爬行垫、玩具",
            "instructions": "每次练习1-2分钟，每天多次"
        },
        {
            "id": 3,
            "activity_name": "抚触按摩",
            "category": "social",
            "age_months_from": 0,
            "age_months_to": 3,
            "description": "轻柔的全身按摩",
            "duration_minutes": 10,
            "benefits": "促进亲子关系，舒缓情绪",
            "materials": "婴儿润肤油",
            "instructions": "温暖的环境下，从头部到脚部轻柔按摩"
        },
        # 3-6个月
        {
            "id": 4,
            "activity_name": "抓握练习",
            "category": "motor",
            "age_months_from": 3,
            "age_months_to": 6,
            "description": "提供不同质地的玩具让宝宝抓握",
            "duration_minutes": 10,
            "benefits": "发展精细动作和触觉",
            "materials": "摇铃、布书、橡胶牙胶",
            "instructions": "将玩具放在宝宝手中，鼓励抓握"
        },
        {
            "id": 5,
            "activity_name": "翻身练习",
            "category": "motor",
            "age_months_from": 3,
            "age_months_to": 6,
            "description": "引导宝宝从仰卧翻到侧卧，再到俯卧",
            "duration_minutes": 5,
            "benefits": "增强核心力量，发展大运动",
            "materials": "玩具",
            "instructions": "用玩具在侧面引导宝宝翻身"
        },
        {
            "id": 6,
            "activity_name": "咿呀学语",
            "category": "language",
            "age_months_from": 3,
            "age_months_to": 6,
            "description": "与宝宝对话，回应宝宝的声音",
            "duration_minutes": 15,
            "benefits": "促进语言发展",
            "materials": "无",
            "instructions": "面对面交流，模仿宝宝的声音，鼓励发声"
        },
        {
            "id": 7,
            "activity_name": "照镜子",
            "category": "cognitive",
            "age_months_from": 3,
            "age_months_to": 6,
            "description": "让宝宝看镜子中的自己",
            "duration_minutes": 5,
            "benefits": "发展自我认知",
            "materials": "安全镜子",
            "instructions": "抱宝宝到镜子前，指出宝宝的身体部位"
        },
        # 6-9个月
        {
            "id": 8,
            "activity_name": "积木游戏",
            "category": "motor",
            "age_months_from": 6,
            "age_months_to": 9,
            "description": "堆积木、敲打积木",
            "duration_minutes": 15,
            "benefits": "发展手眼协调和精细动作",
            "materials": "软积木或木质积木",
            "instructions": "示范堆积木，鼓励宝宝模仿"
        },
        {
            "id": 9,
            "activity_name": "爬行练习",
            "category": "motor",
            "age_months_from": 6,
            "age_months_to": 9,
            "description": "用玩具引导宝宝爬行",
            "duration_minutes": 10,
            "benefits": "增强大运动能力",
            "materials": "玩具、爬行垫",
            "instructions": "在宝宝前方放置玩具，鼓励爬行"
        },
        {
            "id": 10,
            "activity_name": "躲猫猫游戏",
            "category": "cognitive",
            "age_months_from": 6,
            "age_months_to": 9,
            "description": "用手帕或门遮挡脸，然后突然出现",
            "duration_minutes": 10,
            "benefits": "发展客体永久性概念",
            "materials": "手帕",
            "instructions": "说'躲猫猫'，遮挡脸，然后突然出现"
        },
        {
            "id": 11,
            "activity_name": "指认物品",
            "category": "language",
            "age_months_from": 6,
            "age_months_to": 9,
            "description": "教宝宝指认日常物品",
            "duration_minutes": 10,
            "benefits": "发展语言理解能力",
            "materials": "日常用品",
            "instructions": "说出物品名称，让宝宝指出或拿取"
        },
        # 9-12个月
        {
            "id": 12,
            "activity_name": "站立练习",
            "category": "motor",
            "age_months_from": 9,
            "age_months_to": 12,
            "description": "扶站、扶走练习",
            "duration_minutes": 10,
            "benefits": "增强腿部力量，为走路做准备",
            "materials": "稳固的家具、学步车",
            "instructions": "让宝宝扶着稳固的家具站立"
        },
        {
            "id": 13,
            "activity_name": "套圈游戏",
            "category": "motor",
            "age_months_from": 9,
            "age_months_to": 12,
            "description": "将套圈套在柱子上",
            "duration_minutes": 15,
            "benefits": "发展手眼协调和精细动作",
            "materials": "套圈玩具",
            "instructions": "示范套圈，鼓励宝宝尝试"
        },
        {
            "id": 14,
            "activity_name": "简单指令",
            "category": "language",
            "age_months_from": 9,
            "age_months_to": 12,
            "description": "教宝宝理解简单指令",
            "duration_minutes": 10,
            "benefits": "发展语言理解和执行能力",
            "materials": "无",
            "instructions": "说'给我'、'再见'等简单指令"
        },
        {
            "id": 15,
            "activity_name": "模仿游戏",
            "category": "social",
            "age_months_from": 9,
            "age_months_to": 12,
            "description": "拍手、挥手、做鬼脸",
            "duration_minutes": 10,
            "benefits": "发展社交能力和模仿能力",
            "materials": "无",
            "instructions": "做动作让宝宝模仿"
        },
        # 12-18个月
        {
            "id": 16,
            "activity_name": "拼图游戏",
            "category": "cognitive",
            "age_months_from": 12,
            "age_months_to": 18,
            "description": "简单的形状拼图",
            "duration_minutes": 15,
            "benefits": "发展认知和问题解决能力",
            "materials": "形状拼图板",
            "instructions": "从简单的2-3块拼图开始"
        },
        {
            "id": 17,
            "activity_name": "涂鸦",
            "category": "motor",
            "age_months_from": 12,
            "age_months_to": 18,
            "description": "用蜡笔或手指画",
            "duration_minutes": 15,
            "benefits": "发展创造力和精细动作",
            "materials": "安全蜡笔、手指画颜料、纸",
            "instructions": "提供大纸张，让宝宝自由涂鸦"
        },
        {
            "id": 18,
            "activity_name": "角色扮演",
            "category": "social",
            "age_months_from": 12,
            "age_months_to": 18,
            "description": "玩过家家、给玩具喂饭",
            "duration_minutes": 20,
            "benefits": "发展想象力和社交技能",
            "materials": "玩具餐具、娃娃",
            "instructions": "示范日常活动，让宝宝模仿"
        },
        {
            "id": 19,
            "activity_name": "大运动游戏",
            "category": "motor",
            "age_months_from": 12,
            "age_months_to": 18,
            "description": "踢球、爬隧道",
            "duration_minutes": 20,
            "benefits": "发展大运动能力和协调性",
            "materials": "软球、爬行隧道",
            "instructions": "在安全空间让宝宝自由活动"
        },
        # 18-24个月
        {
            "id": 20,
            "activity_name": "积木搭建",
            "category": "motor",
            "age_months_from": 18,
            "age_months_to": 24,
            "description": "用积木搭建简单结构",
            "duration_minutes": 20,
            "benefits": "发展空间认知和精细动作",
            "materials": "木质积木",
            "instructions": "示范搭高、搭桥，鼓励宝宝模仿"
        },
        {
            "id": 21,
            "activity_name": "简单手工",
            "category": "motor",
            "age_months_from": 18,
            "age_months_to": 24,
            "description": "粘贴、串珠",
            "duration_minutes": 20,
            "benefits": "发展精细动作和创造力",
            "materials": "贴纸、大孔珠子、绳子",
            "instructions": "在家长指导下进行"
        },
        {
            "id": 22,
            "activity_name": "绘本阅读",
            "category": "language",
            "age_months_from": 18,
            "age_months_to": 24,
            "description": "阅读简单绘本",
            "duration_minutes": 15,
            "benefits": "发展语言能力和阅读兴趣",
            "materials": "图画书",
            "instructions": "指认图片，讲述故事"
        },
        {
            "id": 23,
            "activity_name": "音乐律动",
            "category": "social",
            "age_months_from": 18,
            "age_months_to": 24,
            "description": "跟随音乐跳舞、做动作",
            "duration_minutes": 15,
            "benefits": "发展节奏感和大运动",
            "materials": "儿童音乐",
            "instructions": "播放音乐，和宝宝一起跳舞"
        }
    ]

    # 发育里程碑
    DEVELOPMENT_MILESTONES = [
        # 运动发育
        {
            "id": 1,
            "age_months": 2,
            "category": "motor",
            "milestone": "能抬头",
            "typical_range": "1-3个月",
            "concern_signs": "3个月仍不能抬头"
        },
        {
            "id": 2,
            "age_months": 4,
            "category": "motor",
            "milestone": "能翻身",
            "typical_range": "3-6个月",
            "concern_signs": "6个月仍不能翻身"
        },
        {
            "id": 3,
            "age_months": 7,
            "category": "motor",
            "milestone": "能独坐",
            "typical_range": "5-8个月",
            "concern_signs": "8个月仍不能独坐"
        },
        {
            "id": 4,
            "age_months": 10,
            "category": "motor",
            "milestone": "能爬行",
            "typical_range": "7-11个月",
            "concern_signs": "12个月仍不能爬行"
        },
        {
            "id": 5,
            "age_months": 12,
            "category": "motor",
            "milestone": "能扶站",
            "typical_range": "9-14个月",
            "concern_signs": "15个月仍不能扶站"
        },
        {
            "id": 6,
            "age_months": 15,
            "category": "motor",
            "milestone": "能独立走几步",
            "typical_range": "12-18个月",
            "concern_signs": "18个月仍不能走路"
        },
        # 语言发育
        {
            "id": 7,
            "age_months": 3,
            "category": "language",
            "milestone": "会发出咿呀声",
            "typical_range": "2-4个月",
            "concern_signs": "4个月仍不会发出声音"
        },
        {
            "id": 8,
            "age_months": 6,
            "category": "language",
            "milestone": "会对声音做出反应",
            "typical_range": "4-7个月",
            "concern_signs": "7个月对声音无反应"
        },
        {
            "id": 9,
            "age_months": 12,
            "category": "language",
            "milestone": "会说1-2个简单词",
            "typical_range": "10-14个月",
            "concern_signs": "15个月仍不会说话"
        },
        {
            "id": 10,
            "age_months": 18,
            "category": "language",
            "milestone": "能说10个以上的词",
            "typical_range": "15-24个月",
            "concern_signs": "20个月词汇量少于10个"
        },
        {
            "id": 11,
            "age_months": 24,
            "category": "language",
            "milestone": "能说简单句子(2-3个词)",
            "typical_range": "20-30个月",
            "concern_signs": "30个月仍不会说句子"
        },
        # 认知发育
        {
            "id": 12,
            "age_months": 3,
            "category": "cognitive",
            "milestone": "会注视人脸和物体",
            "typical_range": "2-4个月",
            "concern_signs": "4个月仍不注视"
        },
        {
            "id": 13,
            "age_months": 6,
            "category": "cognitive",
            "milestone": "会找隐藏的物体",
            "typical_range": "5-8个月",
            "concern_signs": "9个月仍不理解物体永久性"
        },
        {
            "id": 14,
            "age_months": 12,
            "category": "cognitive",
            "milestone": "会模仿动作和声音",
            "typical_range": "9-15个月",
            "concern_signs": "15个月仍不会模仿"
        },
        {
            "id": 15,
            "age_months": 18,
            "category": "cognitive",
            "milestone": "能玩简单假装游戏",
            "typical_range": "15-24个月",
            "concern_signs": "24个月仍不会假装游戏"
        },
        {
            "id": 16,
            "age_months": 24,
            "category": "cognitive",
            "milestone": "能按颜色或形状分类",
            "typical_range": "20-30个月",
            "concern_signs": "30个月仍不会分类"
        },
        # 社交发育
        {
            "id": 17,
            "age_months": 3,
            "category": "social",
            "milestone": "会微笑回应",
            "typical_range": "2-4个月",
            "concern_signs": "4个月仍不会微笑"
        },
        {
            "id": 18,
            "age_months": 6,
            "category": "social",
            "milestone": "会认生",
            "typical_range": "5-9个月",
            "concern_signs": "9个月仍不认生"
        },
        {
            "id": 19,
            "age_months": 12,
            "category": "social",
            "milestone": "会挥手再见",
            "typical_range": "9-14个月",
            "concern_signs": "15个月仍不会示意性动作"
        },
        {
            "id": 20,
            "age_months": 18,
            "category": "social",
            "milestone": "会与其他孩子互动",
            "typical_range": "15-24个月",
            "concern_signs": "24个月仍对其他孩子无兴趣"
        },
        {
            "id": 21,
            "age_months": 24,
            "category": "social",
            "milestone": "会与其他孩子一起玩耍",
            "typical_range": "20-36个月",
            "concern_signs": "30个月仍完全平行游戏"
        }
    ]

    def get_vaccines_by_age(self, age_months: int) -> List[VaccineSchedule]:
        """根据月龄获取推荐疫苗"""
        vaccines = [
            VaccineSchedule(**v) for v in self.VACCINE_SCHEDULE
            if v["age_months"] == age_months
        ]
        return vaccines

    def get_upcoming_vaccines(self, age_months: int) -> List[VaccineSchedule]:
        """获取即将需要接种的疫苗(未来3个月内)"""
        upcoming = [
            VaccineSchedule(**v) for v in self.VACCINE_SCHEDULE
            if 0 <= v["age_months"] - age_months <= 3
        ]
        return upcoming

    def get_foods_by_age(self, age_months: int) -> List[FoodRecommendation]:
        """根据月龄获取辅食推荐"""
        foods = [
            FoodRecommendation(**f) for f in self.FOOD_RECOMMENDATIONS
            if f["age_months_from"] <= age_months <= f["age_months_to"]
        ]
        return foods

    def get_activities_by_age(self, age_months: int) -> List[EducationActivity]:
        """根据月龄获取早教活动"""
        activities = [
            EducationActivity(**a) for a in self.EDUCATION_ACTIVITIES
            if a["age_months_from"] <= age_months <= a["age_months_to"]
        ]
        return activities

    def get_milestones_by_age(self, age_months: int) -> List[DevelopmentMilestone]:
        """根据月龄获取发育里程碑"""
        milestones = [
            DevelopmentMilestone(**m) for m in self.DEVELOPMENT_MILESTONES
            if m["age_months"] == age_months or
               (m["typical_range"] and
                self._is_in_age_range(age_months, m["typical_range"]))
        ]
        return milestones

    def get_comprehensive_knowledge(self, age_months: int) -> KnowledgeBaseResponse:
        """获取综合知识(疫苗、辅食、活动、里程碑)"""
        return KnowledgeBaseResponse(
            baby_age_months=age_months,
            vaccines=self.get_upcoming_vaccines(age_months),
            foods=self.get_foods_by_age(age_months),
            activities=self.get_activities_by_age(age_months),
            milestones=self.get_milestones_by_age(age_months)
        )

    def _is_in_age_range(self, age_months: int, range_str: str) -> bool:
        """检查月龄是否在典型范围内"""
        try:
            # 解析范围字符串，如 "1-3个月" -> [1, 3]
            range_str = range_str.replace("个月", "").strip()
            parts = range_str.split("-")
            if len(parts) == 2:
                min_age = int(parts[0])
                max_age = int(parts[1])
                return min_age <= age_months <= max_age
        except (ValueError, IndexError):
            pass
        return False


# 全局实例
knowledge_base_service = KnowledgeBaseService()
