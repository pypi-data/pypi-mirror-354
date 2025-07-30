"""
搜索小红书笔记工具
支持根据关键词搜索相关笔记
"""

import logging
from typing import Dict, Any
from tools.base_tool import BaseTool, ToolResult

logger = logging.getLogger(__name__)

class SearchNotesTool(BaseTool):
    """搜索小红书笔记工具"""
    
    def __init__(self, adapter):
        super().__init__(
            name="xiaohongshu_search_notes",
            description="根据关键词搜索小红书笔记，获取相关内容的标题和链接"
        )
        self.adapter = adapter
    
    async def execute(self, arguments: Dict[str, Any]) -> ToolResult:
        """
        执行搜索笔记操作
        
        Args:
            arguments: 包含搜索参数的字典
                - keywords: 搜索关键词 (必需)
                - limit: 返回结果数量限制 (可选，默认5，最多20)
        
        Returns:
            搜索结果
        """
        try:
            keywords = arguments["keywords"]
            limit = arguments.get("limit", 5)
            
            # 参数验证
            if not keywords or not keywords.strip():
                return ToolResult(
                    success=False,
                    error="搜索关键词不能为空"
                )
            
            if limit < 1 or limit > 20:
                return ToolResult(
                    success=False,
                    error="结果数量限制必须在1-20之间"
                )
            
            # 执行搜索
            self.logger.info(f"开始搜索笔记，关键词: {keywords}, 限制: {limit}")
            
            result = await self.adapter.search_notes(keywords.strip(), limit)
            
            if result.get("success"):
                search_data = result.get("data", [])
                
                if search_data:
                    # 格式化搜索结果
                    formatted_results = []
                    for i, note in enumerate(search_data, 1):
                        formatted_results.append({
                            "序号": i,
                            "标题": note.get("title", "未知标题"),
                            "链接": note.get("url", "")
                        })
                    
                    return ToolResult(
                        success=True,
                        data={
                            "搜索关键词": keywords,
                            "找到结果": len(search_data),
                            "笔记列表": formatted_results
                        },
                        message=f"成功找到 {len(search_data)} 条与'{keywords}'相关的笔记"
                    )
                else:
                    return ToolResult(
                        success=True,
                        data={
                            "搜索关键词": keywords,
                            "找到结果": 0,
                            "笔记列表": []
                        },
                        message=f"未找到与'{keywords}'相关的笔记，建议尝试其他关键词"
                    )
            else:
                error_message = result.get("message", "搜索失败，未知错误")
                return ToolResult(
                    success=False,
                    error=error_message,
                    message=f"搜索'{keywords}'时出现问题"
                )
        
        except Exception as e:
            self.logger.error(f"搜索笔记时出错: {str(e)}")
            return ToolResult(
                success=False,
                error=str(e),
                message="搜索操作执行失败"
            )
    
    def get_schema(self) -> Dict[str, Any]:
        """
        获取工具的 JSON Schema
        
        Returns:
            工具参数的 JSON Schema
        """
        return {
            "type": "object",
            "properties": {
                "keywords": {
                    "type": "string",
                    "description": "搜索关键词，如：美食、旅行、穿搭、数码等",
                    "minLength": 1,
                    "maxLength": 100
                },
                "limit": {
                    "type": "integer",
                    "description": "返回结果数量限制，默认5条，最多20条",
                    "minimum": 1,
                    "maximum": 20,
                    "default": 5
                }
            },
            "required": ["keywords"]
        }
    
    def _format_success_result(self, result: ToolResult) -> str:
        """格式化成功结果"""
        if not result.data:
            return f"✅ {self.name} 执行成功\n\n📝 {result.message}"
        
        data = result.data
        output = f"🔍 搜索结果\n\n"
        output += f"🔑 关键词: {data.get('搜索关键词', 'N/A')}\n"
        output += f"📊 找到结果: {data.get('找到结果', 0)} 条\n\n"
        
        notes = data.get("笔记列表", [])
        if notes:
            output += "📝 笔记列表:\n"
            for note in notes:
                output += f"\n{note['序号']}. {note['标题']}\n"
                output += f"   🔗 链接: {note['链接']}\n"
        else:
            output += "💡 建议: 尝试使用更通用的关键词，如'美食'、'旅行'、'穿搭'等"
        
        output += f"\n\n🕐 完成时间: {result.timestamp}"
        
        return output 