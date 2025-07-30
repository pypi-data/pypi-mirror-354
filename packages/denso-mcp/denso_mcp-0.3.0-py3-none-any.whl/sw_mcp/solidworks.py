import sys
from typing import Optional, Literal
import clr
from pathlib import Path
import enum

# Add SolidWorks references
sys.path.append(r"C:\Program Files\SOLIDWORKS Corp\SOLIDWORKS (2)\api\redist")
clr.AddReference("SolidWorks.Interop.sldworks")
clr.AddReference("SolidWorks.Interop.swconst")

from SolidWorks.Interop.sldworks import SldWorks, Annotation, View, ModelDoc2, DrawingDoc, ImportStepData  # type: ignore
import SolidWorks.Interop.swconst as swconst  # type: ignore


def create_reverse_enum_map(enum_type):
    enum_keys = [x for x in dir(enum_type) if x.startswith("sw")]
    enum_values = [int(getattr(enum_type, x)) for x in enum_keys]

    return dict(zip(enum_values, enum_keys))


# class ViewType(str, enum.Enum):
#     """Enum for view types in SolidWorks"""

#     FRONT = "*Front"
#     BACK = "*Back"
#     LEFT = "*Left"
#     RIGHT = "*Right"
#     TOP = "*Top"
#     BOTTOM = "*Bottom"
#     ISOMETRIC = "*Isometric"
#     TRIMETRIC = "*Trimetric"

ViewType = Literal[
    "*Front", "*Back", "*Left", "*Right", "*Top", "*Bottom", "*Isometric", "*Trimetric"
]


class PaperSizeEnum(str, enum.Enum):
    """Enum for paper sizes in SolidWorks"""

    A1 = int(swconst.swDwgPaperSizes_e.swDwgPaperA1size)
    A2 = int(swconst.swDwgPaperSizes_e.swDwgPaperA2size)
    A3 = int(swconst.swDwgPaperSizes_e.swDwgPaperA3size)
    A4 = int(swconst.swDwgPaperSizes_e.swDwgPaperA4size)
    USER_DEFINED = int(swconst.swDwgPaperSizes_e.swDwgPapersUserDefined)


PaperSize = Literal["A1", "A2", "A3", "A4", "USER_DEFINED"]


