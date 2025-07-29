import base64
import copy
from io import BytesIO
import json
import os
import re
import tarfile
from tempfile import NamedTemporaryFile
import docker
import rich
import astor
import ast

from datetime import datetime
from inferless_cli.commands.export.convertors import Convertors
from inferless_cli.commands.run.constants import (
    HF_HOME,
    MODEL_DATA_TYPE_MAPPING,
    MODEL_TRITON_DATA_TYPE_MAPPING,
)
from inferless_cli.utils.constants import (
    DEFAULT_RUNTIME_FILE_NAME,
    DEFAULT_YAML_FILE_NAME,
)

from inferless_cli.utils.exceptions import InferlessCLIError
from inferless_cli.utils.helpers import (
    check_pydantic,
    decrypt_tokens,
    delete_files,
    log_exception,
    merge_dicts,
    read_json,
    yaml,
)
from inferless_cli.utils.services import (
    get_cli_files,
    get_default_templates_list,
    get_runtime_by_name,
    get_volume_by_name,
)


def is_docker_running(docker_base_url):
    try:
        client = docker.from_env()
        if docker_base_url is not None:
            client = docker.DockerClient(base_url=docker_base_url)

        client.ping()
    except docker.errors.APIError:
        raise InferlessCLIError("[red]Docker is not running.[/red]")

    except Exception:
        raise InferlessCLIError("[red]Docker is not running.[/red]")


def get_inferless_config(
    name,
    env_dict,
    is_local_runtime,
    volume,
    framework,
    input_schema_path,
    input_json_path,
    output_json_path,
    runtime,
    runtime_version,
    runtime_type,
):
    _, _, _, workspace_id, _ = decrypt_tokens()

    io_schema = True
    optional = {}
    is_pydantic = check_pydantic("app.py")
    if is_pydantic:
        io_schema = True

    if framework != "PYTORCH" and input_json_path and output_json_path:
        io_schema = False
        optional = {
            "input_file_name": input_json_path,
            "output_file_name": output_json_path,
        }

    if io_schema and not input_schema_path:
        raise InferlessCLIError("\n[red]input_schema.py file not Found[/red]\n")
    custom_runtime_id = None
    custom_runtime_version = None
    if runtime:
        if not is_local_runtime:
            res = get_runtime_by_name(workspace_id=workspace_id, runtime_name=runtime)
            custom_runtime_id = res["template_id"]
            if runtime_version:
                custom_runtime_version = runtime_version

    default_runtime_id = None
    default_runtime_url = None
    if not runtime:
        templates = get_default_templates_list()
        if runtime_type == "fastapi":
            fastapi_templates = [
                t
                for t in templates
                if t["name"] == "Inferless Default (FastAPI)" and t["is_latest_version"]
            ]
            if fastapi_templates:
                default_runtime_id = fastapi_templates[0]["id"]
                default_runtime_url = fastapi_templates[0]["template_url"]
            else:
                # Fallback to any FastAPI template if latest not found
                fastapi_templates = [
                    t for t in templates if t["name"] == "Inferless Default (FastAPI)"
                ]
                if fastapi_templates:
                    default_runtime_id = fastapi_templates[0]["id"]
                    default_runtime_url = fastapi_templates[0]["template_url"]
                else:
                    raise InferlessCLIError("No FastAPI runtime template found")
        else:
            default_templates = [
                t
                for t in templates
                if t["name"] == "Inferless Default (FastAPI)" and t["is_latest_version"]
            ]
            if default_templates:
                default_runtime_id = default_templates[0]["id"]
                default_runtime_url = default_templates[0]["template_url"]
            else:
                # Fallback to any FastAPI template if latest not found
                default_templates = [
                    t for t in templates if t["name"] == "Inferless Default (FastAPI)"
                ]
                if default_templates:
                    default_runtime_id = default_templates[0]["id"]
                    default_runtime_url = default_templates[0]["template_url"]
                else:
                    raise InferlessCLIError("No runtime template found")

    custom_volume_id = None
    custom_volume_name = None
    if volume:
        res = get_volume_by_name(workspace_id=workspace_id, volume_name=volume)
        if "volume_id" in res:
            custom_volume_id = res["volume_id"]
            custom_volume_name = res["volume_name"]

    config = {
        "name": name,
        "source_framework_type": framework,
        "io_schema": io_schema,
        "env": env_dict,
        "optional": optional,
        "configuration": {
            "custom_runtime_id": custom_runtime_id,
            "custom_runtime_version": custom_runtime_version,
            "custom_volume_id": custom_volume_id,
            "custom_volume_name": custom_volume_name,
            "default_runtime_id": default_runtime_id,
            "default_runtime_url": default_runtime_url,
        },
    }

    return config


