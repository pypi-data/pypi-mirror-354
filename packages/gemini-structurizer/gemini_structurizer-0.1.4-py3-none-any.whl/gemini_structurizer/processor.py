import google.generativeai as genai
import os
import json
import argparse
import sys # 确保 sys 被导入
import pkg_resources # 用于查找包内资源

# --- Global configuration variables (filename only) ---
DEFAULT_CONFIG_FILENAME = "gemini_structurizer_config.json"
INPUT_FILE_CONFIG_KEY = "input_file_to_process"

# --- 函数，用于定位包内资源 ---
def get_package_resource_path(package_name, resource_relative_path):
    """
    获取包内资源的绝对路径。
    Args:
        package_name (str): 包的名称 (例如 'gemini_structurizer')。
        resource_relative_path (str): 资源文件相对于包根目录的路径。
    Returns:
        str or None: 资源的绝对路径，如果找不到则为 None。
    """
    try:
        # 这种方式更适合查找通过 setup.py/pyproject.toml 中 include_package_data 或 package_data 安装的文件
        if pkg_resources.resource_exists(package_name, resource_relative_path):
            return pkg_resources.resource_filename(package_name, resource_relative_path)
        else:
            # Fallback: 尝试基于 __file__ 定位，这在某些情况下（如本地开发或 sdist 安装）可能有效
            # 但对于 wheel 安装且包含数据的标准方式是上面的 pkg_resources
            print(f"Warning: pkg_resources could not find {resource_relative_path} in {package_name}. Trying __file__ based lookup.")
            # 获取当前文件 (processor.py) 所在的目录
            base_dir = os.path.dirname(os.path.abspath(__file__))
            # 假设配置文件与 processor.py 在同一目录，或者在相对于它的固定位置
            # 如果 resource_relative_path 就是文件名，则可以直接拼接
            potential_path = os.path.join(base_dir, resource_relative_path)
            if os.path.exists(potential_path):
                return potential_path
            print(f"Error: Resource '{resource_relative_path}' not found in package '{package_name}' using pkg_resources or __file__ fallback.")
            return None
    except Exception as e:
        print(f"Error getting package resource path for '{resource_relative_path}' in '{package_name}': {e}")
        return None

# --- 修改 get_config_path ---
def get_config_path(config_filename=DEFAULT_CONFIG_FILENAME):
    """
    获取 gemini_structurizer_config.json 的完整路径。
    假设它作为包数据与 gemini_structurizer 包一起安装。
    """
    # 'gemini_structurizer' 应该是你的包名
    # config_filename 应该是相对于包根目录的路径。
    # 如果 gemini_structurizer_config.json 与 processor.py 在包的同一级别，
    # 那么 resource_relative_path 就是 config_filename。
    # 如果它在包内的一个子目录，例如 'configs/gemini_structurizer_config.json'，
    # 那么 resource_relative_path 应该是 'configs/gemini_structurizer_config.json'。
    # 这里我们假设它与 processor.py 在包的同一级别或你已在 setup.py/pyproject.toml 中正确声明。
    package_name = __name__.split('.')[0] # 获取顶级包名，例如 'gemini_structurizer'
    if package_name == '__main__': # 如果直接运行此文件
        package_name = 'gemini_structurizer' # 假设包名
        print(f"Warning: Running {__file__} as __main__. Assuming package name '{package_name}' for resource loading.")

    path = get_package_resource_path(package_name, config_filename)
    if not path:
        # 终极回退：如果作为 PyInstaller 的一部分，并且通过 --add-data 添加到了 _MEIPASS
        try:
            base_path = sys._MEIPASS
            fallback_path = os.path.join(base_path, config_filename)
            if os.path.exists(fallback_path):
                print(f"Info: Config not found via pkg_resources, but found in PyInstaller bundle: {fallback_path}")
                return fallback_path
        except AttributeError:
            pass # 不在 PyInstaller 环境中
        print(f"Error: Critical - Config file '{config_filename}' could not be located for package '{package_name}'.")
    return path


