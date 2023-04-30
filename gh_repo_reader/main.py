# import logging
# import sys

# logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
# logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

import dataclasses

import subprocess
import os
from typing import Dict, List
from llama_index.readers.file.base import SimpleDirectoryReader
from llama_index import Document, GPTTreeIndex, GPTSimpleKeywordTableIndex

from llama_index import LLMPredictor, ServiceContext

from langchain.chat_models import ChatOpenAI


def infer_folders(file_paths: List[str], summaries: List[str]):
    folder_dict = {}
    max_depth = 0
    
    file_path: str
    summary: str
    for file_path, summary in zip(file_paths, summaries):
        # print(file_path, summary)
        # input("Really??")
        path_parts = file_path.split(os.sep)
        current_path = ''
        
        for part in path_parts[:-1]:  # Exclude the last part (filename or foldername)
            current_path = os.path.join(current_path, part)
            
            if current_path not in folder_dict:
                # folder_dict[current_path] = {'nodes': []}
                folder_dict[current_path] = {'nodes': {}}
            
            next_path = os.path.join(current_path, path_parts[path_parts.index(part) + 1])
            if next_path not in folder_dict[current_path]['nodes']:

                # print(next_path, file_path)
                # input("Really2???")
                if next_path == file_path:
                    folder_dict[current_path]['nodes'][next_path] = summary
                else:
                    folder_dict[current_path]['nodes'][next_path] = ''
    
    # not optimal, O(2n) hack
    folders = list(folder_dict.keys()).copy()
    for folder in folders:
        folder_dict[f"{folder}"] = folder_dict.pop(folder)
    
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

CODE_FILE_EXTENSIONS = [
    ".c",      # C
    ".cpp",    # C++
    ".cs",     # C#
    ".java",   # Java
    ".js",     # JavaScript
    ".ts",     # TypeScript
    ".php",    # PHP
    ".py",     # Python
    ".rb",     # Ruby
    ".go",     # Go
    ".swift",  # Swift
    ".kt",     # Kotlin
    ".rs",     # Rust
    ".html",   # HTML
    ".css",    # CSS
    ".scss",   # Sass
    ".sql",    # SQL
    ".xml",    # XML
    ".json",   # JSON
    ".yaml",   # YAML
    ".yml",    # YAML (alternative)
    ".lua",    # Lua
    ".pl",     # Perl
    ".r",      # R
    ".groovy", # Groovy
    ".sh",     # Shell script
    ".bash",   # Bash script
    ".ps1",    # PowerShell script
    ".vbs",    # VBScript
    ".f",      # Fortran
    ".f90",    # Fortran 90
    ".hs",     # Haskell
    ".elm",    # Elm
    ".dart",   # Dart
    ".pde",    # Processing
    ".ino",    # Arduino
    ".asm",    # Assembly
    ".s",      # Assembly (alternative)
    ".coffee", # CoffeeScript
    ".m",      # Objective-C
    ".md",     # Markdown
    ".tex",    # LaTeX
    ".erl",    # Erlang
    ".clj",    # Clojure
    ".scala",  # Scala
    ".vb",     # Visual Basic
]



def clone_repository(repo_url, target_directory):
    # Make sure the target_directory is an absolute path
    target_directory = os.path.abspath(target_directory)
    
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    try:
        subprocess.run(["git", "clone", repo_url, target_directory], check=True)
        print(f"Successfully cloned {repo_url} to {target_directory}")
    except subprocess.CalledProcessError as e:
        print(f"Error cloning repository: {e}")

paths = []

def file_metadata(file_name: str) -> dict:
    print(file_name)
    paths.append(file_name)
    return { "file_path": file_name }


SUMMARIZE_CODE_FILE_CONTENT_QUERY = """
Please provide a concise summary of the following code file content.
Please limit your answer to 2 sentences.
"""


SUMMARIZE_SUBFOLDER_CONTENT_QUERY = """
Given the following list of summaries, each representing a summary of an individual code file or subfolder in a given folder, generate an overall concise summary that captures the main purpose of the folder.
Please limt your answer to 2 sentences."
"""

global folder_tree
global subfolder_summary_list