class SolidWorks:
    def __init__(self):
        self.app = None
        self.model_doc = None  # .STEP model
        self.draw_doc = None  # .SLDDRW drawing
        self.part_doc = None  # .SLDPRT part file path
        self.file_path = None

        self.tmp_dir = Path.home() / "Documents" / "SolidWorks" / "tmp"
        self.tmp_dir.mkdir(parents=True, exist_ok=True)

    def connect(self, visible: bool = True):
        if self.app is not None:
            return False  # Already connected
        self.app = SldWorks()
        self.app.Visible = visible
        return True

    def disconnect(self):
        if self.app is not None:
            try:
                self.app.ExitApp()
            except Exception:
                pass
            self.app = None

    def is_connected(self):
        return self.app is not None

    def get_app(self):
        if self.app is None:
            raise Exception(
                "SolidWorks connection has not been established. Call connect first."
            )
        return self.app

    def create_drawing(self, paper_size: PaperSize, width: float, height: float):
        try:
            _paper_size = int(PaperSizeEnum[paper_size].value)

            template = self.app.GetDocumentTemplate(
                int(swconst.swDocumentTypes_e.swDocDRAWING), "", _paper_size, 100, 100
            )
            self.draw_doc = DrawingDoc(
                self.app.NewDocument(template, _paper_size, width, height)
            )
        except Exception as e:
            raise Exception(
                f"_paper_size: {_paper_size} paper_size: {paper_size} width: {width} height: {height}\n{str(e)}"
            )

    def add_view(self, view_type: ViewType, pos_x: float, pos_y: float, pos_z: float):
        try:
            view = self.draw_doc.CreateDrawViewFromModelView3(
                str(self.part_doc), view_type, pos_x, pos_y, pos_z
            )

            if view_type == "*Isometric" or view_type == "*Trimetric":
                return view

            # add automatic dimensioning to the view
            self.draw_doc.ActivateView(view.GetName2())
            entities = int(swconst.swAutodimEntities_e.swAutodimEntitiesAll)
            scheme = int(swconst.swAutodimScheme_e.swAutodimSchemeBaseline)
            self.draw_doc.AutoDimension(entities, scheme, 1, scheme, 1)

            return view
        except Exception as e:
            raise Exception(f"view_type: {view_type} {pos_x} {pos_y} {pos_z}\n{str(e)}")

    def open_file(self, file_path: str):
        if not self.is_connected():
            raise Exception("SolidWorks connection has not been established.")

        self.file_path = file_path

        file_data = ImportStepData(self.app.GetImportFileData(file_path))
        doc, _ = self.app.LoadFile4(file_path, "", file_data, -1)

        self.model_doc = ModelDoc2(doc)
        saved_file_path = self.tmp_dir / (Path(file_path).stem + ".sldprt")

        # save the model document to a temporary directory
        self.save_model_doc(str(saved_file_path.absolute().resolve()))
        self.part_doc = saved_file_path

        if doc:
            return {"success": True, "message": f"Document opened: {file_path}"}
        else:
            return {"success": False, "message": "Failed to open document"}

    def get_active_doc(self) -> ModelDoc2:
        app = self.get_app()
        doc = ModelDoc2(app.ActiveDoc)
        if not doc:
            raise Exception("No active document. Open or create a document first.")

        return doc

    def save_model_doc(self, file_path: str, model_doc: Optional[ModelDoc2] = None):
        if not model_doc:
            model_doc = self.model_doc

        return model_doc.SaveAs3(
            file_path,
            int(swconst.swSaveAsVersion_e.swSaveAsCurrentVersion),
            int(swconst.swSaveAsOptions_e.swSaveAsOptions_Silent),
        )

    def get_all_entities_position(self):
        # Create reverse enum maps for better readability
        entity_type_map = create_reverse_enum_map(swconst.swSelectType_e)
        annotation_type_map = create_reverse_enum_map(swconst.swAnnotationType_e)

        # Helper function to extract detailed information from entities
        def parse_entity_details(entity, entity_type):
            details = {
                "type": entity_type_map.get(entity_type, f"Unknown ({entity_type})"),
                "id": None,
            }

            try:
                # Typecast based on entity_type using Python.NET
                if entity_type == swconst.swSelectType_e.swSelDIMENSIONS:
                    dim = entity
                    details.update(
                        {
                            "id": dim.GetID(),
                            "value": dim.GetValue(),
                            "precision": (
                                dim.GetPrecision()
                                if hasattr(dim, "GetPrecision")
                                else None
                            ),
                        }
                    )
                elif entity_type == swconst.swSelectType_e.swSelNOTES:
                    note = entity
                    details.update({"id": note.GetID(), "text": note.GetText()})
                elif entity_type == swconst.swSelectType_e.swSelEDGES:
                    edge = entity
                    details.update({"id": edge.GetID(), "length": edge.GetLength()})
                elif entity_type == swconst.swSelectType_e.swSelFACES:
                    face = entity
                    details.update({"id": face.GetID(), "area": face.GetArea()})
            except Exception as e:
                details["error"] = str(e)

            return details

        # Parse all entities attached to an annotation
        def parse_entities(entities, types):
            result = []
            for i, (entity, entity_type) in enumerate(zip(entities, types)):
                if entity is not None:
                    entity_details = parse_entity_details(entity, entity_type)
                    result.append(entity_details)
            return result

        # Start processing views and sheets
        sheet_view_list = self.draw_doc.GetViews()
        # Convert COM collection to Python list and get first item (array of views)
        views_array = list(sheet_view_list)[0]
        # Convert views array to Python list
        views = list(views_array)
        sheet, views = views[0], views[1:]

        sheet = View(sheet)
        views = list(map(View, views))

        data = {"name": sheet.GetName2(), "views": []}

        for view in views:
            view_name = view.GetName2()

            # Get all annotations
            annotation_objects = view.GetAnnotations()
            annotations = []
            if annotation_objects:
                # Convert COM collection to Python list
                annotations = list(map(Annotation, annotation_objects))

            annotations_data = []

            for annotation in annotations:
                # Position relative to bottom-left corner of the sheet
                pos = list(annotation.GetPosition())

                # Get annotation type
                annotation_type = None
                annotation_type_str = "Unknown"
                try:
                    # Try property first, then method
                    annotation_type = (
                        annotation.Type
                        if hasattr(annotation, "Type")
                        else annotation.GetType()
                    )
                    annotation_type_str = annotation_type_map.get(
                        annotation_type, f"Unknown ({annotation_type})"
                    )
                except Exception as e:
                    pass

                # Get text content if available
                text_content = None
                try:
                    # Try different approaches based on annotation type
                    if hasattr(annotation, "GetText"):
                        text_content = annotation.GetText()
                    elif hasattr(annotation, "Text"):
                        text_content = annotation.Text
                    elif hasattr(annotation, "GetValue"):
                        text_content = str(annotation.GetValue())
                    elif hasattr(annotation, "Value"):
                        text_content = str(annotation.Value)
                except Exception as e:
                    pass

                # Get dimensions for text bounding box if available
                text_bounds = None
                try:
                    if hasattr(annotation, "GetTextBoundingBox"):
                        bounds = annotation.GetTextBoundingBox()
                        if bounds:
                            # Convert COM array to Python list
                            bounds_list = list(bounds)
                            text_bounds = {
                                "bottom_left": (bounds_list[0], bounds_list[1]),
                                "top_right": (bounds_list[2], bounds_list[3]),
                            }
                except Exception as e:
                    pass

                # Get dimension style information
                style_info = {}
                try:
                    if hasattr(annotation, "GetDimensionStyle"):
                        style = annotation.GetDimensionStyle()
                        if style:
                            style_info = {
                                "text_height": (
                                    style.TextHeight
                                    if hasattr(style, "TextHeight")
                                    else None
                                ),
                                "arrow_style": (
                                    style.ArrowStyle
                                    if hasattr(style, "ArrowStyle")
                                    else None
                                ),
                                "precision": (
                                    style.Precision
                                    if hasattr(style, "Precision")
                                    else None
                                ),
                            }
                except Exception as e:
                    pass

                # Get attached entities
                attached_entities = []
                try:
                    entities_obj = annotation.GetAttachedEntities()
                    entity_types_obj = annotation.GetAttachedEntityTypes()

                    if entities_obj and entity_types_obj:
                        # Convert COM collections to Python lists
                        entities = list(entities_obj)
                        entity_types = list(entity_types_obj)
                        attached_entities = parse_entities(entities, entity_types)
                except Exception as e:
                    attached_entities = [{"error": str(e)}]

                # Compile annotation data
                annotation_data = {
                    "name": annotation.GetName(),
                    "type": annotation_type_str,
                    "pos_x": pos[0],
                    "pos_y": pos[1],
                    "pos_z": pos[2],
                    "text": text_content,
                    "style": style_info,
                    "text_bounds": text_bounds,
                    "attached_entities": attached_entities,
                }

                annotations_data.append(annotation_data)

            # Get view position and outline
            view_pos = list(view.Position) if hasattr(view, "Position") else None
            view_outline = (
                list(view.GetOutline()) if hasattr(view, "GetOutline") else None
            )

            # Get all visible entities
            visible_entities = []
            try:
                if hasattr(view, "GetVisibleEntities"):
                    # Try to get edges
                    edge_objects = view.GetVisibleEntities(
                        swconst.swSelectType_e.swSelEDGES
                    )

                    if edge_objects:
                        # Convert COM collection to Python list
                        for edge_obj in list(edge_objects):
                            # Get edge data
                            edge_data = {
                                "type": "edge",
                                "id": (
                                    edge_obj.GetID()
                                    if hasattr(edge_obj, "GetID")
                                    else None
                                ),
                                "length": (
                                    edge_obj.GetLength()
                                    if hasattr(edge_obj, "GetLength")
                                    else None
                                ),
                            }

                            # Try to get start/end points
                            try:
                                if hasattr(edge_obj, "GetStartPoint") and hasattr(
                                    edge_obj, "GetEndPoint"
                                ):
                                    start_pt = list(edge_obj.GetStartPoint())
                                    end_pt = list(edge_obj.GetEndPoint())
                                    edge_data.update({"start": start_pt, "end": end_pt})
                            except:
                                pass

                            visible_entities.append(edge_data)

                    # Try to get faces as well
                    face_objects = view.GetVisibleEntities(
                        swconst.swSelectType_e.swSelFACES
                    )
                    if face_objects:
                        # Convert COM collection to Python list
                        for face_obj in list(face_objects):
                            face_data = {
                                "type": "face",
                                "id": (
                                    face_obj.GetID()
                                    if hasattr(face_obj, "GetID")
                                    else None
                                ),
                                "area": (
                                    face_obj.GetArea()
                                    if hasattr(face_obj, "GetArea")
                                    else None
                                ),
                            }
                            visible_entities.append(face_data)
            except Exception as e:
                visible_entities = [{"error": str(e)}]

            # Compile view data
            view_data = {
                "name": view_name,
                "pos_x": view_pos[0] if view_pos else None,
                "pos_y": view_pos[1] if view_pos else None,
                "bottom_left": tuple(view_outline[:2]) if view_outline else None,
                "top_right": tuple(view_outline[2:]) if view_outline else None,
                "annotations": annotations_data,
                "visible_entities": visible_entities,
            }

            data["views"].append(view_data)

        return data

    def get_build_numbers(self):
        if not self.is_connected():
            return None
        return self.app.GetBuildNumbers()
