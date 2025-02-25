This is a model of production. Here's how the model works:

Sources are things in the world that can be used to get resources.
Collection methods act on sources to produce resources
Production methods are done at a workstation, sometimes with a tool, to produce Materials, Consumer Goods, or tools from resources, materials, and parts.
Workstations in general are constructions in the world that are used during production
Parts are basically just materials that are used to make tools. The distinction is a bit fuzzy.

In general, any good (resource, material, part, tool, consumer) should track what it's made from for useful distinction. For example, cereal crop is a generalised class. They can all be used for the same thing. It's still useful to store the type of grain for quality assessment on end products, as well as specifying type for unique production methods for certain types (for example Rice as a cereal grain can be eaten raw)

Production methods are generally generalised. The time and effort they take depends on the quality of workstation and tool used in the method. As previously discussed, this quality should be determined by specifying properties.

For another example, Pickaxe is a generalised tool that depends highly on what it's built from. A simple bit of stone used as a pickaxe (see Rock Tool) won't come anywhere close to the durability and effectiveness of a modern industrial steel pickaxe.