def main():
    global folder_tree
    global subfolder_summary_list
    # repo_url = "https://github.com/jerryjliu/llama_index"
    # repo_url = "https://github.com/halitdincer/negate"
    repo_url = "https://github.com/ma-anwar/pyircd"
    target_directory = "./repos"

    clone_repository(repo_url, target_directory)

    my_file_extractors = {}

    reader = SimpleDirectoryReader(
        target_directory, 
        recursive=True, 
        file_extractor=my_file_extractors, 
        file_metadata=file_metadata, 
        exclude_hidden=True, 
        required_exts=CODE_FILE_EXTENSIONS
    )

    codes: List[Document] = reader.load_data()

    llm_predictor = LLMPredictor(llm=ChatOpenAI(
        model_name="gpt-4",
        # model_name = "gpt-3.5-turbo",
        verbose=True,
        max_tokens=4096,
    ))
    service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor)

    summary_of_code_files: List[Dict[str, str]] = []

    # dummy_summaries = [f"summary for {paths[i]}" for i in range(len(paths))]
    # print(dummy_summaries)

   

    ####################################################
    ##      Individual Code file content summary      ##
    ####################################################

    for code in codes:
        code_file_path = code.extra_info["file_path"]

        exists = False
        print(f"./saves/{code_file_path.replace('/', '_-_')}.summary")
        with open(f"./saves/{code_file_path.replace('/', '_-_')}.summary", 'r') as f:
            code_file_content_summary_str = f.read()
            if code_file_content_summary_str:
                exists = True

        if not exists:
            code_index = GPTTreeIndex.from_documents([code], service_context=service_context)

            try:
                code_file_content_summary = code_index.query(SUMMARIZE_CODE_FILE_CONTENT_QUERY, mode="summarize")
                code_file_content_summary_str = str(code_file_content_summary)
            except Exception as e:
                print(f"Error summarizing code file content: {e}")
                code_file_content_summary_str = "THIS IS A PLACEHOLDER SUMMARY"
                continue
        else:
            print("USING SAVED SUMMARY")

        print(f"code.extra_info: {code.extra_info['file_path']}")
        print(f"RESPONSE FROM OpenAI: {code_file_content_summary_str}")
        code_file_content_summary_document = Document(text=code_file_content_summary_str, extra_info={"summary": True})

        summary_of_code_files.append({
            "file_path": code.extra_info["file_path"],
            "summary": code_file_content_summary_str,
            "document": code_file_content_summary_document
        })
        # input("Press Enter to continue... 1")

        if not exists:
            with open(f"./saves/{code.extra_info['file_path'].replace('/', '_-_')}.summary", "w") as f:
                f.write(code_file_content_summary_str)

        # print(f"SOURCE TEXT:")
        # print(f"{code_file_content_summary.source_nodes[0].source_text}")

    folder_tree, max_depth = infer_folders(paths, [summary_of_code_file["summary"] for summary_of_code_file in summary_of_code_files])

    import pprint
    pprint.pprint(folder_tree, indent=2)
    print(f"Max depth: {max_depth}")

    subfolder_summary_list = {}


    for depth in sorted(folder_tree.keys(), reverse= True):

        print(type(depth))
        print(depth, folder_tree[depth])

        print(f"Number of folders at depth {depth} is {len(folder_tree[depth].keys())}")

        
        
        for sub_folder in folder_tree[depth].keys():
            text_to_be_summarized = ""
            print(sub_folder)
            # input(f"CURRENT SUB FOLDER: {sub_folder} - Press Enter to continue...")
            for node_key in folder_tree[depth][sub_folder]['nodes']:
                node_summary = folder_tree[depth][sub_folder]['nodes'][node_key]
                if node_summary == "":
                    print(f"NODE KEY: {node_key}")

                    # we need to retrieve the summary of the sub_folder from subfolder_summary_list
                    # text_to_be_summarized += f"- summary for {node_key} should be retrieved from subfolder_summary_list\n"
                    text_to_be_summarized += f"- {subfolder_summary_list[node_key]}\n"
                    continue
                print(f"\t{node_key}")
                text_to_be_summarized += f"- {node_summary}\n"
            print("=============================================")
            print(f"Text to be summarized for {sub_folder}:")
            print(text_to_be_summarized)
            # input("Press Enter to continue...")
            # Here we have to create a Document with the 'text_to_be_summarized' and query with mode summarized
            doc = Document(text=text_to_be_summarized, extra_info={ "subfolder_path": sub_folder})
            subfolder_index = GPTTreeIndex.from_documents([doc], service_context=service_context)
            # input(f"SUMMARIZING SUBFOLDER ({sub_folder}) CONTENT - Press Enter to continue...")
            subfolder_summary_response = subfolder_index.query(SUMMARIZE_SUBFOLDER_CONTENT_QUERY, mode="summarize")
            subfolder_summary_list[sub_folder] = str(subfolder_summary_response)
            
            print("=============================================")
    
    for subfolder_path_name, subfolder_summary_str in subfolder_summary_list.items():
        print('--------------------------------------------')
        print(subfolder_path_name)
        print(subfolder_summary_str)
        print('--------------------------------------------')

    

    
@dataclasses.dataclass
class Summary:
    path_name: str
    summary_str: str


def get_summaries_for_given_path(path:str) -> List[Summary]:
    global folder_tree
    global subfolder_summary_list
    print(folder_tree)
    # actual given path: https://github.com/ma-anwar/pyircd/tree/main/src/daemon
    # example: /src/daemon , depth 2, 2 slashes
    
    # find depth after tree/main 
    found_depth = path.split('/tree/main')[1].count('/')
    path_after_tree_main = path.split('/tree/main')[1]

    print(found_depth)
    print(f"repos{path_after_tree_main}")
    folder_tree[found_depth]
    summaries_to_return = []
    try:
        for node_path_name in folder_tree[found_depth][f"repos{path_after_tree_main}"]['nodes'].keys():
            print(node_path_name)
            print(folder_tree[found_depth][f"repos{path_after_tree_main}"]['nodes'][node_path_name])
            if folder_tree[found_depth][f"repos{path_after_tree_main}"]['nodes'][node_path_name] == "":
                summaries_to_return.append(subfolder_summary_list[node_path_name])
            else:
                summaries_to_return.append(folder_tree[found_depth][f"repos{path_after_tree_main}"]['nodes'][node_path_name])
            print('--------------------------------------------')
    except KeyError:
        print("No summary found for this path")
        return []

    return summaries_to_return





if __name__ == "__main__":
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src/daemon") == 2
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main") == 0
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src") == 1
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src/test") == 2
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src/test/integration_tests") == 3
    # assert get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src/test/parser_tests") == 3
    main()
    print("#============================================#")
    print(get_summaries_for_given_path("https://github.com/ma-anwar/pyircd/tree/main/src"))