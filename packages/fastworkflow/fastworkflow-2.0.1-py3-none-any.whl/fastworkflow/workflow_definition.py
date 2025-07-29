import json
import os
from enum import Enum
from typing import Optional

from speedict import Rdict

import fastworkflow
from pydantic import BaseModel, field_validator, model_validator, ConfigDict


class NodeType(str, Enum):
    Workitem = "Workitem"
    Workflow = "Workflow"


class TypeMetadata(BaseModel):
    node_type: NodeType

    @field_validator("node_type", mode="before")
    def parse_node_type(cls, node_type: NodeType):
        if not node_type:
            raise ValueError("node_type cannot be empty")
        return node_type


class SizeMetaData(BaseModel):
    min: int
    max: Optional[int]

    @field_validator("min", mode="before")
    def parse_min(cls, min: int):
        if min is None:
            raise ValueError("Minimum value cannot be empty")

        if min < 0:
            raise ValueError("Minimum value must be greater than or equal to 0")

        return min

    @field_validator("max", mode="before")
    def parse_max(cls, max: Optional[int]):
        if max is not None and max < 1:
            raise ValueError("Maximum value must be greater than or equal to 1")
        return max

    @model_validator(mode="after")
    def check_size_metadata(cls, size_meta: "SizeMetaData"):
        if size_meta.max is not None and size_meta.min > size_meta.max:
            raise ValueError(
                "Maximum value must be greater than or equal to the minimum value"
            )
        return size_meta


class WorkflowDefinition(BaseModel):
    workflow_folderpath: str
    paths_2_typemetadata: dict[str, TypeMetadata]
    paths_2_allowable_child_paths_2_sizemetadata: dict[str, dict[str, SizeMetaData]]

    @field_validator("paths_2_typemetadata", mode="before")
    def parse_type_metadata(cls, paths_2_typemetadata: dict[str, TypeMetadata]):
        for key, value in paths_2_typemetadata.items():
            if isinstance(value, dict):
                paths_2_typemetadata[key] = TypeMetadata(**value)
            elif not isinstance(paths_2_typemetadata[key], TypeMetadata):
                raise ValueError(f"Invalid value for type metadata '{key}'")
        return paths_2_typemetadata

    @field_validator("paths_2_allowable_child_paths_2_sizemetadata", mode="before")
    def parse_size_metadata(
        cls, paths_2_allowable_child_paths_2_sizemetadata: dict[str, dict[str, SizeMetaData]]
    ):
        for children in paths_2_allowable_child_paths_2_sizemetadata.values():
            for child_type, size_meta in children.items():
                if isinstance(size_meta, dict):
                    children[child_type] = SizeMetaData(**size_meta)
                elif not isinstance(children[child_type], SizeMetaData):
                    raise ValueError(
                        f"Invalid value for child size metadata '{child_type}'"
                    )
        return paths_2_allowable_child_paths_2_sizemetadata

    @model_validator(mode="after")
    def check_workflow_definition(cls, wfd: "WorkflowDefinition"):
        # check that all types have a valid non-empty key
        for key in wfd.paths_2_typemetadata.keys():
            if not key:
                raise ValueError("Workflow/workitem type cannot be an empty string")

        for parent_path, children in wfd.paths_2_allowable_child_paths_2_sizemetadata.items():
            if parent_path not in wfd.paths_2_typemetadata:
                raise ValueError(f"Parent type '{parent_path}' is not defined in types")
            for child_path, size_metadata in children.items():
                if child_path not in wfd.paths_2_typemetadata:
                    raise ValueError(
                        f"Child type '{child_path}' is not defined in types"
                    )
        return wfd

    @classmethod
    def _populate_workflow_definition(
        cls,
        workflow_folderpath: str,
        paths_2_typemetadata: dict[str, TypeMetadata],
        paths_2_allowable_child_paths_2_sizemetadata: dict[str, dict[str, SizeMetaData]],
        parent_path: Optional[str] = None
    ):
        if not os.path.isdir(workflow_folderpath):
            raise ValueError(f"{workflow_folderpath} must be a directory")

        basename = os.path.basename(workflow_folderpath.rstrip('/'))
        if parent_path:
            workitem_path = f"{parent_path}/{basename}"
            if workitem_path not in paths_2_allowable_child_paths_2_sizemetadata:
                if parent_path not in paths_2_allowable_child_paths_2_sizemetadata:
                    paths_2_allowable_child_paths_2_sizemetadata[parent_path] = {}
                paths_2_allowable_child_paths_2_sizemetadata[parent_path][workitem_path] = (
                    SizeMetaData(min=0, max=None)
                )
        else:
            workitem_path = f"/{basename}"

        paths_2_typemetadata[workitem_path] = TypeMetadata(node_type=NodeType.Workitem)


        child_cardinality = {}
        # Read the child cardinality if it exists
        child_cardinality_file = os.path.join(
            workflow_folderpath, "child_cardinality.json"
        )
        if os.path.exists(child_cardinality_file):
            with open(child_cardinality_file, "r") as f:
                child_cardinality = json.load(f)

            if child_cardinality:
                paths_2_typemetadata[workitem_path] = TypeMetadata(node_type=NodeType.Workflow)

        if not child_cardinality:
            return

        # Recursively process subfolders
        for subfolder in os.listdir(workflow_folderpath):
            subfolder_path = os.path.join(workflow_folderpath, subfolder)
            if os.path.isdir(subfolder_path) and not subfolder.startswith("_"):
                child_workitem_path = f"{workitem_path}/{os.path.basename(subfolder_path.rstrip('/'))}"
                cls._populate_workflow_definition(
                    subfolder_path, 
                    paths_2_typemetadata, 
                    paths_2_allowable_child_paths_2_sizemetadata, 
                    workitem_path
                )

        for child_type, size_meta in child_cardinality.items():
            child_path = f"{workitem_path}/{child_type}"
            if child_path not in paths_2_allowable_child_paths_2_sizemetadata[workitem_path]:
                raise ValueError(
                        f"cardinality file contains a child of type {child_type} that does not exist for {workitem_path}"
                )

            paths_2_allowable_child_paths_2_sizemetadata[workitem_path][child_path] = size_meta

    def write(self, filename: str):
        with open(filename, "w") as f:
            f.write(self.model_dump_json(indent=4))

    model_config = ConfigDict(arbitrary_types_allowed=True)