def generate_default_config_content():
    """Generates default/template configuration file content."""
    return {
        "model_name": "gemini-2.5-flash-preview-04-17",
        "system_instruction": "# TODO: Fill in your system-level prompt here (e.g., You are a text analysis expert...)",
        "user_prompt_for_file_processing": "# TODO: Fill in your user prompt for file processing here.\n# You can use {filename} as a placeholder for the uploaded filename.\n# E.g., Please analyze the file named {filename} and extract...",
        "output_json_schema": {
            "type": "object",
            "properties": {
                "example_output_key": {
                    "type": "string",
                    "description": "# TODO: This is an example for your JSON Schema. Please replace it with your actual required Schema."
                }
            },
            "required": ["# TODO: example_output_key"]
        },
        INPUT_FILE_CONFIG_KEY: "# TODO: (Optional) Fill in the full path to the input file you want to process here, or pass it as a function argument."
    }

def load_or_create_config(custom_config_path=None):
    """
    Loads the configuration file using a prioritized strategy.
    """
    # Strategy 1: Prioritize the custom path provided by the caller.
    # We will trust this path and attempt to open it directly.
    # This is the primary way the library should be used in a larger application.
    if custom_config_path:
        print(f"Info: Using custom config path provided by caller: {os.path.abspath(custom_config_path)}")
        try:
            with open(custom_config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
            
            # --- Perform validation on the loaded config ---
            required_core_keys = ["model_name", "system_instruction", "user_prompt_for_file_processing", "output_json_schema"]
            missing_keys = [key for key in required_core_keys if key not in config or str(config.get(key, '')).startswith("# TODO:")]

            if missing_keys:
                print(f"Error: The following core configurations are missing or not filled in the provided config '{os.path.abspath(custom_config_path)}':")
                for key in missing_keys:
                    print(f"- {key}")
                print("Please check and fill in the configuration file, then rerun.")
                return None
            
            return config # Success

        except FileNotFoundError:
            print(f"CRITICAL ERROR: The config file path provided by the caller could not be found or opened.")
            print(f"Attempted path: {os.path.abspath(custom_config_path)}")
            print("This might be due to a path issue in the calling application, especially in a packaged environment.")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing configuration file '{os.path.abspath(custom_config_path)}': {e}")
            return None
        except IOError as e:
            print(f"Error reading configuration file '{os.path.abspath(custom_config_path)}': {e}")
            return None

    # Strategy 2: Fallback for standalone testing or when no custom path is given.
    # This part attempts to find the config bundled with the package itself.
    print("Info: No custom config path provided. Trying to locate package-provided config for standalone use...")
    config_path_to_use = get_config_path()

    if not config_path_to_use or not os.path.exists(config_path_to_use):
        print(f"Error: Could not find a valid package-provided config file. The library requires a configuration to run.")
        return None

    print(f"Info: Found package-provided config at: {os.path.abspath(config_path_to_use)}")
    try:
        with open(config_path_to_use, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        # --- Perform the same validation on the package-provided config ---
        required_core_keys = ["model_name", "system_instruction", "user_prompt_for_file_processing", "output_json_schema"]
        missing_keys = [key for key in required_core_keys if key not in config or str(config.get(key, '')).startswith("# TODO:")]

        if missing_keys:
            print(f"Error: The package-provided config '{os.path.abspath(config_path_to_use)}' is incomplete:")
            for key in missing_keys:
                print(f"- {key}")
            return None
            
        return config # Success

    except Exception as e:
        print(f"An unexpected error occurred while loading the package-provided config: {e}")
        return None

def get_output_json_path(input_filepath):
    """Generates the output JSON file path based on the input file path."""
    if not input_filepath:
        return None
    directory = os.path.dirname(os.path.abspath(input_filepath))
    filename = os.path.basename(input_filepath)
    name_part = filename.rsplit('.', 1)[0]
    return os.path.join(directory, name_part + ".json")


def structure_file_with_gemini(input_filepath, custom_config_path=None, overwrite_existing_output=False):
    """
    Processes the specified file using the Gemini API and generates structured JSON based on the configuration.
    """
    print("--- Gemini File Structurizer (Library Mode) ---")

    if not os.getenv('GOOGLE_API_KEY'):
        print("\nError: GOOGLE_API_KEY environment variable not set. Please configure before calling.")
        return None

    config_data = load_or_create_config(custom_config_path)

    if config_data is None:
        print("\nConfiguration loading or creation failed. Please ensure the configuration file is valid.")
        return None

    if not input_filepath: # input_filepath 现在必须由调用者提供
        print("Error: No valid input_filepath provided to structure_file_with_gemini.")
        return None

    if not os.path.exists(input_filepath):
        print(f"Error: Input file '{os.path.abspath(input_filepath)}' not found.")
        return None

    output_json_filepath = get_output_json_path(input_filepath)
    if not output_json_filepath:
        print(f"Error: Could not generate output path for input '{input_filepath}'.")
        return None

    print(f"\nInput file: '{os.path.abspath(input_filepath)}'")
    print(f"Expected output: '{os.path.abspath(output_json_filepath)}'")

    if not overwrite_existing_output and os.path.exists(output_json_filepath):
        print(f"Info: Output file '{os.path.abspath(output_json_filepath)}' already exists and overwrite is not permitted. Returning path directly.")
        return output_json_filepath

    uploaded_file = None
    try:
        print(f"Uploading file: {input_filepath}...")
        display_name = os.path.basename(input_filepath)
        uploaded_file = genai.upload_file(path=input_filepath, display_name=display_name)
        print(f"File '{display_name}' uploaded as: {uploaded_file.uri} (Resource name: {uploaded_file.name})")

        print(f"Using model: {config_data['model_name']}")
        model = genai.GenerativeModel(
            model_name=config_data["model_name"],
            system_instruction=config_data["system_instruction"],
            generation_config=genai.types.GenerationConfig(
                response_mime_type="application/json",
                response_schema=config_data["output_json_schema"]
            )
        )

        user_prompt = config_data["user_prompt_for_file_processing"].format(filename=display_name)

        print(f"Processing file '{display_name}'...")
        response = model.generate_content([uploaded_file, user_prompt])

        if not response.parts:
            print("Error: No content parts in API response.")
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback:
                 print(f"Prompt feedback: {response.prompt_feedback}")
            return None

        try:
            output_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            print(f"Error: Failed to parse API response as JSON: {e}")
            print(f"Original response text: {response.text}")
            return None
        except AttributeError:
            print("Error: API response object missing .text attribute.")
            return None

        os.makedirs(os.path.dirname(output_json_filepath), exist_ok=True)
        with open(output_json_filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"Successfully extracted file structure to JSON: {os.path.abspath(output_json_filepath)}")
        return output_json_filepath

    except Exception as e:
        print(f"A critical error occurred during processing: {e}")
        import traceback
        print(traceback.format_exc()) # 打印更详细的错误信息
        return None
    finally:
        if uploaded_file and hasattr(uploaded_file, 'name'):
            try:
                print(f"Deleting uploaded file: {uploaded_file.name} ({uploaded_file.uri})...")
                genai.delete_file(uploaded_file.name)
                print(f"Successfully deleted uploaded file: {uploaded_file.name}")
            except Exception as del_e:
                print(f"Error deleting uploaded file {uploaded_file.name}: {del_e}")


def main_cli_entry():
    """Handles command-line execution logic (for testing the package)."""
    parser = argparse.ArgumentParser(description="Gemini File Structurizer (Standalone Test Mode for Package).")
    parser.add_argument(
        "-i", "--input",
        required=True, # 对于包的测试，输入文件应该明确指定
        help="Path to the input file to process."
    )
    parser.add_argument(
        "-c", "--config",
        help=f"Path to a custom configuration file. If not provided, uses the config bundled with the package."
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="If specified, reprocesses and overwrites the output JSON file even if it already exists."
    )
    args = parser.parse_args()

    print("--- Gemini File Structurizer (Standalone Test Mode for Package) ---")

    # GOOGLE_API_KEY 应该在环境外部设置
    if not os.getenv('GOOGLE_API_KEY'):
        print("\nError: GOOGLE_API_KEY environment variable not set. Please set it and retry.")
        print("--- Program End ---")
        exit(1)


    result_path = structure_file_with_gemini(
        input_filepath=args.input,
        custom_config_path=args.config,
        overwrite_existing_output=args.overwrite
    )

    if result_path:
        print(f"\nProcessing complete!")
        if os.path.exists(result_path):
            try:
                with open(result_path, 'r', encoding='utf-8') as f_check:
                    print("\nJSON file content preview (first 500 characters):")
                    preview_content = f_check.read(500)
                    print(preview_content)
                    if len(preview_content) == 500:
                        print("...")
            except Exception as e:
                print(f"Could not read or preview the generated JSON file '{result_path}': {e}")
    else:
        print("\nFile processing failed or was skipped. Please check the messages above.")

    print("\n--- Program End ---")


if __name__ == '__main__':
    main_cli_entry()