def check_and_convert_runtime_file(runtime, runtime_type):
    if runtime and runtime_type == "replicate":
        Convertors.convert_cog_to_runtime_yaml(runtime, DEFAULT_RUNTIME_FILE_NAME)


def get_runtime_file_location(runtime, config):
    if runtime:
        return runtime

    if config.get_value("configuration.optional.runtime_file_name"):
        return config.get_value("configuration.optional.runtime_file_name")

    return DEFAULT_RUNTIME_FILE_NAME


def create_config_from_json(config, config_pbtxt_file):

    inputs = {}
    io_schema = False
    is_pydantic = check_pydantic("app.py")
    data_dict = None
    if config.get_value("io_schema"):
        io_schema = config.get_value("io_schema")
    if not io_schema or not is_pydantic:
        input_json = read_json(config.get_value("optional.input_file_name"))
        output_json = read_json(config.get_value("optional.output_file_name"))
    else:
        input_json = None
        output_json = None

    model_name = config.get_value("name")
    input_schema_path = "input_schema.py"
    if output_json and "outputs" in output_json:
        output_tensor = copy.deepcopy(output_json["outputs"])
    else:
        output_tensor = []

    if is_pydantic:
        inputs, outputs, exec_code, req_name, response_name = extract_inferless_classes(
            "app.py"
        )
        input_tensor = input_to_tensor(inputs)
        output_tensor = output_to_tensor(outputs)
        input_tensor_non_neg = input_to_tensor(inputs, with_size=True)
        inputs = {
            "inputs": copy.deepcopy(input_tensor_non_neg),
        }
    elif not is_pydantic and os.path.exists(input_schema_path):
        data_dict = create_input_from_schema(input_schema_path, False)
        data_dict_without_negitive = create_input_from_schema(input_schema_path, True)
        inputs = data_dict_without_negitive
        input_tensor = copy.deepcopy(data_dict)["inputs"]
    elif input_json and "inputs" in input_json and len(input_json["inputs"]) > 0:
        inputs = input_json
        input_tensor = copy.deepcopy(input_json["inputs"])
    else:
        raise InferlessCLIError("Inputs not found. need atleast 1 input")
    input_tensor = input_tensor_validtor(input_tensor)
    output_tensor = output_tensor_validtor(output_tensor)

    write_config_pbtxt(
        model_name, config_pbtxt_file, input_tensor, output_tensor, data_dict
    )
    return inputs


def input_tensor_validtor(input_tensor):
    for each_input in input_tensor:
        if "name" not in each_input:
            raise InferlessCLIError(
                "\n[red]KeyError: The key 'name' is not present in input tensor.[/red]\n"
            )

        if "shape" not in each_input:
            raise InferlessCLIError(
                "\n[red]KeyError: The key 'shape' is not present in input tensor.[/red]\n"
            )

        if "datatype" not in each_input:
            raise InferlessCLIError(
                "\n[red]KeyError: The key 'datatype' is not present in input tensor.[/red]\n"
            )

        each_input["name"] = "#" + each_input["name"] + "#"
        if "data" in each_input:
            del each_input["data"]
        each_input["dims"] = each_input["shape"]

        del each_input["shape"]
        each_input["data_type"] = MODEL_DATA_TYPE_MAPPING[each_input["datatype"]]
        del each_input["datatype"]

    return input_tensor


def output_tensor_validtor(output_tensor):
    for each_output in output_tensor:
        each_output["name"] = "#" + each_output["name"] + "#"
        del each_output["data"]
        each_output["dims"] = each_output["shape"]

        del each_output["shape"]
        each_output["data_type"] = MODEL_DATA_TYPE_MAPPING[each_output["datatype"]]
        del each_output["datatype"]

    return output_tensor


