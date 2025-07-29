from typing import Optional
import os

FILE_OPERATOR_PROMPT = """
# 文件操作

## 整体协议

%%FILE_OPERATION%%
[操作类型] [文件路径]
[参数键=值]（每行一个）
%%CONTENT%%
[操作内容]
%%END%%

## 限制

- 文件路径只能访问当前目录及其子目录，不能访问其他目录
- 文件路径不能包含 .. 或 /.. 或 \\..\\ 等上级目录
- 文件路径不能以 / 或 \ 开头
- 文件路径不能包含 /etc, /usr, /var, /sys, /proc, /root, /home 等敏感系统路径

## 协议说明

### 读取文件

%%FILE_OPERATION%%
read 文件路径
start_line=[开始行号]
end_line=[结束行号]
%%END%%

### 写入文件

%%FILE_OPERATION%%
write 文件路径
%%CONTENT%%
[内容]
%%END%%

### 追加文件

%%FILE_OPERATION%%
append 文件路径
%%CONTENT%%
[内容]
%%END%%

### 更新文件

%%FILE_OPERATION%%
update 文件路径
%%CONTENT%%
@@ -10,7 +10,7 @@
-    print("Deprecated function")
+    logger.warning("Deprecated function")
%%END%%

### 删除文件内容

%%FILE_OPERATION%%
delete_range 文件路径
start_line=[开始行号]
end_line=[结束行号]
%%END%%

#### 删除全部

%%FILE_OPERATION%%
delete_all 文件路径
%%END%%


# 文件展示格式

%%FILE_CONTENT%%
FILE_PATH
lines=[总行数]
start_line=[内容开始行号]
end_line=[内容结束行号]
%%CONTENT%%
1: xxx
2: 日志
...
31: 以上就是日志内容
%%END%%

## 示例

### 展示文件内容

%%FILE_CONTENT%%
service.log
%%CONTENT%%
1: Hello, World!
2: Hello, Codyer!
%%END%%

"""


def _is_safe_path(file_path: str) -> bool:
    """
    验证文件路径是否安全
    只允许访问当前目录及其子目录，防止路径遍历攻击
    """
    # 不允许绝对路径
    if os.path.isabs(file_path):
        return False
    
    # 规范化路径，解析 . 和 .. 
    normalized_path = os.path.normpath(file_path)
    
    # 不允许包含 .. 的路径（防止访问上级目录）
    if normalized_path.startswith('..') or '/..' in normalized_path or '\\..\\' in normalized_path:
        return False
    
    # 不允许以 / 或 \ 开头（绝对路径）
    if normalized_path.startswith(('/', '\\')):
        return False
    
    # 检查是否尝试访问敏感系统路径
    dangerous_paths = ['/etc', '/usr', '/var', '/sys', '/proc', '/root', '/home']
    for dangerous in dangerous_paths:
        if normalized_path.startswith(dangerous):
            return False
    
    return True


def parse_llm_file_operate(input: str) -> Optional[str]:
    """
    解析大模型输出的文件操作
    支持多个文件操作，依次处理并返回结果
    """
    import re
    
    try:
        # 查找所有的 FILE_OPERATION 块
        operations = _find_all_file_operations(input)
        
        if not operations:
            return "错误：未找到有效的文件操作格式"
        
        results = []
        for i, operation_text in enumerate(operations):
            try:
                operation_data = _parse_file_operation_format(operation_text)
                result = _execute_file_operation(operation_data)
                results.append(f"操作 {i+1}: {result}")
            except Exception as e:
                results.append(f"操作 {i+1} 失败: {str(e)}")
        
        return "\n".join(results)
        
    except Exception as e:
        return f"错误：{str(e)}"


