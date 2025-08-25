In SBAid, a CSV file can be used to add cross sections to the network in bulk. Guidelines for the creation of such a file are the following:

- The file can have a header containing the column names. This is not mandatory. If included, the header must consist of the cells "name", "x-coordinate", "y-coordinate" and "type" in that exact order. This must be the file's first row.


- The first column must contain the names of the cross sections.


- The second column must contain the x-coordinates for the cross sections. This corresponds to the longitude of usual cartesian coordinates. 


- The third column must contain the y-coordinates for the cross sections. This corresponds to the latitude of usual cartesian coordinates. 



- The fourth column must contain the type of the cross sections. The options for this are "display", "measuring" and "combined".


Any inputs that do not follow the given blueprint will not be accepted by SBAid. Cross sections with semantically correct definitions but a location that is not on the project's route will be regarded as invalid. Any invalid cross section definitions will be skipped, while valid ones will always be added to the network.

To facilitate the creation of a cross section import file, feel free to use our [blueprint](cross_section_import_blueprint.csv).