def write_config_pbtxt(
    model_name, config_pbtxt_file, input_tensor, output_tensor, data_dict
):
    fin = config_pbtxt_file
    config_path = "config.pbtxt"
    with open(config_path, "wt") as fout:
        fin = fin.replace("model_name", model_name)
        fin = fin.replace("platform_backend", "python")
        fin = fin.replace("platform", "backend")

        fin = fin.replace(
            "input_tensor",
            json.dumps(input_tensor).replace('"', "").replace("#", '"'),
        )
        fin = fin.replace(
            "output_tensor",
            json.dumps(output_tensor).replace('"', "").replace("#", '"'),
        )

        fout.write(fin)
        if data_dict and "batch_size" in data_dict:
            batch_size_variable = data_dict["batch_size"]
            max_batch_size_variable = str(int(data_dict["batch_size"]) + 1)
            max_queue_delay_variable = data_dict["batch_window"]

            # Appending the desired text with variables
            fout.write("\n\n")  # Add two newline characters for separation
            fout.write("dynamic_batching {\n")
            fout.write(f"  preferred_batch_size: [ {batch_size_variable} ]\n")
            fout.write(f"  max_queue_delay_microseconds: {max_queue_delay_variable}\n")
            fout.write("}\n")
            fout.write(f"max_batch_size: {max_batch_size_variable}\n")


def create_input_from_schema(input_schema_path, is_replace_minus_one=False):
    try:
        return_dict = {"inputs": []}
        with open(input_schema_path, "r") as file:
            input_schema_content = file.read()
        data_dict = {}
        exec(input_schema_content, {}, data_dict)
        for key, value in data_dict["INPUT_SCHEMA"].items():
            each_input_json = {"name": key}

            if "required" in value and not value["required"]:
                each_input_json["optional"] = True

            if "shape" in value:
                if isinstance(value["shape"], list) and len(value["shape"]) > 0:
                    if (
                        is_replace_minus_one
                        and is_negative_one_present(value["shape"])
                        and "example" in value
                    ):
                        each_input_json["shape"] = replace_minus_one(value["example"])
                    else:
                        each_input_json["shape"] = value["shape"]
                else:
                    raise InferlessCLIError(
                        "shape not specified as a python list for input --> " + key
                    )
            else:
                if "required" in value and value["required"]:
                    raise InferlessCLIError("shape not specified for input --> " + key)

            if "example" in value:
                each_input_json["data"] = value["example"]
            else:
                if "required" in value and value["required"]:
                    raise InferlessCLIError(
                        "example not specified for input --> " + key
                    )

                each_input_json["data"] = None

            if "datatype" in value:
                each_input_json["datatype"] = MODEL_TRITON_DATA_TYPE_MAPPING[
                    value["datatype"]
                ]
            else:
                raise InferlessCLIError("Data type not specified for input --> " + key)

            return_dict["inputs"].append(each_input_json)

        if "BATCH_SIZE" in data_dict and data_dict["BATCH_SIZE"] > 0:
            return_dict["batch_size"] = data_dict["BATCH_SIZE"]
            return_dict["batch_window"] = 500000
            if "BATCH_WINDOW" in data_dict and data_dict["BATCH_WINDOW"] > 0:
                return_dict["batch_window"] = data_dict["BATCH_WINDOW"] * 1000
        return return_dict
    except Exception as e:
        raise InferlessCLIError(
            f"[red]Error while creating Input and Output from schema: {e}[/red]"
        )


def get_inputs_from_input_json(config):
    try:
        if config.get_value("io_schema"):
            return None

        if config.get_value("optional.input_file_name"):
            return read_json(config.get_value("optional.input_file_name"))

        return None

    except Exception:
        raise InferlessCLIError(
            "\n[red]Error happened while reading input and ouptut data [/red]\n"
        )