def _find_all_file_operations(input: str) -> list:
    """
    查找输入文本中的所有 FILE_OPERATION 块
    """
    operations = []
    lines = input.split('\n')
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line == "%%FILE_OPERATION%%":
            # 找到操作开始
            start_idx = i
            end_idx = -1
            
            # 查找对应的 %%END%%
            for j in range(i + 1, len(lines)):
                if lines[j].strip() == "%%END%%":
                    end_idx = j
                    break
            
            if end_idx != -1:
                # 提取完整的操作块
                operation_block = '\n'.join(lines[start_idx:end_idx + 1])
                operations.append(operation_block)
                i = end_idx + 1
            else:
                # 没找到结束标记，跳过这个开始标记
                i += 1
        else:
            i += 1
    
    return operations


def _parse_file_operation_format(input: str) -> dict:
    """
    解析 %%FILE_OPERATION%% 格式
    """
    lines = input.strip().split('\n')
    
    # 找到操作开始和结束位置
    start_idx = -1
    end_idx = -1
    content_idx = -1
    
    for i, line in enumerate(lines):
        if line.strip() == "%%FILE_OPERATION%%":
            start_idx = i
        elif line.strip() == "%%CONTENT%%":
            content_idx = i
        elif line.strip() == "%%END%%":
            end_idx = i
            break
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError("格式错误：缺少 %%FILE_OPERATION%% 或 %%END%% 标记")
    
    # 解析操作类型和文件路径
    if start_idx + 1 >= len(lines):
        raise ValueError("格式错误：缺少操作类型和文件路径")
    
    operation_line = lines[start_idx + 1].strip()
    parts = operation_line.split(' ', 1)
    
    if len(parts) < 2:
        raise ValueError("格式错误：操作类型和文件路径格式不正确")
    
    operation_type = parts[0]
    file_path = parts[1]
    
    result = {
        "type": "file_operation",
        "operation": operation_type,
        "file_path": file_path,
        "parameters": {},
        "content": None
    }
    
    # 解析参数
    param_end_idx = content_idx if content_idx != -1 else end_idx
    for i in range(start_idx + 2, param_end_idx):
        line = lines[i].strip()
        if line and '=' in line:
            key, value = line.split('=', 1)
            # 尝试转换为数字，如果失败则保持字符串
            try:
                value = int(value)
            except ValueError:
                pass
            result["parameters"][key] = value
    
    # 解析内容
    if content_idx != -1:
        content_lines = lines[content_idx + 1:end_idx]
        result["content"] = '\n'.join(content_lines)
    
    return result


def _execute_file_operation(operation_data: dict) -> str:
    """
    执行文件操作并返回结果
    """
    operation = operation_data["operation"]
    file_path = operation_data["file_path"]
    parameters = operation_data["parameters"]
    content = operation_data["content"]

    # 验证file_path是否合法
    # file_path只能在当前目录下，或者在当前目录的子目录下，即 ./ 目录下，其他都是非法的
    if not _is_safe_path(file_path):
        return f"错误：文件路径 '{file_path}' 不安全，只能访问当前目录及其子目录"
    
    try:
        if operation == "read":
            return _execute_read_operation(file_path, parameters)
        elif operation == "write":
            return _execute_write_operation(file_path, content)
        elif operation == "append":
            return _execute_append_operation(file_path, content)
        elif operation == "update":
            return _execute_update_operation(file_path, content)
        elif operation == "delete_range":
            return _execute_delete_range_operation(file_path, parameters)
        elif operation == "delete_all":
            return _execute_delete_all_operation(file_path)
        else:
            return f"错误：不支持的操作类型 '{operation}'"
    except Exception as e:
        return f"操作失败：{str(e)}"


