import os

def infer_folders(file_paths, summaries):
    folder_dict = {}
    max_depth = 0
    
    for file_path, summary in zip(file_paths, summaries):
        path_parts = file_path.split(os.sep)
        current_path = ''
        
        for part in path_parts[:-1]:  # Exclude the last part (filename or foldername)
            current_path = os.path.join(current_path, part)
            
            if current_path not in folder_dict:
                # folder_dict[current_path] = {'nodes': []}
                folder_dict[current_path] = {'nodes': {}}
            
            next_path = os.path.join(current_path, path_parts[path_parts.index(part) + 1])
            if next_path not in folder_dict[current_path]['nodes']:
                if next_path == file_path[1:]:
                    folder_dict[current_path]['nodes'][next_path] = summary
                else:
                    folder_dict[current_path]['nodes'][next_path] = ''
    
    # not optimal, O(2n) hack
    folders = list(folder_dict.keys()).copy()
    for folder in folders:
        folder_dict[f"/{folder}"] = folder_dict.pop(folder)
    
    folder_tree = {}
    
    # rearrange by depth
    for path in folder_dict:
        depth = path.count(os.sep)
        if path == '/':
            depth = 0
        max_depth = max(depth, max_depth)
        if depth not in folder_tree:
            folder_tree[depth] = {}
        folder_tree[depth][path] = folder_dict[path]
    
    # return folder_dict
    return folder_tree, max_depth

# SAMPLE USAGE:
# input_list = ['/path/to/file1.txt', '/path/to/folder1/file2.txt', '/path/b/file3.txt']
# summary_list = ['AAAA', 'BBBB', 'CCCC']
# output, max_depth = infer_folders(input_list, summary_list)
# print(output)
# print(max_depth)