def get_inputs_from_input_json_pytorch(config):
    input_schema_path = "input_schema.py"
    is_pydantic = check_pydantic("app.py")

    try:
        if (
            not is_pydantic
            and config.get_value("io_schema")
            and not os.path.exists(input_schema_path)
        ):
            raise InferlessCLIError(
                "\n[red]input_schema.py file not Found or pydantic class not found[/red]\n"
            )

        if (
            not is_pydantic
            and not os.path.exists(input_schema_path)
            and not os.path.exists(config.get_value("optional.input_file_name"))
            and not os.path.exists(config.get_value("optional.output_file_name"))
        ):

            raise InferlessCLIError(
                "\n[red]input_schema.py and input.json and output.json files and pydantic class are not Found[/red]\n"
            )

        if is_pydantic:
            inputs, outputs, exec_code, req_name, response_name = (
                extract_inferless_classes("app.py")
            )
            input_tensor = input_to_tensor(inputs)
            output_tensor = output_to_tensor(outputs)
            input_tensor = input_to_tensor(inputs, with_size=True)
            model_py_file = generate_pydantic_model_file(
                input_tensor, output_tensor, exec_code, req_name, response_name
            )

            return input_tensor, output_tensor, model_py_file

        if config.get_value("io_schema") and os.path.exists(input_schema_path):
            data_dict = create_input_from_schema(input_schema_path, False)
            input_tensor = copy.deepcopy(data_dict["inputs"])
            output_tensor = []
            model_py_file = generate_model_file(config, data_dict)

            return input_tensor, output_tensor, model_py_file

        if config.get_value("optional.input_file_name") and config.get_value(
            "optional.output_file_name"
        ):
            input_json = read_json(config.get_value("optional.input_file_name"))
            output_json = read_json(config.get_value("optional.output_file_name"))
            if input_json and "inputs" in input_json:
                input_tensor = copy.deepcopy(input_json["inputs"])
            if output_json and "outputs" in output_json:
                output_tensor = copy.deepcopy(output_json["outputs"])

            model_py_file = generate_model_file(config, data_dict=None)

            return input_tensor, output_tensor, model_py_file

        raise InferlessCLIError()

    except Exception as e:
        raise InferlessCLIError(
            f"\n[red]Error happened while reading input and ouptut data [/red]\n error: {e}"
        )


def generate_model_file(config, data_dict):
    if config.get_value("configuration.is_serverless"):
        model_py_file_contents = get_cli_files("default_serverless_model.py")
        model_py_file = base64.b64decode(model_py_file_contents).decode("utf-8")
        return model_py_file

    if data_dict and "batch_size" in data_dict:
        model_py_file_contents = get_cli_files("default_batch_model.py")
        model_py_file = base64.b64decode(model_py_file_contents).decode("utf-8")
        return model_py_file

    model_py_file_contents = get_cli_files("default_model.py")
    model_py_file = base64.b64decode(model_py_file_contents).decode("utf-8")
    return model_py_file


def generate_pydantic_model_file(
    input_tensor, output_tensor, exec_code, req_name, response_name
):
    model_py_file_contents = get_cli_files("default_pydantic_model.py")
    model_py_file = base64.b64decode(model_py_file_contents).decode("utf-8")

    try:
        fin = model_py_file
        model_file_path = "model.py"

        fin = fin.replace('["##input_list##"]', str(input_tensor))
        fin = fin.replace('["#output_list#"]', str(output_tensor))
        if exec_code is not None:
            fin = fin.replace("##exec_code##", str(exec_code))
            fin = fin.replace("##request_class_name##", req_name)
            fin = fin.replace("##response_class_name##", response_name)
        with open(model_file_path, "wt") as f:
            f.write(fin)

    except Exception as e:
        raise InferlessCLIError(f"[red]Error while generating model.py file: {e}[/red]")

    return model_py_file


def update_model_file(input_tensor, output_tensor, model_py_file):
    try:
        is_pydantic = check_pydantic("app.py")
        if is_pydantic:
            return
        fin = model_py_file
        model_file_path = "model.py"

        fin = fin.replace('["##input_list##"]', str(input_tensor))
        fin = fin.replace('["#output_list#"]', str(output_tensor))
        with open(model_file_path, "wt") as f:
            f.write(fin)

    except Exception as e:
        raise InferlessCLIError(f"[red]Error while generating model.py file: {e}[/red]")


