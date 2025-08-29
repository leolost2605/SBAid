In SBAid, a CSV file can be used to add parameter values in bulk. Guidelines for the creation of such a file are the following:

- The file must have a header containing the column name "cs_id", followed by cells with the name of each parameter. This must be the file's first row.
	

- The first column must contain the cross section IDs of the cross sections parameters are to be added to. 


- Each cell, corresponding to a cross section and a parameter name, can contain a value that is to be imported to the parameter configuration. In cells that contain strings, the string must be wrapped in quotes. 
	

- A global parameter, meaning one that is to be applied to all cross sections, can be imported by leaving the cross section ID cell empty.

All cells must contain a value that is correspondent to the parameter value type (a [GLib.VariantType](https://docs.gtk.org/glib/struct.VariantType.html) given by the set algorithm), or else it will be deemed invalid. All empty or invalid cells will be skipped, while all valid cells will be added to the parameter configuration. 

To facilitate the creation of a parameter configuration import file, feel free to use our [blueprint](parameter_configuration_import_blueprint.csv). To better understand the format, refer to our [example file](parameter_configuration_import_example.csv).
