from typing import List


class Input:
    """输入相关的类"""
    
    @classmethod
    def texts(cls, prompt: str, max_length: int = None) -> List[str | None]:
        """获取连续的输入文本的列表 直接回车则停止输入

        Args:
            prompt (str): 提示词
            max_length (int): 允许的最大长度 超过则停止输入
        """
        
        print(f"{15 * '-'} {prompt} {15 * '-'}")
        
        results: List[str] = []
        if max_length:
            for i in range(max_length):
                text = input(f"{max_length - i} >> ")

                if not text:
                    break
                
                if text in results:
                    raise ValueError("不允许输入同样的内容")
                
                results.append(text)
            
        else:
            while True:
                text = input(">> ")

                if not text:
                    break
                
                if text in results:
                    raise ValueError("不允许输入同样的内容")
                
                results.append(text)
            
        return results
    
    @classmethod
    def long_text(cls, prompt: str) -> str:
        """获取连续的输入文本 直接回车则停止输入

        Args:
            prompt (str): 提示词
        """
        inputs = cls.texts(prompt)

        return '\n'.join(inputs)
    
    @classmethod
    def select(
            cls,
            prompt: str,
            options: List[str]
    ):
        """获取用户输入选项

        Args:
            prompt (str): 提示词
            options (List[str]): 预设选项

        Returns:
            index (int): 对应选项索引
        """
        
        while True:
            text = input(prompt)

            if text in options:
                return options.index(text)

    @classmethod
    def comfirmed(
            cls,
            prompt: str
    ):
        """获取用户是否确定

        Args:
            prompt (str): 提示词
        """
        
        while True:
            text = input(prompt)

            match text.lower():
                case "yes" | "ys" | "y":
                    return True
                case "no" | "n":
                    return False
                case _:
                    continue