def load_yaml_file(yaml_file, api_text_template_import):
    yaml_dict = yaml.load(yaml_file)
    sys_packages_string = ""
    pip_packages_string = ""
    run_commands_string = ""
    base_image_string = ""
    version_tag_string = ""
    base_image = "triton"
    
    if "base_image" in yaml_dict["build"]:
        base_image = yaml_dict["build"]["base_image"]
        
    if base_image == "triton":
        base_image_string = f"nvcr.io/nvidia/tritonserver"
        version_tag_string = "23.06-py3"
        if "cuda_version" in yaml_dict["build"]:
            if yaml_dict["build"]["cuda_version"] == "12.9.0":
                version_tag_string = "25.04-py3"
            elif yaml_dict["build"]["cuda_version"] == "12.4.1":
                version_tag_string = "24.05-py3"
            elif yaml_dict["build"]["cuda_version"] == "12.1.1":
                version_tag_string = "23.06-py3"
            elif yaml_dict["build"]["cuda_version"] == "11.8.0":
                version_tag_string = "22.11-py3"    
    elif base_image == "fastapi":
        base_image_string = f"inferless/fastapi"
        version_tag_string = "12.1.1-py3"
        if "cuda_version" in yaml_dict["build"]: 
            if yaml_dict["build"]["cuda_version"] == "12.9.0":
                version_tag_string = "12.9.0-py3"
            elif yaml_dict["build"]["cuda_version"] == "12.4.1":
                version_tag_string = "12.4.1-py3"
            elif yaml_dict["build"]["cuda_version"] == "12.1.1":
                version_tag_string = "12.1.1-py3"
            elif yaml_dict["build"]["cuda_version"] == "11.8.0":
                version_tag_string = "11.8.0-py3"
    
    if (
        "system_packages" in yaml_dict["build"]
        and yaml_dict["build"]["system_packages"] is not None
    ):
        sys_packages_string = "RUN apt update && apt -y install "
        for each in yaml_dict["build"]["system_packages"]:
            sys_packages_string = sys_packages_string + each + " "
    if (
        "python_packages" in yaml_dict["build"]
        and yaml_dict["build"]["python_packages"] is not None
    ):
        pip_packages_string = "RUN pip install "
        for each in yaml_dict["build"]["python_packages"]:
            pip_packages_string = pip_packages_string + each + " "

    if "run" in yaml_dict["build"] and yaml_dict["build"]["run"] is not None:
        run_commands_string = ""
        for index, each in enumerate(yaml_dict["build"]["run"]):
            run_commands_string += "RUN " + each + "  \n"

    api_text_template_import = api_text_template_import.replace(
        "##oslibraries##", sys_packages_string
    )
    api_text_template_import = api_text_template_import.replace(
        "##piplibraries##", pip_packages_string
    )
    api_text_template_import = api_text_template_import.replace(
        "##runcommands##", run_commands_string
    )
    api_text_template_import = api_text_template_import.replace(
        "##base_image##", base_image_string
    )
    api_text_template_import = api_text_template_import.replace(
        "##version_tag##", version_tag_string
    )
    return api_text_template_import


