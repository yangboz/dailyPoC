from typing import List, Dict, Optional
import asyncio
from datetime import datetime

class BaseAgent:
    def __init__(self, name: str):
        self.name = name
        self.messages = []
        
    async def process_message(self, message: str) -> str:
        raise NotImplementedError
        
    async def send_message(self, message: str, target_agent: 'BaseAgent') -> None:
        response = await target_agent.process_message(message)
        self.messages.append({
            'timestamp': datetime.now(),
            'from': self.name,
            'to': target_agent.name,
            'message': message,
            'response': response
        })

class CreatorAgent(BaseAgent):
    def __init__(self):
        super().__init__("Creator")
        self.content_types = ["article", "image", "video"]
        self.content_archive = []
        
    async def process_message(self, message: str) -> str:
        if "create" in message.lower():
            content = await self.generate_content(message)
            self.content_archive.append(content)
            return f"Created content: {content[:100]}..."
        return "Message received but no content creation requested."
        
    async def generate_content(self, prompt: str) -> str:
        # 模拟内容生成过程
        return f"Generated content based on: {prompt}\n" + \
               "This is a sample article about technology trends..."
               
    async def analyze_trends(self) -> Dict:
        # 模拟趋势分析
        return {
            "trending_topics": ["AI", "Blockchain", "Sustainability"],
            "audience_engagement": 0.85
        }

class BuilderAgent(BaseAgent):
    def __init__(self):
        super().__init__("Builder")
        self.current_projects = {}
        
    async def process_message(self, message: str) -> str:
        if "build" in message.lower():
            code = await self.generate_code(message)
            return f"Generated code structure: {code[:100]}..."
        return "Message received but no building requested."
        
    async def generate_code(self, specification: str) -> str:
        # 模拟代码生成过程
        return """
        class ProjectStructure:
            def __init__(self):
                self.components = []
                self.database = Database()
                
            def add_component(self, component):
                self.components.append(component)
        """
        
    async def review_code(self, code: str) -> List[str]:
        # 模拟代码审查过程
        return ["Suggestion 1: Optimize database queries", 
                "Suggestion 2: Add error handling"]

class OwnerAgent(BaseAgent):
    def __init__(self):
        super().__init__("Owner")
        self.builder = BuilderAgent()
        self.creator = CreatorAgent()
        self.strategy = {}
        
    async def process_message(self, message: str) -> str:
        if "vision" in message.lower():
            return await self.create_vision(message)
        elif "coordinate" in message.lower():
            return await self.coordinate_tasks(message)
        return "Message received but no specific action requested."
        
    async def create_vision(self, context: str) -> str:
        # 模拟愿景规划过程
        vision = f"Strategic vision based on: {context}\n" + \
                "1. Market expansion\n" + \
                "2. Technology innovation\n" + \
                "3. Community building"
        self.strategy['vision'] = vision
        return vision
        
    async def coordinate_tasks(self, requirements: str) -> str:
        # 分配任务给Builder和Creator
        builder_task = await self.builder.process_message(f"build {requirements}")
        creator_task = await self.creator.process_message(f"create content for {requirements}")
        
        return f"Coordinated tasks:\nBuilder: {builder_task}\nCreator: {creator_task}"

async def main():
    # 创建Agent实例
    owner = OwnerAgent()
    
    # 模拟业务流程
    print("1. Owner creating vision...")
    vision_result = await owner.process_message("Create vision for AI-powered education platform")
    print(vision_result)
    
    print("\n2. Owner coordinating tasks...")
    coordination_result = await owner.coordinate_tasks("Build and promote an online learning system")
    print(coordination_result)
    
    # 模拟直接Agent间交互
    print("\n3. Direct agent interaction...")
    await owner.builder.send_message(
        "Generate backend API for content management",
        owner.creator
    )

if __name__ == "__main__":
    asyncio.run(main())
