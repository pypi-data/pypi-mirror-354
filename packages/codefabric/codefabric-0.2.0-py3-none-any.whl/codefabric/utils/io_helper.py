import os

class IOHelper:
    @staticmethod
    def write_code_to_file(content:str, cwd:str, filepath:str) -> str:
        """
        Streams the code, cleans it using regex filter and writes to a given filepath
        """
        path = os.path.join(cwd, filepath)

        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        
        return content