def build_docker_image(
    dockerfile_content, context_path=".", docker_base_url=None
):
    log_dir = os.path.join(os.getcwd(), ".inferless-logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(
        log_dir,
        f"docker-build-logs-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
    )

    try:
        client = docker.from_env()
        if docker_base_url is not None:
            client = docker.DockerClient(base_url=docker_base_url)

        # Create a temporary tarball for Docker build context using NamedTemporaryFile
        with NamedTemporaryFile(delete=False, suffix=".tar.gz") as temp_tar:
            dockerfile_tar_path = temp_tar.name
            with tarfile.open(name=dockerfile_tar_path, mode="w:gz") as tar:

                # Walk through the context_path directory and add all files to the tarball
                for root, _, files in os.walk(context_path):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, start=context_path)
                        tar.add(file_path, arcname=arcname)

                # Add Dockerfile to tarball
                dockerfile = BytesIO(dockerfile_content.encode("utf-8"))
                info = tarfile.TarInfo(name="Dockerfile")
                info.size = len(dockerfile.getvalue())
                tar.addfile(tarinfo=info, fileobj=dockerfile)

        build_successful = False
        # Build image using the temporary tarball as context
        with open(dockerfile_tar_path, "rb") as fileobj:
            build_logs = client.api.build(
                fileobj=fileobj,
                tag="inferless-inference",
                rm=True,
                custom_context=True,
                encoding="gzip",
                decode=True,  # Ensures you can get readable output
            )

        with open(log_file_path, "a") as log_file:
            for log in build_logs:
                if "stream" in log:
                    log_output = log["stream"]
                    # Write raw output to log file (stripped of ANSI codes)
                    log_file.write(strip_ansi_codes(log_output))
                    if "Successfully built" in log_output:
                        build_successful = True
                if "error" in log:
                    error_output = log["error"]
                    # Write raw error to log file (stripped of ANSI codes)
                    log_file.write(strip_ansi_codes(error_output))
                    # rich.print(log["error"])

        # Clean up the temporary tarball after build
        os.remove(dockerfile_tar_path)

        files_to_delete = ["config.pbtxt", "model.py"]
        delete_files(files_to_delete)

        # Check if the build was successful
        if build_successful:
            rich.print("[green]Docker Image Successfully Built.[/green]\n")
            return client.images.get("inferless-inference")
        else:
            raise Exception("Docker build failed. Check the logs for details.")
    except Exception as e:
        with open(log_file_path, "a") as log_file:
            if "build_logs" in locals():
                for log in build_logs:
                    if "stream" in log:
                        log_file.write(strip_ansi_codes(log.get("stream", "")))
                    if "error" in log:
                        log_file.write(strip_ansi_codes(log.get("error", "")))

        files_to_delete = ["config.pbtxt", "model.py"]
        delete_files(files_to_delete)
        raise InferlessCLIError(
            f"[red]Docker Build Error - {e}[/red]\n\nLogs saved to {log_file_path} \n"
        )


def start_docker_container(volume_path, autostart, env=None, docker_base_url=None,runtime_type="triton",model_name=None):
    if env is None:
        env = {}
    if runtime_type == "triton":
        if autostart:
            command = "tritonserver --model-store=/models --exit-on-error=false --strict-model-config=false --log-verbose=1 --exit-timeout-secs=45"
        else:
            command = "tritonserver --model-store=/models --model-control-mode=explicit --exit-on-error=false --strict-model-config=false --log-verbose=1 --exit-timeout-secs=45"
    elif runtime_type == "fastapi":
        command = f"uvicorn model:app --host 0.0.0.0 --port 8000 --app-dir /models/${model_name}/1/"
        
    log_dir = os.path.join(os.getcwd(), ".inferless-logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(
        log_dir,
        f"docker-container-logs-{datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.txt",
    )
    try:
        environment = {
            "HF_HOME": HF_HOME,
        }
        volume = {
            HF_HOME: {"bind": HF_HOME, "mode": "rw"},
        }

        if env:
            environment = merge_dicts(environment, env)

        if volume_path:
            new_vol_dict = {f"{volume_path}": {"bind": f"{volume_path}", "mode": "rw"}}
            volume = merge_dicts(volume, new_vol_dict)

        client = docker.from_env()
        if docker_base_url is not None:
            client = docker.DockerClient(base_url=docker_base_url)
        container = client.containers.run(
            "inferless-inference",
            detach=True,
            shm_size="2gb",
            tty=True,
            stdout=True,
            stderr=True,
            environment=environment,
            device_requests=[
                docker.types.DeviceRequest(
                    count=1, capabilities=[["gpu"]]
                )  # Request all available GPUs
            ],
            volumes=volume,
            ports={"8000": 8000},
            command=command,
        )
        with open(log_file_path, "a") as log_file:
            for log in container.logs(stream=True):
                log_file.write(log.decode("utf-8"))
                # Stop logging after the container has started
                # if log.decode("utf-8") contains "Started HTTPService at 0.0.0.0:8000" then break:
                break
                # if "Started HTTPService at 0.0.0.0:8000" in log.decode("utf-8"):
                #     break

        return container
    except Exception as e:
        with open(log_file_path, "a") as log_file:
            log_file.write(f"Error occurred: {str(log_file)}\n")
            if "container" in locals():
                log_file.write(container.logs().decode("utf-8"))
                rich.print(container.logs().decode("utf-8"))

        raise InferlessCLIError(
            f"[red]Failed to start docker container: {e}[/red] \n \n Logs saved to {log_file_path}"
        )


def is_negative_one_present(shape):
    for element in shape:
        if isinstance(element, list):
            if is_negative_one_present(element):
                return True
        elif element == -1:
            return True
    return False