def _execute_read_operation(file_path: str, parameters: dict) -> str:
    """执行读取操作"""
    if not os.path.exists(file_path):
        return f"错误：文件 '{file_path}' 不存在"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        start_line = parameters.get("start_line", 1)
        end_line = parameters.get("end_line", len(lines))
        
        # 确保行号范围有效
        start_line = max(1, start_line)
        end_line = min(len(lines), end_line)
        
        if start_line > end_line:
            return f"错误：开始行号 {start_line} 大于结束行号 {end_line}"
        
        # 构建带行号的文件内容
        result_lines = []
        for i in range(start_line - 1, end_line):
            line_content = lines[i].rstrip('\n')
            result_lines.append(f"{i + 1:4d}: {line_content}")
        
        total_lines = len(lines)
        return f"文件 '{file_path}' 内容 (第{start_line}-{end_line}行，共{total_lines}行):\n" + "\n".join(result_lines)
        
    except Exception as e:
        return f"错误：读取文件失败 - {str(e)}"


def _execute_write_operation(file_path: str, content: str) -> str:
    """执行写入操作"""
    try:
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        if dir_path:  # 只有当目录路径不为空时才创建
            os.makedirs(dir_path, exist_ok=True)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return f"成功：已写入文件 '{file_path}'"
    except Exception as e:
        return f"错误：写入文件失败 - {str(e)}"


def _execute_append_operation(file_path: str, content: str) -> str:
    """执行追加操作"""
    try:
        # 确保目录存在
        dir_path = os.path.dirname(file_path)
        if dir_path:  # 只有当目录路径不为空时才创建
            os.makedirs(dir_path, exist_ok=True)
        
        # 检查文件是否存在以及是否需要添加换行符
        add_newline = False
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as f:
                existing_content = f.read()
                # 如果文件不为空且不以换行符结尾，需要添加换行符
                if existing_content and not existing_content.endswith('\n'):
                    add_newline = True
        
        with open(file_path, 'a', encoding='utf-8') as f:
            if add_newline:
                f.write('\n')
            f.write(content)
        
        return f"成功：已追加内容到文件 '{file_path}'"
    except Exception as e:
        return f"错误：追加文件失败 - {str(e)}"


def _execute_update_operation(file_path: str, diff_content: str) -> str:
    """执行更新操作(使用diff格式)"""
    if not os.path.exists(file_path):
        return f"错误：文件 '{file_path}' 不存在"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            original_lines = f.readlines()
        
        # 解析diff格式并应用更改
        updated_lines = _apply_diff(original_lines, diff_content)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(updated_lines)
        
        return f"成功：已更新文件 '{file_path}'"
    except Exception as e:
        return f"错误：更新文件失败 - {str(e)}"


def _execute_delete_range_operation(file_path: str, parameters: dict) -> str:
    """执行删除范围操作"""
    if not os.path.exists(file_path):
        return f"错误：文件 '{file_path}' 不存在"
    
    start_line = parameters.get("start_line")
    end_line = parameters.get("end_line")
    
    if start_line is None or end_line is None:
        return "错误：缺少 start_line 或 end_line 参数"
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 验证行号范围
        if start_line < 1 or end_line > len(lines) or start_line > end_line:
            return f"错误：无效的行号范围 {start_line}-{end_line}，文件共 {len(lines)} 行"
        
        # 删除指定范围的行
        new_lines = lines[:start_line-1] + lines[end_line:]
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.writelines(new_lines)
        
        return f"成功：已删除文件 '{file_path}' 第{start_line}-{end_line}行"
    except Exception as e:
        return f"错误：删除文件内容失败 - {str(e)}"


def _execute_delete_all_operation(file_path: str) -> str:
    """执行删除全部内容操作"""
    if not os.path.exists(file_path):
        return f"错误：文件 '{file_path}' 不存在"
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write("")
        
        return f"成功：已清空文件 '{file_path}' 的所有内容"
    except Exception as e:
        return f"错误：清空文件失败 - {str(e)}"


