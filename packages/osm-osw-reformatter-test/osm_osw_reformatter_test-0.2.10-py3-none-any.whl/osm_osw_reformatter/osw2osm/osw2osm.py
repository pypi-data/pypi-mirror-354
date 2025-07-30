import gc
import logging
import ogr2osm
from pathlib import Path
from ..helpers.osw import OSWHelper
from ..helpers.response import Response
from ..serializer.osm.osm_normalizer import OSMNormalizer

ogr2osmlogger = logging.getLogger('ogr2osm')
ogr2osmlogger.setLevel(logging.DEBUG)
ogr2osmlogger.addHandler(logging.StreamHandler())


class OSW2OSM:
    def __init__(self, zip_file_path: str, workdir: str, prefix: str):
        self.zip_path = str(Path(zip_file_path))
        self.workdir = workdir
        self.prefix = prefix

    def convert(self) -> Response:
        try:
            print(f'Starting converting')
            unzipped_files = OSWHelper.unzip(self.zip_path, self.workdir)
            input_file = OSWHelper.merge(osm_files=unzipped_files, output=self.workdir, prefix=self.prefix)
            output_file = Path(self.workdir, f'{self.prefix}.graph.osm.xml')

            print(f'Input file for conversion: {input_file}')
            # Create the translation object.
            translation_object = OSMNormalizer()

            print(f'Translation object created: {translation_object}')
            # Create the ogr datasource
            datasource = ogr2osm.OgrDatasource(translation_object)
            print(f'Opening datasource for input file: {input_file}')
            datasource.open_datasource(input_file)

            # Instantiate the ogr to osm converter class ogr2osm. OsmData and start the conversion process
            print(f'Processing OSM data from input file: {input_file}')
            osm_data = ogr2osm.OsmData(translation_object)
            print(f'Processing OSM data with translation object')
            osm_data.process(datasource)

            print(f'Writing OSM data to output file: {output_file}')
            # Instantiate either ogr2osm.OsmDataWriter or ogr2osm.PbfDataWriter
            data_writer = ogr2osm.OsmDataWriter(output_file, suppress_empty_tags=True)
            osm_data.output(data_writer)

            del translation_object
            del datasource
            del osm_data
            del data_writer
            # Delete merge file
            Path(input_file).unlink()
            resp = Response(status=True, generated_files=str(output_file))
        except Exception as error:
            print(f'Error during conversion: {error}')
            resp = Response(status=False, error=str(error))
        finally:
            gc.collect()
        return resp