class WorkflowRegistry:   
    @classmethod
    def get_definition(cls, workflow_folderpath: str) -> WorkflowDefinition:
        if workflow_folderpath in cls._workflow_definitions:
            return cls._workflow_definitions[workflow_folderpath]

        workflowdefinitiondb_folderpath_dir = cls._get_workflowdefinition_db_folderpath()
        workflowdefinitiondb = Rdict(workflowdefinitiondb_folderpath_dir)
        workflow_definition = workflowdefinitiondb.get(workflow_folderpath, None)
        workflowdefinitiondb.close()

        if workflow_definition:
            cls._workflow_definitions[workflow_folderpath] = workflow_definition
            return workflow_definition
        
        return WorkflowRegistry.create_definition(workflow_folderpath)

    @classmethod
    def create_definition(cls, workflow_folderpath: str) -> WorkflowDefinition:
        paths_2_typemetadata = {}
        paths_2_allowable_child_paths_2_sizemetadata = {}

        WorkflowDefinition._populate_workflow_definition(
            workflow_folderpath, paths_2_typemetadata, paths_2_allowable_child_paths_2_sizemetadata
        )

        workflow_definition = WorkflowDefinition(
            workflow_folderpath=workflow_folderpath,
            paths_2_typemetadata=paths_2_typemetadata, 
            paths_2_allowable_child_paths_2_sizemetadata=paths_2_allowable_child_paths_2_sizemetadata
        )

        workflowdefinitiondb_folderpath_dir = cls._get_workflowdefinition_db_folderpath()
        workflowdefinitiondb = Rdict(workflowdefinitiondb_folderpath_dir)
        workflowdefinitiondb[workflow_folderpath] = workflow_definition
        workflowdefinitiondb.close()

        cls._workflow_definitions[workflow_folderpath] = workflow_definition
        return workflow_definition

    @classmethod
    def _get_workflowdefinition_db_folderpath(cls) -> str:
        """get the workflow definition db folder path"""
        SPEEDDICT_FOLDERNAME = fastworkflow.get_env_var("SPEEDDICT_FOLDERNAME")
        workflowdefinition_db_folderpath = os.path.join(
            SPEEDDICT_FOLDERNAME,
            "workflowdefinitions"
        )
        os.makedirs(workflowdefinition_db_folderpath, exist_ok=True)
        return workflowdefinition_db_folderpath

    _workflow_definitions: dict[str, WorkflowDefinition] = {}