def replace_minus_one(value):
    shape = []
    if isinstance(value, list):
        shape.append(len(value))
        if shape[0] > 0 and isinstance(value[0], list):
            shape.extend(replace_minus_one(value[0]))
    return shape


def print_curl_command(model_name: str, inputs: dict = None):
    if inputs is None:
        inputs = {}

    filtered_inputs = {
        "inputs": [
            item
            for item in inputs.get("inputs", [])
            if not all(d is None for d in item.get("data", []))
        ]
    }

    # Convert the inputs dict to a JSON string.
    json_data = json.dumps(filtered_inputs)

    # Escape single quotes for shell usage by wrapping the JSON data in double quotes
    # and escaping any internal double quotes.
    json_data_for_shell = json_data.replace('"', '\\"')

    # Prepare the curl command split across lines for readability.
    # Since we can't include backslashes directly in f-string expressions,
    # we add them outside of the expression braces.
    curl_command = (
        f"curl --location 'http://localhost:8000/v2/models/{model_name}/infer' \\\n"
        f"--header 'Content-Type: application/json' \\\n"
        f'--data "{json_data_for_shell}"'
    )

    rich.print(curl_command)
    return curl_command


def print_load_model_curl_command(model_name: str):
    # Prepare the curl command for loading a model
    curl_command = (
        f"curl --location 'http://localhost:8000/v2/repository/models/{model_name}/load' \\\n"
        f"--header 'Content-Type: application/json' \\\n"
        f"--request POST"
    )

    rich.print(curl_command)
    return curl_command


def print_unload_model_curl_command(model_name: str):
    # Prepare the curl command for unloading a model
    curl_command = (
        f"curl --location 'http://localhost:8000/v2/repository/models/{model_name}/unload' \\\n"
        f"--header 'Content-Type: application/json' \\\n"
        f"--request POST"
    )

    rich.print(curl_command)
    return curl_command


def stop_containers_using_port_8000(docker_base_url):
    try:
        client = docker.from_env()
        if docker_base_url is not None:
            client = docker.DockerClient(base_url=docker_base_url)

        for container in client.containers.list():
            ports = container.attrs["HostConfig"]["PortBindings"]
            if (
                ports
                and "8000/tcp" in ports
                and ports["8000/tcp"][0]["HostPort"] == "8000"
            ):
                container.stop()
    except Exception as e:
        log_exception(e)
        raise InferlessCLIError(
            f"[red]Error while stoping the container running on port 8000: {e}[/red]"
        )


def print_docker_exec_command(container_id: str):
    exec_command = f"docker exec -it {container_id} /bin/bash"
    rich.print(
        f"[green]To access the container's shell, you can use the following command:[/green]\n{exec_command}"
    )
    return exec_command


def strip_ansi_codes(text):
    ansi_escape = re.compile(r"\x1B[@-_][0-?]*[ -/]*[@-~]")
    return ansi_escape.sub("", text)


def extract_inferless_classes(filename):
    try:
        with open(filename, "r") as file:
            tree = ast.parse(file.read())
        # Lists to store the required nodes and imports
        required_classes = []
        imports = []
        dependencies = set()
        request_class_name = None
        response_class_name = None

        # Traverse the AST tree
        for node in tree.body:
            if isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
                imports.append(node)
            elif isinstance(node, ast.ClassDef):
                for decorator in node.decorator_list:
                    if isinstance(decorator, ast.Attribute) and decorator.attr in {
                        "request",
                        "response",
                    }:
                        required_classes.append(node)
                        if decorator.attr in {"request"}:
                            request_class_name = node.name
                        if decorator.attr in {"response"}:
                            response_class_name = node.name
                        for base in node.bases:
                            if isinstance(base, ast.Name):
                                dependencies.add(base.id)
                        break

        # Filter imports to only include dependencies related to the extracted classes
        filtered_imports = []
        for imp in imports:
            if isinstance(imp, ast.Import):
                for alias in imp.names:
                    if alias.name in dependencies or alias.name == "inferless":
                        filtered_imports.append(imp)
            elif isinstance(imp, ast.ImportFrom):
                if (
                    imp.module in dependencies
                    or imp.module == "pydantic"
                    or imp.module == "typing"
                ):
                    filtered_imports.append(imp)
        # Create a new module with only the required classes and imports
        new_module = ast.Module(body=filtered_imports + required_classes)
        new_code = astor.to_source(new_module)
        exec(new_code, globals())
        req_class = globals()[request_class_name]
        resp_class = globals()[response_class_name]
        inputs = req_class._json_schema
        outputs = resp_class._json_schema

        return inputs, outputs, new_code, request_class_name, response_class_name
    except Exception as e:
        raise InferlessCLIError(e)


