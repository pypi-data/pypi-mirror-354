# Standard Library
import errno
import json
import logging
import os
import zipfile
from pathlib import Path
from typing import List
from zipfile import ZipFile

from nubia import argument, command, context
from seqslab.exceptions import exception_handler
from seqslab.workspace.internal.common import get_factory as get_workspace_factory
from termcolor import cprint
from yarl import URL

from .internal.utils import create_zip
from .register.common import trs_register
from .resource.common import trs_resource
from .template.base import TrsCreateTemplate, TrsImagesTemplate

"""
Copyright (C) 2022, Atgenomix Incorporated.

All Rights Reserved.

This program is an unpublished copyrighted work which is proprietary to
Atgenomix Incorporated and contains confidential information that is not to
be reproduced or disclosed to any other person or entity without prior
written consent from Atgenomix, Inc. in each and every instance.

Unauthorized reproduction of this program as well as unauthorized
preparation of derivative works based upon the program or distribution of
copies by sale, rental, lease or lending are violations of federal copyright
laws and state trade secret laws, punishable by civil and criminal penalties.
"""


class BaseTools:
    """Tool registration commands"""

    @staticmethod
    @exception_handler
    def _tool(tool_name: str, **kwargs) -> str:
        backend = trs_register().load_resource()
        return backend.tool(tool_name=tool_name, **kwargs)["id"]

    @staticmethod
    @exception_handler
    def _version(
        tool_id: str,
        version_name: str,
        version_id: str,
        descriptor_type: str,
        images: str,
        **kwargs,
    ) -> str:
        image_list = []
        if images:
            images_json = json.loads(images)
            for image in images_json:
                if image.get("checksum"):
                    if len(image.get("checksum").split(":")) == 2:
                        image_list.append(
                            {
                                **image,
                                "checksum_type": image.get("checksum").split(":")[0],
                                "checksum": image.get("checksum").split(":")[1],
                            }
                        )
                    else:
                        raise ValueError(
                            f"Wrong checksum format {image.get('checksum')} in image"
                        )
                else:
                    raise ValueError("No checksum in image")
        else:
            raise ValueError("Please provide a docker image.")

        backend = trs_register().load_resource()
        version_id = backend.version(
            tool_id=tool_id,
            version_name=version_name,
            version_id=version_id,
            images=image_list,
            descriptor_type=descriptor_type,
            **kwargs,
        )["version_id"]
        return version_id

    @staticmethod
    @exception_handler
    def _file(
        tool_id: str,
        version_id: str,
        descriptor_type: str,
        file_info: str,
        zip_file: str,
    ) -> str:
        if os.path.isfile(file_info):
            with open(file_info, "r") as f:
                toolfile_json = json.loads(f.read())
        else:
            toolfile_json = BaseTools.validate_bundle_info_keys(json.loads(file_info))

        # delete name key for each dictionary
        for dic in toolfile_json:
            if dic.get("name", None):
                del dic["name"]

        if not os.path.exists(zip_file):
            raise OSError(f"{zip_file} does not exist")

        backend = trs_register().load_resource()
        return backend.file(
            tool_id=tool_id,
            version_id=version_id,
            descriptor_type=descriptor_type,
            toolfile_json=toolfile_json,
            zip_file=zip_file,
        )

    @staticmethod
    def validate_bundle_info_keys(bundle_info: list) -> list:
        keys_desc = ["path", "file_type", "image_name"]
        keys_other = [
            "path",
            "file_type",
        ]
        ret = []
        for item in bundle_info:
            res = {}
            if "DESCRIPTOR" in item["file_type"]:
                for k in keys_desc:
                    res[k] = item[k]
            else:
                for k in keys_other:
                    res[k] = item[k]
            ret.append(res)
        return ret

    @staticmethod
    def _valide_workspace(workspace: str) -> bool:
        ctx = context.get_context()
        backend = ctx.args.backend
        resource = get_workspace_factory().load_resource()
        return resource.validate_workspace(workspace, backend)

    @command
    @argument(
        "name",
        type=str,
        description="Specify the name of the tool that you want to register (required).",
    )
    @argument(
        "id",
        type=str,
        description="Specify a custom identifier for the tool (optional). "
        "The identifier must only contain alphanumeric characters, hyphen, and underline.",
    )
    @argument(
        "toolclass_name",
        type=str,
        description="Specify the type of tool that you want to register (optional).",
    )
    @argument(
        "toolclass_description",
        type=str,
        description="Specify the type of tool that you want to register (optional).",
    )
    @argument(
        "description",
        type=str,
        description="Specify the description of the tool that you want to register (optional).",
    )
    @argument(
        "aliases",
        type=List[str],
        description="Specify the aliases of the tool that you want to register (optional).",
    )
    @argument(
        "checker_url",
        type=URL,
        description="Specify the URL of the checker tool that you want to register (optional).",
    )
    @argument(
        "has_checker",
        type=bool,
        description="Specify whether or not this tool has a checker tool associated with it (optional).",
    )
    @argument(
        "organization",
        type=str,
        description="Specify the organization of the tool that you want to register (optional).",
    )
    def tool(self, name: str, **kwargs) -> int:
        """
        Register TRS tool object.
        """
        tool_id = self._tool(tool_name=name, **kwargs)
        if isinstance(tool_id, int):
            return tool_id
        cprint(f"trs tool object - {tool_id} create complete", "yellow")
        return 0

    @command
    @argument(
        "workspace",
        type=str,
        description="Specify the workspace based on the signed in account (required).",
    )
    @argument(
        "tool_id",
        type=str,
        description="Specify the ID of a tool that you have already registered "
        "where you plan to register the file in (required).",
    )
    @argument(
        "name",
        type=str,
        description="Specify the name of the version that you want to register (optional).",
    )
    @argument(
        "id",
        type=str,
        description="Specify the version of the tool that you want to register (required)."
        "For example, 0.1, 0.1.2, 1.0, 1.1, etc.",
    )
    @argument(
        "descriptor_type",
        type=str,
        description="Specify the descriptor type of the tool that you want "
        "to register in this version (required).",
        choices=["WDL", "CWL", "NFL"],
    )
    @argument(
        "images",
        type=str,
        description="Specify a JSON string describing a list of images that you want "
        "to register in this version (required).",
    )
    @argument(
        "author",
        type=List[str],
        description="Specify the author of the tool that you want "
        "to register in this version (optional).",
    )
    @argument(
        "verified",
        type=bool,
        description="Specify whether or not the version of the tool that you want "
        "to register is verified (optional, default = false)."
        "For example, CLI mode: verified=True/False, "
        "Interactive mode: --verified or no value specified.",
    )
    @argument(
        "verified_source",
        type=List[str],
        description="Specify the verified source of the tool that you want "
        "to register in this version (optional).",
    )
    @argument(
        "included_apps",
        type=List[str],
        description="Specify the apps to be included with the tool that you want "
        "to register in this version (optional)."
        "For example, CLI mode: --included-apps app1 app2 app3, ..., "
        "Interactive mode: included_apps=['app1', 'app2', ...]",
    )
    @argument(
        "signed",
        type=bool,
        description="Specify whether or not this version of the tool that you want "
        "to register is signed (optional, default = false)."
        "For example, Interactive mode: signed=True/False, CLI mode: given --signed or not given.",
    )
    @argument(
        "is_production",
        type=bool,
        description="Specify whether or not the version of the tool that you want "
        "to register is for production use (optional, default = false).",
    )
    def version(
        self,
        workspace: str,
        tool_id: str,
        id: str,
        descriptor_type: str,
        images: str,
        name: str = "",
        **kwargs,
    ) -> int:
        """
        Register TRS version object.
        """

        if not self._valide_workspace(workspace):
            logging.error("Workspace not found")
            cprint(f"Workspace {workspace} not found.", "red")
            return errno.EINVAL

        kwargs["workspace"] = workspace
        id = self._version(
            tool_id=tool_id,
            version_name=name,
            version_id=id,
            descriptor_type=descriptor_type,
            images=images,
            **kwargs,
        )
        if isinstance(id, int):
            return id
        cprint(f"trs version object - {tool_id}: {id} create complete", "yellow")
        return 0

    @command
    @argument(
        "tool_id",
        type=str,
        description="Specify the ID of a tool that you have already registered "
        "where you plan to register the file in (required).",
    )
    @argument(
        "version_id",
        type=str,
        description="Specify the ID of a version that you have already registered "
        "where you plan to register the file in (required).",
    )
    @argument(
        "descriptor_type",
        type=str,
        description="Specify the descriptor type of a tool that you have already registered "
        "where you plan to register the file in (required).",
        choices=["WDL", "CWL", "NFL"],
    )
    @argument(
        "working_dir",
        type=str,
        description="Specify the path of the working directory (required).",
    )
    @argument(
        "file_info",
        type=str,
        description="Specify the file description used to register TRS. "
        "The default value is extracted from the workflow section of the execs.json file (optional).",
    )
    def file(
        self,
        tool_id: str,
        version_id: str,
        descriptor_type: str,
        working_dir: str,
        file_info: str = "default",
    ) -> int:
        """
        Register TRS file object.
        """
        if not file_info:
            cprint("Enter a valid file_info.", "red")
            return errno.EINVAL
        execs_path = (
            f"{working_dir}/execs.json"
            if file_info == "default"
            else f"{working_dir}/{file_info}"
        )
        try:
            with open(os.path.abspath(os.path.expanduser(execs_path)), "r") as file:
                execs = json.loads(file.read())
                file_info = json.dumps(execs["workflows"])
            zip_file = create_zip(target=working_dir, wdl_only=False)
        except FileNotFoundError as err:
            cprint(err, "red")
            return errno.EINVAL
        except json.JSONDecodeError:
            cprint(
                "Given a valid execs.json. Workflow content must be in JSON format.",
                "red",
            )
            return errno.EINVAL
        files = self._file(
            tool_id=tool_id,
            version_id=version_id,
            descriptor_type=descriptor_type,
            file_info=file_info,
            zip_file=zip_file,
        )
        if isinstance(files, int):
            Path(zip_file).unlink(missing_ok=True)
            return files
        cprint(
            f"trs file object - {tool_id} : {version_id} : {descriptor_type} create complete",
            "yellow",
        )
        cprint(f"workflow url - {files} ", "yellow")
        return 0

    @command
    @argument("scr_id", type=str, description="Specify SCR ID (required).")
    @argument(
        "repositories",
        type=List[str],
        positional=False,
        description="Specify the repository names you want to query (required).",
    )
    @argument(
        "reload",
        type=bool,
        positional=False,
        description="Specify whether to force reload system cache for SCR (optional, default = False).",
    )
    def images(self, scr_id: str, repositories: List[str], reload: bool = False) -> int:
        """
        List image tags and details of given repositories in an SCR.
        """
        if not repositories:
            cprint("Enter at least one repository", "red")
            return errno.EIO
        try:
            resource = trs_resource().load_resource()
            ret = resource.container_registry(scr_id, repositories, reload)
            images_info = TrsImagesTemplate().create(ret)
            cprint(
                f"SCR ID: {scr_id}\n"
                f"Repository list: {repositories}\n"
                f"image list:\n----------------------------------------------",
                "yellow",
            )
            for img in images_info:
                cprint(json.dumps(img), "yellow")
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH

    @command
    @argument(
        "working_dir",
        type=str,
        description="Specify the absolute working directory path hosting all WDL files (required). "
        "For example, /home/ubuntu/wdl/. ",
    )
    @argument(
        "inputs",
        type=str,
        description="Specify the folder path of inputs.json in relation to the working directory (required). "
        "For example, inputs.json. ",
    )
    @argument(
        "main_wdl",
        type=str,
        description="Specify the folder path of the main WDL file in relation to the working "
        "directory (required). "
        "For example, main.wdl. ",
    )
    @argument(
        "output",
        type=str,
        description="Specify the output filename of execs.json in relation to the working directory. "
        "(optional, default = execs.json)",
    )
    @argument(
        "config_import",
        type=List[str],
        positional=False,
        description="Specify one or more subworkflow execution files (execs.json) to configure "
        "operator pipeline settings (optional).",
    )
    def execs(
        self,
        working_dir: str,
        inputs: str,
        main_wdl: str,
        output: str = "working_dir + execs.json",
        config_import: List[str] = [],
    ) -> int:
        """
        Create SeqsLab execs.json file.
        """
        if not os.path.isdir(working_dir):
            cprint(f"{working_dir} does not exist or is not a directory", "red")
            return errno.ENOENT
        if not os.path.isfile(f"{working_dir}/{inputs}"):
            cprint(f"{inputs} does not exist", "red")
            return errno.ENOENT

        iconfig = []
        oconfig = []
        for f in config_import:
            if not os.path.isfile(f"{working_dir}/{f}"):
                cprint(f"{f} does not exist", "red")
                return errno.ENOENT
            with open(f"{working_dir}/{f}") as f:
                obj = json.load(f)
                iconfig.append(obj.get("i_configs"))
                oconfig.append(obj.get("o_configs"))

        try:
            # zip preparation
            zip_file = create_zip(target=working_dir, wdl_only=True)

            with ZipFile(zip_file, "r") as z:
                primary_descriptor = [e for e in z.namelist() if e == main_wdl]
                if not primary_descriptor:
                    cprint("No matching main_wdl name in working_dir.", "red")
                    return errno.ENOENT
                if len(primary_descriptor) != 1:
                    cprint(
                        f"Duplicate main_wdl name in working_dir. {primary_descriptor}",
                        "red",
                    )
                    return errno.EBADF
            with open(f"{working_dir}/{inputs}", "r") as f:
                inputs_content = json.load(f)

            execs_json = TrsCreateTemplate().create(
                zip_file=zip_file,
                primary_descriptor=primary_descriptor[0],
                inputs_json=inputs_content,
                iconfig=iconfig,
                oconfig=oconfig,
            )

            if output == "working_dir + execs.json":
                output = f'{working_dir.rstrip("/")}/execs.json'
            else:
                wdl_path = os.path.abspath(working_dir)
                output = os.path.join(wdl_path, output)

            with open(output, "w") as f:
                json.dump(execs_json, f, indent=4)
            return 0
        except zipfile.BadZipfile as error:
            cprint(f"{error}", "red")
            return errno.EPIPE
        except json.JSONDecodeError as error:
            cprint(f"{error}", "red")
            return errno.EPIPE
        except KeyError as error:
            cprint(f"{error}", "red")
            return errno.ESRCH
        except LookupError as error:
            cprint(f"{error}", "red")
            return errno.ESRCH
        except Exception as exception:
            cprint(f"{exception}", "red")
            return errno.ESRCH
        finally:
            Path(zip_file).unlink(missing_ok=True)

    @command
    @argument(
        "output",
        type=str,
        positional=False,
        description="Specify the output format of the stdout file (optional, default = json).",
        choices=["json", "table"],
    )
    @argument(
        "page",
        type=int,
        positional=False,
        description="Specify the page number in the set of paginated records (optional, default = 1).",
    )
    @argument(
        "page_size",
        type=int,
        positional=False,
        description="Specify the number of records to return in each page (optional, default = 10).",
    )
    @argument(
        "tool_id",
        type=str,
        positional=False,
        description="Specify the ID of each tool version (required).",
    )
    def list(
        self, tool_id: str = None, page: int = 1, page_size: int = 10, output="json"
    ) -> int:
        """
        If tool_id is specified, available versions of the tool are returned. If unspecified, a list of registered tools is returned.
        """
        if tool_id:
            if page or page_size:
                cprint(
                    "WARNING: page and page_size do not affect the list version.",
                    "yellow",
                )
            r = self._list_version(tool_id)
        else:
            r = self._list_tool(page=page, page_size=page_size)

        if isinstance(r, int):
            return r

        self._stdout(r["results"], output)
        return 0

    @staticmethod
    @exception_handler
    def _list_tool(page: int, page_size: int):
        backend = trs_register().load_resource()
        return backend.list_tool(page, page_size)

    @staticmethod
    @exception_handler
    def _list_version(tool_id: str):
        backend = trs_register().load_resource()
        return backend.list_version(tool_id)

    @command
    @argument("tool_id", type=str, description="Specify a TRS ID (required).")
    @argument("version_id", type=str, description="Specify a TRS version (required).")
    def delete(self, tool_id: str, version_id: str = None) -> int:
        """
        Delete a TRS tool version based on the tool ID and tool version ID.
        """

        def __log(result: dict):
            self._stdout(results=result, output="json")
            msg = f"Remove trs_id:{result.get('tool_id')} "
            if "version_id" in result.keys():
                msg += f"version_id:{result.get('version_id')} "
            msg += f"{result.get('status')}"
            if result.get("status").lower == "failed":
                logging.error(msg)
            else:
                logging.info(msg)

        result = self._delete(tool_id, version_id)
        if isinstance(result, int):
            return result
        __log(result)
        return 0

    @staticmethod
    @exception_handler
    def _delete(tool_id: str, version_id: str) -> dict:
        def __status(content: str, status: str) -> dict:
            return {"content": content, "status": status}

        backend = trs_register().load_resource()
        if version_id:
            result = backend.delete_version(tool_id, version_id)
        else:
            result = backend.delete_tool(tool_id)

        if len(result) == 0:
            return __status(content="Delete successfully.", status="Success")
        else:
            return __status(content=result, status="Failed")

    @staticmethod
    def _stdout(results, output: str) -> int:
        from tabulate import tabulate

        """
            stdout:: TODO: support different format ex: json, tsv, table
        """
        if output == "json":
            cprint(json.dumps(results, indent=4))
        elif output == "table":
            table_header = list(results[0].keys())
            table_datas = [result.values() for result in results]
            cprint(
                tabulate(
                    tabular_data=table_datas, headers=table_header, tablefmt="pipe"
                )
            )
        return 0

    @command
    @argument("tool_id", type=str, description="Specify a TRS ID (required).")
    @argument("version_id", type=str, description="Specify a TRS version (required).")
    @argument(
        "descriptor_type",
        type=str,
        description="Specify the TRS descriptor type (optional, default = WDL).",
        choices=["WDL", "CWL"],
    )
    @argument(
        "download_path",
        type=str,
        description="Specify the file path for the tool ZIP file download (required).",
    )
    def get(
        self,
        tool_id: str,
        version_id: str,
        download_path: str,
        descriptor_type: str = "WDL",
    ) -> int:
        """
        Get tool files using the SeqsLab API request /trs/v2/tools/{id}/versions/{version_id}/{type}/files/.
        """
        try:
            backend = trs_register().load_resource()
            backend.get_file(
                tool_id=tool_id,
                version_id=version_id,
                descriptor_type=descriptor_type,
                download_path=download_path,
            )
            return 0
        except Exception as error:
            cprint(f"{error}", "red")
            return errno.ESRCH


@command
class Tools(BaseTools):
    """Tool registration commands"""

    def __init__(self):
        pass
