from pydantic import BaseModel, Field
from typing import Optional
from codefabric.types.enums import PatchType
from codefabric.types.models import FileInfo, Patch, PatchDetails, Patches

class PackagesFormatter(BaseModel):
    packages: list[str] = Field(...,description="List of exact packages names to install.")

    @property
    def to_model(self) -> list[str]:
        return self.packages
    
class FileInfoFormatter(BaseModel):
    name: str = Field(...,description="File Name with extension. Example : server.js")
    path : str = Field(...,description="Path to file from the project root. Example : /path/to/server.js")
    dependencies : list[str] = Field(...,description="List of other file dependencies `path` for the file. Example : ['/path/to/server.js']")
    technical_blueprint : str = Field(...,description="Technical BluePrint and Outline for the file.")

    @property
    def to_model(self) -> FileInfo:
        return FileInfo(
            name=self.name,
            path=self.path,
            dependencies=self.dependencies,
            technical_specifications=self.technical_blueprint,
            is_generated=False,
            code=None
        )

class FileInfosFormatter(BaseModel):
    files : list[FileInfoFormatter] = Field(...,description="List of file infos.")

    @property
    def to_model(self) -> list[FileInfo]:
        return [file.to_model for file in self.files]
    
class GitIgnoreFormatter(BaseModel):
    ignore : list[str] = Field(...,description="List of file/folder names to ignore in git.")

    @property
    def to_model(self) -> list[str]:
        return self.ignore

class PatchDetailsFormatter(BaseModel):
    current_file_path : str = Field(...,alias="Current file path from root directory")
    file_content : Optional[str] = Field(...,alias="File content/code to override or add")
    move_to_file_path : Optional[str] = Field(...,alias="New file path from root directory")

    @property
    def to_model(self) -> PatchDetails:
        return PatchDetails(
            current_file_path=self.current_file_path,
            file_content=self.file_content,
            move_to_file_path=self.move_to_file_path
        )

class PatchFormatter(BaseModel):
    patch_type : PatchType = Field(...,alias="patch-type")
    patch_details : PatchDetailsFormatter = Field(...,alias="Add fields based on Patch type")

    @property
    def to_model(self) -> Patch:
        return Patch(
            patch_type=self.patch_type,
            patch_details=self.patch_details.to_model
        )

class PatchesFormatter(BaseModel):
    patches : list[PatchFormatter] = Field(...,alias="List of patches to apply to the project.")
    steps : list[str] = Field(...,alias="List of steps to apply the patches.")

    @property
    def to_model(self) -> Patches:
        return Patches(
            patches=[patch.to_model for patch in self.patches],
            steps=self.steps
        )