model_triton_data_type_maping = {
    "boolean": "BOOL",
    "UINT8": "UINT8",
    "UINT16": "UINT16",
    "UINT32": "UINT32",
    "UINT64": "UINT64",
    "INT8": "INT8",
    "INT16": "INT16",
    "integer": "INT32",
    "INT64": "INT64",
    "FP16": "FP16",
    "FP32": "FP32",
    "float": "FP64",
    "BYTES": "BYTES",
    "string": "BYTES",
    "BF16": "BF16",
}


def input_to_tensor(inputs, with_size=False):
    try:
        inputs_res = []
        for key, value in inputs.items():
            each_input_json = {}
            each_input_json["name"] = key
            if "required" in value and value["required"] == False:
                each_input_json["optional"] = True

            if "shape" in value:
                if isinstance(value["shape"], list) and len(value["shape"]) > 0:
                    if (
                        with_size
                        and is_negative_one_present(value["shape"])
                        and "example" in value
                    ):
                        each_input_json["shape"] = replace_minus_one(value["example"])
                    else:
                        each_input_json["shape"] = value["shape"]
                else:
                    raise Exception(
                        "shape not specified as a python list for input --> " + key
                    )
            else:
                if "required" in value and value["required"] == True:
                    raise Exception("shape not specified for input --> " + key)

            if "example" in value:
                if isinstance(value["example"], list) and len(value["example"]) > 0:
                    each_input_json["data"] = value["example"]
                else:
                    each_input_json["data"] = [value["example"]]
            else:
                if "required" in value and value["required"] == True:
                    raise Exception("example not specified for input --> " + key)
                else:
                    each_input_json["data"] = None

            if "datatype" in value:
                if value["datatype"] in model_triton_data_type_maping:
                    each_input_json["datatype"] = model_triton_data_type_maping[
                        value["datatype"]
                    ]
                else:
                    raise Exception(
                        "Data type - "
                        + value["datatype"]
                        + " - not supported for input --> "
                        + key
                    )
            else:
                raise Exception("Data type not specified for input --> " + key)

            inputs_res.append(each_input_json)

        return inputs_res
    except Exception as e:
        raise InferlessCLIError(e)


def output_to_tensor(inputs, with_size=False):
    try:
        inputs_res = []
        for key, value in inputs.items():
            each_input_json = {}
            each_input_json["name"] = key

            if "shape" in value:
                if isinstance(value["shape"], list) and len(value["shape"]) > 0:
                    if (
                        with_size
                        and is_negative_one_present(value["shape"])
                        and "example" in value
                    ):
                        each_input_json["shape"] = replace_minus_one(value["example"])
                    else:
                        each_input_json["shape"] = value["shape"]
                else:
                    raise Exception(
                        "shape not specified as a python list for input --> " + key
                    )
            else:
                if "required" in value and value["required"] == True:
                    raise Exception("shape not specified for input --> " + key)

            if "example" in value:
                if isinstance(value["example"], list) and len(value["example"]) > 0:
                    each_input_json["data"] = value["example"]
                else:
                    each_input_json["data"] = [value["example"]]
            else:
                if "required" in value and value["required"] == True:
                    raise Exception("example not specified for input --> " + key)
                else:
                    each_input_json["data"] = None

            if "datatype" in value:
                if value["datatype"] in model_triton_data_type_maping:
                    each_input_json["datatype"] = model_triton_data_type_maping[
                        value["datatype"]
                    ]
                else:
                    raise Exception(
                        "Data type - "
                        + value["datatype"]
                        + " - not supported for input --> "
                        + key
                    )
            else:
                raise Exception("Data type not specified for input --> " + key)

            inputs_res.append(each_input_json)

        return inputs_res
    except Exception as e:
        raise InferlessCLIError(e)
