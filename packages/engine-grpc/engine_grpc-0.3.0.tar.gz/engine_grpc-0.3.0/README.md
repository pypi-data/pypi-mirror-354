
### Command interface examples

```python
UEI().command_parser(cmd=GRPCInterface.method_object_add_component,
                     params=[
                         target,
                         ASSEMBLE_NEARINTERACTIONGRABBABLE,
                         True
                     ])

UEI().command_parser(cmd=GRPCInterface.method_object_add_component,
                     params=[
                         target,
                         ASSEMBLE_MESHCOLLIDER,
                         True
                     ])

UEI().command_parser(cmd=GRPCInterface.method_object_set_reference_value,
                     params=[
                         collision_mesh_asset,
                         ASSETBLE_MESHFILTER,
                         "sharedMesh",
                         target,
                         ASSEMBLE_MESHCOLLIDER,
                         "sharedMesh"
                     ])

UEI().command_parser(cmd=GRPCInterface.method_object_set_value,
                     params=[
                         target,
                         ASSEMBLE_MESHCOLLIDER,
                         "convex",
                         True
                     ])
```