# gemini_list_mapper/mapper.py

import os
import yaml
import re # 引入正则表达式库用于解析
import google.generativeai as genai
from typing import List, Optional, Any, Dict
import importlib.resources as pkg_resources

class GeminiListMapper:
    """
    [V11 - 正则表达式修复版]
    """
    # ... create_default_config 和 __init__ 方法保持不变 ...
    @staticmethod
    def create_default_config(output_path: str='config.yml', overwrite: bool=False):
        if os.path.exists(output_path) and not overwrite: return False
        try:
            template_content = pkg_resources.files('gemini_list_mapper').joinpath('config.template.yml').read_text(encoding='utf-8')
            with open(output_path, 'w', encoding='utf-8') as f: f.write(template_content)
            return True
        except: return False

    def __init__(self, config_path: str = 'config.yml', api_key: Optional[str] = None):
        api_key = api_key or os.environ.get("GOOGLE_API_KEY")
        if not api_key: raise ValueError("API Key not found.")
        genai.configure(api_key=api_key)
        if not os.path.exists(config_path): self.create_default_config(config_path)
        with open(config_path, 'r', encoding='utf-8') as f: self.config = yaml.safe_load(f)

    def _build_final_prompt(self, user_prompt: str, item_count: int) -> str:
        # 这个方法是多余的，但在最终版中我们还是把它删掉以保持代码整洁
        return user_prompt

    def map_list(
        self,
        task_name: str,
        input_list: List[str],
        overrides: Optional[Dict[str, Any]] = None
    ) -> List[str]:
        """
        [V11] 核心映射方法，修复了正则表达式以同时匹配单双引号。
        """
        task_config = self.config['tasks'].get(task_name)
        if not task_config: raise ValueError(f"Task '{task_name}' not found.")

        variables = task_config.get('default_variables', {}).copy()
        if overrides: variables.update(overrides)

        item_count = len(input_list)
        if item_count == 0: return []

        # 格式化输入
        formatted_list_items = "\n".join([f'<item id="{i}">{text}</item>' for i, text in enumerate(input_list)])

        model_name = task_config['model']
        prompt_template = task_config['prompt_template']
        # 注意：这里的final_prompt现在就是填充后的模板，不再需要_build_final_prompt
        final_prompt = prompt_template.format(list_items=formatted_list_items, **variables)

        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(final_prompt)
            raw_text = response.text
            
            # --- 这是核心的修复 ---
            # 使用 ['"] 来匹配单引号或双引号
            regex_pattern = r"<item id=['\"](\d+)['\"]>(.*?)</item>"
            matches = re.finditer(regex_pattern, raw_text, re.DOTALL)
            # --- 修复结束 ---
            
            parsed_results = {int(m.group(1)): m.group(2).strip() for m in matches}
            
            reordered_results = [parsed_results.get(i) for i in range(item_count)]

            # 最终校验：确保没有一个元素是None（意味着ID丢失）
            if None not in reordered_results:
                return reordered_results
            else:
                # 找出丢失的ID以提供更好的调试信息
                missing_ids = [i for i, res in enumerate(reordered_results) if res is None]
                print(f"\n--- DEBUG: Protocol Violation Detected ---")
                print(f"ERROR: Model response was missing items for IDs: {missing_ids}")
                print(f"RAW RESPONSE FROM MODEL:\n---\n{raw_text}\n---")
                return []
                
        except Exception as e:
            print(f"An API call failed with error: {e}")
            return []