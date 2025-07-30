from enum import Enum, auto
from .engine_pipe_abstract import EnginePlatform

GRPC_INTERFACE_METHOD_HEADER = 'method'
GRPC_INTERFACE_PROPERTY_HEADER = 'property'


class GRPCInterface(Enum):

    # unity runtime method
    method_runtime_fetch_scene_hierarchy = auto()
    # declare method interface
    method_system_quit_without_saving = auto()
    method_system_get_service_status = auto()
    method_system_get_projectinfo = auto()
    method_scene_create = auto()

    # UnityEditor built-in static method
    method_editor_assetdatabase_move_asset = auto()
    method_editor_assetdatabase_refresh = auto()
    method_editor_assetdatabase_copy_asset = auto()
    method_editor_assetdatabase_guid_to_path = auto()
    method_editor_assetdatabase_find_assets = auto()
    method_editor_assetdatabase_get_dependencies = auto()
    method_editor_assetdatabase_import_assets = auto()

    method_editor_gameobjectutils_exists = auto()

    method_editor_scenemanager_open = auto()
    method_editor_scenemanager_save = auto()

    # prefab utilities
    method_object_create = auto()
    method_object_merge = auto()
    method_object_add_component = auto()
    """Represent the interface of adding component to the specific gameobject
    
    Example:
        PrefabUtils.AddComponent(
            source: "Assets/Content/Test.prefab",
            componentPath: "default/UnityEngine.MeshCollider, UnityEngine",
            isCreate: true
        );

    'default' is child object name. specify the component type full name and namespace

    """

    method_object_change_activate = auto()
    """Represent the interface of changing the activate state of gameobject or component.
    
    Example:
        PrefabUtils.ChangeActivate(
            source: "Assets/Content/Test.prefab",
            path: "default/UnityEngine.MeshRenderer, UnityEngine",
            isActive: true
        );

    'default' is child object name and the following is the component info. If there was no
    component specified, it would apply the activating on the gameobject only.

    """

    method_object_set_value = auto()
    method_object_set_reference_value = auto()
    method_object_create_mesh_collider_object = auto()
    method_object_create_variant = auto()
    method_object_set_active = auto()
    method_object_trim = auto()

    # material utilities
    method_material_update_textures = auto()

    method_unittest_get_float_array_data = auto()


INTERFACE_MAPPINGS = {

    # ================================== unity runtime method
    GRPCInterface.method_runtime_fetch_scene_hierarchy: {
        EnginePlatform.unity: "UGrpc.AppSceneUtils.FetchSceneHierarchy",
        EnginePlatform.unity_editor: "UGrpc.AppSceneUtils.FetchSceneHierarchy"
    },

    # ================================== unity editor method
    GRPCInterface.method_system_quit_without_saving: {
        EnginePlatform.unity_editor: "UGrpc.SystemUtils.QuitWithoutSaving"
    },
    GRPCInterface.method_system_get_service_status: {
        EnginePlatform.unity_editor: "UGrpc.SystemUtils.GetServiceStatus"
    },
    GRPCInterface.method_system_get_projectinfo: {
        EnginePlatform.unity_editor: "UGrpc.SystemUtils.GetProjectInfo"
    },
    GRPCInterface.method_scene_create: {
        EnginePlatform.unity_editor: "UGrpc.SceneUtils.CreateScene"
    },

    # AssetDatabase
    GRPCInterface.method_editor_assetdatabase_move_asset: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.MoveAsset"
    },
    GRPCInterface.method_editor_assetdatabase_refresh: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.Refresh"
    },
    GRPCInterface.method_editor_assetdatabase_copy_asset: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.CopyAsset"
    },
    GRPCInterface.method_editor_assetdatabase_guid_to_path: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.GUIDToAssetPath"
    },
    GRPCInterface.method_editor_assetdatabase_find_assets: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.FindAssets"
    },
    GRPCInterface.method_editor_assetdatabase_get_dependencies: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.GetDependencies"
    },
    GRPCInterface.method_editor_assetdatabase_import_assets: {
        EnginePlatform.unity_editor: "UnityEditor.AssetDatabase.ImportAsset"
    },
    GRPCInterface.method_editor_gameobjectutils_exists: {
        EnginePlatform.unity_editor: "UGrpc.GameObjectUtils.AssetExists"
    },

    # Prefab utilities
    GRPCInterface.method_object_create: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.CreateModelAsset"
    },
    GRPCInterface.method_object_merge: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.Merge"
    },
    GRPCInterface.method_object_add_component: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.AddComponent"
    },
    GRPCInterface.method_object_change_activate: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.ChangeActivate"
    },
    GRPCInterface.method_object_set_value: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.SetValue"
    },
    GRPCInterface.method_object_set_reference_value: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.SetReferenceValue"
    },
    GRPCInterface.method_object_create_mesh_collider_object: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.CreateMeshColliderObject"
    },
    GRPCInterface.method_object_create_variant: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.CreatePrefabVariant"
    },
    GRPCInterface.method_object_set_active: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.SetActive"
    },
    GRPCInterface.method_object_trim: {
        EnginePlatform.unity_editor: "UGrpc.PrefabUtils.Trim"
    },

    # Scene manager
    GRPCInterface.method_editor_scenemanager_open: {
        EnginePlatform.unity_editor: "UnityEditor.SceneManagement.EditorSceneManager.OpenScene"
    },
    GRPCInterface.method_editor_scenemanager_save: {
        EnginePlatform.unity_editor: "UnityEditor.SceneManagement.EditorSceneManager.SaveScene"
    },

    # Material utilities
    GRPCInterface.method_material_update_textures: {
        EnginePlatform.unity_editor: "UGrpc.MaterialUtils.UpdateTextures"
    },

    # UnitTest utilities
    GRPCInterface.method_unittest_get_float_array_data: {
        EnginePlatform.unity_editor: "UGrpc.UnitTestUtils.GetFloatArrayData"
    }
}