def _apply_diff(original_lines: list, diff_content: str) -> list:
    """
    应用diff格式的更改
    支持多个修改位置的diff（多个@@块）
    
    安全策略：
    - 只有存在删除行(-开头)或添加行(+开头)时才修改文件
    - 如果只有上下文行(空格开头)，则不修改文件
    - diff格式错误时不修改文件
    """
    import re
    
    diff_lines = diff_content.strip().split('\n')
    
    # 解析所有的diff块
    diff_blocks = _parse_multiple_diff_blocks(diff_lines)
    
    if not diff_blocks:
        raise ValueError("无效的diff格式：未找到有效的diff块")
    
    # 检查是否有实际的修改操作
    has_changes = False
    for block in diff_blocks:
        for diff_line in block['content']:
            if diff_line.startswith('-') or diff_line.startswith('+'):
                has_changes = True
                break
        if has_changes:
            break
    
    # 如果没有实际的修改（只有上下文行），直接返回原文件
    if not has_changes:
        return original_lines
    
    # 按照起始行号倒序排列（从后往前应用，避免行号偏移问题）
    diff_blocks.sort(key=lambda x: x['old_start'], reverse=True)
    
    # 依次应用每个diff块
    result_lines = original_lines[:]
    
    for block in diff_blocks:
        result_lines = _apply_single_diff_block(result_lines, block)
    
    return result_lines


def _parse_multiple_diff_blocks(diff_lines: list) -> list:
    """
    解析包含多个@@块的diff内容
    返回diff块列表，每个块包含header信息和内容
    """
    import re
    
    blocks = []
    current_block = None
    
    for line in diff_lines:
        if line.startswith('@@'):
            # 如果有之前的块，先保存它
            if current_block is not None:
                blocks.append(current_block)
            
            # 解析新的diff header
            match = re.match(r'@@ -(\d+),(\d+) \+(\d+),(\d+) @@', line)
            if not match:
                continue  # 跳过格式错误的header
            
            old_start, old_count, new_start, new_count = map(int, match.groups())
            
            current_block = {
                'header': line,
                'old_start': old_start,
                'old_count': old_count,
                'new_start': new_start,
                'new_count': new_count,
                'content': []
            }
        elif current_block is not None:
            # 添加到当前块的内容中
            current_block['content'].append(line)
    
    # 保存最后一个块
    if current_block is not None:
        blocks.append(current_block)
    
    return blocks


def _apply_single_diff_block(original_lines: list, block: dict) -> list:
    """
    应用单个diff块的修改
    """
    old_start = block['old_start']
    old_count = block['old_count']
    diff_content_lines = block['content']
    
    # 转换为Python数组索引（从0开始）
    old_start_idx = old_start - 1
    
    # 验证原始文件行数
    if len(original_lines) < old_start_idx + old_count:
        raise ValueError(f"文件行数不足：需要至少 {old_start_idx + old_count} 行，实际只有 {len(original_lines)} 行")
    
    # 开始构建结果
    result_lines = []
    
    # 1. 复制diff影响范围之前的行
    result_lines.extend(original_lines[:old_start_idx])
    
    # 2. 处理diff范围内的更改
    original_line_idx = old_start_idx
    
    for diff_line in diff_content_lines:
        if not diff_line:  # 跳过空行
            continue
            
        if diff_line.startswith(' '):
            # 上下文行，保持不变
            line_content = diff_line[1:]  # 去掉前缀空格
            
            # 确保有换行符
            if not line_content.endswith('\n'):
                line_content += '\n'
            result_lines.append(line_content)
            original_line_idx += 1
            
        elif diff_line.startswith('-'):
            # 删除行，跳过原始文件中的对应行
            original_line_idx += 1
            
        elif diff_line.startswith('+'):
            # 添加行
            line_content = diff_line[1:]  # 去掉前缀+
            # 确保有换行符
            if not line_content.endswith('\n'):
                line_content += '\n'
            result_lines.append(line_content)
            # 注意：添加行不移动原始文件索引
    
    # 3. 复制diff影响范围之后的剩余行
    remaining_start_idx = old_start_idx + old_count
    if remaining_start_idx < len(original_lines):
        result_lines.extend(original_lines[remaining_start_idx:])
    
    return result_lines